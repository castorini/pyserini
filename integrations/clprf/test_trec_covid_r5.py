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
import json
import gzip
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
        
        self.round5_runs = {
            'https://ir.nist.gov/covidSubmit/archive/round5/covidex.r5.d2q.1s.gz':
                '2181ae5b7fe8bafbd3b41700f3ccde02',
            'https://ir.nist.gov/covidSubmit/archive/round5/covidex.r5.d2q.2s.gz':
                'e61f9b6de5ffbe1b5b82d35216968154',
             'https://ir.nist.gov/covidSubmit/archive/round5/covidex.r5.2s.gz':
                '6e517a5e044d8b7ce983f7e165cf4aeb',
             'https://ir.nist.gov/covidSubmit/archive/round5/covidex.r5.1s.gz':
                'dc9b4b45494294a8448cf0693f07f7fd'
        }
                
        for url in self.round5_runs:
            print(f'Verifying stored run at {url}...')
            filename = url.split('/')[-1]
            filename = re.sub('\\?dl=1$', '', filename)  # Remove the Dropbox 'force download' parameter
            gzip_filename  = (".").join(filename.split('.')[:-1])

            download_url(url, f'{self.tmp}/runs/', md5=self.round5_runs[url], force=True)
            self.assertTrue(os.path.exists(os.path.join(f'{self.tmp}/runs/', filename)))
            with gzip.open(f'{self.tmp}/runs/{filename}', 'rb') as f_in:
            	with open(f'{self.tmp}/runs/{gzip_filename}', 'wb') as f_out:
                	shutil.copyfileobj(f_in, f_out)

    def test_round5(self):
        tmp_folder_name = self.tmp.split('/')[-1]
        prebuilt_index_path = download_prebuilt_index('trec-covid-r5-abstract')
        
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/rank_trec_covid.py \
                    -alpha 0.6 \
                    -clf lr \
                    -vectorizer tfidf \
                    -new_qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round5.txt \
                    -base {self.tmp}/runs/covidex.r5.d2q.1s \
                    -tmp_base {tmp_folder_name} \
                    -qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round4-cumulative.txt \
                    -index {prebuilt_index_path} \
                    -tag covidex.r5.d2q.1s \
                    -output {self.tmp}/output.json')
        with open(f'{self.tmp}/output.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.3859", data['map'])
            self.assertEqual("0.8221", data['ndcg'])
        
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/rank_trec_covid.py \
                    -alpha 0.6 \
                    -clf lr \
                    -vectorizer tfidf \
                    -new_qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round5.txt \
                    -base {self.tmp}/runs/covidex.r5.d2q.2s \
                    -tmp_base {tmp_folder_name} \
                    -qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round4-cumulative.txt \
                    -index {prebuilt_index_path} \
                    -tag covidex.r5.d2q.2s \
                    -output {self.tmp}/output.json')
        with open(f'{self.tmp}/output.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.3875", data['map'])
            self.assertEqual("0.8304", data['ndcg'])
        
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/rank_trec_covid.py \
                    -alpha 0.6 \
                    -clf lr \
                    -vectorizer tfidf \
                    -new_qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round5.txt \
                    -base {self.tmp}/runs/covidex.r5.1s \
                    -tmp_base {tmp_folder_name} \
                    -qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round4-cumulative.txt \
                    -index {prebuilt_index_path} \
                    -tag covidex.r5.1s \
                    -output {self.tmp}/output.json')
        with open(f'{self.tmp}/output.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.3885", data['map'])
            self.assertEqual("0.8135", data['ndcg'])
        
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/rank_trec_covid.py \
                    -alpha 0.6 \
                    -clf lr \
                    -vectorizer tfidf \
                    -new_qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round5.txt \
                    -base {self.tmp}/runs/covidex.r5.2s \
                    -tmp_base {tmp_folder_name} \
                    -qrels {self.pyserini_root}/tools/topics-and-qrels/qrels.covid-round4-cumulative.txt \
                    -index {prebuilt_index_path} \
                    -tag covidex.r5.2s \
                    -output {self.tmp}/output.json')
        with open(f'{self.tmp}/output.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.3922", data['map'])
            self.assertEqual("0.8311", data['ndcg'])
            
    def tearDown(self):
        shutil.rmtree(self.tmp)


if __name__ == '__main__':
    unittest.main()
