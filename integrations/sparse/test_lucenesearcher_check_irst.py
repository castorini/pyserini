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
        #wp term stat
        wp_term_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-passage.20220411.pickle'
        os.system(f'wget {wp_term_url} -P irst_test/')
        self.dl19_pass = 'tools/topics-and-qrels/topics.dl19-passage.txt'
        self.dl20 = 'tools/topics-and-qrels/topics.dl20.txt'
    
    def test_sum_aggregation_dl19_passage(self):
        #dl19 passage
        topic = 'dl19-passage'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_pass} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-passage \
            --output irst_test/regression_test_sum.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-passage.20220411.pickle \
            --alpha 0.1 ')

        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} irst_test/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3281)
        self.assertEqual(ndcg_score, 0.5260)

    def test_sum_aggregation_dl20_passage(self):
        #dl20 passage
        topic = 'dl20-passage'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-passage \
            --output irst_test/regression_test_sum.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-passage.20220411.pickle \
            --alpha 0.1 ')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} irst_test/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3520)
        self.assertEqual(ndcg_score, 0.5578)
    
    def test_max_aggregation_dl19(self):
        #dl19 passage
        topic = 'dl19-passage'
        
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_pass} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-passage \
            --output irst_test/regression_test_max.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-passage.20220411.pickle \
            --alpha 0.3 \
            --max-sim ')
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} irst_test/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3286)
        self.assertEqual(ndcg_score, 0.5371)
        

    def test_max_aggregation_dl20_passage(self):
        #dl20 passage
        topic = 'dl20-passage'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-passage \
            --output irst_test/regression_test_max.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-passage.20220411.pickle \
            --alpha 0.3 \
            --max-sim')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} irst_test/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3357)
        self.assertEqual(ndcg_score, 0.5469)

    def tearDown(self):
        rmtree('irst_test/')


class TestMsmarcoDocumentIrst(unittest.TestCase):
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
        #wp term stat
        wp_term_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-doc.20220411.pickle'
        os.system(f'wget {wp_term_url} -P irst_test/')
        self.dl19_doc = 'tools/topics-and-qrels/topics.dl19-doc.txt'
        self.dl20 = 'tools/topics-and-qrels/topics.dl20.txt'

    def test_sum_aggregation_dl19_doc(self):
        #dl19
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc \
            --output irst_test/regression_test_sum.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc.20220411.pickle \
            --alpha 0.3')

        score_cmd = f'python -m pyserini.eval.trec_eval \
               -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2524)
        self.assertEqual(ndcg_score, 0.5494)

    def test_sum_aggregation_dl20_doc(self):
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc \
            --output irst_test/regression_test_sum.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc.20220411.pickle \
            --alpha 0.3 ')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3825)
        self.assertEqual(ndcg_score, 0.5559)

    def test_max_aggregation_dl19_doc(self):
        #dl19
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc \
            --output irst_test/regression_test_max.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc.20220411.pickle \
            --alpha 0.3 \
            --max-sim')

        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2204)
        self.assertEqual(ndcg_score, 0.4912)

    def test_max_aggregation_dl20_doc(self):
        #dl20
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc \
            --output irst_test/regression_test_max.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc.20220411.pickle \
            --alpha 0.3 \
            --max-sim')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3373)
        self.assertEqual(ndcg_score, 0.5015)

    def tearDown(self):
        rmtree('irst_test/')


class TestMsmarcoDocumentSegIrst(unittest.TestCase):
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
        #wp term stat
        wp_term_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle'
        os.system(f'wget {wp_term_url} -P irst_test/')
        self.dl19_doc = 'tools/topics-and-qrels/topics.dl19-doc.txt'
        self.dl20 = 'tools/topics-and-qrels/topics.dl20.txt'

    def test_sum_aggregation_dl19_doc_seg(self):
        #dl19
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc-segmented \
            --output irst_test/regression_test_sum.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle \
            --hits 10000 --segments \
            --alpha 0.3')

        score_cmd = f'python -m pyserini.eval.trec_eval \
               -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2711)
        self.assertEqual(ndcg_score, 0.5596)

    def test_sum_aggregation_dl20_doc_seg(self):
        #dl20
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc-segmented \
            --output irst_test/regression_test_sum.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle \
            --hits 10000 --segments \
            --alpha 0.3 ')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3759)
        self.assertEqual(ndcg_score, 0.5343)

    def test_max_aggregation_dl19_doc_seg(self):
        #dl19
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc-segmented \
            --output irst_test/regression_test_max.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle \
            --alpha 0.3 \
            --hits 10000 --segments \
            --max-sim')

        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2425)
        self.assertEqual(ndcg_score, 0.5195)

    def test_max_aggregation_dl20_doc_seg(self):
        #dl20
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --translation-model irst_test/ibm_model_1_bert_tok_20211117/ \
            --index msmarco-v1-doc-segmented \
            --output irst_test/regression_test_max.{topic}.txt \
            --wp-stat irst_test/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle \
            --alpha 0.3 \
            --hits 10000 --segments \
            --max-sim')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} irst_test/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3496)
        self.assertEqual(ndcg_score, 0.5089)

    def tearDown(self):
        rmtree('irst_test/')



if __name__ == '__main__':
    unittest.main()
