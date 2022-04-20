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

"""Integration tests for nmslib index search"""

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

    def test_msmarco_passage_deepimpact_nmslib_hnsw(self):
        output_file = 'test_run.msmarco-passage.deepimpact.nmslib.tsv'
        self.temp_files.append(output_file)
        cmd = 'wget https://raw.githubusercontent.com/castorini/pyserini-data/main/encoded-queries/deepimpact_msmarco_passage_dev_topic.jsonl'
        status = os.system(cmd)
        cmd = 'wget https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-indexes/nmslib-index.msmarco-passage.deepimpact.20211012.58d286.tar.gz'
        status = os.system(cmd)
        cmd = 'tar -xvf nmslib-index.msmarco-passage.deepimpact.20211012.58d286.tar.gz'
        status = os.system(cmd)
        self.temp_files.append('deepimpact_msmarco_passage_dev_topic.jsonl')
        self.temp_files.append('nmslib-index.msmarco-passage.deepimpact.20211012.58d286.tar.gz')
        self.temp_files.append('nmslib-index.msmarco-passage.deepimpact.20211012.58d286')
        cmd1 = f'python -m pyserini.search.nmslib --topics deepimpact_msmarco_passage_dev_topic.jsonl \
                          --index nmslib-index.msmarco-passage.deepimpact.20211012.58d286 \
                          --output {output_file} \
                          --hits 1000 --batch {self.batch_size} --threads {self.threads} \
                          --output-format msmarco --is-sparse --ef 1000'
        cmd2 = f'python -m pyserini.eval.msmarco_passage_eval msmarco-passage-dev-subset {output_file}'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd2)
        score = parse_score(stdout, "MRR @10")
        self.assertEqual(status, 0)
        self.assertAlmostEqual(score, 0.298, delta=0.001)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()