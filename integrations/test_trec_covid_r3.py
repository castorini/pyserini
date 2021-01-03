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
import json
import gzip

import sys
sys.path.append('..')

from random import randint
from pyserini.util import download_url,download_prebuilt_index
from integrations.simplesearcher_checker import SimpleSearcherChecker



class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        self.round4_runs = {
            'https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.covid-round3-cumulative.txt':
                'dfccc32efd58a8284ae411e5c6b27ce9',
            'https://raw.githubusercontent.com/castorini/anserini/master/src/main/resources/topics-and-qrels/qrels.covid-round4-cumulative.txt':
                '7a5c27e8e052c49ff72d557051825973',
        }

        self.tmp = f'tmp{randint(0, 10000)}'
        download_url('https://ir.nist.gov/covidSubmit/archive/round4/covidex.r4.d2q.duot5.gz', 'runs')

        with gzip.open(f'runs/covidex.r4.d2q.duot5.gz', 'rb') as f_in:
            with open(f'runs/covidex.r4.d2q.duot5', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        # In the rare event there's a collision
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)

        os.mkdir(self.tmp)
        for url in self.round4_runs:
            print(f'Verifying stored run at {url}...')
            filename = url.split('/')[-1]
            filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter

            download_url(url, self.tmp, md5=self.round4_runs[url], force=True)
            self.assertTrue(os.path.exists(os.path.join(self.tmp, filename)))
            print('')


    def test_bm25(self):

        prebuilt_index_path = download_prebuilt_index('trec-covid-r4-abstract')
        os.system(f'python3 ../../trec-covid-r3/ranker.py \
                    -alpha 0.6 \
                    -clf lr \
                    -vectorizer tfidf \
                    -new_qrels ../tools/topics-and-qrels/qrels.covid-round4-cumulative.txt \
                    -base runs/covidex.r4.d2q.duot5 \
                    -qrels ../tools/topics-and-qrels/qrels.covid-round3-cumulative.txt \
                    -index {prebuilt_index_path} \
                    -tag ../../trec-covid-r3/data/covidex.r4.d2q.duot5.lr \
                    -output {self.tmp}/output.json')
        with open(f'{self.tmp}/output.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.1764\\n'", data['map'])
            self.assertEqual("0.7662\\n'", data['ndcg'])


    def tearDown(self):
        shutil.rmtree(self.tmp)
        os.remove('runs/covidex.r4.d2q.duot5.gz')
        os.remove('runs/covidex.r4.d2q.duot5')
        os.remove('runs/covidex.r4.d2q.duot5.lr.tfidf.R12.A0.6.txt')


if __name__ == '__main__':
    unittest.main()