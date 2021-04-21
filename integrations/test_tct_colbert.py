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

"""Integration tests for TCT-ColBERT model using on-the-fly query encoding."""

import os
import socket
import unittest
from integrations.utils import clean_files, run_command, parse_score


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 12
        self.batch_size = 36

        # Hard-code larger values for internal servers
        if socket.gethostname().startswith('damiano') or socket.gethostname().startswith('orca'):
            self.threads = 36
            self.batch_size = 144

    def test_msmarco_passage_tct_colbert_bf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-bf \
                             --encoded-queries tct_colbert-msmarco-passage-dev-subset \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        print(stderr)
        # We get a small difference in scores on macOS vs. Linux, better way to check:
        self.assertAlmostEqual(score, 0.3350, delta=0.0001)

    def test_msmarco_passage_tct_colbert_bf_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-bf \
                             --encoder castorini/tct_colbert-msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        # We get a small difference in scores on macOS vs. Linux, better way to check:
        self.assertAlmostEqual(score, 0.3350, delta=0.0001)

    def test_msmarco_passage_tct_colbert_hnsw(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.hnsw.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --encoded-queries tct_colbert-msmarco-passage-dev-subset \
                             --encoder castorini/tct_colbert-msmarco \
                             --output {output_file} \
                             --msmarco '
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3345, places=4)

    def test_msmarco_passage_tct_colbert_hnsw_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.hnsw-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-hnsw \
                             --encoder castorini/tct_colbert-msmarco \
                             --output {output_file} \
                             --msmarco '
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3345, places=4)

    def test_msmarco_passage_tct_colbert_bf_bm25_hybrid(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.12 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3529, places=4)

    def test_msmarco_passage_tct_colbert_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf-otf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.12 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3529, places=4)

    def test_msmarco_passage_tct_colbert_bf_d2q_hybrid(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-passage-dev-subset \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.22 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3647, places=4)

    def test_msmarco_passage_tct_colbert_bf_d2q_hybrid_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf-otf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.22 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3647, places=4)

    def test_msmarco_doc_tct_colbert_bf(self):
        output_file = 'test_run.msmarco-doc.passage.tct_colbert.txt'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-doc-dev \
                             --index msmarco-doc-tct_colbert-bf \
                             --encoded-queries tct_colbert-msmarco-doc-dev  \
                             --output {output_file} \
                             --hits 1000 \
                             --max-passage \
                             --max-passage-hits 100 \
                             --msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3323, places=4)

    def test_msmarco_doc_tct_colbert_bf_otf(self):
        output_file = 'test_run.msmarco-doc.passage.tct_colbert-otf.txt'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-doc-dev \
                             --index msmarco-doc-tct_colbert-bf \
                             --encoder castorini/tct_colbert-msmarco \
                             --output {output_file} \
                             --hits 1000 \
                             --max-passage \
                             --max-passage-hits 100 \
                             --msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads}'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3323, places=4)

    def test_msmarco_doc_tct_colbert_bf_bm25_hybrid(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-doc-dev \
                             sparse --index msmarco-doc-per-passage \
                             fusion --alpha 0.25 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3701, places=4)

    def test_msmarco_doc_tct_colbert_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf-otf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-doc-per-passage \
                             fusion --alpha 0.25 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3701, places=4)

    def test_msmarco_doc_tct_colbert_bf_d2q_hybrid(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoded-queries tct_colbert-msmarco-doc-dev \
                             sparse --index msmarco-doc-expanded-per-passage \
                             fusion --alpha 0.32 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3784, places=4)

    def test_msmarco_doc_tct_colbert_bf_d2q_hybrid_otf(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf-otf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-doc-expanded-per-passage \
                             fusion --alpha 0.32 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3784, places=4)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
