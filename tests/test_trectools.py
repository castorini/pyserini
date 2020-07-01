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

import filecmp
import os
from pyserini.trectools import TrecRun, Qrels, RescoreMethod
import unittest


class TestTrecTools(unittest.TestCase):
    def setUp(self):
        self.output_path = 'output_test_trectools.txt'

    def test_trec_run_read(self):
        input_path = 'tests/resources/simple_trec_run_read.txt'
        verify_path = 'tests/resources/simple_trec_run_read_verify.txt'

        run = TrecRun(filepath=input_path)
        run.save_to_txt(self.output_path)
        self.assertTrue(filecmp.cmp(verify_path, self.output_path))

    def test_simple_qrels(self):
        qrels = Qrels('tools/topics-and-qrels/qrels.covid-round1.txt')
        self.assertEqual(len(qrels.get_docids(topic=1, relevance_grades=[1, 2])), 101)
        self.assertEqual(len(qrels.get_docids(topic=1, relevance_grades=[2])), 56)
        self.assertEqual(len(qrels.get_docids(topic=1, relevance_grades=[1])), 45)

    def test_discard_qrels(self):
        run = TrecRun('tests/resources/simple_trec_run_filter.txt')
        qrels = Qrels('tools/topics-and-qrels/qrels.covid-round1.txt')

        run.discard_qrels(qrels, clone=False).save_to_txt(output_path=self.output_path)
        self.assertTrue(filecmp.cmp('tests/resources/simple_trec_run_remove_verify.txt', self.output_path))

    def test_retain_qrels(self):
        run = TrecRun('tests/resources/simple_trec_run_filter.txt')
        qrels = Qrels('tools/topics-and-qrels/qrels.covid-round1.txt')

        run.retain_qrels(qrels, clone=True).save_to_txt(output_path=self.output_path)
        self.assertTrue(filecmp.cmp('tests/resources/simple_trec_run_keep_verify.txt', self.output_path))

    def test_normalize_scores(self):
        run = TrecRun('tests/resources/simple_trec_run_fusion_1.txt')
        run.rescore(RescoreMethod.NORMALIZE).save_to_txt(self.output_path)
        self.assertTrue(filecmp.cmp('tests/resources/simple_trec_run_normalize_verify.txt', self.output_path))

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


if __name__ == '__main__':
    unittest.main()
