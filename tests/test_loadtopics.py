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

import unittest

from pyserini.search import pysearch


class TestLoadTopics(unittest.TestCase):

    def test_robust04(self):
        topics = pysearch.get_topics('robust04')
        self.assertEqual(len(topics), 250)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_core17(self):
        topics = pysearch.get_topics('core17')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_core18(self):
        topics = pysearch.get_topics('core18')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_car15(self):
        topics = pysearch.get_topics('car17v1.5_benchmarkY1test')
        self.assertEqual(len(topics), 2125)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

    def test_car20(self):
        topics = pysearch.get_topics('car17v2.0_benchmarkY1test')
        self.assertEqual(len(topics), 2254)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_doc(self):
        topics = pysearch.get_topics('msmarco_doc_dev')
        self.assertEqual(len(topics), 5193)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage(self):
        topics = pysearch.get_topics('msmarco_passage_dev_subset')
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round1(self):
        topics = pysearch.get_topics('covid_round1')
        self.assertEqual(len(topics), 30)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))


if __name__ == '__main__':
    unittest.main()
