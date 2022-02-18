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

from pyserini.search.jass import JASSv2Searcher, JASSv2SearcherResult
import pyjass 
from pyserini.index import Document


class TestSearchPyJass(unittest.TestCase):
    def setUp(self):
        # Download pre-built CACM index; append a random value to avoid filename clashes.
        #TODO To-be filled in by the test runner.
        r = randint(0, 10000000)
        self.collection_url = 'https://github.com/prasys/anserini-data/raw/master/CACM/jass-index.cacm.tar.gz' # to be replaced
        self.tarball_name = 'jass-index.cacm-{}.tar.gz'.format(r)
        self.index_dir = 'jass{}/'.format(r)

        filename, headers = urlretrieve(self.collection_url, self.tarball_name)

        tarball = tarfile.open(self.tarball_name)
        tarball.extractall(self.index_dir)
        tarball.close()

        self.searcher = JASSv2Searcher(f'{self.index_dir}jass-index.cacm')

    def test_basic(self):
        hits = self.searcher.search('information retrieval')

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(hits, List))

        self.assertTrue(isinstance(hits[0], JASSv2SearcherResult))
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertEqual(hits[0].score, 664.0)



        self.assertTrue(isinstance(hits[9], JASSv2SearcherResult))
        self.assertEqual(hits[9].docid, 'CACM-2631')
        self.assertEqual(hits[9].score, 589.0)

        hits = self.searcher.search('search')

        self.assertTrue(isinstance(hits[0], JASSv2SearcherResult))
        self.assertEqual(hits[0].docid, 'CACM-3041')
        self.assertEqual(hits[0].score, 413.0)

        self.assertTrue(isinstance(hits[9], JASSv2SearcherResult))
        self.assertEqual(hits[9].docid, 'CACM-1815')
        self.assertEqual(hits[9].score, 392.0)

    def test_batch(self):
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], threads=2)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))

        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JASSv2SearcherResult))
        self.assertEqual(results['q1'][0].docid, 'CACM-3134')
        self.assertEqual(results['q1'][0].score, 664.0)

        self.assertTrue(isinstance(results['q1'][9], JASSv2SearcherResult))
        self.assertEqual(results['q1'][9].docid, 'CACM-2631')
        self.assertEqual(results['q1'][9].score, 589.0)

        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JASSv2SearcherResult))
        self.assertEqual(results['q2'][0].docid, 'CACM-3041')
        self.assertEqual(results['q2'][0].score, 413.0)

        self.assertTrue(isinstance(results['q2'][9], JASSv2SearcherResult))
        self.assertEqual(results['q2'][9].docid, 'CACM-1815')
        self.assertEqual(results['q2'][9].score, 392.0)

    def test_basic_k(self):
        hits = self.searcher.search('information retrieval', k=100)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JASSv2SearcherResult))
        self.assertEqual(len(hits), 100)

    def test_batch_k(self):
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], k=100, threads=2)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))
        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JASSv2SearcherResult))
        self.assertEqual(len(results['q1']), 100)
        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JASSv2SearcherResult))
        self.assertEqual(len(results['q2']), 99)

    def test_basic_rho(self):
        hits = self.searcher.search('information retrieval', k=42, rho=50)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JASSv2SearcherResult))
        self.assertEqual(hits[9].docid, 'CACM-1725')
        self.assertEqual(hits[9].score, 362.0)
        self.assertEqual(len(hits), 42)

    def test_batch_rho(self):
        # This test just provides a sanity check, it's not that interesting as it only searches one field.
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], k=42,
                                              threads=2, rho=50)

        self.assertEqual(3204, self.searcher.num_docs)
        self.assertTrue(isinstance(results, Dict))
        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JASSv2SearcherResult))
        self.assertEqual(len(results['q1']), 42)
        self.assertEqual(results['q1'][9].docid, 'CACM-1725')
        self.assertEqual(results['q1'][9].score, 362.0)

        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JASSv2SearcherResult))
        self.assertEqual(len(results['q2']), 42)
        self.assertEqual(results['q2'][9].docid, 'CACM-1815')
        self.assertEqual(results['q2'][9].score, 392.0)

    # def test_different_similarity(self):

    def test_ascii(self):
        output = self.searcher.set_ascii_parser()
        self.assertEqual(0, output)

    
    
    def test_basic_parser(self):
        output = self.searcher.set_basic_parser()
        self.assertEqual(0, output)



    def tearDown(self):
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()