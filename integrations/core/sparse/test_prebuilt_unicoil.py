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

"""Integration tests for uniCOIL models using on-the-fly query encoding."""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 16
        self.batch_size = 128

    def test_msmarco_passage_tilde_otf(self):
        output_file = 'test_run.msmarco-passage.tilde.otf.tsv'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene \
                   --threads {self.threads} --batch-size {self.batch_size} \
                   --index msmarco-v1-passage.unicoil-tilde \
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
