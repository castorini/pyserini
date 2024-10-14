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
import unittest

from pyserini.encode import QueryEncoder
from pyserini.encode import TctColBertDocumentEncoder
from pyserini.search import get_topics


class TestEncodeTctColBert(unittest.TestCase):
    def test_tct_colbert_encoder(self):
        texts = []
        with open('tests/resources/simple_cacm_corpus.json') as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = TctColBertDocumentEncoder('castorini/tct_colbert-msmarco', device='cpu')
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.01649557, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.05648308, places=4)
        self.assertAlmostEqual(vectors[2][0], -0.10293338, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.05549275, places=4)

    def test_msmarco_doc_tct_colbert_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('tct_colbert-msmarco-doc-dev')
        topics = get_topics('msmarco-doc-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_msmarco_passage_tct_colbert_v2_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('tct_colbert-v2-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_msmarco_passage_tct_colbert_v2_hn_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('tct_colbert-v2-hn-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_msmarco_passage_tct_colbert_v2_hnp_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('tct_colbert-v2-hnp-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)


if __name__ == '__main__':
    unittest.main()
