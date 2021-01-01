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
import hashlib
import os
import re
import shutil
import unittest
from random import randint
from pyserini.util import download_url


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.round3_runs = {
            'https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.covid-round3-cumulative.txt':
                'dfccc32efd58a8284ae411e5c6b27ce9',
            'https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.covid-round4-cumulative.txt':
                '7a5c27e8e052c49ff72d557051825973'
        }
        self.tmp = f'../trec-covid-r3/check_data'

        # In the rare event there's a collision
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)

        os.mkdir(self.tmp)
        for url in self.round3_runs:
            print(f'Verifying stored run at {url}...')
            filename = url.split('/')[-1]
            filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter

            download_url(url, self.tmp, md5=self.round3_runs[url], force=True)
            self.assertTrue(os.path.exists(os.path.join(self.tmp, filename)))
            print('')


    def test_round3_score_runs(self):
        os.system(f'python3 ../trec-covid-r3/ranker.py \
            -alpha 0.6 \
            -clf lr \
            -vectorizer tfidf \
            -trec_covid_home ../trec-covid-r3 \
            -base ../trec-covid-r3/data/covidex.r4.d2q.duot5 \
            -qrels {self.tmp}/qrels.covid-round3-cumulative.txt \
            -index ../trec-covid-r3/data/lucene-index-cord19-abstract-2020-06-19 \
            -tag ../trec-covid-r3/data/covidex.r4.d2q.duot5.lr')


    # def tearDown(self):
    #     shutil.rmtree(self.tmp)
    #     shutil.rmtree('runs')


if __name__ == '__main__':
    unittest.main()