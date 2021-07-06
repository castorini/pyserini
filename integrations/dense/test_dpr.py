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

"""Integration tests for DPR model using pre-encoded queries."""

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

        # Hard-code larger values for internal servers
        if socket.gethostname().startswith('damiano') or socket.gethostname().startswith('orca'):
            self.threads = 36
            self.batch_size = 144

    def test_dpr_nq_test_bf_otf(self):
        output_file = 'test_run.dpr.nq-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.nq-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoder facebook/dpr-question_encoder-multiset-base \
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
        self.assertAlmostEqual(score, 0.7947, places=4)

    def test_dpr_nq_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.nq-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.nq-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-nq-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
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
        self.assertAlmostEqual(score, 0.8260, places=4)

    def test_dpr_nq_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-nq-test')
        topics = get_topics('dpr-nq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_trivia_test_bf_otf(self):
        output_file = 'test_run.dpr.trivia-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.trivia-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.dsearch --topics dpr-trivia-test \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --index wikipedia-dpr-multi-bf \
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
        self.assertAlmostEqual(score, 0.7887, places=4)

    def test_dpr_trivia_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.trivia-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.trivia-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.95 \
                             run    --topics dpr-trivia-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
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
        self.assertAlmostEqual(score, 0.8264, places=4)

    def test_dpr_trivia_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-trivia-test')
        topics = get_topics('dpr-trivia-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_wq_test_bf_otf(self):
        output_file = 'test_run.dpr.wq-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.wq-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.dsearch --topics dpr-wq-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-wq-test \
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
        self.assertAlmostEqual(score, 0.7505, places=4)

    def test_dpr_wq_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.wq-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.wq-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 0.95 \
                             run    --topics dpr-wq-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-wq-test \
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
        self.assertAlmostEqual(score, 0.7712, places=4)

    def test_dpr_wq_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-wq-test')
        topics = get_topics('dpr-wq-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_curated_test_bf_otf(self):
        output_file = 'test_run.dpr.curated-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.curated-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.dsearch --topics dpr-curated-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-curated-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file} \
                                                           --regex'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20 --regex'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.8876, places=4)

    def test_dpr_curated_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.curated-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.curated-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.05 \
                             run    --topics dpr-curated-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-curated-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file} \
                                                           --regex'
        cmd3 = f'python -m pyserini.eval.evaluate_dpr_retrieval --retrieval {retrieval_file} --topk 20 --regex'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertAlmostEqual(score, 0.9006, places=4)

    def test_dpr_curated_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-curated-test')
        topics = get_topics('dpr-curated-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_dpr_squad_test_bf_otf(self):
        output_file = 'test_run.dpr.squad-test.multi.bf.otf.trec'
        retrieval_file = 'test_run.dpr.squad-test.multi.bf.otf.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.dsearch --topics dpr-squad-test \
                             --index wikipedia-dpr-multi-bf \
                             --encoder facebook/dpr-question_encoder-multiset-base \
                             --output {output_file} \
                             --batch-size {self.batch_size} --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-squad-test \
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
        self.assertAlmostEqual(score, 0.5199, places=4)

    def test_dpr_squad_test_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.dpr.squad-test.multi.bf.otf.bm25.trec'
        retrieval_file = 'test_run.dpr.squad-test.multi.bf.otf.bm25.json'
        self.temp_files.extend([output_file, retrieval_file])
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                                    --encoder facebook/dpr-question_encoder-multiset-base \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 2.0 \
                             run    --topics dpr-squad-test \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output {output_file} '
        cmd2 = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run --topics dpr-squad-test \
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
        self.assertAlmostEqual(score, 0.7511, places=4)

    def test_dpr_squad_test_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('dpr_multi-squad-test')
        topics = get_topics('dpr-squad-test')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
