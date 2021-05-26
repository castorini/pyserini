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

import os
import re
import shutil
import unittest
from random import randint

from pyserini.util import download_url


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.round3_runs = {
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
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.fusion1.txt':
                '61cbd73c6e60ba44f18ce967b5b0e5b3',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.covid-r3.fusion2.txt':
                'd7eabf3dab840104c88de925e918fdab',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.final-r3.fusion1.txt':
                'c1caf63a9c3b02f0b12e233112fc79a6',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.final-r3.fusion2.txt':
                '12679197846ed77306ecb2ca7895b011',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.final-r3.rf.txt':
                '7192a08c5275b59d5ef18395917ff694',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.final-r3.fusion1.post-processed.txt':
                'f7c69c9bff381a847af86e5a8daf7526',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.final-r3.fusion2.post-processed.txt':
                '84c5fd2c7de0a0282266033ac4f27c22',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round3/anserini.final-r3.rf.post-processed.txt':
                '3e79099639a9426cb53afe7066239011'
        }

        self.round4_runs = {
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
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.fusion1.txt':
                '8ae9d1fca05bd1d9bfe7b24d1bdbe270',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.fusion2.txt':
                'e1894209c815c96c6ddd4cacb578261a',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.covid-r4.abstract.qdel.bm25%2Brm3Rf.txt':
                '9d954f31e2f07e11ff559bcb14ef16af',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.final-r4.fusion1.txt':
                'a8ab52e12c151012adbfc8e37d666760',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.final-r4.fusion2.txt':
                '1500104c928f463f38e76b58b91d4c07',
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round4/anserini.final-r4.rf.txt':
                '41d746eb86a99d2f33068ebc195072cd'
        }

    def check_runs(self, runs):
        tmp = f'tmp{randint(0, 10000)}'

        # In the rare event there's a collision
        if os.path.exists(tmp):
            shutil.rmtree(tmp)

        os.mkdir(tmp)
        for url in runs:
            print(f'Verifying stored run at {url}...')
            filename = url.split('/')[-1]
            filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter

            download_url(url, tmp, md5=runs[url], force=True)
            self.assertTrue(os.path.exists(os.path.join(tmp, filename)))
            print('')

        shutil.rmtree(tmp)

    def test_round3_runs(self):
        self.check_runs(self.round3_runs)

    def test_round4_runs(self):
        self.check_runs(self.round4_runs)


if __name__ == '__main__':
    unittest.main()
