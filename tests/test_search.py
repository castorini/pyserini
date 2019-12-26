import os
import shutil
import tarfile
import unittest

from pyserini.search import pysearch
from urllib.request import urlretrieve
from random import randint

class TestSearch(unittest.TestCase):
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

    def test_basic(self):
        searcher = pysearch.SimpleSearcher('{}lucene-index.cacm'.format(self.index_dir))
        hits = searcher.search('information retrieval')

        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)

        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

    def tearDown(self):
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()
