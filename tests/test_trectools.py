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

import filecmp
import os
import unittest

from pyserini.trectools import TrecRun, Qrels, RescoreMethod


class TestTrecTools(unittest.TestCase):
    def setUp(self):
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('tests'):
            self.root = '../'
        else:
            self.root = '.'

        self.output_path = os.path.join(self.root, 'output_test_trectools.txt')

    def test_trec_run_read(self):
        input_path = os.path.join(self.root, 'tests/resources/simple_trec_run_read.txt')
        verify_path = os.path.join(self.root, 'tests/resources/simple_trec_run_read_verify.txt')

        run = TrecRun(filepath=input_path)
        run.save_to_txt(self.output_path)
        self.assertTrue(filecmp.cmp(verify_path, self.output_path))

    def test_trec_run_topics(self):
        input_path = os.path.join(self.root, 'tests/resources/simple_trec_run_msmarco_doc1.txt')

        run = TrecRun(filepath=input_path)
        self.assertEqual(run.topics(), {320792, 174249, 1090270, 1101279})

        for topic in run.topics():
            self.assertEqual(len(run.get_docs_by_topic(topic)), 5)

    def test_simple_qrels(self):
        qrels = Qrels(os.path.join(self.root, 'tools/topics-and-qrels/qrels.covid-round1.txt'))
        self.assertEqual(len(qrels.get_docids(topic=1, relevance_grades=[1, 2])), 101)
        self.assertEqual(len(qrels.get_docids(topic=1, relevance_grades=[2])), 56)
        self.assertEqual(len(qrels.get_docids(topic=1, relevance_grades=[1])), 45)

    def test_discard_qrels(self):
        run = TrecRun(os.path.join(self.root, 'tests/resources/simple_trec_run_filter.txt'))
        qrels = Qrels(os.path.join(self.root, 'tools/topics-and-qrels/qrels.covid-round1.txt'))

        run.discard_qrels(qrels, clone=False).save_to_txt(output_path=self.output_path)
        self.assertTrue(filecmp.cmp(os.path.join(self.root, 'tests/resources/simple_trec_run_remove_verify.txt'),
                                    self.output_path))

    def test_retain_qrels(self):
        run = TrecRun(os.path.join(self.root, 'tests/resources/simple_trec_run_filter.txt'))
        qrels = Qrels(os.path.join(self.root, 'tools/topics-and-qrels/qrels.covid-round1.txt'))

        run.retain_qrels(qrels, clone=True).save_to_txt(output_path=self.output_path)
        self.assertTrue(filecmp.cmp(os.path.join(self.root, 'tests/resources/simple_trec_run_keep_verify.txt'),
                                    self.output_path))

    def test_normalize_scores(self):
        run = TrecRun(os.path.join(self.root, 'tests/resources/simple_trec_run_fusion_1.txt'))
        run.rescore(RescoreMethod.NORMALIZE).save_to_txt(self.output_path)
        self.assertTrue(filecmp.cmp(os.path.join(self.root, 'tests/resources/simple_trec_run_normalize_verify.txt'),
                                    self.output_path))

    def tearDown(self):
        if os.path.exists(self.output_path):
            os.remove(self.output_path)


if __name__ == '__main__':
    unittest.main()
