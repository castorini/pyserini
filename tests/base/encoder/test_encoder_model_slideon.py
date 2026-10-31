#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np
import torch

from pyserini.encode import SlideOnDocumentEncoder, SlideOnQueryEncoder
from pyserini.encode.__main__ import init_encoder
from pyserini.encode._slideon import parse_max_active_dims


class TestSlideOnEncoder(unittest.TestCase):
    def setUp(self):
        self.model = Mock()
        self.model.to.return_value = self.model
        self.model.eval.return_value = self.model
        self.model.config = SimpleNamespace(
            inference={'prompts': {'query': 'query: ', 'document': 'document: '},
                       'query_length': 32, 'document_length': 64},
            tokenizer_settings={},
        )
        self.model.get_embedding_dimension.return_value = 4
        self.model.return_value = {'sentence_embedding': torch.tensor([[0., 0.5, 1., 0.]])}
        self.tokenizer = Mock(mask_token_id=1, eos_token_id=2)
        self.tokenizer.return_value = {
            'input_ids': torch.tensor([[2, 3]]),
            'attention_mask': torch.tensor([[1, 1]]),
        }
        for target, result in [('AutoModel', self.model), ('AutoTokenizer', self.tokenizer)]:
            patcher = patch(f'pyserini.encode._slideon.{target}.from_pretrained', return_value=result)
            patcher.start()
            self.addCleanup(patcher.stop)

    def test_defaults(self):
        query = SlideOnQueryEncoder('test')
        document = SlideOnDocumentEncoder('test', device='cpu')
        self.assertEqual(query.max_active_dims, 64)
        self.assertEqual(document.max_active_dims, 512)
        self.assertEqual(query.encode('hello'), {'1': 50, '2': 100})
        self.assertEqual(self.model.call_args.kwargs['max_active_dims'], 64)
        self.assertEqual(self.model.call_args.kwargs['task'], 'query')
        self.assertEqual(document.encode(['hello']), [{'1': 50, '2': 100}])
        self.assertEqual(self.model.call_args.kwargs['max_active_dims'], 512)
        self.assertEqual(self.model.call_args.kwargs['task'], 'document')

    def test_explicit_caps_and_none(self):
        for cls in (SlideOnQueryEncoder, SlideOnDocumentEncoder):
            for cap in (2, None):
                with self.subTest(encoder=cls.__name__, cap=cap):
                    encoder = cls('test', device='cpu', max_active_dims=cap)
                    encoder.encode('hello')
                    self.assertEqual(self.model.call_args.kwargs['max_active_dims'],
                                     4 if cap is None else cap)

    def test_invalid_caps(self):
        for cls in (SlideOnQueryEncoder, SlideOnDocumentEncoder):
            for cap in (0, -1, True, 1.5, 'None'):
                with self.subTest(encoder=cls.__name__, cap=cap):
                    with self.assertRaises(ValueError):
                        cls('test', max_active_dims=cap)

    def test_document_factory_defaults_and_none(self):
        for options, expected in [({}, 512), ({'max_active_dims': None}, None),
                                  ({'max_active_dims': 128}, 128)]:
            encoder = init_encoder('lightonai/SlideOn', None, 'cpu', **options)
            self.assertEqual(encoder.max_active_dims, expected)

    def test_quantization(self):
        encoder = SlideOnQueryEncoder('test', scale=1)
        self.assertEqual(encoder._quantize_weights([0, 0.5, 1.5, 2.5]), {'2': 2, '3': 2})
        for weights in ([-1], [np.nan], [np.inf], [[1]], [2**31]):
            with self.subTest(weights=weights):
                with self.assertRaises(ValueError):
                    encoder._quantize_weights(weights)

    def test_cli_cap_parser(self):
        for text in ('None', 'none', 'NONE'):
            self.assertIsNone(parse_max_active_dims(text))
        self.assertEqual(parse_max_active_dims('128'), 128)
        for text in ('0', '-1', '1.5', 'invalid'):
            with self.subTest(text=text):
                with self.assertRaises(argparse.ArgumentTypeError):
                    parse_max_active_dims(text)


if __name__ == '__main__':
    unittest.main()
