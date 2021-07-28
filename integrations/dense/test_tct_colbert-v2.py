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

"""Integration tests for TCT-ColBERTv2 models using on-the-fly query encoding."""

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

    def test_msmarco_passage_tct_colbert_v2_bf_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert-v2.bf-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-bf \
                             --encoder castorini/tct_colbert-v2-msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3440, delta=0.0001)

    def test_msmarco_passage_tct_colbert_v2_hn_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert-v2-hn.bf-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-hn-bf \
                             --encoder castorini/tct_colbert-v2-hn-msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3543, delta=0.0001)

    def test_msmarco_passage_tct_colbert_v2_hnp_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert-v2-hnp.bf-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-tct_colbert-v2-hnp-bf \
                             --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3585, delta=0.0001)

    def test_msmarco_passage_tct_colbert_v2_hnp_bf_bm25_hybrid_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert-v2-hnp.bf-otf.bm25.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
                                    --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             sparse --index msmarco-passage \
                             fusion --alpha 0.06 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3682, delta=0.0001)

    def test_msmarco_passage_tct_colbert_v2_hnp_bf_d2q_hybrid_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert-v2-hnp.bf-otf.doc2queryT5.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.hsearch dense  --index msmarco-passage-tct_colbert-v2-hnp-bf \
                                    --encoder castorini/tct_colbert-v2-hnp-msmarco \
                             sparse --index msmarco-passage-expanded \
                             fusion --alpha 0.1 \
                             run    --topics msmarco-passage-dev-subset \
                                    --output {output_file} \
                                    --batch-size {self.batch_size} --threads {self.threads} \
                                    --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3731, delta=0.0001)

    def test_msmarco_passage_tct_colbert_v2_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('tct_colbert-v2-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_msmarco_passage_tct_colbert_v2_hn_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('tct_colbert-v2-hn-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def test_msmarco_passage_tct_colbert_v2_hnp_encoded_queries(self):
        encoder = QueryEncoder.load_encoded_queries('tct_colbert-v2-hnp-msmarco-passage-dev-subset')
        topics = get_topics('msmarco-passage-dev-subset')
        for t in topics:
            self.assertTrue(topics[t]['title'] in encoder.embedding)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
