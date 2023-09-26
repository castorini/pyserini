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

import multiprocessing
import os
import unittest

from integrations.utils import clean_files, run_command, parse_score


class TestTctColBertV2(unittest.TestCase):
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

    def test_msmarco_passage_tct_colbert_v2_bf_otf(self):
        output_file = 'test_run.msmarco-passage.tct_colbert-v2.bf-otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search.faiss --topics msmarco-passage-dev-subset \
                             --index msmarco-v1-passage.tct_colbert-v2 \
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
        cmd1 = f'python -m pyserini.search.faiss --topics msmarco-passage-dev-subset \
                             --index msmarco-v1-passage.tct_colbert-v2-hn \
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

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
