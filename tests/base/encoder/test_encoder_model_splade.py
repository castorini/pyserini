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
import unittest
from unittest.mock import MagicMock, patch

from pyserini.encode import SpladeQueryEncoder


class TestEncodeSplade(unittest.TestCase):
    def test_splade_load_disables_safetensors_conversion(self):
        model = MagicMock()

        def from_pretrained(*args, **kwargs):
            self.assertEqual(os.environ['DISABLE_SAFETENSORS_CONVERSION'], '1')
            return model

        with patch.dict(os.environ, {}, clear=False), \
                patch('pyserini.encode._splade.AutoModelForMaskedLM.from_pretrained', side_effect=from_pretrained) as from_pretrained_mock, \
                patch('pyserini.encode._splade.AutoTokenizer.from_pretrained'):
            os.environ.pop('DISABLE_SAFETENSORS_CONVERSION', None)

            encoder = SpladeQueryEncoder('fake-model', device='cpu')

            self.assertIs(encoder.model, model)
            from_pretrained_mock.assert_called_once_with('fake-model', use_safetensors=False)
            model.to.assert_called_once_with('cpu')
            self.assertNotIn('DISABLE_SAFETENSORS_CONVERSION', os.environ)

    def test_splade_load_restores_existing_safetensors_conversion_setting(self):
        model = MagicMock()

        def from_pretrained(*args, **kwargs):
            self.assertEqual(os.environ['DISABLE_SAFETENSORS_CONVERSION'], '1')
            return model

        with patch.dict(os.environ, {'DISABLE_SAFETENSORS_CONVERSION': 'previous'}, clear=False), \
                patch('pyserini.encode._splade.AutoModelForMaskedLM.from_pretrained', side_effect=from_pretrained), \
                patch('pyserini.encode._splade.AutoTokenizer.from_pretrained'):
            SpladeQueryEncoder('fake-model', device='cpu')

            self.assertEqual(os.environ['DISABLE_SAFETENSORS_CONVERSION'], 'previous')

    def test_splade_encoder(self):
        encoder = SpladeQueryEncoder('naver/splade-v3')
        weights = encoder.encode('information retrieval')

        self.assertEqual(weights['retrieval'], 151)
        self.assertEqual(weights['information'], 139)
        self.assertEqual(weights['retrieve'], 107)
        self.assertEqual(weights['retrieved'], 92)
        self.assertEqual(weights['archive'], 53)


if __name__ == '__main__':
    unittest.main()
