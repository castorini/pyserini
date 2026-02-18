import os
import tarfile
import unittest
from random import randint
from urllib.request import urlretrieve

from pyserini.search.lucene import LuceneSearcher
from pyserini.search.lucene.rerank.rm3_reranker import RM3Reranker
from pyserini.search.lucene.rerank.rocchio_reranker import RocchioReranker


class TestPythonRerankers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Randomize filenames to avoid clashes
        r = randint(0, 10000000)
        cls.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene9-index.cacm.tar.gz'
        cls.tarball_name = f'lucene-index.cacm-{r}.tar.gz'
        cls.searcher_index_dir = f'cacm_index_{r}/'

        if not os.path.exists(cls.searcher_index_dir):
            urlretrieve(cls.collection_url, cls.tarball_name)
            with tarfile.open(cls.tarball_name) as tarball:
                tarball.extractall(cls.searcher_index_dir)

        # Full CACM searcher for rerankers (with doc vectors)
        cls.searcher = LuceneSearcher(f'{cls.searcher_index_dir}lucene9-index.cacm')

        corpus_path = 'tests/resources/sample_collection_json'
        cls.no_vec_searcher_index_dir = 'no_vec_index'
        if not os.path.exists(cls.no_vec_searcher_index_dir):
            os.system(
                f'python -m pyserini.index.lucene -collection JsonCollection '
                f'-generator DefaultLuceneDocumentGenerator -threads 1 '
                f'-input {corpus_path} -index {cls.no_vec_searcher_index_dir}'
            )
        cls.no_vec_searcher = LuceneSearcher(cls.no_vec_searcher_index_dir)

    def test_rm3_changes_ranking(self):
        self.searcher.set_rm3(use_python=True)
        self.assertTrue(self.searcher.is_using_rm3())

        hits = self.searcher.search('information retrieval')

        # Check top-10 results and scores (these numbers are from CACM reference)
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 2.17350, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 1.70180, places=5)

        # Disable RM3
        self.searcher.unset_rm3()
        self.assertFalse(self.searcher.is_using_rm3())
        self.assertIsNone(self.searcher.get_feedback_terms('information retrieval'))

        hits = self.searcher.search('information retrieval')
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

        # Set RM3 with custom parameters
        self.searcher.set_rm3(fb_docs=4, fb_terms=6, original_query_weight=0.3, use_python=True)
        self.assertTrue(self.searcher.is_using_rm3())

        hits = self.searcher.search('information retrieval')
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 2.17150, places=5)
        self.assertEqual(hits[9].docid, 'CACM-1457')
        self.assertAlmostEqual(hits[9].score, 1.45560, places=5)

        # RM3 should fail on index without document vectors
        with self.assertRaises(TypeError):
            self.no_vec_searcher.set_rm3(use_python=True)

        self.searcher.unset_rm3()

    def test_rocchio_changes_ranking(self):
        self.searcher.set_rocchio(use_python=True)
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')

        # Check top-10 results and scores (CACM reference)
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 7.18830, delta=0.002)
        self.assertEqual(hits[9].docid, 'CACM-2140')
        self.assertAlmostEqual(hits[9].score, 5.57970, delta=5)

        # Disable Rocchio
        self.searcher.unset_rocchio()
        self.searcher.unset_rm3()
        self.assertFalse(self.searcher.is_using_rocchio())
        self.assertIsNone(self.searcher.get_feedback_terms('information retrieval'))

        hits = self.searcher.search('information retrieval')
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

        # Rocchio with negative feedback
        self.searcher.set_rocchio(
            top_fb_terms=10, top_fb_docs=8, bottom_fb_terms=10, bottom_fb_docs=8,
            alpha=0.4, beta=0.5, gamma=0.1, debug=False, use_negative=True, use_python=True
        )
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 3.64890, delta=0.08)
        self.assertEqual(hits[9].docid, 'CACM-1032')
        self.assertAlmostEqual(hits[9].score, 2.57510, delta=0.006)

        # Rocchio without negative feedback
        self.searcher.set_rocchio(
            top_fb_terms=10, top_fb_docs=8, bottom_fb_terms=10, bottom_fb_docs=8,
            alpha=0.4, beta=0.5, gamma=0.0, debug=False, use_negative=False, use_python=True
        )
        self.assertTrue(self.searcher.is_using_rocchio())

        hits = self.searcher.search('information retrieval')
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.03900, delta=0.0003)
        self.assertEqual(hits[9].docid, 'CACM-1032')
        self.assertAlmostEqual(hits[9].score, 2.91550, delta=0.0005)

        # Rocchio should fail on index without document vectors
        with self.assertRaises(TypeError):
            self.no_vec_searcher.set_rocchio(use_python=True)


if __name__ == '__main__':
    unittest.main()
