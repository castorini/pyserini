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

"""Integration tests for MS MARCO V1 passage corpora using pre-built indexes."""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score, parse_score_msmarco_as_string


class TestPrebuiltMsMarcoV1Passage(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    def test_passage_trec_output(self):
        output_file = 'test_run.msmarco-passage.1.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage --output {output_file} --bm25'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.1958, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'recall_1000')
        self.assertAlmostEqual(score, 0.8573, delta=0.0001)

    def test_passage_msmarco_output(self):
        output_file = 'test_run.msmarco-passage.2.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage --output {output_file} --bm25 --output-format msmarco'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score_msmarco_as_string(stdout, 'MRR @10')
        self.assertEqual(score, '0.18741227770955546')

    def test_passage_slim_trec_output(self):
        output_file = 'test_run.msmarco-passage.3.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage-slim --output {output_file} --bm25'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.1958, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'recall_1000')
        self.assertAlmostEqual(score, 0.8573, delta=0.0001)

    def test_passage_slim_msmarco_output(self):
        output_file = 'test_run.msmarco-passage.4.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage-slim --output {output_file} --bm25 --output-format msmarco'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score_msmarco_as_string(stdout, 'MRR @10')
        self.assertEqual(score, '0.18741227770955546')

    def test_passage_full_trec_output(self):
        output_file = 'test_run.msmarco-passage.5.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage-full --output {output_file} --bm25'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.1958, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'recall_1000')
        self.assertAlmostEqual(score, 0.8573, delta=0.0001)

    def test_passage_full_msmarco_output(self):
        output_file = 'test_run.msmarco-passage.6.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage-full --output {output_file} --bm25 --output-format msmarco'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score_msmarco_as_string(stdout, 'MRR @10')
        self.assertEqual(score, '0.18741227770955546')

    def test_passage_expanded_trec_output(self):
        output_file = 'test_run.msmarco-passage.expanded.1.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage-d2q-t5 --output {output_file} --bm25'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.2893, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'recall_1000')
        self.assertAlmostEqual(score, 0.9506, delta=0.0001)

    def test_passage_expanded_msmarco_output(self):
        output_file = 'test_run.msmarco-passage.expanded.2.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-passage-dev-subset --index msmarco-v1-passage-d2q-t5 --output {output_file} --bm25 --output-format msmarco'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score_msmarco_as_string(stdout, 'MRR @10')
        self.assertEqual(score, '0.281560751807885')

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()