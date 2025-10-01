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

from integrations.core.lucenesearcher_anserini_checker import LuceneSearcherAnseriniMatchChecker
from pyserini.search.lucene import LuceneSearcher


class CheckSearchResultsAgainstAnseriniForRobust04(unittest.TestCase):
    def setUp(self):
        # Make sure the required index is downloaded.
        LuceneSearcher.from_prebuilt_index('disk45')

        self.checker = LuceneSearcherAnseriniMatchChecker(
            index='disk45',
            topics='tools/topics-and-qrels/topics.robust04.txt',
            pyserini_topics='robust04',
            qrels='tools/topics-and-qrels/qrels.robust04.txt')

    def test_bm25(self):
        self.assertTrue(self.checker.run('robust04_bm25', '-bm25', '--bm25'))

    def test_bm25_rm3(self):
        self.assertTrue(self.checker.run('robust04_bm25_rm3', '-bm25 -rm3', '--bm25 --rm3'))

    def test_qld(self):
        self.assertTrue(self.checker.run('robust04_qld', '-qld', '--qld'))

    def test_qld_rm3(self):
        self.assertTrue(self.checker.run('robust04_qld_rm3', '-qld -rm3', '--qld --rm3'))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
