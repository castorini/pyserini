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

"""Integration tests for MS MARCO V1 doc corpora using pre-built indexes."""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score, parse_score_msmarco_as_string, run_retrieval_and_return_scores


class TestPrebuiltMsMarcoV1Doc(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    #
    # doc "full" conditions
    #

    def test_doc_full_trec_output(self):
        """Test case for MS MARCO V1 doc (full), dev queries, TREC output
           on all three pre-built indexes (base, slim, full)."""

        # Loop over all three pre-built indexes.
        for index in ['msmarco-v1-doc', 'msmarco-v1-doc-slim', 'msmarco-v1-doc-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc.trec.txt',
                f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index {index} --bm25 --hits 1000',
                'msmarco-doc-dev',
                'trec_eval',
                [['map', 'map'], ['recall.1000', 'recall_1000']])

            self.assertTrue('map' in scores)
            self.assertTrue('recall.1000' in scores)
            self.assertAlmostEqual(scores['map'],0.2774, delta=0.0001)
            self.assertAlmostEqual(scores['recall.1000'], 0.9357, delta=0.0001)

    def test_doc_full_msmarco_output(self):
        """Test case for MS MARCO V1 doc (full), dev queries, MS MARCO output
           on all three pre-built indexes (base, slim, full)."""

        # Loop over all three pre-built indexes.
        for index in ['msmarco-v1-doc', 'msmarco-v1-doc-slim', 'msmarco-v1-doc-full']:
            scores = run_retrieval_and_return_scores(
                'runs/test_run.msmarco-doc.msmarco.txt',
                f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index {index} --bm25 --hits 100 --output-format msmarco',
                'msmarco-doc-dev',
                'msmarco_doc_string', [])

            self.assertTrue('MRR@100' in scores)
            self.assertEqual(scores['MRR@100'], '0.2766351807440808')

    # #
    # # doc segmented conditions
    # #
    #
    # def test_doc_segmented_trec_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.1.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented --output {output_file} --bm25 --hits 10000 --max-passage --max-passage-hits 1000'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'map')
    #     self.assertAlmostEqual(score, 0.2762, delta=0.0001)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'recall_1000')
    #     self.assertAlmostEqual(score, 0.9311, delta=0.0001)
    #
    # def test_doc_segmented_msmarco_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.2.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented --output {output_file} --output-format msmarco --bm25 --hits 1000 --max-passage --max-passage-hits 100'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score_msmarco_as_string(stdout, 'MRR @100')
    #     self.assertEqual(score, '0.2755196341768384')
    #
    # def test_doc_segmented_slim_trec_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.3.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented-slim --output {output_file} --bm25 --hits 10000 --max-passage --max-passage-hits 1000'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'map')
    #     self.assertAlmostEqual(score, 0.2762, delta=0.0001)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'recall_1000')
    #     self.assertAlmostEqual(score, 0.9311, delta=0.0001)
    #
    # def test_doc_segmented_slim_msmarco_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.4.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented-slim --output {output_file} --output-format msmarco --bm25 --hits 1000 --max-passage --max-passage-hits 100'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score_msmarco_as_string(stdout, 'MRR @100')
    #     self.assertEqual(score, '0.2755196341768384')
    #
    # def test_doc_segmented_full_trec_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.5.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented-full --output {output_file} --bm25 --hits 10000 --max-passage --max-passage-hits 1000'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'map')
    #     self.assertAlmostEqual(score, 0.2762, delta=0.0001)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'recall_1000')
    #     self.assertAlmostEqual(score, 0.9311, delta=0.0001)
    #
    # def test_doc_segmented_full_msmarco_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.6.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented-full --output {output_file} --output-format msmarco --bm25 --hits 1000 --max-passage --max-passage-hits 100'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score_msmarco_as_string(stdout, 'MRR @100')
    #     self.assertEqual(score, '0.2755196341768384')
    #
    # #
    # # doc2query conditions
    # #
    #
    # def test_doc_d2q_trec_output(self):
    #     output_file = 'runs/test_run.msmarco-doc.expanded.1.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-d2q-t5 --output {output_file} --bm25 --hits 1000'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'map')
    #     self.assertAlmostEqual(score, 0.3273, delta=0.0001)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'recall_1000')
    #     self.assertAlmostEqual(score, 0.9553, delta=0.0001)
    #
    # def test_doc_d2q_msmarco_output(self):
    #     output_file = 'runs/test_run.msmarco-doc.expanded.2.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-d2q-t5 --output {output_file} --output-format msmarco --bm25 --hits 100'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score_msmarco_as_string(stdout, 'MRR @100')
    #     self.assertEqual(score, '0.3268656233100833')
    #
    # def test_doc_segmented_d2q_trec_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.expanded.2.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented-d2q-t5 --output {output_file} --bm25 --hits 10000 --max-passage --max-passage-hits 1000'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m map msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'map')
    #     self.assertAlmostEqual(score, 0.3213, delta=0.0001)
    #
    #     cmd = f'python -m pyserini.eval.trec_eval -c -m recall.1000 msmarco-doc-dev {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score(stdout, 'recall_1000')
    #     self.assertAlmostEqual(score, 0.9530, delta=0.0001)
    #
    # def test_doc_segmented_d2q_msmarco_output(self):
    #     output_file = 'runs/test_run.msmarco-doc-segmented.expanded.2.txt'
    #     self.temp_files.append(output_file)
    #     cmd = f'python -m pyserini.search.lucene --topics msmarco-doc-dev --index msmarco-v1-doc-segmented-d2q-t5 --output {output_file} --output-format msmarco --bm25 --hits 1000 --max-passage --max-passage-hits 100'
    #     status = os.system(cmd)
    #     self.assertEqual(status, 0)
    #
    #     cmd = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
    #     stdout, stderr = run_command(cmd)
    #     score = parse_score_msmarco_as_string(stdout, 'MRR @100')
    #     self.assertEqual(score, '0.320918438140918')

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
