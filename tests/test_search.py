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
from pyserini.index.lucene import Document


class TestSearch(unittest.TestCase):
    tarball_name = None
    collection_url = None
    searcher = None
    searcher_index_dir = None
    no_vec_searcher = None
    no_vec_searcher_index_dir = None

    @classmethod
    def setUpClass(cls):
        # Download pre-built CACM index built using Lucene 9; append a random value to avoid filename clashes.
        r = randint(0, 10000000)
        cls.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene9-index.cacm.tar.gz'
        cls.tarball_name = 'lucene-index.cacm-{}.tar.gz'.format(r)
        cls.searcher_index_dir = 'index{}/'.format(r)

        urlretrieve(cls.collection_url, cls.tarball_name)

        tarball = tarfile.open(cls.tarball_name)
        tarball.extractall(cls.searcher_index_dir)
        tarball.close()

        cls.searcher = LuceneSearcher(f'{cls.searcher_index_dir}lucene9-index.cacm')

        # Create index without document vectors
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('tests'):
            corpus_path = '../tests/resources/sample_collection_json'
        else:
            corpus_path = 'tests/resources/sample_collection_json'

        cls.no_vec_searcher_index_dir = 'no_vec_index'
        cmd1 = f'python -m pyserini.index.lucene -collection JsonCollection ' + \
               f'-generator DefaultLuceneDocumentGenerator ' + \
               f'-threads 1 -input {corpus_path} -index {cls.no_vec_searcher_index_dir}'
        os.system(cmd1)
        cls.no_vec_searcher = LuceneSearcher(cls.no_vec_searcher_index_dir)

    def test_basic(self):
        self.assertTrue(self.searcher.get_similarity().toString().startswith('BM25'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(hits, List))

        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertEqual(hits[0].lucene_docid, 3133)
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)

        # Test accessing the raw Lucene document and fetching fields from it:
        self.assertEqual(hits[0].lucene_document.getField('id').stringValue(), 'CACM-3134')
        self.assertEqual(hits[0].lucene_document.get('id'), 'CACM-3134')      # simpler call, same result as above
        self.assertEqual(len(hits[0].lucene_document.getField('contents').stringValue()), 1500)
        self.assertEqual(len(hits[0].lucene_document.get('contents')), 1500)  # simpler call, same result as above
        self.assertEqual(len(hits[0].lucene_document.getField('raw').stringValue()), 1532)
        self.assertEqual(len(hits[0].lucene_document.get('raw')), 1532)       # simpler call, same result as above

        self.assertTrue(isinstance(hits[9], JScoredDoc))
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

        hits = self.searcher.search('search')

        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(hits[0].docid, 'CACM-3058')
        self.assertAlmostEqual(hits[0].score, 2.85760, places=5)

        self.assertTrue(isinstance(hits[9], JScoredDoc))
        self.assertEqual(hits[9].docid, 'CACM-3040')
        self.assertAlmostEqual(hits[9].score, 2.68780, places=5)

    def test_batch(self):
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], threads=2)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))

        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JScoredDoc))
        self.assertEqual(results['q1'][0].docid, 'CACM-3134')
        self.assertAlmostEqual(results['q1'][0].score, 4.76550, places=5)

        self.assertTrue(isinstance(results['q1'][9], JScoredDoc))
        self.assertEqual(results['q1'][9].docid, 'CACM-2516')
        self.assertAlmostEqual(results['q1'][9].score, 4.21740, places=5)

        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JScoredDoc))
        self.assertEqual(results['q2'][0].docid, 'CACM-3058')
        self.assertAlmostEqual(results['q2'][0].score, 2.85760, places=5)

        self.assertTrue(isinstance(results['q2'][9], JScoredDoc))
        self.assertEqual(results['q2'][9].docid, 'CACM-3040')
        self.assertAlmostEqual(results['q2'][9].score, 2.68780, places=5)

    def test_batch_rocchio(self):
        self.searcher.set_rocchio()
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], threads=2)
        self.searcher.unset_rocchio()

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))

        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JScoredDoc))
        self.assertEqual(results['q1'][0].docid, 'CACM-3134')
        self.assertAlmostEqual(results['q1'][0].score, 7.18830, places=5)

        self.assertTrue(isinstance(results['q1'][9], JScoredDoc))
        self.assertEqual(results['q1'][9].docid, 'CACM-2140')
        self.assertAlmostEqual(results['q1'][9].score, 5.57970, places=5)

        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JScoredDoc))
        self.assertEqual(results['q2'][0].docid, 'CACM-3041')
        self.assertAlmostEqual(results['q2'][0].score, 6.14870, places=5)

        self.assertTrue(isinstance(results['q2'][9], JScoredDoc))
        self.assertEqual(results['q2'][9].docid, 'CACM-2251')
        self.assertAlmostEqual(results['q2'][9].score, 4.97380, places=5)

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
        hits = self.searcher.search('information retrieval', k=42, fields={'contents': 2.0})

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
        self.assertAlmostEqual(hits[0].score, 3.68030, places=5)
        self.assertEqual(hits[9].docid, 'CACM-1927')
        self.assertAlmostEqual(hits[9].score, 2.53240, places=5)

        # bm25, default parameters
        self.searcher.set_bm25()
        self.assertTrue(self.searcher.get_similarity().toString().startswith('BM25'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

        # qld, custom mu
        self.searcher.set_qld(100)
        self.assertTrue(self.searcher.get_similarity().toString().startswith('LM Dirichlet'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 6.35580, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2631')
        self.assertAlmostEqual(hits[9].score, 5.18960, places=5)

        # bm25, custom parameters
        self.searcher.set_bm25(0.8, 0.3)
        self.assertTrue(self.searcher.get_similarity().toString().startswith('BM25'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.86880, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.33320, places=5)

    def test_rm3(self):
        self.searcher = LuceneSearcher(f'{self.searcher_index_dir}lucene9-index.cacm')
        self.searcher.set_rm3()
        self.assertTrue(self.searcher.is_using_rm3())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 2.17350, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 1.70180, places=5)

        feedback_terms = self.searcher.get_feedback_terms('information retrieval')
        self.assertEqual(len(feedback_terms), 10)
        self.assertAlmostEqual(feedback_terms['storag'], 0.024701, places=5)

        self.searcher.unset_rm3()
        self.assertFalse(self.searcher.is_using_rm3())
        self.assertIsNone(self.searcher.get_feedback_terms('information retrieval'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

        self.searcher.set_rm3(fb_docs=4, fb_terms=6, original_query_weight=0.3)
        self.assertTrue(self.searcher.is_using_rm3())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 2.17150, places=5)
        self.assertEqual(hits[9].docid, 'CACM-1457')
        self.assertAlmostEqual(hits[9].score, 1.45560, places=5)

        with self.assertRaises(TypeError):
            self.no_vec_searcher.set_rm3()

    def test_rocchio(self):
        self.searcher = LuceneSearcher(f'{self.searcher_index_dir}lucene9-index.cacm')
        self.searcher.set_rocchio()
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 7.18830, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2140')
        self.assertAlmostEqual(hits[9].score, 5.57970, places=5)

        feedback_terms = self.searcher.get_feedback_terms('information retrieval')
        self.assertEqual(len(feedback_terms), 10)
        self.assertAlmostEqual(feedback_terms['storag'], 0.132200, places=5)

        self.searcher.unset_rocchio()
        self.assertFalse(self.searcher.is_using_rocchio())
        self.assertIsNone(self.searcher.get_feedback_terms('information retrieval'))

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

        self.searcher.set_rocchio(top_fb_terms=10, top_fb_docs=8, bottom_fb_terms=10,
                                  bottom_fb_docs=8, alpha=0.4, beta=0.5, gamma=0.1,
                                  debug=False, use_negative=True)
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 3.64890, places=5)
        self.assertEqual(hits[9].docid, 'CACM-1032')
        self.assertAlmostEqual(hits[9].score, 2.57510, places=5)

        self.searcher.set_rocchio(top_fb_terms=10, top_fb_docs=8, bottom_fb_terms=10,
                                  bottom_fb_docs=8, alpha=0.4, beta=0.5, gamma=0.1,
                                  debug=False, use_negative=False)
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.03900, places=5)
        self.assertEqual(hits[9].docid, 'CACM-1032')
        self.assertAlmostEqual(hits[9].score, 2.91550, places=5)

        with self.assertRaises(TypeError):
            self.no_vec_searcher.set_rocchio()

    def test_doc_int(self):
        # The doc method is overloaded: if input is int, it's assumed to be a Lucene internal docid.
        doc = self.searcher.doc(1)
        self.assertTrue(isinstance(doc, Document))

        # These are all equivalent ways to get the docid.
        self.assertEqual('CACM-0002', doc.id())
        self.assertEqual('CACM-0002', doc.docid())
        self.assertEqual('CACM-0002', doc.get('id'))
        self.assertEqual('CACM-0002', doc.lucene_document().getField('id').stringValue())

        # These are all equivalent ways to get the 'raw' field
        self.assertEqual(186, len(doc.raw()))
        self.assertEqual(186, len(doc.get('raw')))
        self.assertEqual(186, len(doc.lucene_document().get('raw')))
        self.assertEqual(186, len(doc.lucene_document().getField('raw').stringValue()))

        # These are all equivalent ways to get the 'contents' field
        self.assertEqual(154, len(doc.contents()))
        self.assertEqual(154, len(doc.get('contents')))
        self.assertEqual(154, len(doc.lucene_document().get('contents')))
        self.assertEqual(154, len(doc.lucene_document().getField('contents').stringValue()))

        # Should return None if we request a docid that doesn't exist
        self.assertTrue(self.searcher.doc(314159) is None)

    def test_doc_str(self):
        # The doc method is overloaded: if input is str, it's assumed to be an external collection docid.
        doc = self.searcher.doc('CACM-0002')
        self.assertTrue(isinstance(doc, Document))

        # These are all equivalent ways to get the docid.
        self.assertEqual(doc.lucene_document().getField('id').stringValue(), 'CACM-0002')
        self.assertEqual(doc.id(), 'CACM-0002')
        self.assertEqual(doc.docid(), 'CACM-0002')
        self.assertEqual(doc.get('id'), 'CACM-0002')

        # These are all equivalent ways to get the 'raw' field
        self.assertEqual(186, len(doc.raw()))
        self.assertEqual(186, len(doc.get('raw')))
        self.assertEqual(186, len(doc.lucene_document().get('raw')))
        self.assertEqual(186, len(doc.lucene_document().getField('raw').stringValue()))

        # These are all equivalent ways to get the 'contents' field
        self.assertEqual(154, len(doc.contents()))
        self.assertEqual(154, len(doc.get('contents')))
        self.assertEqual(154, len(doc.lucene_document().get('contents')))
        self.assertEqual(154, len(doc.lucene_document().getField('contents').stringValue()))

        # Should return None if we request a docid that doesn't exist
        self.assertTrue(self.searcher.doc('foo') is None)

    def test_batch_doc(self):
        docids = ['CACM-0002', 'CACM-3134', 'Fake Doc1', 'Fake Doc2']
        batch_doc = self.searcher.batch_doc(docids, threads=2)

        # Doc Id should have corresponding Document object in batch result
        for docid in docids[:2]:
            doc = batch_doc.get(docid)
            self.assertTrue(isinstance(doc, Document))
            self.assertEqual(doc.lucene_document().getField('id').stringValue(), docid)
            self.assertEqual(doc.id(), docid)
            self.assertEqual(doc.docid(), docid)
            self.assertEqual(doc.get('id'), docid)

        # None should be returned for docids that don't exist
        for docid in docids[2:]:
            doc = batch_doc.get(docid[-1])
            self.assertEqual(doc, None)

    def test_doc_by_field(self):
        self.assertEqual(self.searcher.doc('CACM-3134').docid(),
                         self.searcher.doc_by_field('id', 'CACM-3134').docid())

        # Should return None if we request a docid that doesn't exist
        self.assertTrue(self.searcher.doc_by_field('foo', 'bar') is None)

    @classmethod
    def tearDownClass(cls):
        cls.searcher.close()
        cls.no_vec_searcher.close()
        os.remove(cls.tarball_name)
        shutil.rmtree(cls.searcher_index_dir)
        shutil.rmtree(cls.no_vec_searcher_index_dir)


if __name__ == '__main__':
    unittest.main()
