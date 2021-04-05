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

"""Integration tests for ANCE model using on-the-fly query encoding."""

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

    def test_msmarco_passage_distilbert_kd_bf(self):
        output_file = 'test_run.msmarco-passage.distilbert-dot-margin_mse-T2.bf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.dsearch --topics msmarco-passage-dev-subset \
                             --index msmarco-passage-distilbert-dot-margin_mse-T2-bf \
                             --encoder sebastian-hofstaetter/distilbert-dot-margin_mse-T2-msmarco \
                             --batch-size {self.batch_size} \
                             --threads {self.threads} \
                             --output {output_file} \
                             --msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3251, delta=0.0001)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
