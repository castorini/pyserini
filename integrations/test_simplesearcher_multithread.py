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

import os
import unittest

from integrations.simplesearcher_checker import SimpleSearcherChecker


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('integrations'):
            anserini_root = '../../anserini'
            pyserini_root = '..'
        else:
            anserini_root = '../anserini'
            pyserini_root = '.'

        self.checker = SimpleSearcherChecker(
            anserini_root=anserini_root,
            index=os.path.join(
                anserini_root, 'indexes/lucene-index.robust04.pos+docvectors+raw'),
            topics=os.path.join(
                pyserini_root, 'tools/topics-and-qrels/topics.robust04.txt'),
            pyserini_topics='robust04',
            qrels=os.path.join(pyserini_root, 'tools/topics-and-qrels/qrels.robust04.txt'))

        self.checker_msmarco = SimpleSearcherChecker(
            anserini_root=anserini_root,
            index=os.path.join(
                # TODO: What is the proper name of the index?
                anserini_root, 'indexes/lucene-index.index-msmarco-passage-20201117-f87c94'),
            topics=os.path.join(
                pyserini_root, 'tools/topics-and-qrels/topics.msmarco-doc.dev.txt'),
            pyserini_topics='msmarco_passage_dev_subset',
            qrels=os.path.join(pyserini_root, 'tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt'))

        self.checker_doc_per_passage = SimpleSearcherChecker(
            anserini_root=anserini_root,
            index=os.path.join(
                # TODO: What is the proper name of the index?
                anserini_root, 'indexes/lucene-index.index-msmarco-doc-per-passage-20201204-f50dcc'),
            topics=os.path.join(
                pyserini_root, 'tools/topics-and-qrels/topics.msmarco-doc.dev.txt'),
            pyserini_topics='msmarco_doc_dev',
            qrels=os.path.join(pyserini_root, 'tools/topics-and-qrels/qrels.msmarco-doc.dev.txt'))

        self.anserini_max_passage_extras = '-hits 1000 -selectMaxPassage -selectMaxPassage.hits 100'
        self.pyserini_max_passage_extras = '--msmarco --hits 1000 --max-passage --max-passage-hits 100'

    def test_single_thread_(self):
        self.assertTrue(self.checker.run(
            'robust04', '-bm25', '--bm25 --threads 1 --batch-size 64'))
        # self.assertTrue(self.checker_msmarco.run(
        #     'msmarco_passage_dev_subset', '-bm25', '--bm25 --threads 1 --batch-size 64'))
        # self.assertTrue(self.checker_doc_per_passage.run('msmarco_doc_dev', f'-bm25 {self.anserini_max_passage_extras}',
        #                                          f'--threads 1 --batch-size 64 {self.pyserini_max_passage_extras}'))

    def test_thread_4_(self):
        self.assertTrue(self.checker.run(
            'robust04', '-bm25', '--bm25 --threads 4 --batch-size 64'))
        # self.assertTrue(self.checker_msmarco.run(
        #     'msmarco_passage_dev_subset', '-bm25', '--bm25 --threads 4 --batch-size 64'))
        # self.assertTrue(self.checker_doc_per_passage.run('msmarco_doc_dev', f'-bm25 {self.anserini_max_passage_extras}',
        #                                          f'--threads 1 --batch-size 64 {self.pyserini_max_passage_extras}'))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
