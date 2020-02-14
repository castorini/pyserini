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
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(postings_list[0].docid), 'CACM-0239')
        self.assertEqual(postings_list[0].tf, 1)
        self.assertEqual(len(postings_list[0].positions), 1)

        self.assertEqual(postings_list[-1].docid, 3168)
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(postings_list[-1].docid), 'CACM-3169')
        self.assertEqual(postings_list[-1].tf, 1)
        self.assertEqual(len(postings_list[-1].positions), 1)

    def test_doc_vector(self):
        doc_vector = self.index_utils.get_document_vector('CACM-3134')
        self.assertEqual(len(doc_vector), 94)
        self.assertEqual(doc_vector['inform'], 8)
        self.assertEqual(doc_vector['retriev'], 7)

    def test_doc_vector_matches_index(self):
        # From the document vector, look up the term frequency of "information".
        doc_vector = self.index_utils.get_document_vector('CACM-3134')
        self.assertEqual(doc_vector['inform'], 8)

        # Now look up the postings list for "information".
        term = 'information'
        postings_list = list(self.index_utils.get_postings_list(term))

        for i in range(len(postings_list)):
            if self.index_utils.convert_internal_docid_to_collection_docid(postings_list[i].docid) == 'CACM-3134':
                # The tf values should match.
                self.assertEqual(postings_list[i].tf, 8)

    def test_raw_doc(self):
        lines = self.index_utils.get_raw_document('CACM-3134').splitlines()
        self.assertEqual(len(lines), 55)
        self.assertEqual(lines[4], 'The Use of Normal Multiplication Tables')
        self.assertEqual(lines[29], 'rapid retrieval, space economy')

    def test_bm25_weight(self):
        self.assertAlmostEqual(self.index_utils.get_bm25_term_weight('CACM-3134', 'inform'), 1.925014, places=5)
        self.assertAlmostEqual(self.index_utils.get_bm25_term_weight('CACM-3134', 'retriev'), 2.496352, places=5)

    def test_docid_converstion(self):
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(1), 'CACM-0002')
        self.assertEqual(self.index_utils.convert_collection_docid_to_internal_docid('CACM-0002'), 1)
        self.assertEqual(self.index_utils.convert_internal_docid_to_collection_docid(1000), 'CACM-1001')
        self.assertEqual(self.index_utils.convert_collection_docid_to_internal_docid('CACM-1001'), 1000)

    def tearDown(self):
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()
