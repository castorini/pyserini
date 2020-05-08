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
from urllib.request import urlretrieve

from pyserini.search import pysearch, pyquerybuilder
from pyserini.analysis.pyanalysis import get_lucene_analyzer


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

        self.searcher = pysearch.SimpleSearcher(f'{self.index_dir}lucene-index.cacm')

    def testBuildBoostedQuery(self):
        term_query1 = pyquerybuilder.get_term_query('information')
        term_query2 = pyquerybuilder.get_term_query('retrieval')

        boost1 = pyquerybuilder.get_boost_query(term_query1, 1.)
        boost2 = pyquerybuilder.get_boost_query(term_query2, 1.)

        should = pyquerybuilder.get_clause_should()

        boolean_query = pyquerybuilder.get_boolean_query_builder()
        boolean_query.add(boost1, should)
        boolean_query.add(boost2, should)

        bq = boolean_query.build()
        hits1 = self.searcher.search(bq)

        boolean_query2 = pyquerybuilder.get_boolean_query_builder()
        boolean_query2.add(term_query1, should)
        boolean_query2.add(term_query2, should)

        bq2 = boolean_query2.build()
        hits2 = self.searcher.search(bq2)

        self.assertEqual(hits1[0].docid, hits2[0].docid)
        self.assertEqual(hits1[0].score, hits2[0].score)

        boost3 = pyquerybuilder.get_boost_query(term_query1, 2.)
        boost4 = pyquerybuilder.get_boost_query(term_query2, 3.)

        should = pyquerybuilder.get_clause_should()

        boolean_query = pyquerybuilder.get_boolean_query_builder()
        boolean_query.add(boost3, should)
        boolean_query.add(boost4, should)

        bq3 = boolean_query.build()
        hits3 = self.searcher.search(bq3)

        self.assertNotEqual(hits1[0].score, hits3[0].score)

    def testTermQuery(self):
        term_query1 = pyquerybuilder.get_term_query('information')
        term_query2 = pyquerybuilder.get_term_query('retrieval')

        should = pyquerybuilder.get_clause_should()

        boolean_query1 = pyquerybuilder.get_boolean_query_builder()
        boolean_query1.add(term_query1, should)
        boolean_query1.add(term_query2, should)

        bq1 = boolean_query1.build()
        hits1 = self.searcher.search(bq1)
        hits2 = self.searcher.search('information retrieval')

        self.assertEqual(hits1[0].docid, hits2[0].docid)
        self.assertEqual(hits1[0].score, hits2[0].score)

    def testTermQuery2(self):
        term_query1 = pyquerybuilder.get_term_query('inform', analyzer=get_lucene_analyzer(stemming=False))
        term_query2 = pyquerybuilder.get_term_query('retriev', analyzer=get_lucene_analyzer(stemming=False))

        should = pyquerybuilder.get_clause_should()

        boolean_query1 = pyquerybuilder.get_boolean_query_builder()
        boolean_query1.add(term_query1, should)
        boolean_query1.add(term_query2, should)

        bq1 = boolean_query1.build()
        hits1 = self.searcher.search(bq1)
        hits2 = self.searcher.search('information retrieval')

        self.assertEqual(hits1[0].docid, hits2[0].docid)
        self.assertEqual(hits1[0].score, hits2[0].score)

    def tearDown(self):
        self.searcher.close()
        os.remove(self.tarball_name)
        shutil.rmtree(self.index_dir)


if __name__ == '__main__':
    unittest.main()
