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
    'MRR@100': '-c -M 100 -m recip_rank',
    'R@100': '-c -m recall.100',
}


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
                            score = float(run_eval_and_return_metric(metric, f'{eval_key}-{split}',
                                                                     trec_eval_metric_definitions[metric], runfile))
                            result = ok_str if math.isclose(score, float(expected[metric])) \
                                else fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result}')

            print('')

    #             short_topic_key = ''
    #             if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
    #                 short_topic_key = find_table_topic_set_key_v1(topic_key)
    #             else:
    #                 short_topic_key = find_table_topic_set_key_v2(topic_key)
    #
    #             if not args.skip_eval:
    #                 print(f'  - topic_key: {topic_key}')
    #
    #             runfile = f'runs/run.{collection}.{name}.{short_topic_key}.txt'
    #             cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile)
    #
    #             if not args.skip_eval:
    #                 if not os.path.exists(runfile):
    #                     print(f'    Running: {cmd}')
    #                     os.system(cmd)
    #
    #             if not args.skip_eval:
    #                 print('')
    #
    #             for expected in topic_set['scores']:
    #                 for metric in expected:
    #                     table_keys[name] = display
    #                     if not args.skip_eval:
    #                         score = float(run_eval_and_return_metric(metric, eval_key,
    #                                                                  trec_eval_metric_definitions[collection], runfile))
    #                         result = ok_str if math.isclose(score, float(expected[metric])) \
    #                             else fail_str + f' expected {expected[metric]:.4f}'
    #                         print(f'    {metric:7}: {score:.4f} {result}')
    #                         table[name][short_topic_key][metric] = score
    #                     else:
    #                         table[name][short_topic_key][metric] = expected[metric]
    #
    #             if not args.skip_eval:
    #                 print('')
    #
    # if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
    #     print(' ' * 69 + 'TREC 2019' + ' ' * 16 + 'TREC 2020' + ' ' * 12 + 'MS MARCO dev')
    #     print(' ' * 62 + 'MAP    nDCG@10    R@1K       MAP nDCG@10    R@1K    MRR@10    R@1K')
    #     print(' ' * 62 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14)
    #     for name in models[collection]:
    #         if not name:
    #             print('')
    #             continue
    #         print(f'{table_keys[name]:60}' +
    #               f'{table[name]["dl19"]["MAP"]:8.4f}{table[name]["dl19"]["nDCG@10"]:8.4f}{table[name]["dl19"]["R@1K"]:8.4f}  ' +
    #               f'{table[name]["dl20"]["MAP"]:8.4f}{table[name]["dl20"]["nDCG@10"]:8.4f}{table[name]["dl20"]["R@1K"]:8.4f}  ' +
    #               f'{table[name]["dev"]["MRR@10"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}')
    # else:
    #     print(' ' * 77 + 'TREC 2021' + ' ' * 18 + 'MS MARCO dev' + ' ' * 6 + 'MS MARCO dev2')
    #     print(' ' * 62 + 'MAP@100 nDCG@10 MRR@100 R@100   R@1K     MRR@100   R@1K    MRR@100   R@1K')
    #     print(' ' * 62 + '-' * 38 + '    ' + '-' * 14 + '    ' + '-' * 14)
    #     for name in models[collection]:
    #         if not name:
    #             print('')
    #             continue
    #         print(f'{table_keys[name]:60}' +
    #               f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}' +
    #               f'{table[name]["dl21"]["MRR@100"]:8.4f}{table[name]["dl21"]["R@100"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
    #               f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
    #               f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}')
