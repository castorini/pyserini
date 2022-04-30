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

"""Integration tests for BEIR baselines"""

import os
import unittest

from integrations.utils import clean_files, run_command, parse_score


class TestSearchIntegration(unittest.TestCase):
    beir_flat = {
        'trec-covid': {'ndcg_cut_10': 0.5947, 'recall_100': 0.1091, 'recall_1000': 0.3955},
        'bioasq': {'ndcg_cut_10': 0.5225, 'recall_100': 0.7687, 'recall_1000': 0.9030},
        'nfcorpus': {'ndcg_cut_10': 0.3218, 'recall_100': 0.2457, 'recall_1000': 0.3704},
        'nq': {'ndcg_cut_10': 0.3055, 'recall_100': 0.7513, 'recall_1000': 0.8958},
        'hotpotqa': {'ndcg_cut_10': 0.6330, 'recall_100': 0.7957, 'recall_1000': 0.8820},
        'fiqa': {'ndcg_cut_10': 0.2361, 'recall_100': 0.5395, 'recall_1000': 0.7393},
        'signal1m': {'ndcg_cut_10': 0.3304, 'recall_100': 0.3703, 'recall_1000': 0.5642},
        'trec-news': {'ndcg_cut_10': 0.3952, 'recall_100': 0.4469, 'recall_1000': 0.7051},
        'robust04': {'ndcg_cut_10': 0.4070, 'recall_100': 0.3746, 'recall_1000': 0.6345},
        'arguana': {'ndcg_cut_10': 0.3970, 'recall_100': 0.9324, 'recall_1000': 0.9872},
        'webis-touche2020': {'ndcg_cut_10': 0.4422, 'recall_100': 0.5822, 'recall_1000': 0.8621},
        'cqadupstack-android': {'ndcg_cut_10': 0.3801, 'recall_100': 0.6829, 'recall_1000': 0.8632},
        'cqadupstack-english': {'ndcg_cut_10': 0.3453, 'recall_100': 0.5757, 'recall_1000': 0.7323},
        'cqadupstack-gaming': {'ndcg_cut_10': 0.4822, 'recall_100': 0.7651, 'recall_1000': 0.8945},
        'cqadupstack-gis': {'ndcg_cut_10': 0.2901, 'recall_100': 0.6119, 'recall_1000': 0.8174},
        'cqadupstack-mathematica': {'ndcg_cut_10': 0.2015, 'recall_100': 0.4877, 'recall_1000': 0.7221},
        'cqadupstack-physics': {'ndcg_cut_10': 0.3214, 'recall_100': 0.6326, 'recall_1000': 0.8340},
        'cqadupstack-programmers': {'ndcg_cut_10': 0.2802, 'recall_100': 0.5588, 'recall_1000': 0.7734},
        'cqadupstack-stats': {'ndcg_cut_10': 0.2711, 'recall_100': 0.5338, 'recall_1000': 0.7310},
        'cqadupstack-tex': {'ndcg_cut_10': 0.2244, 'recall_100': 0.4686, 'recall_1000': 0.6907},
        'cqadupstack-unix': {'ndcg_cut_10': 0.2749, 'recall_100': 0.5417, 'recall_1000': 0.7616},
        'cqadupstack-webmasters': {'ndcg_cut_10': 0.3059, 'recall_100': 0.5820, 'recall_1000': 0.8066},
        'cqadupstack-wordpress': {'ndcg_cut_10': 0.2483, 'recall_100': 0.5152, 'recall_1000': 0.7552},
        'quora': {'ndcg_cut_10': 0.7886, 'recall_100': 0.9733, 'recall_1000': 0.9950},
        'dbpedia-entity': {'ndcg_cut_10': 0.3180, 'recall_100': 0.4682, 'recall_1000': 0.6760},
        'scidocs': {'ndcg_cut_10': 0.1490, 'recall_100': 0.3477, 'recall_1000': 0.5638},
        'fever': {'ndcg_cut_10': 0.6513, 'recall_100': 0.9185, 'recall_1000': 0.9589},
        'climate-fever': {'ndcg_cut_10': 0.1651, 'recall_100': 0.4249, 'recall_1000': 0.6324},
        'scifact': {'ndcg_cut_10': 0.6789, 'recall_100': 0.9253, 'recall_1000': 0.9767},
    }

    beir_multifield = {
        'trec-covid': {'ndcg_cut_10': 0.6559, 'recall_100': 0.1141, 'recall_1000': 0.3891},
        'bioasq': {'ndcg_cut_10': 0.4646, 'recall_100': 0.7145, 'recall_1000': 0.8428},
        'nfcorpus': {'ndcg_cut_10': 0.3254, 'recall_100': 0.2500, 'recall_1000': 0.3718},
        'nq': {'ndcg_cut_10': 0.3285, 'recall_100': 0.7597, 'recall_1000': 0.9019},
        'hotpotqa': {'ndcg_cut_10': 0.6027, 'recall_100': 0.7400, 'recall_1000': 0.8405},
        'fiqa': {'ndcg_cut_10': 0.2361, 'recall_100': 0.5395, 'recall_1000': 0.7393},
        'signal1m': {'ndcg_cut_10': 0.3304, 'recall_100': 0.3703, 'recall_1000': 0.5642},
        'trec-news': {'ndcg_cut_10': 0.3977, 'recall_100': 0.4216, 'recall_1000': 0.6993},
        'robust04': {'ndcg_cut_10': 0.4070, 'recall_100': 0.3746, 'recall_1000': 0.6345},
        'arguana': {'ndcg_cut_10': 0.4142, 'recall_100': 0.9431, 'recall_1000': 0.9893},
        'webis-touche2020': {'ndcg_cut_10': 0.3673, 'recall_100': 0.5376, 'recall_1000': 0.8668},
        'cqadupstack-android': {'ndcg_cut_10': 0.3709, 'recall_100': 0.6889, 'recall_1000': 0.8712},
        'cqadupstack-english': {'ndcg_cut_10': 0.3321, 'recall_100': 0.5842, 'recall_1000': 0.7574},
        'cqadupstack-gaming': {'ndcg_cut_10': 0.4418, 'recall_100': 0.7571, 'recall_1000': 0.8882},
        'cqadupstack-gis': {'ndcg_cut_10': 0.2904, 'recall_100': 0.6458, 'recall_1000': 0.8248},
        'cqadupstack-mathematica': {'ndcg_cut_10': 0.2046, 'recall_100': 0.5215, 'recall_1000': 0.7559},
        'cqadupstack-physics': {'ndcg_cut_10': 0.3248, 'recall_100': 0.6486, 'recall_1000': 0.8506},
        'cqadupstack-programmers': {'ndcg_cut_10': 0.2963, 'recall_100': 0.6194, 'recall_1000': 0.8096},
        'cqadupstack-stats': {'ndcg_cut_10': 0.2790, 'recall_100': 0.5719, 'recall_1000': 0.7619},
        'cqadupstack-tex': {'ndcg_cut_10': 0.2086, 'recall_100': 0.4954, 'recall_1000': 0.7222},
        'cqadupstack-unix': {'ndcg_cut_10': 0.2788, 'recall_100': 0.5721, 'recall_1000': 0.7783},
        'cqadupstack-webmasters': {'ndcg_cut_10': 0.3008, 'recall_100': 0.6100, 'recall_1000': 0.8226},
        'cqadupstack-wordpress': {'ndcg_cut_10': 0.2562, 'recall_100': 0.5526, 'recall_1000': 0.7848},
        'quora': {'ndcg_cut_10': 0.7886, 'recall_100': 0.9733, 'recall_1000': 0.9950},
        'dbpedia-entity': {'ndcg_cut_10': 0.3128, 'recall_100': 0.3981, 'recall_1000': 0.5848},
        'scidocs': {'ndcg_cut_10': 0.1581, 'recall_100': 0.3561, 'recall_1000': 0.5599},
        'fever': {'ndcg_cut_10': 0.7530, 'recall_100': 0.9309, 'recall_1000': 0.9599},
        'climate-fever': {'ndcg_cut_10': 0.2129, 'recall_100': 0.4357, 'recall_1000': 0.6099},
        'scifact': {'ndcg_cut_10': 0.6647, 'recall_100': 0.9076, 'recall_1000': 0.9800},
    }

    def setUp(self):
        self.temp_files = []
        self.commitid = 'xxxxxx'
        self.date = '20220430'

    def test_beir_flat(self):
        for key in self.beir_flat:
            output_file = f'runs/run.beir-v1.0.0-{key}-flat.trec'
            self.temp_files.append(output_file)

            cmd = f'python -m pyserini.search.lucene \
                      --index indexes/lucene-index.beir-v1.0.0-{key}-flat.{self.date}.{self.commitid} \
                      --topics beir-v1.0.0-{key}-test \
                      --output {output_file} \
                      --output-format trec \
                      --batch 36 --threads 12 \
                      --remove-query --hits 1000'
            os.system(cmd)

            eval_cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 \
                         beir-v1.0.0-{key}-test runs/run.beir-v1.0.0-{key}-flat.trec'
            stdout, stderr = run_command(eval_cmd)
            for metric in ['ndcg_cut_10', 'recall_100', 'recall_1000']:
                score = parse_score(stdout, metric)
                self.assertAlmostEqual(score, self.beir_flat[key][metric], delta=1e-5)

    def test_beir_multifield(self):
        for key in self.beir_multifield:
            output_file = f'runs/run.beir-v1.0.0-{key}-multifield.trec'
            self.temp_files.append(output_file)

            cmd = f'python -m pyserini.search.lucene \
                      --index indexes/lucene-index.beir-v1.0.0-{key}-multifield.{self.date}.{self.commitid} \
                      --topics beir-v1.0.0-{key}-test \
                      --output runs/run.beir-v1.0.0-{key}-multifield.trec \
                      --output-format trec \
                      --batch 36 --threads 12 \
                      --fields contents=1.0 title=1.0 \
                      --remove-query --hits 1000'
            os.system(cmd)

            eval_cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 \
                         beir-v1.0.0-{key}-test runs/run.beir-v1.0.0-{key}-multifield.trec'
            stdout, stderr = run_command(eval_cmd)
            for metric in ['ndcg_cut_10', 'recall_100', 'recall_1000']:
                score = parse_score(stdout, metric)
                self.assertAlmostEqual(score, self.beir_multifield[key][metric], delta=1e-5)

    def tearDown(self):
        clean_files(self.temp_files)


if __name__ == '__main__':
    unittest.main()
