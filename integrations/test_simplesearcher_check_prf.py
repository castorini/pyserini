#
# Pyserini: python interface to the Anserini IR toolkit built on Lucene
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
import tarfile
import unittest

from random import randint
from integrations.utils import run_command, parse_score
from integrations.simplesearcher_score_checker import SimpleSearcherScoreChecker


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('integrations'):
            self.pyserini_root = '..'
            self.anserini_root = '../../anserini'
        else:
            self.pyserini_root = '.'
            self.anserini_root = '../anserini'

        self.tmp = f'{self.pyserini_root}/integrations/tmp{randint(0, 10000)}'

        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)
        else:
            os.mkdir(self.tmp)

        self.core17_checker = SimpleSearcherScoreChecker(
            index=os.path.join(self.anserini_root, 'indexes/lucene-index.core17.pos+docvectors+raw'),
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.core17.txt'),
            pyserini_topics='core17',
            qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.core17.txt'),
            eval=f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30')

        try:
            if os.path.exists(f'{self.tmp}/core17') == False:
                tar = tarfile.open(f"{self.pyserini_root}/integrations/core17.tar.gz", "r:gz")
                tar.extractall(path=f'{self.tmp}')
                tar.close()
        except:
            shutil.rmtree(f'{self.tmp}')
            print(f'core17.tar.gz is not saved in {self.pyserini_root}/integrations')
            raise

        self.core18_checker = SimpleSearcherScoreChecker(
                index=os.path.join(self.anserini_root, 'indexes/lucene-index.core18.pos+docvectors+raw'),
                topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.core18.txt'),
                pyserini_topics='core18',
                qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.core18.txt'),
                eval=f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30')

        try:
            if os.path.exists(f'{self.tmp}/core18') == False:
                tar = tarfile.open(f"{self.pyserini_root}/integrations/core18.tar.gz", "r:gz")
                tar.extractall(path=f'{self.tmp}')
                tar.close()
        except:
            shutil.rmtree(f'{self.tmp}')
            print(f'core18.tar.gz is not saved in {self.pyserini_root}/integrations')
            raise

        self.robust04_checker = SimpleSearcherScoreChecker(
            index=os.path.join(self.anserini_root, 'indexes/lucene-index.robust04.pos+docvectors+raw'),
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.robust04.txt'),
            pyserini_topics='robust04',
            qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.robust04.txt'),
            eval=f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30')

        try:
            if os.path.exists(f'{self.tmp}/robust04') == False:
                tar = tarfile.open(f"{self.pyserini_root}/integrations/robust04.tar.gz", "r:gz")
                tar.extractall(path=f'{self.tmp}')
                tar.close()
        except:
            shutil.rmtree(f'{self.tmp}')
            print(f'robust04.tar.gz is not saved in {self.pyserini_root}/integrations')
            raise

        self.robust05_checker = SimpleSearcherScoreChecker(
            index=os.path.join(self.anserini_root, 'indexes/lucene-index.robust05.pos+docvectors+raw'),
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.robust05.txt'),
            pyserini_topics='robust05',
            qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.robust05.txt'),
            eval=f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30')

        try:
            if os.path.exists(f'{self.tmp}/robust05') == False:
                tar = tarfile.open(f"{self.pyserini_root}/integrations/robust05.tar.gz", "r:gz")
                tar.extractall(path=f'{self.tmp}')
                tar.close()
        except:
            shutil.rmtree(f'{self.tmp}')
            print(f'robust05.tar.gz is not saved in {self.pyserini_root}/integrations')
            raise

    def test_core17(self):
        self.assertTrue(self.core17_checker.run('core17_bm25', '--bm25', 0.2087))

    def test_core17_rm3(self):
        self.assertTrue(self.core17_checker.run('core17_bm25', '--bm25 --rm3', 0.2823))

    def test_core17_lr(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_lr.txt --classifier lr ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt {self.tmp}/core17_lr.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2462, delta=0.0001)

    def test_core17_lr_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_lr_rm3.txt --classifier lr -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_lr_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2906, delta=0.0001)

    def test_core17_svm(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_svm.txt --classifier svm')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2367, delta=0.0001)

    def test_core17_svm_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_svm_rm3.txt --classifier svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2940, delta=0.0001)

    def test_core17_avg(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_lr+svm.txt --classifier lr+svm ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_lr+svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2426, delta=0.0001)

    def test_core17_avg_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_lr+svm_rm3.txt --classifier lr+svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_lr+svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2952, delta=0.0001)

    def test_core17_rrf(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_rrf.txt --classifier rrf')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_rrf.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2433, delta=0.0001)

    def test_core17_rrf_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core17 --output {self.tmp}/core17_rrf_rm3.txt --classifier rrf -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core17.txt \
                {self.tmp}/core17_rrf_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, "map")

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2951, delta=0.0001)

    def test_core18(self):
        self.assertTrue(self.core18_checker.run('core18_bm25', '--bm25', 0.2495))

    def test_core18_rm3(self):
        self.assertTrue(self.core18_checker.run('core18_bm25', '--bm25 --rm3', 0.3135))

    def test_core18_lr(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_lr.txt --classifier lr')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_lr.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2837, delta=0.0001)

    def test_core18_lr_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_lr_rm3.txt --classifier lr -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_lr_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3195, delta=0.0001)

    def test_core18_svm(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_svm.txt --classifier svm ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2786, delta=0.0001)

    def test_core18_svm_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_svm_rm3.txt --classifier svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3220, delta=0.0001)

    def test_core18_avg(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_lr+svm.txt --classifier lr+svm')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_lr+svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2821, delta=0.0001)

    def test_core18_avg_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_lr+svm_rm3.txt --classifier lr+svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_lr+svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3200, delta=0.0001)

    def test_core18_rrf(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_rrf.txt --classifier rrf')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_rrf.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2871, delta=0.0001)

    def test_core18_rrf_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection core18 --output {self.tmp}/core18_rrf_rm3.txt --classifier rrf -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                {self.tmp}/core18_rrf_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.3204, delta=0.0001)

    def test_robust04(self):
        self.assertTrue(self.robust04_checker.run('robust04_bm25', '--bm25', 0.2531))

    def test_robust04_rm3(self):
        self.assertTrue(self.robust04_checker.run('robust04_bm25_rm3', '--bm25 --rm3', 0.2903))

    def test_robust04_lr(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_lr.txt --classifier lr ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                {self.tmp}/robust04_lr.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2721, delta=0.0001)

    def test_robust04_lr_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_lr_rm3.txt --classifier lr -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                {self.tmp}/robust04_lr_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2961, delta=0.0001)

    def test_robust04_svm(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_svm.txt --classifier svm ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                {self.tmp}/robust04_svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2716, delta=0.0001)

    def test_robust04_svm_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_svm_rm3.txt --classifier svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                {self.tmp}/robust04_svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2963, delta=0.0001)

    def test_robust04_avg(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_lr+svm.txt --classifier lr+svm')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                {self.tmp}/robust04_lr+svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2745, delta=0.0001)

    def test_robust04_avg_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_lr+svm_rm3.txt --classifier lr+svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                 {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                 {self.tmp}/robust04_lr+svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2980, delta=0.0001)

    def test_robust04_rrf(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_rrf.txt --classifier rrf')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                {self.tmp}/robust04_rrf.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2740, delta=0.0001)

    def test_robust04_rrf_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust04 --output {self.tmp}/robust04_rrf_rm3.txt --classifier rrf -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                 {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust04.txt \
                 {self.tmp}/robust04_rrf_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2975, delta=0.0001)

    def test_robust05(self):
        self.assertTrue(self.robust05_checker.run('robust05_bm25', '--bm25', 0.2032))

    def test_robust05_rm3(self):
        self.assertTrue(self.robust05_checker.run('robust05_bm25_rm3', '--bm25 --rm3', 0.2602))

    def test_robust05_lr(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_lr.txt --classifier lr ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_lr.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2476, delta=0.0001)

    def test_robust05_lr_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_lr_rm3.txt --classifier lr -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_lr_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2845, delta=0.0001)

    def test_robust05_svm(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_svm.txt --classifier svm ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2454, delta=0.0001)

    def test_robust05_svm_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_svm_rm3.txt --classifier svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2850, delta=0.0001)

    def test_robust05_avg(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_lr+svm.txt --classifier lr+svm ')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_lr+svm.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2485, delta=0.0001)

    def test_robust05_avg_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_lr+svm_rm3.txt --classifier lr+svm -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_lr+svm_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2860, delta=0.0001)

    def test_robust05_rrf(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_rrf.txt --classifier rrf')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_rrf.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2490, delta=0.0001)

    def test_robust05_rrf_rm3(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py \
                    --anserini {self.anserini_root} --run_file {self.tmp} --pyserini {self.pyserini_root} \
                    --collection robust05 --output {self.tmp}/robust05_rrf_rm3.txt --classifier rrf -rm3')

        cmd = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.robust05.txt \
                {self.tmp}/robust05_rrf_rm3.txt'

        status = os.system(cmd)
        stdout, stderr = run_command(cmd)
        score = parse_score(stdout, 'map')

        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2870, delta=0.0001)

    def tearDown(self):
        shutil.rmtree(f'{self.tmp}')


if __name__ == '__main__':
    unittest.main()