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
import unittest

from integrations.simplesearcher_anserini_checker import SimpleSercherAnseriniMatchChecker


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('sparse'):
            anserini_root = '../../../anserini'
            pyserini_root = '../..'
        else:
            anserini_root = '../anserini'
            pyserini_root = '.'

        self.checker = SimpleSercherAnseriniMatchChecker(
            anserini_root=anserini_root,
            index=os.path.join(anserini_root, 'indexes/lucene-index.core18.pos+docvectors+raw'),
            topics=os.path.join(pyserini_root, 'tools/topics-and-qrels/topics.core18.txt'),
            pyserini_topics='core18',
            qrels=os.path.join(pyserini_root, 'tools/topics-and-qrels/qrels.core18.txt'),
            eval_root=pyserini_root)

    def test_bm25(self):
        self.assertTrue(self.checker.run('core18_bm25', '-bm25', '--bm25'))

    def test_bm25_rm3(self):
        self.assertTrue(self.checker.run('core18_bm25_rm3', '-bm25 -rm3', '--bm25 --rm3'))

    def test_qld(self):
        self.assertTrue(self.checker.run('core18_qld', '-qld', '--qld'))

    def test_qld_rm3(self):
        self.assertTrue(self.checker.run('core18_qld_rm3', '-qld -rm3', '--qld --rm3'))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
