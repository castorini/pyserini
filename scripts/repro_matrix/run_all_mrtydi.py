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

import yaml

from scripts.repro_matrix.defs_mrtydi import models, languages, trec_eval_metric_definitions
from scripts.repro_matrix.utils import run_eval_and_return_metric, ok_str, fail_str


def print_results(metric, split):
    print(f'Metric = {metric}, Split = {split}')
    print(' ' * 22, end='')
    for lang in languages:
        print(f'{lang[0]:3}    ', end='')
    print('')
    for model in models:
        print(f'{model:20}', end='')
        for lang in languages:
            key = f'{model}.{lang[0]}'
            print(f'{table[key][split][metric]:7.3f}', end='')
        print('')
    print('')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for Mr.TyDi.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    args = parser.parse_args()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open('pyserini/resources/mrtydi.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            eval_key = condition['eval_key']
            cmd_template = condition['command']

            print(f'condition {name}:')

            for splits in condition['splits']:
                split = splits['split']

                print(f'  - split: {split}')

                runfile = f'runs/run.mrtydi.{name}.{split}.txt'
                cmd = Template(cmd_template).substitute(split=split, output=runfile)

                if not os.path.exists(runfile):
                    print(f'    Running: {cmd}')
                    os.system(cmd)

                for expected in splits['scores']:
                    for metric in expected:
                        if not args.skip_eval:
                            score = float(run_eval_and_return_metric(metric, f'{eval_key}-{split}',
                                                                     trec_eval_metric_definitions[metric], runfile))
                            result = ok_str if math.isclose(score, float(expected[metric])) \
                                else fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result}')
                            table[name][split][metric] = score
                        else:
                            table[name][split][metric] = expected[metric]

            print('')

    for metric in ['MRR@100', 'R@100']:
        for split in ['test', 'dev', 'train']:
            print_results(metric, split)
