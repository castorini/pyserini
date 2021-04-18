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

import gzip
import os
import json
import shutil
import unittest
from random import randint
import tarfile
from pyserini.util import download_url
from integrations.utils import run_command, parse_score
from integrations.simplesearcher_checker import SimpleSearcherChecker


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

        self.checker = SimpleSearcherChecker(
            anserini_root=self.anserini_root,
            index=os.path.join(self.anserini_root, 'indexes/lucene-index.core18.pos+docvectors+raw'),
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.core18.txt'),
            pyserini_topics='core18',
            qrels=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.core18.txt'))

        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)
        else:
            os.mkdir(self.tmp)

        download_url('https://www.dropbox.com/s/6b81d5na2iuyvnc/core18.tar.gz?dl=1', f'{self.pyserini_root}/integrations')

        if os.path.exists(f'{self.tmp}/core18') == False:
            tar = tarfile.open(f"{self.pyserini_root}/integrations/core18.tar.gz", "r:gz")
            tar.extractall(path=f'{self.tmp}')
            tar.close()

    def test_core18(self):
        cmd1 = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                               {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                               {self.anserini_root}/runs/run.core18.bm25.topics.core18.txt'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd1)
        score = parse_score(stdout, "map")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2495, delta=0.0001)

    def test_core18_lr(self):
        os.system(f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py --anserini {self.anserini_root} \
                     --run_file {self.tmp} --pyserini {self.pyserini_root} \
                     --collection core18 --output {self.tmp}/core18_lr.txt --classifier lr ')

        cmd1 = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                       {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                       {self.tmp}/core18_lr.txt'
        status = os.system(cmd1)
        stdout, stderr = run_command(cmd1)
        score = parse_score(stdout, "map")
        self.assertEqual(status, 0)
        self.assertEqual(stderr, '')
        self.assertAlmostEqual(score, 0.2837, delta=0.0001)

    def test_core18_svm(self):
            os.system(
                f'python {self.pyserini_root}/scripts/classifier_prf/cross_validate.py --anserini {self.anserini_root} \
                      --run_file {self.tmp} --pyserini {self.pyserini_root} \
                      --collection core18 --output {self.tmp}/core18_svm.txt --classifier svm ')

            cmd1 = f'{self.anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30 \
                        {self.anserini_root}/src/main/resources/topics-and-qrels/qrels.core18.txt \
                        {self.tmp}/core18_svm.txt'
            status = os.system(cmd1)
            stdout, stderr = run_command(cmd1)
            score = parse_score(stdout, "map")
            os.remove(f'{self.pyserini_root}/integrations/core18.tar.gz')
            self.assertEqual(status, 0)
            self.assertEqual(stderr, '')
            self.assertAlmostEqual(score, 0.2786, delta=0.0001)

    def tearDown(self):
        shutil.rmtree(f'{self.tmp}')



if __name__ == '__main__':
    unittest.main()