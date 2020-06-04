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

import filecmp
import os
from pyserini.trectools import TrecRun
import unittest


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.qruns = ['tests/resources/covidex.t5', 'tests/resources/covidex.sim']
        self.output_path = 'tests/resources/output.txt'

    def test_reciprocal_rank_fusion(self):
        answer_path = 'tests/resources/rrf_verify.txt'

        cmd = f'python -m pyserini.fusion --runs {self.qruns[0]} {self.qruns[1]} --output {self.output_path} --tag reciprocal_rank_fusion_k=60'
        os.system(cmd)
        self.assertTrue(filecmp.cmp(answer_path, self.output_path))
        os.remove(self.output_path)

    def test_trec_run_read(self):
        input_path = 'tests/resources/simple_trec_run.txt'
        verify_path = 'tests/resources/simple_trec_run_verify.txt'

        run = TrecRun(filepath=input_path)
        run.save_to_txt(self.output_path)
        self.assertTrue(filecmp.cmp(verify_path, self.output_path))
        os.remove(self.output_path)


if __name__ == '__main__':
    unittest.main()
