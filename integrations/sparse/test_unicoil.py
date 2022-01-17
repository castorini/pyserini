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

"""Integration tests for uniCOIL and Tilde models using on-the-fly query encoding."""

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

    def test_msmarco_passage_unicoil_d2q_otf(self):
        output_file = 'test_run.msmarco-passage.unicoil-d2q.otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search --topics msmarco-passage-dev-subset \
                          --encoder castorini/unicoil-d2q-msmarco-passage \
                          --index msmarco-passage-unicoil-d2q \
                          --output {output_file} \
                          --impact \
                          --hits 1000 --batch {self.batch_size} --threads {self.threads} \
                          --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3509, delta=0.0001)

    def test_msmarco_doc_unicoil_d2q_otf(self):
        output_file = 'test_run.msmarco-doc.unicoil-d2q.otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search --topics msmarco-doc-dev \
                          --encoder castorini/unicoil-d2q-msmarco-passage \
                          --index msmarco-doc-per-passage-unicoil-d2q \
                          --output {output_file} \
                          --impact \
                          --hits 1000 --batch {self.batch_size} --threads {self.threads} \
                          --max-passage --max-passage-hits 100 \
                          --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_doc_eval --judgments msmarco-doc-dev --run {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3531, delta=0.0001)
    
    def test_msmarco_passage_tilde_otf(self):
        output_file = 'test_run.msmarco-passage.tilde.otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search --topics msmarco-passage-dev-subset \
                          --encoder ielab/unicoil-tilde200-msmarco-passage \
                          --index msmarco-passage-unicoil-tilde \
                          --output {output_file} \
                          --impact \
                          --hits 1000 --batch {self.batch_size} --threads {self.threads} \
                          --output-format msmarco'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.3495, delta=0.0001)
    
    def test_msmarco_v2_passage_unicoil_noexp_otf(self):
        output_file = 'test_run.msmarco-v2-passage.unicoil-noexp.0shot.otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search --topics msmarco-v2-passage-dev \
                          --encoder castorini/unicoil-noexp-msmarco-passage \
                          --index msmarco-v2-passage-unicoil-noexp-0shot  \
                          --output {output_file} \
                          --impact \
                          --hits 1000 \
                          --batch {self.batch_size} \
                          --threads {self.threads} \
                          --min-idf 1'
        cmd2 = f'python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-passage-dev {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "recip_rank")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.1314, delta=0.0001)
    
    def test_msmarco_v2_doc_unicoil_noexp_otf(self):
        output_file = 'test_run.msmarco-v2-doc.unicoil-noexp.0shot.otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search --topics msmarco-v2-doc-dev \
                          --encoder castorini/unicoil-noexp-msmarco-passage \
                          --index msmarco-v2-doc-per-passage-unicoil-noexp-0shot  \
                          --output {output_file} \
                          --impact \
                          --hits 10000 \
                          --batch {self.batch_size} \
                          --threads {self.threads} \
                          --max-passage-hits 1000 \
                          --max-passage \
                          --min-idf 1'
        cmd2 = f'python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-doc-dev {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "recip_rank")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.2032, delta=0.0001)
    
    def test_msmarco_v2_passage_tilde_otf(self):
        output_file = 'test_run.msmarco-v2-passage.tilde.0shot.otf.tsv'
        self.temp_files.append(output_file)
        cmd1 = f'python -m pyserini.search --topics msmarco-v2-passage-dev \
                          --encoder ielab/unicoil-tilde200-msmarco-passage \
                          --index msmarco-v2-passage-unicoil-tilde \
                          --output {output_file} \
                          --impact \
                          --hits 1000 \
                          --batch {self.batch_size} \
                          --threads {self.threads} \
                          --min-idf 1'
        cmd2 = f'python -m pyserini.eval.trec_eval -c -M 100 -m map -m recip_rank msmarco-v2-passage-dev {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "recip_rank")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.1480, delta=0.0001)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()