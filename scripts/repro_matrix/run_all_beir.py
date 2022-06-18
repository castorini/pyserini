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

import argparse
import math
import os
from collections import defaultdict
from string import Template
import subprocess

import yaml

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK] '

trec_eval_metric_definitions = {
    'nDCG@10': '-c -m ndcg_cut.10',
    'R@100': '-c -m recall.100',
    'R@1000': '-c -m recall.1000'
}

beir_keys = ['trec-covid',
             'bioasq',
             'nfcorpus',
             'nq',
             'hotpotqa',
             'fiqa',
             'signal1m',
             'trec-news',
             'robust04',
             'arguana',
             'webis-touche2020',
             'cqadupstack-android',
             'cqadupstack-english',
             'cqadupstack-gaming',
             'cqadupstack-gis',
             'cqadupstack-mathematica',
             'cqadupstack-physics',
             'cqadupstack-programmers',
             'cqadupstack-stats',
             'cqadupstack-tex',
             'cqadupstack-unix',
             'cqadupstack-webmasters',
             'cqadupstack-wordpress',
             'quora',
             'dbpedia-entity',
             'scidocs',
             'fever',
             'climate-fever',
             'scifact'
             ]

def run_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    return stdout, stderr


def run_eval_and_return_metric(metric, eval_key, defs, runfile):
    eval_cmd = f'python -m pyserini.eval.trec_eval {defs} {eval_key} {runfile}'
    eval_stdout, eval_stderr = run_command(eval_cmd)

    for line in eval_stdout.split('\n'):
        parts = line.split('\t')
        if len(parts) == 3 and parts[1] == 'all':
            return round(float(parts[2]), 4)

    return 0.0


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for BEIR.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    args = parser.parse_args()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open('pyserini/resources/beir.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            cmd_template = condition['command']

            print(f'condition {name}:')

            for datasets in condition['datasets']:
                dataset = datasets['dataset']

                print(f'  - dataset: {dataset}')

                runfile = f'runs/run.beir-{name}.{dataset}.txt'
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile)

                if not os.path.exists(runfile):
                    print(f'    Running: {cmd}')
                    os.system(cmd)

                for expected in datasets['scores']:
                    for metric in expected:
                        if not args.skip_eval:
                            score = float(run_eval_and_return_metric(metric, f'beir-v1.0.0-{dataset}-test',
                                                                     trec_eval_metric_definitions[metric], runfile))
                            result = ok_str if math.isclose(score, float(expected[metric])) \
                                else fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result}')

                            table[dataset][name][metric] = score
                        else:
                            table[dataset][name][metric] = expected[metric]

            print('')

    models = ['flat', 'multifield', 'splade-distil-cocodenser-medium']
    metrics = ['nDCG@10', 'R@100', 'R@1000']

    top_level_sums = defaultdict(lambda: defaultdict(float))
    cqadupstack_sums = defaultdict(lambda: defaultdict(float))
    final_scores = defaultdict(lambda: defaultdict(float))

    # Compute the running sums to compute the final mean scores
    for key in beir_keys:
        for model in models:
            for metric in metrics:
                if key.startswith('cqa'):
                    # The running sum for cqa needs to be kept separately.
                    cqadupstack_sums[model][metric] += table[key][model][metric]
                else:
                    top_level_sums[model][metric] += table[key][model][metric]

    # Compute the final mean
    for model in models:
        for metric in metrics:
            # Compute mean over cqa sub-collections first
            cqa_score = cqadupstack_sums[model][metric] / 12
            # Roll cqa scores into final overall mean
            final_score = (top_level_sums[model][metric] + cqa_score) / 18
            final_scores[model][metric] = final_score

    print(' ' * 30 + 'BM25-flat' + ' ' * 10 + 'BM25-mf' + ' ' * 11 + 'SPLADE')
    print(' ' * 26 + 'nDCG@10   R@100   ' * 3)
    print(' ' * 27 + '-' * 14 + '    ' + '-' * 14 + '    ' + '-' * 14)
    for dataset in beir_keys:
        print(f'{dataset:25}' +
              f'{table[dataset]["flat"]["nDCG@10"]:8.4f}{table[dataset]["flat"]["R@100"]:8.4f}  ' +
              f'{table[dataset]["multifield"]["nDCG@10"]:8.4f}{table[dataset]["multifield"]["R@100"]:8.4f}  ' +
              f'{table[dataset]["splade-distil-cocodenser-medium"]["nDCG@10"]:8.4f}{table[dataset]["splade-distil-cocodenser-medium"]["R@100"]:8.4f}')
    print(' ' * 27 + '-' * 14 + '    ' + '-' * 14 + '    ' + '-' * 14)
    print('avg' + ' ' * 22 + f'{final_scores["flat"]["nDCG@10"]:8.4f}{final_scores["flat"]["R@100"]:8.4f}  ' +
          f'{final_scores["multifield"]["nDCG@10"]:8.4f}{final_scores["multifield"]["R@100"]:8.4f}  ' +
          f'{final_scores["splade-distil-cocodenser-medium"]["nDCG@10"]:8.4f}{final_scores["splade-distil-cocodenser-medium"]["R@100"]:8.4f} ')
