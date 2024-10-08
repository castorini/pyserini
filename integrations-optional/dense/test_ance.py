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

"""Integration tests for ANCE and ANCE PRF using on-the-fly query encoding."""

import multiprocessing
import os
import unittest

from integrations.utils import clean_files, run_command, parse_score_qa, parse_score_msmarco
from pyserini.search import get_topics
from pyserini.search.faiss._searcher import QueryEncoder


class TestAnce(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 16
        self.batch_size = self.threads * 32
        self.rocchio_alpha = 0.4
        self.rocchio_beta = 0.6

        half_cores = int(multiprocessing.cpu_count() / 2)
        # If server supports more threads, then use more threads.
        # As a heuristic, use up half up available CPU cores.
        if half_cores > self.threads:
            self.threads = half_cores
            self.batch_size = half_cores * 32

    def test_msmarco_doc_ance_bf_otf(self):
        output_file = 'test_run.msmarco-doc.passage.ance-maxp.otf.txt'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.faiss --topics msmarco-doc-dev \
                             --index msmarco-v1-doc.ance-maxp \
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
        score = parse_score_msmarco(stdout, 'MRR @100')
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
        cmd1 = f'python -m pyserini.search.faiss --topics dpr-nq-test \
                             --index wikipedia-dpr-100w.ance-multi \
                             --encoder castorini/ance-dpr-question-multi \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-nq-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
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
        cmd1 = f'python -m pyserini.search.faiss --topics dpr-trivia-test \
                             --index wikipedia-dpr-100w.ance-multi \
                             --encoder castorini/ance-dpr-question-multi \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-trivia-test \
                                                           --index wikipedia-dpr-100w \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score_qa(stdout, 'Top20')
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
