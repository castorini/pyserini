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

import json
import os
from shutil import rmtree
import unittest


class TestLtrMsmarcoPassageIbm(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('sparse'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'

        if(os.path.isdir('ibm_test')):
            rmtree('ibm_test')
            os.mkdir('ibm_test')
        # ibm model
        ibm_model_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz'
        ibm_model_tar_name = 'ibm_model_1_bert_tok_20211117.tar.gz'
        os.system(f'wget {ibm_model_url} -P ibm_test/')
        os.system(f'tar -xzvf ibm_test/{ibm_model_tar_name} -C ibm_test')
        # queries process
        os.system('python scripts/ltr_msmarco/convert_queries.py --input tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt --output ibm_test/queries.dev.small.json')

    def test_ibm_reranking(self):
        os.system('python -m pyserini.search.lucene.tprob --qrels tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt --tran_path ibm_test/ibm_model_1_bert_tok_20211117/ --query_path ibm_test/queries.dev.small.json --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3/ --output ibm_test/regression_test_ibm.txt --score_path ibm_test/regression_test_ibm.json --alpha 0.1 ')
        with open('ibm_test/regression_test_ibm.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.2294", data['map'])
            self.assertEqual("0.2997", data['ndcg'])

    def test_colbert_reranking(self):
        os.system('python -m pyserini.search.lucene.tprob --qrels tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt --tran_path ibm_test/ibm_model_1_bert_tok_20211117/ --query_path ibm_test/queries.dev.small.json --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3/ --output ibm_test/regression_test_colbert.txt --score_path ibm_test/regression_test_colbert.json --alpha 0.3 --max_sim')

        with open('ibm_test/regression_test_colbert.json') as json_file:
            data = json.load(json_file)
            self.assertEqual("0.2234", data['map'])
            self.assertEqual("0.2907", data['ndcg'])

    def tearDown(self):
        rmtree('ibm_test/')


if __name__ == '__main__':
    unittest.main()
