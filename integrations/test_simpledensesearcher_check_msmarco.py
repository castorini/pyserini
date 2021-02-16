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

    def test_msmarco_passage_tct_colbert_bf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-bf \
                             --batch-size 36 \
                             --threads 12 \
                             --output {output_file} \
                             --msmarco'
        cmd2 = f'python tools/scripts/msmarco/msmarco_passage_eval.py \
                    tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
                    {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.33498851594123724, places=4)

    def test_msmarco_passage_tct_colbert_hnsw(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.hnsw.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-hnsw \
                             --output {output_file} \
                             --msmarco '
        cmd2 = f'python tools/scripts/msmarco/msmarco_passage_eval.py \
                    tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
                    {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.33446763996907186, places=4)

    def test_msmarco_passage_tct_colbert_bf_bm25_hybrid(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.12 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size 36 --threads 12 \
                                    --msmarco'
        cmd2 = f'python tools/scripts/msmarco/msmarco_passage_eval.py \
                    tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
                    {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.35290080502114884, places=4)

    def test_msmarco_passage_tct_colbert_bf_d2q_hybrid(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-bf \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.22 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size 36 --threads 12 \
                                    --msmarco'
        cmd2 = f'python tools/scripts/msmarco/msmarco_passage_eval.py \
                    tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
                    {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.364655705644245, places=4)

    def test_msmarco_doc_tct_colbert_bf(self):
        output_file = 'test_run.msmarco-doc.passage.tct_colbert.txt'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-doc-dev \
                             --index msmarco-doc-tct_colbert-bf \
                             --encoder castorini/tct_colbert-msmarco \
                             --output {output_file} \
                             --hits 1000 \
                             --max-passage \
                             --max-passage-hits 100 \
                             --msmarco \
                             --batch-size 36 \
                             --threads 12'
        cmd2 = f'python tools/scripts/msmarco/msmarco_doc_eval.py \
                    tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
                    {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3323255796764856, places=4)

    def test_msmarco_doc_tct_colbert_bf_bm25_hybrid(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-doc-per-passage \
                             fusion --alpha 0.25 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size 36 --threads 12 \
                                    --msmarco'
        cmd2 = f'python tools/scripts/msmarco/msmarco_doc_eval.py \
                    tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
                    {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3323255796764856, places=4)

    def test_msmarco_doc_tct_colbert_bf_d2q_hybrid(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-doc-tct_colbert-bf \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-doc-expanded-per-passage \
                             fusion --alpha 0.32 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size 36 --threads 12 \
                                    --msmarco'
        cmd2 = f'python tools/scripts/msmarco/msmarco_doc_eval.py \
                    tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
                    {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3323255796764856, places=4)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
