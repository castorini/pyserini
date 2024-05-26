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
from random import randint

from integrations.utils import run_command, parse_score


class TestMsmarcoPassageIrst(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('sparse'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'
        self.tmp = f'tmp{randint(0, 10000)}'
        if os.path.isdir(self.tmp):
            rmtree(self.tmp)
        os.mkdir(self.tmp)
        self.dl19_pass = 'dl19-passage'
        self.dl20 = 'dl20'
    
    def test_sum_aggregation_dl19_passage(self):
        # dl19 passage sum
        topic = 'dl19-passage'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_pass} \
            --index msmarco-v1-passage \
            --output {self.tmp}/regression_test_sum.{topic}.txt \
            --alpha 0.1 ')

        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} {self.tmp}/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3281)
        self.assertEqual(ndcg_score, 0.5260)

    def test_sum_aggregation_dl20_passage(self):
        # dl20 passage sum
        topic = 'dl20-passage'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --index msmarco-v1-passage \
            --output {self.tmp}/regression_test_sum.{topic}.txt \
            --alpha 0.1 ')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} {self.tmp}/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3520)
        self.assertEqual(ndcg_score, 0.5578)
    
    def test_max_aggregation_dl19(self):
        # dl19 passage max
        topic = 'dl19-passage'
        
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_pass} \
            --index msmarco-v1-passage \
            --output {self.tmp}/regression_test_max.{topic}.txt \
            --alpha 0.3 \
            --max-sim ')
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} {self.tmp}/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3286)
        self.assertEqual(ndcg_score, 0.5371)

    def test_max_aggregation_dl20_passage(self):
        # dl20 passage max
        topic = 'dl20-passage'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --index msmarco-v1-passage \
            --output {self.tmp}/regression_test_max.{topic}.txt \
            --alpha 0.3 \
            --max-sim')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -l 2 {topic} {self.tmp}/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3357)
        self.assertEqual(ndcg_score, 0.5469)

    def tearDown(self):
        rmtree(self.tmp)


class TestMsmarcoDocumentIrst(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('sparse'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'
        self.tmp = f'tmp{randint(0, 10000)}'
        if os.path.isdir(self.tmp):
            rmtree(self.tmp)
        os.mkdir(self.tmp)
        self.dl19_doc = 'dl19-doc'
        self.dl20 = 'dl20'

    def test_sum_aggregation_dl19_doc(self):
        # dl19-doc-sum
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --index msmarco-v1-doc \
            --output {self.tmp}/regression_test_sum.{topic}.txt \
            --alpha 0.3')

        score_cmd = f'python -m pyserini.eval.trec_eval \
               -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2524)
        self.assertEqual(ndcg_score, 0.5494)

    def test_sum_aggregation_dl20_doc(self):
        # dl20-doc-sum
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --index msmarco-v1-doc \
            --output {self.tmp}/regression_test_sum.{topic}.txt \
            --alpha 0.3 ')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3825)
        self.assertEqual(ndcg_score, 0.5559)

    def test_max_aggregation_dl19_doc(self):
        # dl19-doc-max
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --index msmarco-v1-doc \
            --output {self.tmp}/regression_test_max.{topic}.txt \
            --alpha 0.3 \
            --max-sim')

        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2205)
        self.assertEqual(ndcg_score, 0.4917)

    def test_max_aggregation_dl20_doc(self):
        # dl20-doc-max
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --index msmarco-v1-doc \
            --output {self.tmp}/regression_test_max.{topic}.txt \
            --alpha 0.3 \
            --max-sim')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3373)
        self.assertEqual(ndcg_score, 0.5015)

    def tearDown(self):
        rmtree(self.tmp)


class TestMsmarcoDocumentSegIrst(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('sparse'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'
        self.tmp = f'tmp{randint(0, 10000)}'
        if os.path.isdir(self.tmp):
            rmtree(self.tmp)
        os.mkdir(self.tmp)
        self.dl19_doc = 'dl19-doc'
        self.dl20 = 'dl20'

    def test_sum_aggregation_dl19_doc_seg(self):
        # dl19-doc-seg-sum
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --index msmarco-v1-doc-segmented \
            --output {self.tmp}/regression_test_sum.{topic}.txt \
            --hits 10000 --segments \
            --alpha 0.3')

        score_cmd = f'python -m pyserini.eval.trec_eval \
               -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2711)
        self.assertEqual(ndcg_score, 0.5596)

    def test_sum_aggregation_dl20_doc_seg(self):
        # dl20-doc-seg-sum
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --index msmarco-v1-doc-segmented \
            --output {self.tmp}/regression_test_sum.{topic}.txt \
            --hits 10000 --segments \
            --alpha 0.3 ')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_sum.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3759)
        self.assertEqual(ndcg_score, 0.5343)

    def test_max_aggregation_dl19_doc_seg(self):
        # dl19-doc-seg-max
        topic = 'dl19-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl19_doc} \
            --index msmarco-v1-doc-segmented \
            --output {self.tmp}/regression_test_max.{topic}.txt \
            --alpha 0.3 \
            --hits 10000 --segments \
            --max-sim')

        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.2425)
        self.assertEqual(ndcg_score, 0.5193)

    def test_max_aggregation_dl20_doc_seg(self):
        # dl20-doc-seg-max
        topic = 'dl20-doc'
        os.system(f'python -m pyserini.search.lucene.irst \
            --topics {self.dl20} \
            --index msmarco-v1-doc-segmented \
            --output {self.tmp}/regression_test_max.{topic}.txt \
            --alpha 0.3 \
            --hits 10000 --segments \
            --max-sim')
        
        score_cmd = f'python -m pyserini.eval.trec_eval \
                -c -m map -m ndcg_cut.10 -M 100 {topic} {self.tmp}/regression_test_max.{topic}.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        map_score = parse_score(stdout, "map")
        ndcg_score = parse_score(stdout, "ndcg")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertEqual(map_score, 0.3496)
        self.assertEqual(ndcg_score, 0.5089)

    def tearDown(self):
        rmtree(self.tmp)


if __name__ == '__main__':
    unittest.main()
