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

"""Integration tests for TCT-ColBERTv1 models using on-the-fly query encoding."""

import multiprocessing
import os
import unittest

from integrations.core.utils import clean_files, run_command, parse_score
from pyserini.encode import QueryEncoder
from pyserini.search import get_topics


class TestTctColBert(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 16
        self.batch_size = self.threads * 32

        half_cores = int(multiprocessing.cpu_count() / 2)
        # If server supports more threads, then use more threads.
        # As a heuristic, use up half up available CPU cores.
        if half_cores > self.threads:
            self.threads = half_cores
            self.batch_size = half_cores * 32

    def test_msmarco_passage_tct_colbert_bf_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.faiss --topics msmarco-passage-dev-subset \
                             --index msmarco-v1-passage.tct_colbert \
                             --encoder castorini/tct_colbert-msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        # We get a small difference in scores on macOS vs. Linux, better way to check:
        self.assertAlmostEqual(score, 0.3350, delta=0.0002)

    def test_msmarco_passage_tct_colbert_hnsw_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.hnsw-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.faiss --topics msmarco-passage-dev-subset \
                             --index msmarco-v1-passage.tct_colbert.hnsw \
                             --encoder castorini/tct_colbert-msmarco \
                             --output {output_file} \
                             --output-format msmarco '
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3345, delta=0.0002)

    def test_msmarco_passage_tct_colbert_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf-otf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.hybrid dense  --index msmarco-v1-passage.tct_colbert \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-v1-passage \
                             fusion --alpha 0.12 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3529, places=4)

    def test_msmarco_passage_tct_colbert_bf_d2q_hybrid_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert.bf-otf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.hybrid dense  --index msmarco-v1-passage.tct_colbert \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-v1-passage.d2q-t5 \
                             fusion --alpha 0.22 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3647, delta=0.0002)

    def test_msmarco_passage_tct_colbert_encoded_queries(self):
        encoded = QueryEncoder.load_encoded_queries('tct_colbert-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoded.embedding)

    def test_msmarco_doc_tct_colbert_bf_otf(self):
        output_file = 'test_run.msmarco-doc.passage.tct_colbert-otf.txt'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.faiss --topics msmarco-doc-dev \
                             --index msmarco-v1-doc.tct_colbert \
                             --encoder castorini/tct_colbert-msmarco \
                             --output {output_file} \
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
        self.assertAlmostEqual(score, 0.3323, places=4)

    def test_msmarco_doc_tct_colbert_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf-otf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.hybrid dense  --index msmarco-v1-doc.tct_colbert \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-v1-doc-segmented \
                             fusion --alpha 0.25 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @100")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3701, places=4)

    def test_msmarco_doc_tct_colbert_bf_d2q_hybrid_otf(self):
        output_file = 'test_run.msmarco-doc.tct_colbert.bf-otf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.hybrid dense  --index msmarco-v1-doc.tct_colbert \
                                    --encoder castorini/tct_colbert-msmarco \
                             sparse --index msmarco-v1-doc-segmented.d2q-t5 \
                             fusion --alpha 0.32 \
                             run    --topics msmarco-doc-dev \
                                    --output {output_file} \
                                    --hits 1000 --max-passage --max-passage-hits 100 \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output-format msmarco'
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
