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

import json
import os
import unittest

from pyserini.encode import TctColBertDocumentEncoder, TctColBertQueryEncoder
from tests.base.encoder.utils import assert_encode_query_cli_output, assert_query_encoder_output


EXPECTED_VALUES_TCT_COLBERT_MSMARCO = [(0.14085, -0.15662, 5), (-0.14778, 0.10030, 5)]
EXPECTED_VALUES_TCT_COLBERT_V2_MSMARCO = [(0.18285, -0.10137, 5), (-0.03068, 0.08468, 5)]
EXPECTED_VALUES_TCT_COLBERT_V2_HN_MSMARCO = [(0.15629, -0.09900, 5), (-0.04446, 0.07603, 5)]
EXPECTED_VALUES_TCT_COLBERT_V2_HNP_MSMARCO = [(0.15061, -0.08704, 5), (-0.05862, 0.10783, 5)]


class TestEncodeTctColBert(unittest.TestCase):
    def test_tct_colbert_encoder(self):
        texts = []
        resource_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources', 'simple_cacm_corpus.json'))
        with open(resource_path) as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = TctColBertDocumentEncoder('castorini/tct_colbert-msmarco', device='cpu')
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.01650, places=5)
        self.assertAlmostEqual(vectors[0][-1], -0.05648, places=5)
        self.assertAlmostEqual(vectors[2][0], -0.10293, places=5)
        self.assertAlmostEqual(vectors[2][-1], 0.05549, places=5)

    def test_msmarco_doc_tct_colbert_encode_query_cli(self):
        assert_encode_query_cli_output(self, 'msmarco-passage-dev-subset', 'castorini/tct_colbert-msmarco', EXPECTED_VALUES_TCT_COLBERT_MSMARCO)

    def test_msmarco_doc_tct_colbert_query_encoder(self):
        encoder = TctColBertQueryEncoder('castorini/tct_colbert-msmarco', device='cpu')
        assert_query_encoder_output(self, 'msmarco-passage-dev-subset', encoder, EXPECTED_VALUES_TCT_COLBERT_MSMARCO)

    def test_msmarco_passage_tct_colbert_v2_encode_query_cli(self):
        assert_encode_query_cli_output(self, 'msmarco-passage-dev-subset', 'castorini/tct_colbert-v2-msmarco', EXPECTED_VALUES_TCT_COLBERT_V2_MSMARCO)

    def test_msmarco_passage_tct_colbert_v2_query_encoder(self):
        encoder = TctColBertQueryEncoder('castorini/tct_colbert-v2-msmarco', device='cpu')
        assert_query_encoder_output(self, 'msmarco-passage-dev-subset', encoder, EXPECTED_VALUES_TCT_COLBERT_V2_MSMARCO)

    def test_msmarco_passage_tct_colbert_v2_hn_encode_query_cli(self):
        assert_encode_query_cli_output(self, 'msmarco-passage-dev-subset', 'castorini/tct_colbert-v2-hn-msmarco', EXPECTED_VALUES_TCT_COLBERT_V2_HN_MSMARCO)

    def test_msmarco_passage_tct_colbert_v2_hn_query_encoder(self):
        encoder = TctColBertQueryEncoder('castorini/tct_colbert-v2-hn-msmarco', device='cpu')
        assert_query_encoder_output(self, 'msmarco-passage-dev-subset', encoder, EXPECTED_VALUES_TCT_COLBERT_V2_HN_MSMARCO)

    def test_msmarco_passage_tct_colbert_v2_hnp_encode_query_cli(self):
        assert_encode_query_cli_output(self, 'msmarco-passage-dev-subset', 'castorini/tct_colbert-v2-hnp-msmarco', EXPECTED_VALUES_TCT_COLBERT_V2_HNP_MSMARCO)

    def test_msmarco_passage_tct_colbert_v2_hnp_query_encoder(self):
        encoder = TctColBertQueryEncoder('castorini/tct_colbert-v2-hnp-msmarco', device='cpu')
        assert_query_encoder_output(self, 'msmarco-passage-dev-subset', encoder, EXPECTED_VALUES_TCT_COLBERT_V2_HNP_MSMARCO)


if __name__ == '__main__':
    unittest.main()
