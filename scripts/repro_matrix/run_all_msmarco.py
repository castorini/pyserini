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
import time
from collections import defaultdict
from string import Template

import yaml

from scripts.repro_matrix.defs_msmarco import models, trec_eval_metric_definitions
from scripts.repro_matrix.utils import run_eval_and_return_metric, ok_str, okish_str, fail_str, \
    find_msmarco_table_topic_set_key_v1, find_msmarco_table_topic_set_key_v2

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO corpora.')
    parser.add_argument('--collection', type=str, help='Collection = {v1-passage, v1-doc, v2-passage, v2-doc}.', required=True)
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    args = parser.parse_args()

    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    table_keys = {}

    if args.collection == 'v1-passage':
        collection = 'msmarco-v1-passage'
        yaml_file = 'pyserini/resources/msmarco-v1-passage.yaml'
    elif args.collection == 'v1-doc':
        collection = 'msmarco-v1-doc'
        yaml_file = 'pyserini/resources/msmarco-v1-doc.yaml'
    elif args.collection == 'v2-passage':
        collection = 'msmarco-v2-passage'
        yaml_file = 'pyserini/resources/msmarco-v2-passage.yaml'
    elif args.collection == 'v2-doc':
        collection = 'msmarco-v2-doc'
        yaml_file = 'pyserini/resources/msmarco-v2-doc.yaml'
    else:
        raise ValueError(f'Unknown corpus: {args.collection}')

    with open(yaml_file) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            display = condition['display']
            cmd_template = condition['command']

            if not args.skip_eval:
                print(f'# Running condition "{name}": {display}\n')
            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                short_topic_key = ''
                if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
                    short_topic_key = find_msmarco_table_topic_set_key_v1(topic_key)
                else:
                    short_topic_key = find_msmarco_table_topic_set_key_v2(topic_key)

                if not args.skip_eval:
                    print(f'  - topic_key: {topic_key}')

                runfile = f'runs/run.{collection}.{name}.{short_topic_key}.txt'
                cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile)

                if not args.skip_eval:
                    if not os.path.exists(runfile):
                        print(f'    Running: {cmd}')
                        os.system(cmd)

                if not args.skip_eval:
                    print('')

                for expected in topic_set['scores']:
                    for metric in expected:
                        table_keys[name] = display
                        if not args.skip_eval:
                            score = float(
                                run_eval_and_return_metric(metric,
                                                           eval_key,
                                                           trec_eval_metric_definitions[collection][eval_key][metric],
                                                           runfile))
                            if math.isclose(score, float(expected[metric])):
                                result_str = ok_str
                            # Flaky test: small difference on my iMac Studio
                            elif args.collection == 'v1-passage' and topic_key == 'msmarco-passage-dev-subset' and \
                                 name == 'ance-otf' and math.isclose(score, float(expected[metric]), abs_tol=2e-4):
                                result_str = okish_str
                            else:
                                result_str = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'    {metric:7}: {score:.4f} {result_str}')
                            table[name][short_topic_key][metric] = score
                        else:
                            table[name][short_topic_key][metric] = expected[metric]

                if not args.skip_eval:
                    print('')

    if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
        print(' ' * 69 + 'TREC 2019' + ' ' * 16 + 'TREC 2020' + ' ' * 12 + 'MS MARCO dev')
        print(' ' * 62 + 'MAP    nDCG@10    R@1K       MAP nDCG@10    R@1K    MRR@10    R@1K')
        print(' ' * 62 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14)
        for name in models[collection]:
            if not name:
                print('')
                continue
            print(f'{table_keys[name]:60}' +
                  f'{table[name]["dl19"]["MAP"]:8.4f}{table[name]["dl19"]["nDCG@10"]:8.4f}{table[name]["dl19"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dl20"]["MAP"]:8.4f}{table[name]["dl20"]["nDCG@10"]:8.4f}{table[name]["dl20"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev"]["MRR@10"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}')
    else:
        print(' ' * 77 + 'TREC 2021' + ' ' * 18 + 'MS MARCO dev' + ' ' * 6 + 'MS MARCO dev2')
        print(' ' * 62 + 'MAP@100 nDCG@10 MRR@100 R@100   R@1K     MRR@100   R@1K    MRR@100   R@1K')
        print(' ' * 62 + '-' * 38 + '    ' + '-' * 14 + '    ' + '-' * 14)
        for name in models[collection]:
            if not name:
                print('')
                continue
            print(f'{table_keys[name]:60}' +
                  f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}' +
                  f'{table[name]["dl21"]["MRR@100"]:8.4f}{table[name]["dl21"]["R@100"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}')

    end = time.time()
    print(f'Total elapsed time: {end - start:.0f}s')
