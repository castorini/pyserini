import os
import shutil
import tarfile
import unittest
from random import randint
from urllib.request import urlretrieve
from pyserini.analysis import pyanalysis
from pyserini.search import pysearch
from pyserini.index import pyutils
from pyserini.pyclass import JString


class TestAnalyzers(unittest.TestCase):

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
        self.searcher = pysearch.SimpleSearcher(f'{self.index_dir}lucene-index.cacm')
        self.index_utils = pyutils.IndexReaderUtils('{self.index_dir}lucene-index.cacm')

    def test_different_analyzers_are_different(self):
        self.searcher.set_analyzer(pyanalysis.get_analyzer('tokenize'))
        hits_first = self.searcher.search('information retrieval')
        self.searcher.set_analyzer(pyanalysis.get_analyzer(''))
        hits_second = self.searcher.search('information retrieval')
        self.assertNotEqual(hits_first, hits_second)

    def test_analyze_with_analyzer(self):
        tokenizer = pyanalysis.get_analyzer('tokenize')
        query = JString('information retrieval')
        only_tokenization = self.index_utils.object.analyze_with_analyzer(query, tokenizer)
        token_list = []
        for token in only_tokenization.toArray():
            token_list.append(token)
        self.assertEqual(token_list, ['information', 'retrieval'])

    def tearDown(self):
        self.searcher.close()
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)
