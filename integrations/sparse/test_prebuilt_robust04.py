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

"""Integration tests for Robust04 using pre-built indexes."""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score


class TestPrebuiltRobust04(unittest.TestCase):
    def setUp(self):
        self.temp_files = []

    def test_robust04(self):
        output_file = 'test_run.robust04.bm25.txt'
        self.temp_files.append(output_file)
        cmd = f'python -m pyserini.search.lucene --topics robust04 --index robust04 --output {output_file} --bm25'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        cmd = f'python -m pyserini.eval.trec_eval -m map robust04 {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')
        self.assertAlmostEqual(score, 0.2531, delta=0.0001)

        cmd = f'python -m pyserini.eval.trec_eval -m P.30 robust04 {output_file}'
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'P_30')
        self.assertAlmostEqual(score, 0.3102, delta=0.0001)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()