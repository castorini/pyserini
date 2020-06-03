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

import filecmp
import os
import unittest


class TestSearch(unittest.TestCase):
    def setUp(self):
        self.qruns = ['covidex.t5', 'covidex.sim']
        self.cmps = ['myfused.txt', 'fused.txt']

        for qrun in self.qruns:
            os.system(f'wget -q -nc https://ir.nist.gov/covidSubmit/archive/round2/{qrun}')

        os.system('wget -q -nc https://www.dropbox.com/s/scl0lm7x47jrsxh/fused.txt')

    def test_reciprocal_rank_fusion(self):
        os.system('python -m pyserini.fusion --runs covidex.sim covidex.t5 --output myfused.txt --tag reciprocal_rank_fusion_k=60')
        self.assertTrue(filecmp.cmp(self.cmps[0], self.cmps[1]))

    def tearDown(self):
        for path in self.qruns + self.cmps:
            os.remove(path)


if __name__ == '__main__':
    unittest.main()
