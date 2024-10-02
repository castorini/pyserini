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

import glob
import os
import unittest

from pyserini.search import get_topics
from pyserini.search.lucene import LuceneHnswDenseSearcher, LuceneFlatDenseSearcher
from pyserini.util import get_cache_home


class TestLuceneDenseSearch(unittest.TestCase):
    def test_lucene_hnsw_dense_searcher(self):
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

        # We now run the same test again, but passing in a physical index directory location, as opposed to
        # a symbol representing the index.
        pattern = os.path.join(get_cache_home(), 'indexes/lucene-hnsw.beir-v1.0.0-arguana.bge-base-en-v1.5*')
        directories = [d for d in glob.glob(pattern, recursive=False) if os.path.isdir(d)]

        self.assertEqual(len(directories), 1)
        index_dir = directories[0]

        searcher = LuceneHnswDenseSearcher(index_dir, encoder='BgeBaseEn15')
        hits = searcher.search(q, k=5)

        self.assertEqual(len(hits), 5)
        self.assertEqual(hits[1].docid, 'test-culture-ahrtsdlgra-con03a')
        self.assertEqual(hits[2].docid, 'test-culture-ahrtsdlgra-con01b')
        self.assertEqual(hits[3].docid, 'test-culture-ahrtsdlgra-pro02b')
        self.assertEqual(hits[4].docid, 'test-culture-ahrtsdlgra-pro02a')
        self.assertAlmostEqual(hits[1].score, 0.893029, places=5)
        self.assertAlmostEqual(hits[2].score, 0.892179, places=5)
        self.assertAlmostEqual(hits[3].score, 0.888884, places=5)
        self.assertAlmostEqual(hits[4].score, 0.883876, places=5)

    def test_lucene_hnsw_dense_searcher_batch(self):
        searcher = LuceneHnswDenseSearcher.from_prebuilt_index(
            'beir-v1.0.0-arguana.bge-base-en-v1.5.hnsw', encoder='BgeBaseEn15')
        topics = get_topics('beir-v1.0.0-arguana-test')
        qids = ['test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con02a']
        queries = [topics[qids[0]]['title'], topics[qids[1]]['title']]

        results = searcher.batch_search(queries, qids, k=5, threads=2)

        # Ground truth results
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-con03a 1 0.893029 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-con01b 2 0.892179 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-pro02b 3 0.888884 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-pro02a 4 0.883876 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 training-free-speech-debate-nvhsibsv-con01a 1 0.886786 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 training-digital-freedoms-piidfphwbaa-con01b 2 0.878777 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 training-digital-freedoms-fehwbawdh-con01a 3 0.876869 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 test-culture-ahrtsdlgra-con02b 4 0.876068 Anserini

        self.assertEqual(len(results), 2)
        self.assertEqual(len(results['test-culture-ahrtsdlgra-con01a']), 5)
        self.assertEqual(len(results['test-culture-ahrtsdlgra-con02a']), 5)

        hits = results['test-culture-ahrtsdlgra-con01a']
        # First query: skip first hit, because it's just the query.
        self.assertEqual(hits[1].docid, 'test-culture-ahrtsdlgra-con03a')
        self.assertEqual(hits[2].docid, 'test-culture-ahrtsdlgra-con01b')
        self.assertEqual(hits[3].docid, 'test-culture-ahrtsdlgra-pro02b')
        self.assertEqual(hits[4].docid, 'test-culture-ahrtsdlgra-pro02a')

        self.assertAlmostEqual(hits[1].score, 0.893029, places=5)
        self.assertAlmostEqual(hits[2].score, 0.892179, places=5)
        self.assertAlmostEqual(hits[3].score, 0.888884, places=5)
        self.assertAlmostEqual(hits[4].score, 0.883876, places=5)

        hits = results['test-culture-ahrtsdlgra-con02a']
        self.assertEqual(hits[1].docid, 'training-free-speech-debate-nvhsibsv-con01a')
        self.assertEqual(hits[2].docid, 'training-digital-freedoms-piidfphwbaa-con01b')
        self.assertEqual(hits[3].docid, 'training-digital-freedoms-fehwbawdh-con01a')
        self.assertEqual(hits[4].docid, 'test-culture-ahrtsdlgra-con02b')

        self.assertAlmostEqual(hits[1].score, 0.886786, places=5)
        self.assertAlmostEqual(hits[2].score, 0.878777, places=5)
        self.assertAlmostEqual(hits[3].score, 0.876869, places=5)
        self.assertAlmostEqual(hits[4].score, 0.876068, places=5)

    def test_lucene_flat_dense_searcher(self):
        searcher = LuceneFlatDenseSearcher.from_prebuilt_index(
            'beir-v1.0.0-arguana.bge-base-en-v1.5.flat', encoder='BgeBaseEn15')
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

        # We now run the same test again, but passing in a physical index directory location, as opposed to
        # a symbol representing the index.
        pattern = os.path.join(get_cache_home(), 'indexes/lucene-flat.beir-v1.0.0-arguana.bge-base-en-v1.5*')
        directories = [d for d in glob.glob(pattern, recursive=False) if os.path.isdir(d)]

        self.assertEqual(len(directories), 1)
        index_dir = directories[0]

        searcher = LuceneFlatDenseSearcher(index_dir, encoder='BgeBaseEn15')
        hits = searcher.search(q, k=5)

        self.assertEqual(len(hits), 5)
        self.assertEqual(hits[1].docid, 'test-culture-ahrtsdlgra-con03a')
        self.assertEqual(hits[2].docid, 'test-culture-ahrtsdlgra-con01b')
        self.assertEqual(hits[3].docid, 'test-culture-ahrtsdlgra-pro02b')
        self.assertEqual(hits[4].docid, 'test-culture-ahrtsdlgra-pro02a')
        self.assertAlmostEqual(hits[1].score, 0.893029, places=5)
        self.assertAlmostEqual(hits[2].score, 0.892179, places=5)
        self.assertAlmostEqual(hits[3].score, 0.888884, places=5)
        self.assertAlmostEqual(hits[4].score, 0.883876, places=5)

    def test_lucene_flat_dense_searcher_batch(self):
        searcher = LuceneFlatDenseSearcher.from_prebuilt_index(
            'beir-v1.0.0-arguana.bge-base-en-v1.5.flat', encoder='BgeBaseEn15')
        topics = get_topics('beir-v1.0.0-arguana-test')
        qids = ['test-culture-ahrtsdlgra-con01a', 'test-culture-ahrtsdlgra-con02a']
        queries = [topics[qids[0]]['title'], topics[qids[1]]['title']]

        results = searcher.batch_search(queries, qids, k=5, threads=2)

        # Ground truth results
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-con03a 1 0.893029 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-con01b 2 0.892179 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-pro02b 3 0.888884 Anserini
        # test-culture-ahrtsdlgra-con01a Q0 test-culture-ahrtsdlgra-pro02a 4 0.883876 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 training-free-speech-debate-nvhsibsv-con01a 1 0.886786 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 training-digital-freedoms-piidfphwbaa-con01b 2 0.878777 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 training-digital-freedoms-fehwbawdh-con01a 3 0.876869 Anserini
        # test-culture-ahrtsdlgra-con02a Q0 test-culture-ahrtsdlgra-con02b 4 0.876068 Anserini

        self.assertEqual(len(results), 2)
        self.assertEqual(len(results['test-culture-ahrtsdlgra-con01a']), 5)
        self.assertEqual(len(results['test-culture-ahrtsdlgra-con02a']), 5)

        hits = results['test-culture-ahrtsdlgra-con01a']
        # First query: skip first hit, because it's just the query.
        self.assertEqual(hits[1].docid, 'test-culture-ahrtsdlgra-con03a')
        self.assertEqual(hits[2].docid, 'test-culture-ahrtsdlgra-con01b')
        self.assertEqual(hits[3].docid, 'test-culture-ahrtsdlgra-pro02b')
        self.assertEqual(hits[4].docid, 'test-culture-ahrtsdlgra-pro02a')

        self.assertAlmostEqual(hits[1].score, 0.893029, places=5)
        self.assertAlmostEqual(hits[2].score, 0.892179, places=5)
        self.assertAlmostEqual(hits[3].score, 0.888884, places=5)
        self.assertAlmostEqual(hits[4].score, 0.883876, places=5)

        hits = results['test-culture-ahrtsdlgra-con02a']
        self.assertEqual(hits[1].docid, 'training-free-speech-debate-nvhsibsv-con01a')
        self.assertEqual(hits[2].docid, 'training-digital-freedoms-piidfphwbaa-con01b')
        self.assertEqual(hits[3].docid, 'training-digital-freedoms-fehwbawdh-con01a')
        self.assertEqual(hits[4].docid, 'test-culture-ahrtsdlgra-con02b')

        self.assertAlmostEqual(hits[1].score, 0.886786, places=5)
        self.assertAlmostEqual(hits[2].score, 0.878777, places=5)
        self.assertAlmostEqual(hits[3].score, 0.876869, places=5)
        self.assertAlmostEqual(hits[4].score, 0.876068, places=5)


if __name__ == '__main__':
    unittest.main()
