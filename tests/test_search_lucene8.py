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
import shutil
import tarfile
import unittest
from random import randint
from typing import List, Dict
from urllib.request import urlretrieve

from pyserini.search.lucene import LuceneSearcher, JScoredDoc


class TestSearch(unittest.TestCase):
    searcher = None
    index_dir = None
    collection_url = None
    tarball_name = None

    @classmethod
    def setUpClass(cls):
        # Download pre-built CACM index; append a random value to avoid filename clashes.
        r = randint(0, 10000000)
        cls.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene-index.cacm.tar.gz'
        cls.tarball_name = 'lucene-index.cacm-{}.tar.gz'.format(r)
        cls.index_dir = 'index{}/'.format(r)
        urlretrieve(cls.collection_url, cls.tarball_name)

        tarball = tarfile.open(cls.tarball_name)
        tarball.extractall(cls.index_dir)
        tarball.close()

        cls.searcher = LuceneSearcher(f'{cls.index_dir}lucene-index.cacm')

    def test_basic(self):
        self.assertTrue(self.searcher.get_similarity().toString().startswith('BM25'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(hits, List))

        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertEqual(hits[0].lucene_docid, 3133)
        self.assertAlmostEqual(hits[0].score, 4.7655, places=4)

        # Test accessing the raw Lucene document and fetching fields from it:
        self.assertEqual(hits[0].lucene_document.getField('id').stringValue(), 'CACM-3134')
        self.assertEqual(hits[0].lucene_document.get('id'), 'CACM-3134')      # simpler call, same result as above
        self.assertEqual(len(hits[0].lucene_document.getField('contents').stringValue()), 1500)
        self.assertEqual(len(hits[0].lucene_document.get('contents')), 1500)  # simpler call, same result as above
        self.assertEqual(len(hits[0].lucene_document.getField('raw').stringValue()), 1532)
        self.assertEqual(len(hits[0].lucene_document.get('raw')), 1532)       # simpler call, same result as above

        self.assertTrue(isinstance(hits[9], JScoredDoc))
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.2174, places=4)

        hits = self.searcher.search('search')

        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(hits[0].docid, 'CACM-3058')
        self.assertAlmostEqual(hits[0].score, 2.8576, places=4)

        self.assertTrue(isinstance(hits[9], JScoredDoc))
        self.assertEqual(hits[9].docid, 'CACM-3040')
        self.assertAlmostEqual(hits[9].score, 2.6878, places=4)

    def test_batch(self):
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], threads=2)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))

        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JScoredDoc))
        self.assertEqual(results['q1'][0].docid, 'CACM-3134')
        self.assertAlmostEqual(results['q1'][0].score, 4.7655, places=4)

        self.assertTrue(isinstance(results['q1'][9], JScoredDoc))
        self.assertEqual(results['q1'][9].docid, 'CACM-2516')
        self.assertAlmostEqual(results['q1'][9].score, 4.2174, places=4)

        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JScoredDoc))
        self.assertEqual(results['q2'][0].docid, 'CACM-3058')
        self.assertAlmostEqual(results['q2'][0].score, 2.8576, places=4)

        self.assertTrue(isinstance(results['q2'][9], JScoredDoc))
        self.assertEqual(results['q2'][9].docid, 'CACM-3040')
        self.assertAlmostEqual(results['q2'][9].score, 2.6878, places=4)

    def test_basic_k(self):
        hits = self.searcher.search('information retrieval', k=100)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(len(hits), 100)

    def test_batch_k(self):
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], k=100, threads=2)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))
        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JScoredDoc))
        self.assertEqual(len(results['q1']), 100)
        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JScoredDoc))
        self.assertEqual(len(results['q2']), 100)

    def test_basic_fields(self):
        # This test just provides a sanity check, it's not that interesting as it only searches one field.
        hits = self.searcher.search('information retrieval', k=42, fields={'contents': 2.0},)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(len(hits), 42)

    def test_batch_fields(self):
        # This test just provides a sanity check, it's not that interesting as it only searches one field.
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], k=42,
                                             threads=2, fields={'contents': 2.0})

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))
        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JScoredDoc))
        self.assertEqual(len(results['q1']), 42)
        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JScoredDoc))
        self.assertEqual(len(results['q2']), 42)

    def test_different_similarity(self):
        # qld, default mu
        self.searcher.set_qld()
        self.assertTrue(self.searcher.get_similarity().toString().startswith('LM Dirichlet'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 3.6803, places=4)
        self.assertEqual(hits[9].docid, 'CACM-1927')
        self.assertAlmostEqual(hits[9].score, 2.5324, places=4)

        # bm25, default parameters
        self.searcher.set_bm25()
        self.assertTrue(self.searcher.get_similarity().toString().startswith('BM25'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.7655, places=4)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.2174, places=4)

        # qld, custom mu
        self.searcher.set_qld(100)
        self.assertTrue(self.searcher.get_similarity().toString().startswith('LM Dirichlet'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 6.3558, places=4)
        self.assertEqual(hits[9].docid, 'CACM-2631')
        self.assertAlmostEqual(hits[9].score, 5.1896, places=4)

        # bm25, custom parameters
        self.searcher.set_bm25(0.8, 0.3)
        self.assertTrue(self.searcher.get_similarity().toString().startswith('BM25'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.8688, places=4)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.3332, places=4)

    def test_rm3(self):
        self.searcher = LuceneSearcher(f'{self.index_dir}lucene-index.cacm')
        self.searcher.set_rm3()
        self.assertTrue(self.searcher.is_using_rm3())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 2.1735, places=4)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 1.7018, places=4)

        self.searcher.unset_rm3()
        self.assertFalse(self.searcher.is_using_rm3())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.7655, places=4)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.2174, places=4)

        self.searcher.set_rm3(fb_docs=4, fb_terms=6, original_query_weight=0.3)
        self.assertTrue(self.searcher.is_using_rm3())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 2.1715, places=4)
        self.assertEqual(hits[9].docid, 'CACM-1457')
        self.assertAlmostEqual(hits[9].score, 1.4556, places=4)

    def test_rocchio(self):
        self.searcher = LuceneSearcher(f'{self.index_dir}lucene-index.cacm')
        self.searcher.set_rocchio()
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 7.1883, places=4)
        self.assertEqual(hits[9].docid, 'CACM-2140')
        self.assertAlmostEqual(hits[9].score, 5.5797, places=4)

        self.searcher.unset_rocchio()
        self.assertFalse(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.7655, places=4)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.2174, places=4)

        self.searcher.set_rocchio(top_fb_terms=10, top_fb_docs=8, bottom_fb_terms=10,
                                  bottom_fb_docs=8, alpha=0.4, beta=0.5, gamma=0.1,
                                  debug=False, use_negative=True)
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 3.6489, places=4)
        self.assertEqual(hits[9].docid, 'CACM-1032')
        self.assertAlmostEqual(hits[9].score, 2.5751, places=4)

        self.searcher.set_rocchio(top_fb_terms=10, top_fb_docs=8, bottom_fb_terms=10,
                                  bottom_fb_docs=8, alpha=0.4, beta=0.5, gamma=0.1,
                                  debug=False, use_negative=False)
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.0390, places=4)
        self.assertEqual(hits[9].docid, 'CACM-1032')
        self.assertAlmostEqual(hits[9].score, 2.9155, places=4)

    @classmethod
    def tearDownClass(cls):
        cls.searcher.close()
        os.remove(cls.tarball_name)
        shutil.rmtree(cls.index_dir)


if __name__ == '__main__':
    unittest.main()
