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
#

import unittest
import os
import shutil
from pyserini.search import get_topics
from pyserini.query_iterator import query_iterator


class TestEncodedQueries(unittest.TestCase):

    def setUp(self):
        pass

    def test_default_order(self):
        topics = get_topics('core17')
        topic_ids, _ = zip(*list(query_iterator(topics, 'core17')))
        self.assertTrue(topic_ids[0], 307)
        self.assertTrue(topic_ids[1], 310)
        self.assertTrue(topic_ids[-1], 690)

    def test_specified_order(self):
        topics = get_topics('msmarco-passage-dev-subset')
        topic_ids, _ = zip(*list(query_iterator(topics, 'msmarco-passage-dev-subset')))
        self.assertTrue(topic_ids[0], 1048585)
        self.assertTrue(topic_ids[1], 2)
        self.assertTrue(topic_ids[-1], 524332)

    def tearDown(self):
        pass
