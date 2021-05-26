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

"""Integration tests for KILT integration."""

import os
import re
import socket
import unittest

from integrations.utils import clean_files, run_command


def parse_kilt_score(output, metric, digits=4):
    pattern = re.compile(r"[0-1]\.[0-9]*")
    for line in output.split('\n')[::-1]:
        if metric in line:
            score = float(pattern.search(line).group(0))
            return round(score, digits)
    return None


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.temp_files = []
        self.threads = 12
        self.batch_size = 36

        # Hard-code larger values for internal servers
        if socket.gethostname().startswith('damiano') or socket.gethostname().startswith('orca'):
            self.threads = 36
            self.batch_size = 144

    def test_kilt_search(self):
        run_file = 'test_run.fever-dev-kilt.jsonl'
        self.temp_files.append(run_file)
        cmd1 = f'python -m pyserini.search --topics fever-dev-kilt \
                             --topics-format kilt \
                             --index wikipedia-kilt-doc \
                             --output {run_file} \
                             --output-format kilt \
                             --threads {self.threads} \
                             --batch-size {self.batch_size}'
        status = os.system(cmd1)
        self.assertEqual(status, 0)
        cmd2 = f'python -m pyserini.eval.evaluate_kilt_retrieval {run_file} fever-dev-kilt --ks 1,100'
        stdout, stderr = run_command(cmd2)
        score = parse_kilt_score(stdout, "Rprec")
        self.assertAlmostEqual(score, 0.3821, delta=0.0001)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
