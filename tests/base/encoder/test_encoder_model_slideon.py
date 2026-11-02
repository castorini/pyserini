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

import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

import numpy as np
import torch

from pyserini.encode import SlideOnDocumentEncoder, SlideOnQueryEncoder
from pyserini.encode.__main__ import init_encoder


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

    def test_document_cap_not_configurable(self):
        with self.assertRaises(TypeError):
            SlideOnDocumentEncoder('test', max_active_dims=128)

    def test_query_cap_not_configurable(self):
        with self.assertRaises(TypeError):
            SlideOnQueryEncoder('test', max_active_dims=128)

    def test_document_factory(self):
        encoder = init_encoder('lightonai/SlideOn', None, 'cpu')
        self.assertEqual(encoder.max_active_dims, 512)
        with self.assertRaises(TypeError):
            init_encoder('lightonai/SlideOn', None, 'cpu', max_active_dims=128)

    def test_scale_not_configurable(self):
        for cls in (SlideOnQueryEncoder, SlideOnDocumentEncoder):
            with self.subTest(encoder=cls.__name__), self.assertRaises(TypeError):
                cls('test', scale=1)

    def test_invalid_text(self):
        with self.assertRaises(TypeError):
            SlideOnQueryEncoder('test').encode(123)
        encoder = SlideOnDocumentEncoder('test', device='cpu')
        with self.assertRaises(TypeError):
            encoder.encode([123])

    def test_document_titles(self):
        encoder = SlideOnDocumentEncoder('test', device='cpu')
        with patch.object(encoder, '_encode', return_value=[]) as encode:
            encoder.encode(['body one', 'body two'], titles=['title one', 'title two'], max_length=32)
            encode.assert_called_once_with(['title one body one', 'title two body two'], max_length=32)
            encode.reset_mock()
            encoder.encode('body', titles='title')
            encode.assert_called_once_with(['title body'], max_length=None)
            encode.reset_mock()
            encoder.encode(['body'])
            encode.assert_called_once_with(['body'], max_length=None)

    def test_invalid_document_titles(self):
        encoder = SlideOnDocumentEncoder('test', device='cpu')
        with self.assertRaises(ValueError):
            encoder.encode(['body'], titles=[])
        with self.assertRaises(TypeError):
            encoder.encode(['body'], titles=[123])
        with self.assertRaises(TypeError):
            encoder.encode([123], titles=['title'])

    def test_quantization(self):
        encoder = SlideOnQueryEncoder('test')
        self.assertEqual(encoder._quantize_weights([0, 0.005, 0.015, 0.025]), {'2': 2, '3': 2})
        for weights in ([-1], [np.nan], [np.inf], [[1]], [2**31]):
            with self.subTest(weights=weights):
                with self.assertRaises(ValueError):
                    encoder._quantize_weights(weights)


if __name__ == '__main__':
    unittest.main()
