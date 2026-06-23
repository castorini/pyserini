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

from pyserini.encode import AutoQueryEncoder
from tests.base.encoder.utils import assert_encode_query_cli_output, assert_query_encoder_output


EXPECTED_VALUES = [(0.01859, -0.02723, 5), (-0.04856, 0.03721, 5)]


class TestEncodeSBert(unittest.TestCase):
    def test_msmarco_passage_sbert_encode_query_cli(self):
        assert_encode_query_cli_output(self, 'msmarco-passage-dev-subset', 'sentence-transformers/msmarco-distilbert-base-v3', EXPECTED_VALUES)

    def test_msmarco_passage_sbert_query_encoder_direct(self):
        encoder = AutoQueryEncoder('sentence-transformers/msmarco-distilbert-base-v3', device='cpu', pooling='mean', l2_norm=True)
        assert_query_encoder_output(self, 'msmarco-passage-dev-subset', encoder, EXPECTED_VALUES)


if __name__ == '__main__':
    unittest.main()
