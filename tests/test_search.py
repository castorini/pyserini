# -*- coding: utf-8 -*-
#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

import os
import shutil
import tarfile
import unittest
from random import randint
from typing import List, Dict
from urllib.request import urlretrieve

from pyserini.pyclass import JResult
from pyserini.search import pysearch


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

        self.searcher = pysearch.SimpleSearcher(f'{self.index_dir}lucene-index.cacm')

    def test_basic(self):
        hits = self.searcher.search('information retrieval')

        self.assertTrue(isinstance(hits, List))

        self.assertTrue(isinstance(hits[0], JResult))
        self.assertEqual(hits[0].docid, 'CACM-3134')
        self.assertEqual(hits[0].lucene_docid, 3133)
        self.assertEqual(hits[0].contents, None)
        self.assertEqual(len(hits[0].raw), 1532)
        self.assertAlmostEqual(hits[0].score, 4.76550, places=5)

        # Test accessing the raw Lucene document and fetching fields from it:
        self.assertEqual(hits[0].lucene_document.getField('id').stringValue(), 'CACM-3134')
        self.assertEqual(hits[0].lucene_document.get('id'), 'CACM-3134')  # simpler call, same result as above
        self.assertEqual(len(hits[0].lucene_document.getField('raw').stringValue()), 1532)
        self.assertEqual(len(hits[0].lucene_document.get('raw')), 1532)   # simpler call, same result as above

        self.assertTrue(isinstance(hits[9], JResult))
        self.assertEqual(hits[9].docid, 'CACM-2516')
        self.assertAlmostEqual(hits[9].score, 4.21740, places=5)

        hits = self.searcher.search('search')

        self.assertTrue(isinstance(hits[0], JResult))
        self.assertEqual(hits[0].docid, 'CACM-3058')
        self.assertAlmostEqual(hits[0].score, 2.85760, places=5)

        self.assertTrue(isinstance(hits[9], JResult))
        self.assertEqual(hits[9].docid, 'CACM-3040')
        self.assertAlmostEqual(hits[9].score, 2.68780, places=5)

    def test_batch(self):
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], threads=2)

        self.assertTrue(isinstance(results, Dict))

        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JResult))
        self.assertEqual(results['q1'][0].docid, 'CACM-3134')
        self.assertAlmostEqual(results['q1'][0].score, 4.76550, places=5)

        self.assertTrue(isinstance(results['q1'][9], JResult))
        self.assertEqual(results['q1'][9].docid, 'CACM-2516')
        self.assertAlmostEqual(results['q1'][9].score, 4.21740, places=5)

        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JResult))
        self.assertEqual(results['q2'][0].docid, 'CACM-3058')
        self.assertAlmostEqual(results['q2'][0].score, 2.85760, places=5)

        self.assertTrue(isinstance(results['q2'][9], JResult))
        self.assertEqual(results['q2'][9].docid, 'CACM-3040')
        self.assertAlmostEqual(results['q2'][9].score, 2.68780, places=5)

    def test_basic_k(self):
        hits = self.searcher.search('information retrieval', k=100)

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JResult))
        self.assertEqual(len(hits), 100)

    def test_batch_k(self):
        results = self.searcher.batch_search(['information retrieval', 'search'], ['q1', 'q2'], k=100, threads=2)

        self.assertTrue(isinstance(results, Dict))
        self.assertTrue(isinstance(results['q1'], List))
        self.assertTrue(isinstance(results['q1'][0], JResult))
        self.assertEqual(len(results['q1']), 100)
        self.assertTrue(isinstance(results['q2'], List))
        self.assertTrue(isinstance(results['q2'][0], JResult))
        self.assertEqual(len(results['q2']), 100)

    def test_doc_int(self):
        # The doc method is overloaded: if input is int, it's assumed to be a Lucene internal docid.
        doc = self.searcher.doc(1)

        self.assertTrue(isinstance(doc, pysearch.Document))
        self.assertEqual(doc.docid(), 'CACM-0002')

        self.assertEqual(doc.lucene_document().getField('id').stringValue(), 'CACM-0002')
        self.assertEqual(len(doc.lucene_document().getField('raw').stringValue()), 186)

    def test_doc_str(self):
        # The doc method is overloaded: if input is str, it's assumed to be an external collection docid.
        doc = self.searcher.doc('CACM-0002')

        self.assertTrue(isinstance(doc, pysearch.Document))
        self.assertEqual(doc.docid(), 'CACM-0002')

        self.assertEqual(doc.lucene_document().getField('id').stringValue(), 'CACM-0002')
        self.assertEqual(len(doc.lucene_document().getField('raw').stringValue()), 186)

    def tearDown(self):
        self.searcher.close()
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()
