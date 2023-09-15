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

"""Integration tests for DistilBERT KD."""

import unittest

from pyserini.search import QueryEncoder
from pyserini.search import get_topics


class TestLoadEncodedQueries(unittest.TestCase):
    def test_ance_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('ance-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('ance-dl19-passage')
        topics = get_topics('dl19-passage')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('ance-dl20')
        topics = get_topics('dl20')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_distilbert_kd_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('distilbert_kd-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('distilbert_kd-dl19-passage')
        topics = get_topics('dl19-passage')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('distilbert_kd-dl20')
        topics = get_topics('dl20')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_distilbert_kd_tas_b_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('distilbert_tas_b-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('distilbert_tas_b-dl19-passage')
        topics = get_topics('dl19-passage')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

        encoded = QueryEncoder.load_encoded_queries('distilbert_tas_b-dl20')
        topics = get_topics('dl20')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

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

    def test_msmarco_passage_sbert_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('sbert-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)


if __name__ == '__main__':
    unittest.main()
