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

import tempfile
import unittest

from pyserini.query_iterator import DefaultQueryIterator, QueryIterator
from pyserini.query_iterator_order_info import QUERY_IDS


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

    def test_get_predefined_order_bare_key(self):
        # A bare, already-hyphenated predefined name resolves to its QUERY_IDS order.
        order = QueryIterator.get_predefined_order('msmarco-passage-dev-subset')
        self.assertEqual(order, QUERY_IDS['msmarco-passage-dev-subset'])

    def test_get_predefined_order_underscore_topics(self):
        # The underscore form is normalized to hyphens for the membership test, so the
        # lookup must use that same normalized key, not the raw topics value.
        # Before the fix this raised KeyError: 'msmarco_passage_dev_subset'.
        order = QueryIterator.get_predefined_order('msmarco_passage_dev_subset')
        self.assertEqual(order, QUERY_IDS['msmarco-passage-dev-subset'])

    def test_get_predefined_order_file_path_topics(self):
        # A --topics value given as a file path (directory + extension) normalizes to
        # the bare stem, so the lookup must use that stem rather than the raw path.
        # Before the fix this raised KeyError on the full path.
        order = QueryIterator.get_predefined_order('/data/topics/msmarco-passage-dev-subset.tsv')
        self.assertEqual(order, QUERY_IDS['msmarco-passage-dev-subset'])

    def test_get_predefined_order_all_predefined_resolve(self):
        # Every predefined name must resolve without raising, in its bare, underscore,
        # and file-path forms, and always to the same order list.
        for name in QueryIterator.PREDEFINED_ORDER:
            expected = QUERY_IDS[name]
            self.assertEqual(QueryIterator.get_predefined_order(name), expected)
            self.assertEqual(QueryIterator.get_predefined_order(name.replace('-', '_')), expected)
            self.assertEqual(QueryIterator.get_predefined_order(f'/tmp/{name}.tsv'), expected)

    def test_get_predefined_order_unknown_returns_none(self):
        # A topics value that is not a predefined order returns None, so the iterator
        # falls back to sorted-key ordering downstream.
        self.assertIsNone(QueryIterator.get_predefined_order('core17'))
        self.assertIsNone(QueryIterator.get_predefined_order('/data/topics/not-predefined.tsv'))

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


if __name__ == '__main__':
    unittest.main()
