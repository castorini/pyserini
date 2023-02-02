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
import unittest

from integrations.utils import clean_files, run_command, parse_score


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 16
        self.batch_size = 128

    def test_msmarco_doc_unicoil_d2q_otf(self):
        output_file = 'test_run.msmarco-doc.unicoil-d2q.otf.tsv'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene \
                   --threads {self.threads} --batch-size {self.batch_size} \
                   --index msmarco-v1-doc-segmented-unicoil \
                   --topics msmarco-doc-dev \
                   --encoder castorini/unicoil-msmarco-passage \
                   --output {output_file} \
                   --impact --hits 10000 --max-passage --max-passage-hits 1000'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        # Match score in https://castorini.github.io/pyserini/2cr/msmarco-v1-doc.html
        stdout, stderr = run_command(f'python -m pyserini.eval.trec_eval -c -M 100 -m recip_rank \
                                         msmarco-doc-dev {output_file}')
        self.assertAlmostEqual(0.3532, parse_score(stdout, "recip_rank"), delta=0.0001)

        stdout, stderr = run_command(f'python -m pyserini.eval.trec_eval -c -m recall.1000 \
                                         msmarco-doc-dev {output_file}')
        self.assertAlmostEqual(0.9546, parse_score(stdout, "recall_1000"), delta=0.0001)

    def test_msmarco_passage_tilde_otf(self):
        output_file = 'test_run.msmarco-passage.tilde.otf.tsv'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene \
                   --threads {self.threads} --batch-size {self.batch_size} \
                   --index msmarco-v1-passage-unicoil-tilde \
                   --topics msmarco-passage-dev-subset \
                   --encoder ielab/unicoil-tilde200-msmarco-passage \
                   --output {output_file} \
                   --output-format msmarco \
                   --impact --hits 1000'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        # Match score in https://github.com/castorini/pyserini/blob/master/docs/experiments-unicoil-tilde-expansion.md
        stdout, stderr = run_command(f'python -m pyserini.eval.msmarco_passage_eval \
                                         msmarco-passage-dev-subset {output_file}')
        self.assertAlmostEqual(0.3495, parse_score(stdout, "MRR @10"), delta=0.0001)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
