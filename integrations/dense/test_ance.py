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

"""Integration tests for ANCE model and ANCE PRF using on-the-fly query encoding."""

import os
import socket
import unittest

from integrations.utils import clean_files, run_command, parse_score
from pyserini.dsearch import QueryEncoder
from pyserini.search import get_topics


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 12
        self.batch_size = 36
        self.rocchio_alpha = 0.4
        self.rocchio_beta = 0.6

        # Hard-code larger values for internal servers
        if socket.gethostname().startswith('damiano') or socket.gethostname().startswith('orca'):
            self.threads = 36
            self.batch_size = 144

    def test_msmarco_passage_ance_bf_otf(self):
        output_file = 'test_run.msmarco-passage.ance.bf.otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-ance-bf \
                             --encoder castorini/ance-msmarco-passage \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3302, delta=0.0001)

    def test_msmarco_passage_ance_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('ance-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_msmarco_passage_ance_avg_prf_otf(self):
        output_file = 'test_run.dl2019.ance.avg-prf.otf.trec'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics dl19-passage \
                                     --index msmarco-passage-ance-bf \
                                     --encoder castorini/ance-msmarco-passage \
                                     --batch-size {self.batch_size} \
                                     --threads {self.threads} \
                                     --output {output_file} \
                                     --prf-depth 3 \
                                     --prf-method avg'

        cmd2 = f'python -m pyserini.eval.trec_eval -l 2 -m map dl19-passage {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "map")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.4247, delta=0.0001)

    def test_msmarco_passage_ance_rocchio_prf_otf(self):
        output_file = 'test_run.dl2019.ance.rocchio-prf.otf.trec'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics dl19-passage \
                                     --index msmarco-passage-ance-bf \
                                     --encoder castorini/ance-msmarco-passage \
                                     --batch-size {self.batch_size} \
                                     --threads {self.threads} \
                                     --output {output_file} \
                                     --prf-depth 5 \
                                     --prf-method rocchio \
                                     --threads {self.threads} \
                                     --rocchio-alpha {self.rocchio_alpha} \
                                     --rocchio-beta {self.rocchio_beta}'

        cmd2 = f'python -m pyserini.eval.trec_eval -l 2 -m map dl19-passage {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "map")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.4211, delta=0.0001)

    def test_msmarco_doc_ance_bf_otf(self):
        output_file = 'test_run.msmarco-doc.passage.ance-maxp.otf.txt'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-doc-dev \
                             --index msmarco-doc-ance-maxp-bf \
                             --encoder castorini/ance-msmarco-doc-maxp \
                             --output {output_file}\
                             --hits 1000 \
                             --max-passage \
                             --max-passage-hits 100 \
                             --output-format msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        # We get a small difference, 0.3794 on macOS.
        self.assertAlmostEqual(score, 0.3796, delta=0.0002)

    def test_msmarco_doc_ance_bf_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('ance_maxp-msmarco-doc-dev')
        topics = get_topics('msmarco-doc-dev')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_nq_test_ance_bf_otf(self):
        output_file = 'test_run.ance.nq-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.ance.nq-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-ance-multi-bf \
                             --encoder castorini/ance-dpr-question-multi \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.8224, places=4)

    def test_nq_test_ance_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-nq-test')
        topics = get_topics('dpr-nq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_trivia_test_ance_bf_otf(self):
        output_file = 'test_run.ance.trivia-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.ance.trivia-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.dsearch --topics dpr-trivia-test \
                             --index wikipedia-ance-multi-bf \
                             --encoder castorini/ance-dpr-question-multi \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.8010, places=4)

    def test_trivia_test_ance_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-trivia-test')
        topics = get_topics('dpr-trivia-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
