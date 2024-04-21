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

from integrations.run_lucenesearcher import RunLuceneSearcher


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.test_threads = ['--threads 1 --batch-size 64', '--threads 4 --batch-size 64']

    def check_equal(self, runner: RunLuceneSearcher, runtag: str, extras: str) -> bool:
        checksums = []
        for i, config in enumerate(self.test_threads):
            checksum = runner.run(runtag=f'{runtag}-{i}', extras=f'{config} {extras}')
            if len(checksum) == 0:
                print(f'[FAIL] {runtag} {config} failed to run!')
                return False
            checksums.append(checksum)
        equal = all(x == checksums[0] for x in checksums)
        if equal:
            print(f'[SUCCESS] {runtag} results match!')
        else:
            print(f'[FAIL] {runtag} results do not match!')
        return equal

    def test_robust04(self):
        checker = RunLuceneSearcher(index='robust04', topics='robust04')
        self.assertTrue(self.check_equal(checker, 'robust04', extras=''))

    def test_msmarco_passage(self):
        checker = RunLuceneSearcher(index='msmarco-v1-passage', topics='msmarco-passage-dev-subset')
        self.assertTrue(self.check_equal(checker, 'msmarco-v1-passage', extras='--output-format msmarco'))

    def test_msmarco_passage_docTTTTTquery(self):
        checker = RunLuceneSearcher(index='msmarco-v1-passage.d2q-t5', topics='msmarco-passage-dev-subset')
        self.assertTrue(self.check_equal(checker, 'msmarco-v1-passage.d2q-t5', extras='--output-format msmarco'))

    def test_msmarco_doc(self):
        checker = RunLuceneSearcher(index='msmarco-v1-doc', topics='msmarco-doc-dev')
        self.assertTrue(self.check_equal(checker, 'msmarco-v1-doc', extras='--hits 100 --output-format msmarco'))

    def test_msmarco_doc_docTTTTTquery(self):
        checker = RunLuceneSearcher(index='msmarco-v1-doc.d2q-t5', topics='msmarco-doc-dev')
        self.assertTrue(self.check_equal(checker, 'msmarco-v1-doc.d2q-t5',
                                         extras='--hits 100 --output-format msmarco'))

    def test_msmarco_doc_per_passage(self):
        checker = RunLuceneSearcher(index='msmarco-v1-doc-segmented', topics='msmarco-doc-dev')
        self.assertTrue(
            self.check_equal(checker, 'msmarco-v1-doc-segmented',
                             extras='--hits 1000 --max-passage --max-passage-hits 100 --output-format msmarco'))

    def test_msmarco_doc_docTTTTTquery_passage(self):
        checker = RunLuceneSearcher(index='msmarco-v1-doc-segmented.d2q-t5', topics='msmarco-doc-dev')
        self.assertTrue(self.check_equal(checker, 'msmarco-v1-doc-segmented.d2q-t5',
                                         extras='--hits 1000 --max-passage --max-passage-hits 100 --output-format msmarco'))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
