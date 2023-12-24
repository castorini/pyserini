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
import random
from typing import List

from pyserini.index.lucene import LuceneIndexer, IndexReader, JacksonObjectMapper
from pyserini.search.lucene import JScoredDoc, LuceneSearcher


class TestIndexOTF(unittest.TestCase):
    def setUp(self):
        self.docs = []
        self.tmp_dir = f'tmp_{self.__class__.__name__}_{str(random.randint(0, 1000))}'

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
                indexer.add_doc_raw(doc)

        indexer.close()

        searcher = LuceneSearcher(self.tmp_dir)
        self.assertEqual(3, searcher.num_docs)

        hits = searcher.search('semantic networks')

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(1, len(hits))
        self.assertEqual('CACM-2274', hits[0].docid)
        self.assertAlmostEqual(1.53650, hits[0].score, places=5)

    def test_indexer_batch1(self):
        batch = []
        with open(self.test_file) as f:
            for doc in f:
                batch.append(doc)

        # Test different ways to initialize indexer.
        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_batch_raw(batch)
        indexer.close()

        searcher = LuceneSearcher(self.tmp_dir)
        self.assertEqual(3, searcher.num_docs)

        hits = searcher.search('semantic networks')

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(1, len(hits))
        self.assertEqual('CACM-2274', hits[0].docid)
        self.assertAlmostEqual(1.53650, hits[0].score, places=5)

        # Test different ways to initialize indexer.
        indexer = LuceneIndexer(self.tmp_dir, threads=2)
        indexer.add_batch_raw(batch)
        indexer.close()

        searcher = LuceneSearcher(self.tmp_dir)
        self.assertEqual(3, searcher.num_docs)

        hits = searcher.search('semantic networks')

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(1, len(hits))
        self.assertEqual('CACM-2274', hits[0].docid)
        self.assertAlmostEqual(1.53650, hits[0].score, places=5)

        # Test different ways to initialize indexer.
        indexer = LuceneIndexer(self.tmp_dir, threads=4)
        indexer.add_batch_raw(batch)
        indexer.close()

        searcher = LuceneSearcher(self.tmp_dir)
        self.assertEqual(3, searcher.num_docs)

        hits = searcher.search('semantic networks')

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(1, len(hits))
        self.assertEqual('CACM-2274', hits[0].docid)
        self.assertAlmostEqual(1.53650, hits[0].score, places=5)

        # Test different ways to initialize indexer
        indexer = LuceneIndexer(args=['-index', self.tmp_dir, '-threads', '4'])
        indexer.add_batch_raw(batch)
        indexer.close()

        searcher = LuceneSearcher(self.tmp_dir)
        self.assertEqual(3, searcher.num_docs)

        hits = searcher.search('semantic networks')

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(1, len(hits))
        self.assertEqual('CACM-2274', hits[0].docid)
        self.assertAlmostEqual(1.53650, hits[0].score, places=5)

    def test_indexer_with_args(self):
        indexer = LuceneIndexer(args=['-index', self.tmp_dir, '-pretokenized'])

        with open(self.test_file) as f:
            for doc in f:
                indexer.add_doc_raw(doc)

        indexer.close()

        searcher = LuceneSearcher(self.tmp_dir)
        self.assertEqual(3, searcher.num_docs)

        hits = searcher.search('semantic networks')

        self.assertTrue(isinstance(hits, List))
        self.assertTrue(isinstance(hits[0], JScoredDoc))
        self.assertEqual(1, len(hits))
        self.assertEqual('CACM-2274', hits[0].docid)
        self.assertAlmostEqual(0.62610, hits[0].score, places=5)

    def test_indexer_append1(self):
        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_doc_raw('{"id": "0", "contents": "Document 0"}')
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(1, stats['documents'])
        self.assertIsNotNone(reader.doc('0'))

        indexer = LuceneIndexer(self.tmp_dir, append=True)
        indexer.add_doc_raw('{"id": "1", "contents": "Document 1"}')
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNotNone(reader.doc('0'))
        self.assertIsNotNone(reader.doc('1'))

    def test_indexer_append2(self):
        # Make sure it's okay if we append to an empty index.
        indexer = LuceneIndexer(self.tmp_dir, append=True)
        indexer.add_doc_raw('{"id": "0", "contents": "Document 0"}')
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(1, stats['documents'])
        self.assertIsNotNone(reader.doc('0'))

        # Confirm that we are overwriting.
        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_doc_raw('{"id": "1", "contents": "Document 1"}')
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(1, stats['documents'])
        self.assertIsNone(reader.doc('0'))
        self.assertIsNotNone(reader.doc('1'))

        # Now we're appending.
        indexer = LuceneIndexer(self.tmp_dir, append=True)
        indexer.add_doc_raw('{"id": "x", "contents": "Document x"}')
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNone(reader.doc('0'))
        self.assertIsNotNone(reader.doc('1'))
        self.assertIsNotNone(reader.doc('x'))

    def test_indexer_type_raw(self):
        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_doc_raw('{"id": "doc0", "contents": "document 0 contents"}')
        indexer.add_doc_raw('{"id": "doc1", "contents": "document 1 contents"}')
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNotNone(reader.doc('doc0'))
        self.assertIsNotNone(reader.doc('doc1'))

    def test_indexer_type_raw_batch(self):
        batch = ['{"id": "doc0", "contents": "document 0 contents"}',
                 '{"id": "doc1", "contents": "document 1 contents"}']

        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_batch_raw(batch)
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNotNone(reader.doc('doc0'))
        self.assertIsNotNone(reader.doc('doc1'))

    def test_indexer_type_dict(self):
        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_doc_dict({'id': 'doc0', 'contents': 'document 0 contents'})
        indexer.add_doc_dict({'id': 'doc1', 'contents': 'document 1 contents'})
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNotNone(reader.doc('doc0'))
        self.assertIsNotNone(reader.doc('doc1'))

    def test_indexer_type_dict_batch(self):
        batch = [{'id': 'doc0', 'contents': 'document 0 contents'},
                 {'id': 'doc1', 'contents': 'document 1 contents'}]

        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_batch_dict(batch)
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNotNone(reader.doc('doc0'))
        self.assertIsNotNone(reader.doc('doc1'))

    def test_indexer_type_json(self):
        mapper = JacksonObjectMapper()

        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_doc_json(mapper.createObjectNode().put('id', 'doc0').put('contents', 'document 0 contents'))
        indexer.add_doc_json(mapper.createObjectNode().put('id', 'doc1').put('contents', 'document 1 contents'))
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNotNone(reader.doc('doc0'))
        self.assertIsNotNone(reader.doc('doc1'))

    def test_indexer_type_json_batch(self):
        mapper = JacksonObjectMapper()
        batch = [mapper.createObjectNode().put('id', 'doc0').put('contents', 'document 0 contents'),
                 mapper.createObjectNode().put('id', 'doc1').put('contents', 'document 1 contents')]

        indexer = LuceneIndexer(self.tmp_dir)
        indexer.add_batch_json(batch)
        indexer.close()

        reader = IndexReader(self.tmp_dir)
        stats = reader.stats()
        self.assertEqual(2, stats['documents'])
        self.assertIsNotNone(reader.doc('doc0'))
        self.assertIsNotNone(reader.doc('doc1'))

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
