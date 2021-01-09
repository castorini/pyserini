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

from integrations.run_simplesearcher import RunSimpleSearcher


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.checker_robust = RunSimpleSearcher(
            index='robust04',
            topics='robust04')

        self.checker_msmarco = RunSimpleSearcher(
            index='msmarco-passage',
            topics='msmarco_passage_dev_subset')

        self.checker_doc_per_passage = RunSimpleSearcher(
            index='msmarco-doc-per-passage',
            topics='msmarco_doc_dev')

        self.test_threads = ['--threads 1 --batch-size 64',
                             '--threads 4 --batch-size 64']

    def check_equal(self, runner: RunSimpleSearcher, runtag: str, extras: str) -> bool:
        checksums = []
        for i, config in enumerate(self.test_threads):
            checksum = runner.run(runtag=f'{runtag}-{i}',
                                  extras=f'{config} {extras}')
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

    def test_robust04_(self):
        self.assertTrue(self.check_equal(self.checker_robust,
                                         'robust04', extras=''))

    def test_msmarco_passage_(self):
        self.assertTrue(self.check_equal(self.checker_msmarco,
                                         'msmarco_passage_dev_subset', extras=''))

    def test_msmarco_doc_(self):
        self.assertTrue(self.check_equal(self.checker_doc_per_passage, 'msmarco_doc_dev',
                                         extras='--hits 1000 --max-passage --max-passage-hits 100'))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
