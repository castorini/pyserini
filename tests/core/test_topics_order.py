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

import unittest
import tempfile
from pyserini.query_iterator import DefaultQueryIterator


class TestEncodedQueries(unittest.TestCase):

    def setUp(self):
        pass

    def test_default_order(self):
        query_iterator = DefaultQueryIterator.from_topics('core17')
        topic_ids, _ = zip(*list(query_iterator))
        self.assertTrue(topic_ids[0], 307)
        self.assertTrue(topic_ids[1], 310)
        self.assertTrue(topic_ids[-1], 690)

    def test_specified_order(self):
        query_iterator = DefaultQueryIterator.from_topics('msmarco-passage-dev-subset')
        topic_ids, _ = zip(*list(query_iterator))
        self.assertTrue(topic_ids[0], 1048585)
        self.assertTrue(topic_ids[1], 2)
        self.assertTrue(topic_ids[-1], 524332)

    def test_topics_as_int(self):
        topics_int = (
            "1999\tA simple query\n"
            "1998\tAnother simple query\n"
        )
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.tsv') as tmpfile:
            tmpfile.write(topics_int)
            tmpfile_path = tmpfile.name
    
        query_iterator = DefaultQueryIterator.from_topics(tmpfile_path)
        topic_ids, _ = zip(*list(query_iterator))
        self.assertEqual(topic_ids[0], 1998)
        self.assertEqual(topic_ids[1], 1999)
        
    def test_topics_as_str(self):
        topics_str = (
            "B\tAnother simple query\n"
            "A\tA simple query\n"
        )
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.tsv') as tmpfile:
            tmpfile.write(topics_str)
            tmpfile_path = tmpfile.name

        query_iterator = DefaultQueryIterator.from_topics(tmpfile_path)
        topic_ids, _ = zip(*list(query_iterator))
        self.assertEqual(topic_ids[0], "A")
        self.assertEqual(topic_ids[1], "B")

    def test_topics_as_int_str(self):
        topics_int_string = (
            "B\tAnother simple query\n"
            "1998\tA simple query\n"
        )
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.tsv') as tmpfile:
            tmpfile.write(topics_int_string)
            tmpfile_path = tmpfile.name
    
        query_iterator = DefaultQueryIterator.from_topics(tmpfile_path)
        topic_ids, _ = zip(*list(query_iterator))
        self.assertEqual(topic_ids[0], 1998)
        self.assertEqual(topic_ids[1], "B")
            
            
    def tearDown(self):
        pass
