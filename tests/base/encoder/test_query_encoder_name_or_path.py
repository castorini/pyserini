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
from unittest.mock import MagicMock, patch

from pyserini.encode import AutoQueryEncoder
from pyserini.encode._base import resolve_encoder_name_or_path


class TestQueryEncoderNameOrPath(unittest.TestCase):
    def test_resolve_encoder_name_or_path_prefers_new_name(self):
        self.assertEqual(
            resolve_encoder_name_or_path('castorini/model', None),
            'castorini/model',
        )

    def test_resolve_encoder_name_or_path_accepts_legacy_alias(self):
        self.assertEqual(
            resolve_encoder_name_or_path(None, 'castorini/model'),
            'castorini/model',
        )

    def test_resolve_encoder_name_or_path_rejects_conflicting_values(self):
        with self.assertRaisesRegex(ValueError, 'refer to different models'):
            resolve_encoder_name_or_path('castorini/model-a', 'castorini/model-b')

    @patch('pyserini.encode._auto.load_auto_tokenizer')
    @patch('pyserini.encode._auto.AutoModel.from_pretrained')
    def test_auto_query_encoder_accepts_new_name(self, from_pretrained, load_tokenizer):
        model = MagicMock()
        from_pretrained.return_value = model

        encoder = AutoQueryEncoder(encoder_name_or_path='castorini/model', device='cpu')

        self.assertTrue(encoder.has_model)
        from_pretrained.assert_called_once_with('castorini/model')
        model.to.assert_called_once_with('cpu')
        load_tokenizer.assert_called_once_with('castorini/model', clean_up_tokenization_spaces=True)

    @patch('pyserini.encode._auto.load_auto_tokenizer')
    @patch('pyserini.encode._auto.AutoModel.from_pretrained')
    def test_auto_query_encoder_accepts_legacy_alias(self, from_pretrained, load_tokenizer):
        model = MagicMock()
        from_pretrained.return_value = model

        encoder = AutoQueryEncoder(encoder_dir='castorini/model', device='cpu')

        self.assertTrue(encoder.has_model)
        from_pretrained.assert_called_once_with('castorini/model')
        model.to.assert_called_once_with('cpu')
        load_tokenizer.assert_called_once_with('castorini/model', clean_up_tokenization_spaces=True)

    def test_auto_query_encoder_rejects_conflicting_names(self):
        with self.assertRaisesRegex(ValueError, 'refer to different models'):
            AutoQueryEncoder(
                encoder_name_or_path='castorini/model-a',
                encoder_dir='castorini/model-b',
            )


if __name__ == '__main__':
    unittest.main()
