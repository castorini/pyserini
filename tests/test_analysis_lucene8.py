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
from urllib.request import urlretrieve

from pyserini.analysis import get_lucene_analyzer
from pyserini.index.lucene import IndexReader
from pyserini.search.lucene import LuceneSearcher


class TestAnalyzersForLucene8(unittest.TestCase):
    # This class contains the test cases from test_analysis that require Lucene 8 backwards compatibility.
    def setUp(self):
        # Download pre-built CACM index built using Lucene 8; append a random value to avoid filename clashes.
        r = randint(0, 10000000)
        self.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene8-index.cacm.tar.gz'
        self.tarball_name = 'lucene-index.cacm-{}.tar.gz'.format(r)
        self.index_dir = 'index{}/'.format(r)

        _, _ = urlretrieve(self.collection_url, self.tarball_name)

        tarball = tarfile.open(self.tarball_name)
        tarball.extractall(self.index_dir)
        tarball.close()
        self.searcher = LuceneSearcher(f'{self.index_dir}lucene-index.cacm')
        self.index_utils = IndexReader(f'{self.index_dir}lucene-index.cacm')

    def test_different_analyzers_are_different(self):
        self.searcher.set_analyzer(get_lucene_analyzer(stemming=False))
        hits_first = self.searcher.search('information retrieval')
        self.searcher.set_analyzer(get_lucene_analyzer())
        hits_second = self.searcher.search('information retrieval')
        self.assertNotEqual(hits_first, hits_second)

    def tearDown(self):
        self.searcher.close()
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)
