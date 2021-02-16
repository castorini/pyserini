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
from integrations.utils import clean_files, run_command, parse_score


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    def test_dpr_nq_test_bf(self):
        output_file = 'test_run.dpr.nq-test.multi.bf.trec'
        retrieval_file = 'test_run.dpr.nq-test.multi.bf.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics dpr-nq-test \
                             --index wikipedia-dpr-multi-bf \
                             --output {output_file} \
                             --batch 36 --threads 12'
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-nq-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.7947368421052632, places=4)

    def test_dpr_nq_test_bf_bm25_hybrid(self):
        output_file = 'test_run.dpr.nq-test.multi.bf.bm25.trec'
        retrieval_file = 'test_run.dpr.nq-test.multi.bf.bm25.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-nq-test \
                                    --batch-size 36 --threads 12 \
                                    --output {output_file} '
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-nq-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.8260387811634349, places=4)

    def test_dpr_trivia_test_bf(self):
        output_file = 'test_run.dpr.trivia-test.multi.bf.trec'
        retrieval_file = 'test_run.dpr.trivia-test.multi.bf.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics dpr-trivia-test \
                             --index wikipedia-dpr-multi-bf \
                             --output {output_file} \
                             --batch 36 --threads 12'
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-trivia-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.7887386192875453, places=4)

    def test_dpr_trivia_test_bf_bm25_hybrid(self):
        output_file = 'test_run.dpr.trivia-test.multi.bf.bm25.trec'
        retrieval_file = 'test_run.dpr.trivia-test.multi.bf.bm25.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-trivia-test \
                                    --batch-size 36 --threads 12 \
                                    --output {output_file} '
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-trivia-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.8263944135065854, places=4)

    def test_dpr_wq_test_bf(self):
        output_file = 'test_run.dpr.wq-test.multi.bf.trec'
        retrieval_file = 'test_run.dpr.wq-test.multi.bf.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics dpr-wq-test \
                             --index wikipedia-dpr-multi-bf \
                             --output {output_file} \
                             --batch 36 --threads 12'
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-wq-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.750492125984252, places=4)

    def test_dpr_wq_test_bf_bm25_hybrid(self):
        output_file = 'test_run.dpr.wq-test.multi.bf.bm25.trec'
        retrieval_file = 'test_run.dpr.wq-test.multi.bf.bm25.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-wq-test \
                                    --batch-size 36 --threads 12 \
                                    --output {output_file} '
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-wq-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.7711614173228346, places=4)

    def test_dpr_curated_test_bf(self):
        output_file = 'test_run.dpr.curated-test.multi.bf.trec'
        retrieval_file = 'test_run.dpr.curated-test.multi.bf.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics dpr-curated-test \
                             --index wikipedia-dpr-multi-bf \
                             --output {output_file} \
                             --batch 36 --threads 12'
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-curated-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20 --regex'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.8876080691642652, places=4)

    def test_dpr_curated_test_bf_bm25_hybrid(self):
        output_file = 'test_run.dpr.curated-test.multi.bf.bm25.trec'
        retrieval_file = 'test_run.dpr.curated-test.multi.bf.bm25.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-curated-test \
                                    --batch-size 36 --threads 12 \
                                    --output {output_file} '
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-curated-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20 --regex'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.9005763688760807, places=4)

    def test_dpr_squad_test_bf(self):
        output_file = 'test_run.dpr.squad-test.multi.bf.trec'
        retrieval_file = 'test_run.dpr.squad-test.multi.bf.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics dpr-squad-test \
                             --index wikipedia-dpr-multi-bf \
                             --output {output_file} \
                             --batch 36 --threads 12'
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-squad-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.5198675496688742, places=4)

    def test_dpr_squad_test_bf_bm25_hybrid(self):
        output_file = 'test_run.dpr.squad-test.multi.bf.bm25.trec'
        retrieval_file = 'test_run.dpr.squad-test.multi.bf.bm25.json'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index wikipedia-dpr-multi-bf \
                             sparse --index wikipedia-dpr \
                             fusion --alpha 1.3 \
                             run    --topics dpr-squad-test \
                                    --batch-size 36 --threads 12 \
                                    --output {output_file} '
        cmd2 = f'python scripts/dpr/convert_trec_run_to_retrieval_json.py --topics dpr-squad-test \
                                                           --index wikipedia-dpr \
                                                           --input {output_file} \
                                                           --output {retrieval_file}'
        cmd3 = f'python tools/scripts/dpr/evaluate_retrieval.py --retrieval {retrieval_file} --topk 20'
        status1 = os.system(cmd1)
        status2 = os.system(cmd2)
        stdout, stderr = run_command(cmd3)
        score = parse_score(stdout, "Top20")
        self.assertEqual(status1, 0)
        self.assertEqual(status2, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.7510879848628192, places=4)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
