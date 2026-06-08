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
from unittest.mock import patch

from pyserini.encode._base import load_head_weights
import torch


class TestEncodeBase(unittest.TestCase):
    def test_load_head_weights_uses_fallback_prefixes(self):
        model = torch.nn.Module()
        model.tok_proj = torch.nn.Linear(2, 1)

        checkpoint = {
            'tok_proj.weight': torch.tensor([[1.0, 2.0]]),
            'tok_proj.bias': torch.tensor([3.0]),
        }

        with patch('pyserini.encode._base.cached_file', return_value='fake.bin'), \
                patch('pyserini.encode._base.torch.load', return_value=checkpoint):
            load_head_weights(model, 'fake-model', {
                'tok_proj': ['coil_encoder.tok_proj', 'tok_proj'],
            })

        self.assertTrue(torch.equal(model.tok_proj.weight, checkpoint['tok_proj.weight']))
        self.assertTrue(torch.equal(model.tok_proj.bias, checkpoint['tok_proj.bias']))

    def test_load_head_weights_uses_prefixed_ance_keys(self):
        model = torch.nn.Module()
        model.embeddingHead = torch.nn.Linear(2, 1)
        model.norm = torch.nn.LayerNorm(1)

        checkpoint = {
            'ance_encoder.embeddingHead.weight': torch.tensor([[1.0, 2.0]]),
            'ance_encoder.embeddingHead.bias': torch.tensor([3.0]),
            'ance_encoder.norm.weight': torch.tensor([4.0]),
            'ance_encoder.norm.bias': torch.tensor([5.0]),
        }

        with patch('pyserini.encode._base.cached_file', return_value='fake.bin'), \
                patch('pyserini.encode._base.torch.load', return_value=checkpoint):
            load_head_weights(model, 'fake-model', {
                'embeddingHead': ['ance_encoder.embeddingHead', 'embeddingHead'],
                'norm': ['ance_encoder.norm', 'norm'],
            })

        self.assertTrue(torch.equal(model.embeddingHead.weight, checkpoint['ance_encoder.embeddingHead.weight']))
        self.assertTrue(torch.equal(model.embeddingHead.bias, checkpoint['ance_encoder.embeddingHead.bias']))
        self.assertTrue(torch.equal(model.norm.weight, checkpoint['ance_encoder.norm.weight']))
        self.assertTrue(torch.equal(model.norm.bias, checkpoint['ance_encoder.norm.bias']))


if __name__ == '__main__':
    unittest.main()
