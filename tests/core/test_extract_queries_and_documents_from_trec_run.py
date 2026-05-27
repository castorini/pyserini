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

"""
Parity checks for io.anserini.cli.ExtractQueriesAndDocumentsFromTrecRun (see
ExtractQueriesAndDocumentsFromTrecRunTest.java). One on-the-fly Lucene index;
no bundled binary indexes.
"""

import json
import os
import shutil
import tempfile
import unittest

from pyserini.eval.extract_queries_and_documents_from_trec_run import run
from pyserini.index.lucene import LuceneIndexer


class TestExtractQueriesAndDocumentsFromTrecRun(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('core'):
            self.resource_dir = '../resources'
        else:
            self.resource_dir = 'tests/resources'

        self.tmp_index = tempfile.mkdtemp(prefix='extract_trec_run_idx_')
        # Default Anserini SimpleIndexer has storeRaw=false; extract uses doc_raw(), which
        # requires the raw field to be stored (see IndexCollection.Args / usage-index.md).
        indexer = LuceneIndexer(args=['-index', self.tmp_index, '-storeRaw'], threads=1)
        indexer.add_doc_raw(
            '{"id": "doc1", "contents": "body1"}'
        )
        indexer.add_doc_raw(
            '{"id": "doc2", "contents": "body2"}'
        )
        indexer.add_doc_raw(
            '{"id": "doc3", "contents": "body3"}'
        )
        indexer.close()

        self.topics_path = os.path.join(
            self.resource_dir, 'sample_queries.tsv'
        )
        self.run_path = os.path.join(
            self.resource_dir, 'simple_trec_run_extract_queries_and_documents.txt'
        )

    def tearDown(self):
        shutil.rmtree(self.tmp_index, ignore_errors=True)

    def test_generate(self):
        """End-to-end JSONL shape; fixtures: sample_queries.tsv + simple_trec_run_extract_queries_and_documents.txt."""
        fd, out_path = tempfile.mkstemp(suffix='.jsonl')
        os.close(fd)
        try:
            run(
                self.tmp_index,
                self.run_path,
                self.topics_path,
                'TsvString',
                'title',
                out_path,
                hits=100,
            )
            with open(out_path, encoding='utf-8') as f:
                lines = [json.loads(ln) for ln in f if ln.strip()]
            self.assertEqual(len(lines), 4)

            q1, q2, q3, q4 = lines
            self.assertEqual(q1['query']['qid'], '1')
            self.assertEqual(q1['query']['text'], 'document')
            self.assertEqual(len(q1['candidates']), 2)
            self.assertEqual(q1['candidates'][0]['docid'], 'doc1')
            self.assertEqual(q1['candidates'][0]['score'], 2.4)
            self.assertEqual(q1['candidates'][0]['doc']['id'], 'doc1')
            self.assertEqual(q1['candidates'][1]['docid'], 'doc2')
            self.assertEqual(q1['candidates'][1]['doc']['id'], 'doc2')

            self.assertEqual(q2['query']['qid'], '2')
            self.assertEqual(q2['query']['text'], 'one')
            self.assertEqual(q2['candidates'][0]['docid'], 'doc3')
            self.assertEqual(q2['candidates'][0]['score'], 4.1)
            self.assertEqual(q2['candidates'][1]['docid'], 'doc1')
            self.assertEqual(q2['candidates'][1]['score'], 3.3)

            self.assertEqual(q3['query']['qid'], '3')
            self.assertEqual(q3['query']['text'], 'contents')
            self.assertEqual(len(q3['candidates']), 1)
            self.assertEqual(q3['candidates'][0]['docid'], 'doc3')
            self.assertEqual(q3['candidates'][0]['score'], 123.0)

            self.assertEqual(q4['query']['qid'], '4')
            self.assertEqual(q4['query']['text'], 'text')
            self.assertEqual(q4['candidates'][0]['docid'], 'doc2')
            self.assertEqual(q4['candidates'][0]['score'], 561.0)
        finally:
            os.remove(out_path)

    def test_hits_limits_depth_per_query(self):
        fd, out_path = tempfile.mkstemp(suffix='.jsonl')
        os.close(fd)
        try:
            run(
                self.tmp_index,
                self.run_path,
                self.topics_path,
                'TsvString',
                'title',
                out_path,
                hits=1,
            )
            with open(out_path, encoding='utf-8') as f:
                recs = [json.loads(ln) for ln in f if ln.strip()]
            self.assertEqual(len(recs), 4)
            self.assertEqual(len(recs[0]['candidates']), 1)
            self.assertEqual(recs[0]['candidates'][0]['docid'], 'doc1')
            self.assertEqual(recs[1]['candidates'][0]['docid'], 'doc3')
            self.assertEqual(recs[2]['candidates'][0]['docid'], 'doc3')
            self.assertEqual(recs[3]['candidates'][0]['docid'], 'doc2')
        finally:
            os.remove(out_path)

    def test_bad_topics(self):
        """Anserini testBadTopics: run qids not present in topics file."""
        fd_run, run_path = tempfile.mkstemp(suffix='.run')
        os.close(fd_run)
        with open(run_path, 'w', encoding='utf-8') as f:
            f.write('query1 Q0 doc1 1 7.0 t\n')

        fd_out, out_path = tempfile.mkstemp(suffix='.jsonl')
        os.close(fd_out)
        try:
            with self.assertRaises(ValueError) as ctx:
                run(
                    self.tmp_index,
                    run_path,
                    self.topics_path,
                    'TsvString',
                    'title',
                    out_path,
                    hits=100,
                )
            self.assertIn('Unable to find query for query1', str(ctx.exception))
        finally:
            os.remove(run_path)
            os.remove(out_path)

    def test_bad_index_missing_raw_doc(self):
        """Anserini testBadIndex: docid in run not found in index."""
        fd_run, run_path = tempfile.mkstemp(suffix='.run')
        os.close(fd_run)
        with open(run_path, 'w', encoding='utf-8') as f:
            f.write('1 Q0 no_such_doc 1 1.0 t\n')

        fd_out, out_path = tempfile.mkstemp(suffix='.jsonl')
        os.close(fd_out)
        try:
            with self.assertRaises(ValueError) as ctx:
                run(
                    self.tmp_index,
                    run_path,
                    self.topics_path,
                    'TsvString',
                    'title',
                    out_path,
                    hits=100,
                )
            self.assertIn('Raw document with docid no_such_doc', str(ctx.exception))
            self.assertIn('not found in index', str(ctx.exception))
        finally:
            os.remove(run_path)
            os.remove(out_path)


if __name__ == '__main__':
    unittest.main()
