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

from pyserini.search import get_topics
from pyserini.search.lucene import LuceneHnswDenseSearcher


class TestLuceneDenseSearch(unittest.TestCase):
    def test_lucene_hnsw_searcher(self):
        searcher = LuceneHnswDenseSearcher.from_prebuilt_index(
            'beir-v1.0.0-arguana.bge-base-en-v1.5.hnsw', encoder='BgeBaseEn15')
        topics = get_topics('beir-v1.0.0-arguana-test')
        qid = 'test-culture-ahrtsdlgra-con01a'
        q = topics[qid]['title']

        hits = searcher.search(q, k=5)

        # Ground truth results
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-con03a 1 0.893029 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-con01b 2 0.892179 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-pro02b 3 0.888884 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-pro02a 4 0.883876 Anserini

        self.assertEqual(len(hits), 5)

        # Skip first hit, because it's just the query.
        self.assertEqual(hits[1].docid, 'test-culture-ahrtsdlgra-con03a')
        self.assertEqual(hits[2].docid, 'test-culture-ahrtsdlgra-con01b')
        self.assertEqual(hits[3].docid, 'test-culture-ahrtsdlgra-pro02b')
        self.assertEqual(hits[4].docid, 'test-culture-ahrtsdlgra-pro02a')

        self.assertAlmostEqual(hits[1].score, 0.893029, places=5)
        self.assertAlmostEqual(hits[2].score, 0.892179, places=5)
        self.assertAlmostEqual(hits[3].score, 0.888884, places=5)
        self.assertAlmostEqual(hits[4].score, 0.883876, places=5)


if __name__ == '__main__':
    unittest.main()
