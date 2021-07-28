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

import hashlib
import os
import re
import shutil
import unittest
from random import randint

from pyserini.util import download_url


# The purpose of this test case is that, up through and including round 4, the TREC-COVID fusion baselines were
# generated using trectools [1]. This test case ensures that our own internal fusion tools generate *exactly* the
# same output (based on MD5 checksums).
#
# [1] https://github.com/joaopalotti/trectools
class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.runs = {
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.abstract.qq.bm25.txt':
                'd08d85c87e30d6c4abf54799806d282f',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.abstract.qdel.bm25.txt':
                'd552dff90995cd860a5727637f0be4d1',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.full-text.qq.bm25.txt':
                '6c9f4c09d842b887262ca84d61c61a1f',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.full-text.qdel.bm25.txt':
                'c5f9db7733c72eea78ece2ade44d3d35',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.paragraph.qq.bm25.txt':
                '872673b3e12c661748d8899f24d3ba48',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.paragraph.qdel.bm25.txt':
                'c1b966e4c3f387b6810211f339b35852',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.abstract.qq.bm25.txt':
                '56ac5a0410e235243ca6e9f0f00eefa1',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.abstract.qdel.bm25.txt':
                '115d6d2e308b47ffacbc642175095c74',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.full-text.qq.bm25.txt':
                'af0d10a5344f4007e6781e8d2959eb54',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.full-text.qdel.bm25.txt':
                '594d469b8f45cf808092a3d8e870eaf5',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.paragraph.qq.bm25.txt':
                '6f468b7b60aaa05fc215d237b5475aec',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.paragraph.qdel.bm25.txt':
                'b7b39629c12573ee0bfed8687dacc743',
        }

        self.tmp = f'tmp{randint(0, 10000)}'

        # In the rare event there's a collision
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)

        os.mkdir(self.tmp)
        for url in self.runs:
            print(f'Verifying stored run at {url}...')
            filename = url.split('/')[-1]
            filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter

            download_url(url, self.tmp, md5=self.runs[url], force=True)
            self.assertTrue(os.path.exists(os.path.join(self.tmp, filename)))
            print('')

    def test_round3_fusion_runs(self):
        os.system(f'python -m pyserini.fusion --method rrf --runs ' +
                  f'{self.tmp}/anserini.covid-r3.abstract.qq.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r3.full-text.qq.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r3.paragraph.qq.bm25.txt ' +
                  f' --output {self.tmp}/anserini.covid-r3.fusion1.txt ' +
                  f'--runtag reciprocal_rank_fusion_k=60 --k 100000')

        with open(f'{self.tmp}/anserini.covid-r3.fusion1.txt', 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        self.assertEqual('61cbd73c6e60ba44f18ce967b5b0e5b3', md5)

        os.system(f'python -m pyserini.fusion --method rrf --runs ' +
                  f'{self.tmp}/anserini.covid-r3.abstract.qdel.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r3.full-text.qdel.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r3.paragraph.qdel.bm25.txt ' +
                  f' --output {self.tmp}/anserini.covid-r3.fusion2.txt ' +
                  f'--runtag reciprocal_rank_fusion_k=60 --k 100000')

        with open(f'{self.tmp}/anserini.covid-r3.fusion2.txt', 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        self.assertEqual('d7eabf3dab840104c88de925e918fdab', md5)

    def test_round3_fusion_runs(self):
        os.system(f'python -m pyserini.fusion --method rrf --runs ' +
                  f'{self.tmp}/anserini.covid-r4.abstract.qq.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r4.full-text.qq.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r4.paragraph.qq.bm25.txt ' +
                  f' --output {self.tmp}/anserini.covid-r4.fusion1.txt ' +
                  f'--runtag reciprocal_rank_fusion_k=60 --k 100000')

        with open(f'{self.tmp}/anserini.covid-r4.fusion1.txt', 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        self.assertEqual('8ae9d1fca05bd1d9bfe7b24d1bdbe270', md5)

        os.system(f'python -m pyserini.fusion --method rrf --runs ' +
                  f'{self.tmp}/anserini.covid-r4.abstract.qdel.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r4.full-text.qdel.bm25.txt ' +
                  f'{self.tmp}/anserini.covid-r4.paragraph.qdel.bm25.txt ' +
                  f' --output {self.tmp}/anserini.covid-r4.fusion2.txt ' +
                  f'--runtag reciprocal_rank_fusion_k=60 --k 100000')

        with open(f'{self.tmp}/anserini.covid-r4.fusion2.txt', 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        self.assertEqual('e1894209c815c96c6ddd4cacb578261a', md5)

    def tearDown(self):
        shutil.rmtree(self.tmp)


if __name__ == '__main__':
    unittest.main()
