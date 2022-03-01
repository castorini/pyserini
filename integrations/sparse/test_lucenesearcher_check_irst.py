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
import unittest
from shutil import rmtree

from integrations.utils import run_command, parse_score


class TestMsmarcoPassageIrst(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('sparse'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'
        if(os.path.isdir('irst_test')):
            rmtree('irst_test')
            os.mkdir('irst_test')
        # ibm model
        ibm_model_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz'
        ibm_model_tar_name = 'ibm_model_1_bert_tok_20211117.tar.gz'
        os.system(f'wget {ibm_model_url} -P irst_test/')
        os.system(f'tar -xzvf irst_test/{ibm_model_tar_name} -C irst_test')
        # queries process
        os.system('python scripts/ltr_msmarco/convert_queries.py \
            --input tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt \
            --output irst_test/queries.dev.small.json')
        # qrel
        self.qrels_path = f'{self.pyserini_root}/tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt'

    def test_sum_aggregation(self):
        os.system('python -m pyserini.search.lucene.irst \
            --qrels tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
            --tran_path irst_test/ibm_model_1_bert_tok_20211117/ \
            --query_path irst_test/queries.dev.small.json \
            --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3/ \
            --output irst_test/regression_test_sum.txt \
            --alpha 0.1 ')

        score_cmd = f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval \
                -c -M1000 -m map -m ndcg_cut.20 {self.qrels_path} irst_test/regression_test_sum.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2294)
        self.assertEqual(ndcg_score, 0.2997)

    def test_max_aggregation(self):
        os.system('python -m pyserini.search.lucene.irst \
            --qrels tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
            --tran_path irst_test/ibm_model_1_bert_tok_20211117/ \
            --query_path irst_test/queries.dev.small.json \
            --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3/ \
            --output irst_test/regression_test_max.txt \
            --alpha 0.3 \
            --max_sim')

        score_cmd = f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval \
                -c -M1000 -m map -m ndcg_cut.20 {self.qrels_path} irst_test/regression_test_max.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2234)
        self.assertEqual(ndcg_score, 0.2907)

    def tearDown(self):
        rmtree('irst_test/')


if __name__ == '__main__':
    unittest.main()
