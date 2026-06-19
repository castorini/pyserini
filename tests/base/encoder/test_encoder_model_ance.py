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

import os
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd

from pyserini.encode import AnceQueryEncoder
from pyserini.encode._ance import AnceEncoder
from pyserini.query_iterator import DefaultQueryIterator


EXPECTED_VALUES = [(-1.34755, -1.22419), (-1.36109, -1.47927)]


class TestEncodeAnce(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    def test_ance_load_disables_safetensors_conversion(self):
        model = MagicMock()

        def from_pretrained(*args, **kwargs):
            self.assertEqual(os.environ['DISABLE_SAFETENSORS_CONVERSION'], '1')
            return model

        with patch.dict(os.environ, {}, clear=False), \
                patch.object(AnceEncoder, 'from_pretrained', side_effect=from_pretrained) as from_pretrained_mock, \
                patch('pyserini.encode._ance.load_head_weights'):
            os.environ.pop('DISABLE_SAFETENSORS_CONVERSION', None)

            loaded_model = AnceEncoder.load_pretrained_encoder('fake-model', 'cpu')

            self.assertIs(loaded_model, model)
            from_pretrained_mock.assert_called_once_with('fake-model', use_safetensors=False)
            model.to.assert_called_once_with('cpu')
            self.assertNotIn('DISABLE_SAFETENSORS_CONVERSION', os.environ)

    def test_ance_load_restores_existing_safetensors_conversion_setting(self):
        model = MagicMock()

        def from_pretrained(*args, **kwargs):
            self.assertEqual(os.environ['DISABLE_SAFETENSORS_CONVERSION'], '1')
            return model

        with patch.dict(os.environ, {'DISABLE_SAFETENSORS_CONVERSION': 'previous'}, clear=False), \
                patch.object(AnceEncoder, 'from_pretrained', side_effect=from_pretrained), \
                patch('pyserini.encode._ance.load_head_weights'):
            AnceEncoder.load_pretrained_encoder('fake-model', 'cpu')

            self.assertEqual(os.environ['DISABLE_SAFETENSORS_CONVERSION'], 'previous')

    def test_ance_encode_query_cli(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'encoded_queries.pkl')
            subprocess.run(
                [
                    sys.executable, '-m', 'pyserini.encode.query',
                    '--topics', 'msmarco-passage-dev-subset',
                    '--encoder', 'castorini/ance-msmarco-passage',
                    '--output', output_path,
                    '--device', 'cpu',
                    '--max-queries', '2',
                ],
                cwd=self.repo_dir,
                check=True,
            )

            encoded = pd.read_pickle(output_path)
            self.assertEqual(encoded.shape, (2, 3))
            self.assertEqual(encoded.columns.tolist(), ['id', 'text', 'embedding'])
            self.assertEqual(len(encoded.iloc[0]['embedding']), 768)
            for i, (first_value, last_value) in enumerate(EXPECTED_VALUES):
                self.assertAlmostEqual(encoded.iloc[i]['embedding'][0], first_value, places=5)
                self.assertAlmostEqual(encoded.iloc[i]['embedding'][-1], last_value, places=5)

    def test_ance_query_encoder_direct(self):
        encoder = AnceQueryEncoder('castorini/ance-msmarco-passage', device='cpu')
        query_iterator = DefaultQueryIterator.from_topics('msmarco-passage-dev-subset')
        for i, (_, text) in enumerate(query_iterator):
            if i == 2:
                break
            embedding = encoder.encode(text)
            self.assertEqual(len(embedding), 768)
            self.assertAlmostEqual(embedding[0], EXPECTED_VALUES[i][0], places=5)
            self.assertAlmostEqual(embedding[-1], EXPECTED_VALUES[i][1], places=5)

    def test_ance_weights_loaded(self):
        encoder = AnceQueryEncoder('castorini/ance-msmarco-passage')
        norm_weights = encoder.model.norm.weight.detach().cpu().numpy()
        norm_bias = encoder.model.norm.bias.detach().cpu().numpy()
        self.assertFalse(np.allclose(norm_weights, np.ones_like(norm_weights)), 'norm weights appear to be default initialized, not loaded from checkpoint')
        self.assertFalse(np.allclose(norm_bias, np.zeros_like(norm_bias)), 'norm bias appear to be default initialized, not loaded from checkpoint')


if __name__ == '__main__':
    unittest.main()
