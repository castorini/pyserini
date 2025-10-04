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

from integrations.utils import run_command, parse_score
from pyserini.util import download_url


class TestTrecEvalComputeJudged(unittest.TestCase):
    def test_trec_eval_compute_judged(self):
        # Data from https://github.com/castorini/anserini/blob/master/docs/experiments-covid.md
        runs = {
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.abstract.qq.bm25.txt': {
                'checksum': 'b1ccc364cc9dab03b383b71a51d3c6cb',
                'ndcg_cut_10': 0.4580,
                'judged_10': 0.5880,
                'recall_1000': 0.4525,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.abstract.qdel.bm25.txt': {
                'checksum': 'ee4e3e6cf87dba2fd021fbb89bd07a89',
                'ndcg_cut_10': 0.4912,
                'judged_10': 0.6240,
                'recall_1000': 0.4714,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.full-text.qq.bm25.txt': {
                'checksum': 'd7457dd746533326f2bf8e85834ecf5c',
                'ndcg_cut_10': 0.3240,
                'judged_10': 0.5660,
                'recall_1000': 0.3758,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.full-text.qdel.bm25.txt': {
                'checksum': '8387e4ad480ec4be7961c17d2ea326a1',
                'ndcg_cut_10': 0.4634,
                'judged_10': 0.6460,
                'recall_1000': 0.4368,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.paragraph.qq.bm25.txt': {
                'checksum': '62d713a1ed6a8bf25c1454c66182b573',
                'ndcg_cut_10': 0.4077,
                'judged_10': 0.6160,
                'recall_1000': 0.4877,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.paragraph.qdel.bm25.txt': {
                'checksum': '16b295fda9d1eccd4e1fa4c147657872',
                'ndcg_cut_10': 0.4918,
                'judged_10': 0.6440,
                'recall_1000': 0.5101,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.fusion1.txt': {
                'checksum': '16875b6d32a9b5ef96d7b59315b101a7',
                'ndcg_cut_10': 0.4696,
                'judged_10': 0.6520,
                'recall_1000': 0.5027,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.fusion2.txt': {
                'checksum': '8f7d663d551f831c65dceb8e4e9219c2',
                'ndcg_cut_10': 0.5077,
                'judged_10': 0.6800,
                'recall_1000': 0.5378,
            },
            'https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round5/anserini.covid-r5.abstract.qdel.bm25%2Brm3Rf.txt': {
                'checksum': '909ccbbd55736eff60c7dbeff1404c94',
                'ndcg_cut_10': 0.6177,
                'judged_10': 0.6620,
                'recall_1000': 0.5505,
            }
        }

        tmp = f'tmp{randint(0, 10000)}'

        # In the rare event there's a collision
        if os.path.exists(tmp):
            shutil.rmtree(tmp)

        os.mkdir(tmp)
        for url in runs:
            filename = url.split('/')[-1]

            download_url(url, tmp, md5=runs[url]['checksum'], force=True)
            full_path = os.path.join(tmp, filename)
            self.assertTrue(os.path.exists(full_path))

            eval_cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.1000 -m judged.10,100,1000 \
                           tools/topics-and-qrels/qrels.covid-round4-cumulative.txt \
                           {full_path}'
            stdout, stderr = run_command(eval_cmd)
            self.assertAlmostEqual(parse_score(stdout, 'ndcg_cut_10'), runs[url]['ndcg_cut_10'], delta=0.0001)
            self.assertAlmostEqual(parse_score(stdout, 'judged_10'), runs[url]['judged_10'], delta=0.0001)
            self.assertAlmostEqual(parse_score(stdout, 'recall_1000'), runs[url]['recall_1000'], delta=0.0001)

        shutil.rmtree(tmp)


if __name__ == '__main__':
    unittest.main()
