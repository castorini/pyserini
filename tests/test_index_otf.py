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
import unittest
from typing import List

from pyserini.index.lucene import LuceneIndexer
from pyserini.search.lucene import JLuceneSearcherResult, LuceneSearcher


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.docs = []
        self.tmp_dir = "temp_dir"

        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('tests'):
            self.test_file = '../tests/resources/simple_cacm_corpus.json'
        else:
            self.test_file = 'tests/resources/simple_cacm_corpus.json'

    def test_indexer(self):
        indexer = LuceneIndexer(self.tmp_dir)

        with open(self.test_file) as f:
            for doc in f:
                indexer.add(doc)

        indexer.close()

        searcher = LuceneSearcher(self.tmp_dir)
        self.assertEqual(3, searcher.num_docs)

        hits = searcher.search('semantic networks')

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JLuceneSearcherResult))
        self.assertEqual(1, len(hits))
        self.assertEqual('CACM-2274', hits[0].docid)
        self.assertAlmostEqual(1.53650, hits[0].score, places=5)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
