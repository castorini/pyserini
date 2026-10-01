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

from pyserini.search.faiss import FaissSearcher


class TestFaissSearcherTrustRemoteCode(unittest.TestCase):
    def test_default_branch_forwards_trust_remote_code(self):
        with patch('pyserini.search.faiss._searcher.AutoQueryEncoder') as auto_query_encoder:
            FaissSearcher._init_encoder_from_str('some/remote-code-model', trust_remote_code=True)
            auto_query_encoder.assert_called_once_with(encoder_dir='some/remote-code-model', trust_remote_code=True)

    def test_default_branch_defaults_trust_remote_code_to_false(self):
        with patch('pyserini.search.faiss._searcher.AutoQueryEncoder') as auto_query_encoder:
            FaissSearcher._init_encoder_from_str('some/plain-model')
            auto_query_encoder.assert_called_once_with(encoder_dir='some/plain-model', trust_remote_code=False)

    def test_sentence_branch_forwards_trust_remote_code(self):
        with patch('pyserini.search.faiss._searcher.AutoQueryEncoder') as auto_query_encoder:
            FaissSearcher._init_encoder_from_str('sentence-transformers/some-model', trust_remote_code=True)
            auto_query_encoder.assert_called_once_with(
                encoder_dir='sentence-transformers/some-model', pooling='mean', l2_norm=True, trust_remote_code=True
            )
