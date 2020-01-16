import os
import shutil
import tarfile
import unittest

from pyserini.index import pyutils
from urllib.request import urlretrieve
from random import randint


class TestIndexUtils(unittest.TestCase):
    def setUp(self):
        # Download pre-built CACM index; append a random value to avoid filename clashes.
        r = randint(0, 10000000)
        self.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene-index.cacm.tar.gz'
        self.tarball_name = 'lucene-index.cacm-{}.tar.gz'.format(r)
        self.index_dir = 'index{}/'.format(r)

        filename, headers = urlretrieve(self.collection_url, self.tarball_name)

        tarball = tarfile.open(self.tarball_name)
        tarball.extractall(self.index_dir)
        tarball.close()

        self.index_utils = pyutils.IndexReaderUtils('{}lucene-index.cacm'.format(self.index_dir))

    def test_terms(self):
        self.assertEqual(sum(1 for x in self.index_utils.terms()), 14363)

    def test_analyze(self):
        self.assertEqual(' '.join(self.index_utils.analyze('retrieval')), 'retriev')
        self.assertEqual(' '.join(self.index_utils.analyze('rapid retrieval, space economy')), 'rapid retriev space economi')

    def test_term_stats(self):
        collection_freq, doc_freq = self.index_utils.get_term_counts('retrieval')
        self.assertEqual(collection_freq, 275)
        self.assertEqual(doc_freq, 138)

    def test_postings(self):
        term = 'retrieval'
        postings_list = list(self.index_utils.get_postings_list(term))
        self.assertEqual(len(postings_list), 138)

        self.assertEqual(postings_list[0].docid, 238)
        self.assertEqual(postings_list[0].term_freq, 1)

        self.assertEqual(postings_list[-1].docid, 3168)
        self.assertEqual(postings_list[-1].term_freq, 1)

    def test_doc_vector(self):
        doc_vector = self.index_utils.get_document_vector('CACM-3134')
        self.assertEqual(len(doc_vector), 94)
        self.assertEqual(doc_vector['inform'], 8)
        self.assertEqual(doc_vector['retriev'], 7)

    def test_raw_doc(self):
        lines = self.index_utils.get_raw_document('CACM-3134').splitlines()
        self.assertEqual(len(lines), 55)
        self.assertEqual(lines[4], 'The Use of Normal Multiplication Tables')
        self.assertEqual(lines[29], 'rapid retrieval, space economy')

    def test_bm25_weight(self):
        self.assertAlmostEqual(self.index_utils.get_bm25_term_weight('CACM-3134', 'inform'), 1.925014, places=5)
        self.assertAlmostEqual(self.index_utils.get_bm25_term_weight('CACM-3134', 'retriev'), 2.496352, places=5)

    def tearDown(self):
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()
