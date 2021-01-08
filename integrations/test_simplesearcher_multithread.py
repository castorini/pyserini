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

from integrations.compare_simplesearcher import CompareSimpleSearcher


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        index_cache_root = "~/.cache/pyserini/indexes/"

        self.checker_robust = CompareSimpleSearcher(
            index=os.path.join(index_cache_root,
                               'index-robust04-20191213.15f3d001489c97849a010b0a4734d018'),
            topics='robust04')

        self.checker_msmarco = CompareSimpleSearcher(
            index=os.path.join(
                index_cache_root, 'index-msmarco-passage-20201117-f87c94.1efad4f1ae6a77e235042eff4be1612d'),
            topics='msmarco_passage_dev_subset')

        self.checker_doc_per_passage = CompareSimpleSearcher(
            index=os.path.join(index_cache_root,
                               'index-msmarco-doc-per-passage-20201204-f50dcc.797367406a7542b649cefa6b41cf4c33'),
            topics='msmarco_doc_dev')

        self.test_threads = ['--threads 1 --batch-size 64',
                             '--threads 4 --batch-size 64']

    def test_robust04_(self):
        self.assertTrue(self.checker_robust.run(
            'robust04', '', self.test_threads))

    def test_msmarco_passage_(self):
        self.assertTrue(self.checker_msmarco.run(
            'msmarco_passage_dev_subset', '', self.test_threads))

    def test_msmarco_doc_(self):
        max_passage = '--hits 1000 --max-passage --max-passage-hits 100'
        extras = [
            f'{max_passage} {threads}' for threads in self.test_threads]
        self.assertTrue(self.checker_doc_per_passage.run('msmarco_doc_dev', max_passage,
                                                         extras))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
