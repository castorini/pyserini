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
import shutil
import unittest
from random import randint

from integrations.lucenesearcher_score_checker import LuceneSearcherScoreChecker
from integrations.utils import run_command, parse_score


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('clprf'):
            self.pyserini_root = '../..'
            self.anserini_root = '../../../anserini'
        else:
            self.pyserini_root = '.'
            self.anserini_root = '../anserini'

        self.tmp = f'{self.pyserini_root}/integrations/tmp{randint(0, 10000)}'

        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)
        else:
            os.mkdir(self.tmp)

        self.pyserini_search_cmd = 'python -m pyserini.search.lucene'
        self.pyserini_fusion_cmd = 'python -m pyserini.fusion'
        self.pyserini_eval_cmd = 'python -m pyserini.eval.trec_eval'

        self.core17_index_path = os.path.join(self.anserini_root, 'indexes/lucene-index.nyt')
        self.core17_qrels_path = os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.core17.txt')

        self.core18_index_path = os.path.join(self.anserini_root, 'indexes/lucene-index.wapo.v2')
        self.core18_qrels_path = os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.core18.txt')

        self.robust04_index_path = os.path.join(self.anserini_root, 'indexes/lucene-index.disk45')
        self.robust04_qrels_path = os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.robust04.txt')

        self.robust05_index_path = os.path.join(self.anserini_root, 'indexes/lucene-index.robust05')
        self.robust05_qrels_path = os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.robust05.txt')

        self.core17_checker = LuceneSearcherScoreChecker(
            index=self.core17_index_path,
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.core17.txt'),
            pyserini_topics='core17',
            qrels=self.core17_qrels_path,
            eval=f'{self.pyserini_eval_cmd} -m map -m P.30')

        self.core18_checker = LuceneSearcherScoreChecker(
            index=self.core18_index_path,
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.core18.txt'),
            pyserini_topics='core18',
            qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.core18.txt'),
            eval=f'{self.pyserini_eval_cmd} -m map -m P.30')

        self.robust04_checker = LuceneSearcherScoreChecker(
            index=self.robust04_index_path,
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.robust04.txt'),
            pyserini_topics='robust04',
            qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.robust04.txt'),
            eval=f'{self.pyserini_eval_cmd} -m map -m P.30')

        self.robust05_checker = LuceneSearcherScoreChecker(
            index=self.robust05_index_path,
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.robust05.txt'),
            pyserini_topics='robust05',
            qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.robust05.txt'),
            eval=f'{self.pyserini_eval_cmd} -m map -m P.30')

    def test_cross_validation(self):
        pyserini_topics = 'core17'
        os.mkdir(f'{self.tmp}/core17')
        for alpha in [x / 10.0 for x in range(0, 11)]:
            run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                               --topics {pyserini_topics} --output {self.tmp}/core17/core17_lr_A{alpha}_bm25.txt \
                               --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha {alpha}'

            status = os.system(run_file_cmd)
            self.assertEqual(status, 0)
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                      --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                      --collection core17 --output {self.tmp}/core17_lr.txt --classifier lr ')

        cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_lr.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2462, delta=0.0001)

    def test_core17(self):
        self.assertTrue(self.core17_checker.run('core17_bm25', '--bm25', 0.2087))

    def test_core17_rm3(self):
        self.assertTrue(self.core17_checker.run('core17_bm25', '--bm25 --rm3', 0.2798))

    def test_core17_lr(self):
        pyserini_topics = 'core17'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core17_lr.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.7'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_lr.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2473, delta=0.0001)

    def test_core17_lr_rm3(self):
        pyserini_topics = 'core17'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core17_lr_rm3.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.4 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_lr_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2926, delta=0.0001)

    def test_core17_svm(self):
        pyserini_topics = 'core17'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core17_svm.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.7'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_svm.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2385, delta=0.0001)

    def test_core17_svm_rm3(self):
        pyserini_topics = 'core17'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core17_svm_rm3.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.4 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_svm_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2956, delta=0.0001)

    def test_core17_avg(self):
        pyserini_topics = 'core17'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core17_avg.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_avg.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2442, delta=0.0001)

    def test_core17_avg_rm3(self):
        pyserini_topics = 'core17'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core17_avg_rm3.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_avg_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2950, delta=0.0001)

    def test_core17_rrf(self):
        pyserini_topics = 'core17'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/core17_lr.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.7'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/core17_svm.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.7'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                      --runs {self.tmp}/core17_lr.txt {self.tmp}/core17_svm.txt \
                      --output {self.tmp}/core17_rrf.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_rrf.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2446, delta=0.0001)

    def test_core17_rrf_rm3(self):
        pyserini_topics = 'core17'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/core17_lr_rm3.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.4 --rm3'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.core17_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/core17_svm_rm3.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.4 --rm3'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                      --runs {self.tmp}/core17_lr_rm3.txt {self.tmp}/core17_svm_rm3.txt \
                      --output {self.tmp}/core17_rrf_rm3.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core17.txt \
                      {self.tmp}/core17_rrf_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2957, delta=0.0001)

    def test_core18(self):
        self.assertTrue(self.core18_checker.run('core18_bm25', '--bm25', 0.2496))

    def test_core18_rm3(self):
        self.assertTrue(self.core18_checker.run('core18_bm25', '--bm25 --rm3', 0.3129))

    def test_core18_lr(self):
        pyserini_topics = 'core18'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core18_lr.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_lr.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2839, delta=0.0001)

    def test_core18_lr_rm3(self):
        pyserini_topics = 'core18'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core18_lr_rm3.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_lr_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3216, delta=0.0001)

    def test_core18_svm(self):
        pyserini_topics = 'core18'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core18_svm.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_svm.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2841, delta=0.0001)

    def test_core18_svm_rm3(self):
        pyserini_topics = 'core18'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core18_svm_rm3.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_svm_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3200, delta=0.0001)

    def test_core18_avg(self):
        pyserini_topics = 'core18'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core18_avg.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.4'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_avg.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2860, delta=0.0001)

    def test_core18_avg_rm3(self):
        pyserini_topics = 'core18'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/core18_avg_rm3.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.4 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_avg_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3215, delta=0.0001)

    def test_core18_rrf(self):
        pyserini_topics = 'core18'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/core18_lr.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/core18_svm.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                     --runs {self.tmp}/core18_lr.txt {self.tmp}/core18_svm.txt \
                     --output {self.tmp}/core18_rrf.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_rrf.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2881, delta=0.0001)

    def test_core18_rrf_rm3(self):
        pyserini_topics = 'core18'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/core18_lr_rm3.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5 --rm3'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.core18_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/core18_svm_rm3.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5 --rm3'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                      --runs {self.tmp}/core18_lr_rm3.txt {self.tmp}/core18_svm_rm3.txt \
                      --output {self.tmp}/core18_rrf_rm3.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.core18.txt \
                      {self.tmp}/core18_rrf_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3205, delta=0.0001)

    def test_robust04(self):
        self.assertTrue(self.robust04_checker.run('robust04_bm25', '--bm25', 0.2531))

    def test_robust04_rm3(self):
        self.assertTrue(self.robust04_checker.run('robust04_bm25_rm3', '--bm25 --rm3', 0.2908))

    def test_robust04_lr(self):
        pyserini_topics = 'robust04'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust04_lr.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_lr.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2747, delta=0.0001)

    def test_robust04_lr_rm3(self):
        pyserini_topics = 'robust04'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust04_lr_rm3.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.3 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_lr_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2969, delta=0.0001)

    def test_robust04_svm(self):
        pyserini_topics = 'robust04'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust04_svm.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_svm.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2726, delta=0.0001)

    def test_robust04_svm_rm3(self):
        pyserini_topics = 'robust04'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust04_svm_rm3.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.3 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_svm_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2972, delta=0.0001)

    def test_robust04_avg(self):
        pyserini_topics = 'robust04'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust04_avg.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_avg.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.276, delta=0.0001)

    def test_robust04_avg_rm3(self):
        pyserini_topics = 'robust04'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust04_avg_rm3.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.3 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_avg_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2980, delta=0.0001)

    def test_robust04_rrf(self):
        pyserini_topics = 'robust04'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/robust04_lr.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/robust04_svm.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                      --runs {self.tmp}/robust04_lr.txt {self.tmp}/robust04_svm.txt \
                      --output {self.tmp}/robust04_rrf.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_rrf.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.275, delta=0.0001)

    def test_robust04_rrf_rm3(self):
        pyserini_topics = 'robust04'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/robust04_lr_rm3.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.3 --rm3'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.robust04_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/robust04_svm_rm3.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.3 --rm3'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                      --runs {self.tmp}/robust04_lr_rm3.txt {self.tmp}/robust04_svm_rm3.txt \
                      --output {self.tmp}/robust04_rrf_rm3.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust04.txt \
                      {self.tmp}/robust04_rrf_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2977, delta=0.0001)

    def test_robust05(self):
        self.assertTrue(self.robust05_checker.run('robust05_bm25', '--bm25', 0.2032))

    def test_robust05_rm3(self):
        self.assertTrue(self.robust05_checker.run('robust05_bm25_rm3', '--bm25 --rm3', 0.2624))

    def test_robust05_lr(self):
        pyserini_topics = 'robust05'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust05_lr.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.8'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_lr.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2476, delta=0.0001)

    def test_robust05_lr_rm3(self):
        pyserini_topics = 'robust05'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust05_lr_rm3.txt \
                           --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_lr_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2872, delta=0.0001)

    def test_robust05_svm(self):
        pyserini_topics = 'robust05'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust05_svm.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.8'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_svm.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2486, delta=0.0001)

    def test_robust05_svm_rm3(self):
        pyserini_topics = 'robust05'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust05_svm_rm3.txt \
                           --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_svm_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2871, delta=0.0001)

    def test_robust05_avg(self):
        pyserini_topics = 'robust05'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust05_avg.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.8'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_avg.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2485, delta=0.0001)

    def test_robust05_avg_rm3(self):
        pyserini_topics = 'robust05'

        run_file_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                           --topics {pyserini_topics} --output {self.tmp}/robust05_avg_rm3.txt \
                           --prcl lr svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.6 --rm3'

        status = os.system(run_file_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_avg_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2880, delta=0.0001)

    def test_robust05_rrf(self):
        pyserini_topics = 'robust05'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/robust05_lr.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/robust05_svm.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.5'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                      --runs {self.tmp}/robust05_lr.txt {self.tmp}/robust05_svm.txt \
                      --output {self.tmp}/robust05_rrf.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_rrf.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2401, delta=0.0001)

    def test_robust05_rrf_rm3(self):
        pyserini_topics = 'robust05'
        lr_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                     --topics {pyserini_topics} --output {self.tmp}/robust05_lr_rm3.txt \
                     --prcl lr --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.3 --rm3'

        status = os.system(lr_cmd)
        self.assertEqual(status, 0)

        svm_cmd = f'{self.pyserini_search_cmd} --index {self.robust05_index_path} \
                      --topics {pyserini_topics} --output {self.tmp}/robust05_svm_rm3.txt \
                      --prcl svm --prcl.vectorizer TfidfVectorizer --prcl.alpha 0.3 --rm3'

        status = os.system(svm_cmd)
        self.assertEqual(status, 0)

        rrf_cmd = f'{self.pyserini_fusion_cmd} \
                      --runs {self.tmp}/robust05_lr_rm3.txt {self.tmp}/robust05_svm_rm3.txt \
                      --output {self.tmp}/robust05_rrf_rm3.txt --resort'

        status = os.system(rrf_cmd)
        self.assertEqual(status, 0)

        score_cmd = f'{self.pyserini_eval_cmd} -m map -m P.30 \
                      {self.anserini_root}/tools/topics-and-qrels/qrels.robust05.txt \
                      {self.tmp}/robust05_rrf_rm3.txt'

        status = os.system(score_cmd)
        stdout, stderr = run_command(score_cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2808, delta=0.0001)

    def tearDown(self):
        shutil.rmtree(f'{self.tmp}')


if __name__ == '__main__':
    unittest.main()
