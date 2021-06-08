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

from pyserini import search
from pyserini.analysis import get_lucene_analyzer
from pyserini.search import querybuilder


class TestQueryBuilding(unittest.TestCase):
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

        self.searcher = search.SimpleSearcher(f'{self.index_dir}lucene-index.cacm')

    def testBuildBoostedQuery(self):
        term_query1 = querybuilder.get_term_query('information')
        term_query2 = querybuilder.get_term_query('retrieval')

        boost1 = querybuilder.get_boost_query(term_query1, 2.)
        boost2 = querybuilder.get_boost_query(term_query2, 2.)

        should = querybuilder.JBooleanClauseOccur['should'].value

        boolean_query = querybuilder.get_boolean_query_builder()
        boolean_query.add(boost1, should)
        boolean_query.add(boost2, should)

        bq = boolean_query.build()
        hits1 = self.searcher.search(bq)

        boolean_query2 = querybuilder.get_boolean_query_builder()
        boolean_query2.add(term_query1, should)
        boolean_query2.add(term_query2, should)

        bq2 = boolean_query2.build()
        hits2 = self.searcher.search(bq2)

        for h1, h2 in zip(hits1, hits2):
            self.assertEqual(h1.docid, h2.docid)
            self.assertAlmostEqual(h1.score, h2.score*2, delta=0.001)

        boost3 = querybuilder.get_boost_query(term_query1, 2.)
        boost4 = querybuilder.get_boost_query(term_query2, 3.)

        boolean_query = querybuilder.get_boolean_query_builder()
        boolean_query.add(boost3, should)
        boolean_query.add(boost4, should)

        bq3 = boolean_query.build()
        hits3 = self.searcher.search(bq3)

        for h1, h3 in zip(hits1, hits3):
            self.assertNotEqual(h1.score, h3.score)

    def testTermQuery(self):
        should = querybuilder.JBooleanClauseOccur['should'].value
        query_builder = querybuilder.get_boolean_query_builder()
        query_builder.add(querybuilder.get_term_query('information'), should)
        query_builder.add(querybuilder.get_term_query('retrieval'), should)

        query = query_builder.build()
        hits1 = self.searcher.search(query)
        hits2 = self.searcher.search('information retrieval')

        for h1, h2 in zip(hits1, hits2):
            self.assertEqual(h1.docid, h2.docid)
            self.assertEqual(h1.score, h2.score)

    def testIncompatabilityWithRM3(self):
        should = querybuilder.JBooleanClauseOccur['should'].value
        query_builder = querybuilder.get_boolean_query_builder()
        query_builder.add(querybuilder.get_term_query('information'), should)
        query_builder.add(querybuilder.get_term_query('retrieval'), should)

        query = query_builder.build()
        hits = self.searcher.search(query)
        self.assertEqual(10, len(hits))

        self.searcher.set_rm3()
        self.assertTrue(self.searcher.is_using_rm3())

        with self.assertRaises(NotImplementedError):
            self.searcher.search(query)

    def testTermQuery2(self):
        term_query1 = querybuilder.get_term_query('inform', analyzer=get_lucene_analyzer(stemming=False))
        term_query2 = querybuilder.get_term_query('retriev', analyzer=get_lucene_analyzer(stemming=False))

        should = querybuilder.JBooleanClauseOccur['should'].value

        boolean_query1 = querybuilder.get_boolean_query_builder()
        boolean_query1.add(term_query1, should)
        boolean_query1.add(term_query2, should)

        bq1 = boolean_query1.build()
        hits1 = self.searcher.search(bq1)
        hits2 = self.searcher.search('information retrieval')

        for h1, h2 in zip(hits1, hits2):
            self.assertEqual(h1.docid, h2.docid)
            self.assertEqual(h1.score, h2.score)

    def tearDown(self):
        self.searcher.close()
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()
