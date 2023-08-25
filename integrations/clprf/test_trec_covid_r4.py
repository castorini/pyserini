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

import gzip
import json
import os
import re
import shutil
import unittest
from random import randint

from pyserini.util import download_url, download_prebuilt_index


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):

        curdir = os.getcwd()
        if curdir.endswith('clprf'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'

        self.tmp = f'{self.pyserini_root}/integrations/tmp{randint(0, 10000)}'

        # In the rare event there's a collision
        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)

        os.mkdir(self.tmp)
        os.mkdir(f'{self.tmp}/runs')

        self.round4_runs = {
            'https://raw.githubusercontent.com/castorini/anserini-tools/master/topics-and-qrels/qrels.covid-round4-cumulative.txt':
                '7a5c27e8e052c49ff72d557051825973',
        }

        download_url('https://ir.nist.gov/covidSubmit/archive/round4/covidex.r4.d2q.duot5.gz',
                     f'{self.tmp}/runs')

        with gzip.open(f'{self.tmp}/runs/covidex.r4.d2q.duot5.gz', 'rb') as f_in:
            with open(f'{self.tmp}/runs/covidex.r4.d2q.duot5', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        for url in self.round4_runs:
            print(f'Verifying stored run at {url}...')
            filename = url.split('/')[-1]
            filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter

            download_url(url, self.tmp, md5=self.round4_runs[url], force=True)
            self.assertTrue(os.path.exists(os.path.join(self.tmp, filename)))
            print('')

    def test_bm25(self):
        tmp_folder_name = self.tmp.split('/')[-1]
        prebuilt_index_path = download_prebuilt_index('trec-covid-r4-abstract')
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/rank_trec_covid.py \
                    -alpha 0.6 \
                    -clf lr \
                    -vectorizer tfidf \
                    -new_qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round4.txt \
                    -base {self.tmp}/runs/covidex.r4.d2q.duot5 \
                    -tmp_base {tmp_folder_name} \
                    -qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round3-cumulative.txt \
                    -index {prebuilt_index_path} \
                    -tag covidex.r4.d2q.duot5.lr \
                    -output {self.tmp}/output.json')
        with open(f'{self.tmp}/output.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.3846", data['map'])
            self.assertEqual("0.7745", data['ndcg'])

    def tearDown(self):
        shutil.rmtree(self.tmp)


if __name__ == '__main__':
    unittest.main()
