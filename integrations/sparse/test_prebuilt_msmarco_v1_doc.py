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

    def test_doc_trec_output(self):
        output_file = 'test_run.msmarco-doc.1.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc --output {output_file} --bm25 --hits 1000'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.2774, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'recall_1000')
        self.assertAlmostEqual(score, 0.9357, delta=0.0001)

    def test_doc_msmarco_output(self):
        output_file = 'test_run.msmarco-doc.2.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc --output {output_file} --bm25 --hits 100 --output-format msmarco'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score_msmarco_as_string(stdout, 'MRR @100')
        self.assertEqual(score, '0.2766351807440808')

    def test_doc_slim_trec_output(self):
        output_file = 'test_run.msmarco-doc.3.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-slim --output {output_file} --bm25 --hits 1000'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.2774, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'recall_1000')
        self.assertAlmostEqual(score, 0.9357, delta=0.0001)

    def test_doc_slim_msmarco_output(self):
        output_file = 'test_run.msmarco-doc.4.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-slim --output {output_file} --bm25 --hits 100 --output-format msmarco'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score_msmarco_as_string(stdout, 'MRR @100')
        self.assertEqual(score, '0.2766351807440808')

    def test_doc_full_trec_output(self):
        output_file = 'test_run.msmarco-doc.5.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-full --output {output_file} --bm25 --hits 1000'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.2774, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'recall_1000')
        self.assertAlmostEqual(score, 0.9357, delta=0.0001)

    def test_doc_full_msmarco_output(self):
        output_file = 'test_run.msmarco-doc.6.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-full --output {output_file} --bm25 --hits 100 --output-format msmarco'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score_msmarco_as_string(stdout, 'MRR @100')
        self.assertEqual(score, '0.2766351807440808')

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()