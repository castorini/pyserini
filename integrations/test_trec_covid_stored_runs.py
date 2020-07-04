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

import os
import re
import shutil
import unittest
from random import randint

from pyserini.util import download_url


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.round3_runs = {
            'https://www.dropbox.com/s/g80cqdxud1l06wq/anserini.covid-r3.abstract.qq.bm25.txt?dl=1':
                'd08d85c87e30d6c4abf54799806d282f',
            'https://www.dropbox.com/s/sjcnxq7h0a3j3xz/anserini.covid-r3.abstract.qdel.bm25.txt?dl=1':
                'd552dff90995cd860a5727637f0be4d1',
            'https://www.dropbox.com/s/4bjx35sgosu0jz0/anserini.covid-r3.full-text.qq.bm25.txt?dl=1':
                '6c9f4c09d842b887262ca84d61c61a1f',
            'https://www.dropbox.com/s/mjt7y1ywae784d0/anserini.covid-r3.full-text.qdel.bm25.txt?dl=1':
                'c5f9db7733c72eea78ece2ade44d3d35',
            'https://www.dropbox.com/s/qwn7jd8vg2chjik/anserini.covid-r3.paragraph.qq.bm25.txt?dl=1':
                '872673b3e12c661748d8899f24d3ba48',
            'https://www.dropbox.com/s/2928i60fj2i09bt/anserini.covid-r3.paragraph.qdel.bm25.txt?dl=1':
                'c1b966e4c3f387b6810211f339b35852',
            'https://www.dropbox.com/s/6vk5iohqf81iy8b/anserini.covid-r3.fusion1.txt?dl=1':
                '61cbd73c6e60ba44f18ce967b5b0e5b3',
            'https://www.dropbox.com/s/n09595t1eqymkks/anserini.covid-r3.fusion2.txt?dl=1':
                'd7eabf3dab840104c88de925e918fdab',
            'https://www.dropbox.com/s/ypoe9tgwef17rak/anserini.final-r3.fusion1.txt?dl=1':
                'c1caf63a9c3b02f0b12e233112fc79a6',
            'https://www.dropbox.com/s/uvfrssp6nw2v2jl/anserini.final-r3.fusion2.txt?dl=1':
                '12679197846ed77306ecb2ca7895b011',
            'https://www.dropbox.com/s/2wrg7ceaca3n7ac/anserini.final-r3.rf.txt?dl=1':
                '7192a08c5275b59d5ef18395917ff694',
            'https://www.dropbox.com/s/ilqgky1tti0zvez/anserini.final-r3.fusion1.post-processed.txt?dl=1':
                'f7c69c9bff381a847af86e5a8daf7526',
            'https://www.dropbox.com/s/ue3z6xxxca9krkb/anserini.final-r3.fusion2.post-processed.txt?dl=1':
                '84c5fd2c7de0a0282266033ac4f27c22',
            'https://www.dropbox.com/s/95vk831wp1ldnpm/anserini.final-r3.rf.post-processed.txt?dl=1':
                '3e79099639a9426cb53afe7066239011'
        }

        self.round4_runs = {
            'https://www.dropbox.com/s/mf79huhxfy96g6i/anserini.covid-r4.abstract.qq.bm25.txt?dl=1':
                '56ac5a0410e235243ca6e9f0f00eefa1',
            'https://www.dropbox.com/s/4zau6ejrkvgn9m7/anserini.covid-r4.abstract.qdel.bm25.txt?dl=1':
                '115d6d2e308b47ffacbc642175095c74',
            'https://www.dropbox.com/s/bpdopie6gqffv0w/anserini.covid-r4.full-text.qq.bm25.txt?dl=1':
                'af0d10a5344f4007e6781e8d2959eb54',
            'https://www.dropbox.com/s/rh0uy71ogbpas0v/anserini.covid-r4.full-text.qdel.bm25.txt?dl=1':
                '594d469b8f45cf808092a3d8e870eaf5',
            'https://www.dropbox.com/s/ifkjm8ff8g2aoh1/anserini.covid-r4.paragraph.qq.bm25.txt?dl=1':
                '6f468b7b60aaa05fc215d237b5475aec',
            'https://www.dropbox.com/s/keuogpx1dzinsgy/anserini.covid-r4.paragraph.qdel.bm25.txt?dl=1':
                'b7b39629c12573ee0bfed8687dacc743',
            'https://www.dropbox.com/s/zjc0069do0a4gu3/anserini.covid-r4.fusion1.txt?dl=1':
                '8ae9d1fca05bd1d9bfe7b24d1bdbe270',
            'https://www.dropbox.com/s/qekc9vr3oom777n/anserini.covid-r4.fusion2.txt?dl=1':
                'e1894209c815c96c6ddd4cacb578261a',
            'https://www.dropbox.com/s/2jx27rh3lknps9q/anserini.covid-r4.abstract.qdel.bm25%2Brm3Rf.txt?dl=1':
                '9d954f31e2f07e11ff559bcb14ef16af',
            'https://www.dropbox.com/s/g3giixyusk4tzro/anserini.final-r4.fusion1.txt?dl=1':
                'a8ab52e12c151012adbfc8e37d666760',
            'https://www.dropbox.com/s/z4wbqj9gfos8wln/anserini.final-r4.fusion2.txt?dl=1':
                '1500104c928f463f38e76b58b91d4c07',
            'https://www.dropbox.com/s/28w83b07yzndlbg/anserini.final-r4.rf.txt?dl=1':
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
