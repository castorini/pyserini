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

"""Integration tests for BEIR SPLADE-distill CoCodenser-medium"""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score


class TestSearchIntegration(unittest.TestCase):
    beir_splade = {
        'trec-covid': {'ndcg_cut_10': 0.7109, 'recall_100': 0.1308, 'recall_1000': 0.4433},
        'bioasq': {'ndcg_cut_10': 0.5035, 'recall_100': 0.7422, 'recall_1000': 0.8904},
        'nfcorpus': {'ndcg_cut_10': 0.3454, 'recall_100': 0.2891, 'recall_1000': 0.5694},
        'nq': {'ndcg_cut_10': 0.5442, 'recall_100': 0.9285, 'recall_1000': 0.9812},
        'hotpotqa': {'ndcg_cut_10': 0.6860, 'recall_100': 0.8144, 'recall_1000': 0.8945},
        'fiqa': {'ndcg_cut_10': 0.3514, 'recall_100': 0.6298, 'recall_1000': 0.8323},
        'signal1m': {'ndcg_cut_10': 0.2957, 'recall_100': 0.3311, 'recall_1000': 0.5514},
        'trec-news': {'ndcg_cut_10': 0.3936, 'recall_100': 0.4323, 'recall_1000': 0.6977},
        'robust04': {'ndcg_cut_10': 0.4581, 'recall_100': 0.3773, 'recall_1000': 0.6099},
        'arguana': {'ndcg_cut_10': 0.5210, 'recall_100': 0.9822, 'recall_1000': 0.9950},
        'webis-touche2020': {'ndcg_cut_10': 0.2435, 'recall_100': 0.4723, 'recall_1000': 0.8116},
        'cqadupstack-android': {'ndcg_cut_10': 0.3954, 'recall_100': 0.7405, 'recall_1000': 0.9035},
        'cqadupstack-english': {'ndcg_cut_10': 0.4026, 'recall_100': 0.6768, 'recall_1000': 0.8346},
        'cqadupstack-gaming': {'ndcg_cut_10': 0.5061, 'recall_100': 0.8138, 'recall_1000': 0.9253},
        'cqadupstack-gis': {'ndcg_cut_10': 0.3223, 'recall_100': 0.6419, 'recall_1000': 0.8385},
        'cqadupstack-mathematica': {'ndcg_cut_10': 0.2423, 'recall_100': 0.5732, 'recall_1000': 0.7848},
        'cqadupstack-physics': {'ndcg_cut_10': 0.3668, 'recall_100': 0.7286, 'recall_1000': 0.8931},
        'cqadupstack-programmers': {'ndcg_cut_10': 0.3412, 'recall_100': 0.6653, 'recall_1000': 0.8451},
        'cqadupstack-stats': {'ndcg_cut_10': 0.3142, 'recall_100': 0.5889, 'recall_1000': 0.7823},
        'cqadupstack-tex': {'ndcg_cut_10': 0.2575, 'recall_100': 0.5231, 'recall_1000': 0.7372},
        'cqadupstack-unix': {'ndcg_cut_10': 0.3292, 'recall_100': 0.6192, 'recall_1000': 0.8225},
        'cqadupstack-webmasters': {'ndcg_cut_10': 0.3343, 'recall_100': 0.6404, 'recall_1000': 0.8767},
        'cqadupstack-wordpress': {'ndcg_cut_10': 0.2839, 'recall_100': 0.5974, 'recall_1000': 0.8036},
        'quora': {'ndcg_cut_10': 0.8136, 'recall_100': 0.9817, 'recall_1000': 0.9979},
        'dbpedia-entity': {'ndcg_cut_10': 0.4416, 'recall_100': 0.5636, 'recall_1000': 0.7774},
        'scidocs': {'ndcg_cut_10': 0.1590, 'recall_100': 0.3671, 'recall_1000': 0.5891},
        'fever': {'ndcg_cut_10': 0.7962, 'recall_100': 0.9550, 'recall_1000': 0.9751},
        'climate-fever': {'ndcg_cut_10': 0.2276, 'recall_100': 0.5140, 'recall_1000': 0.7084},
        'scifact': {'ndcg_cut_10': 0.6992, 'recall_100': 0.9270, 'recall_1000': 0.9767},
    }

    def setUp(self):
        self.temp_files = []
        self.commitid = 'xxxxxx'
        self.date = '20220430'

    def test_beir_splade(self):
        for key in self.beir_splade:
            output_file = f'runs/run.beir-v1.0.0-{key}-splade_distil_cocodenser_medium.trec'
            self.temp_files.append(output_file)

            cmd = f'python -m pyserini.search.lucene \
                      --index indexes/lucene-index.beir-v1.0.0-{key}-splade_distil_cocodenser_medium.{self.date}.{self.commitid} \
                      --topics beir-v1.0.0-{key}-test-splade_distil_cocodenser_medium \
                      --output runs/run.beir-v1.0.0-{key}-splade_distil_cocodenser_medium.trec \
                      --output-format trec \
                      --batch 36 --threads 12 \
                      --remove-query --impact --hits 1000'
            os.system(cmd)

            eval_cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 \
                         beir-v1.0.0-{key}-test runs/run.beir-v1.0.0-{key}-splade_distil_cocodenser_medium.trec'
            stdout, stderr = run_command(eval_cmd)
            for metric in ['ndcg_cut_10', 'recall_100', 'recall_1000']:
                score = parse_score(stdout, metric)
                self.assertAlmostEqual(score, self.beir_splade[key][metric], delta=1e-5)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
