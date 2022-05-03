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
import subprocess
import yaml
from collections import defaultdict


collection = 'msmarco-v1-doc'

# The models: the rows of the results table will be ordered this way.
models = ['bm25-doc-tuned',
          'bm25-doc-segmented-tuned',
          'bm25-rm3-doc-tuned',
          'bm25-rm3-doc-segmented-tuned',
          '',
          'bm25-doc-default',
          'bm25-doc-segmented-default',
          'bm25-rm3-doc-default',
          'bm25-rm3-doc-segmented-default',
          '',
          'unicoil-noexp',
          'unicoil-noexp-otf',
          '',
          'unicoil',
          'unicoil-otf']

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK] '

trec_eval_metric_definitions = {
    'msmarco-doc-dev': {
        'MRR@10': '-c -M 100 -m recip_rank',
        'R@1K': '-c -m recall.1000'
    },
    'dl19-doc': {
        'MAP': '-c -M 100 -m map',
        'nDCG@10': '-c -m ndcg_cut.10',
        'R@1K': '-c -m recall.1000'
    },
    'dl20-doc': {
        'MAP': '-c -M 100 -m map',
        'nDCG@10': '-c -m ndcg_cut.10',
        'R@1K': '-c -m recall.1000'
    }
}

table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
table_keys = {}


def run_command(cmd):
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    stdout = stdout.decode('utf-8')
    stderr = stderr.decode('utf-8')

    return stdout, stderr


def run_eval_and_return_metric(metric, eval_key, runfile):
    eval_cmd = f'python -m pyserini.eval.trec_eval {trec_eval_metric_definitions[eval_key][metric]} {eval_key} runs/{runfile}'
    eval_stdout, eval_stderr = run_command(eval_cmd)

    # TODO: This is very brittle... fix me later.
    return eval_stdout.split('\n')[-3].split('\t')[2]


def find_table_topic_set_key(topic_key):
    # E.g., we want to map variants like 'dl19-doc-unicoil' and 'dl19-doc' both into 'dl19'
    key = ''
    if topic_key.startswith('dl19'):
        key = 'dl19'
    elif topic_key.startswith('dl20'):
        key = 'dl20'
    elif topic_key.startswith('msmarco'):
        key = 'msmarco'

    return key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO V1 doc corpus.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    args = parser.parse_args()

    with open('pyserini/resources/msmarco-v1-doc.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            display = condition['display']
            cmd_template = condition['command']

            print(f'# Running condition "{name}": {display}\n')
            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                print(f'  - topic_key: {topic_key}')

                runfile = f'run.{collection}.{topic_key}.{name}.txt'
                cmd = cmd_template.replace('_R_', f'runs/{runfile}').replace('_T_', topic_key)

                if not os.path.exists(f'runs/{runfile}'):
                    print(f'    Running: {cmd}')
                    os.system(cmd)

                print('')
                for expected in topic_set['scores']:
                    for metric in expected:
                        table_keys[name] = display
                        if not args.skip_eval:
                            score = float(run_eval_and_return_metric(metric, eval_key, runfile))
                            result = ok_str if math.isclose(score, float(expected[metric])) else fail_str + f' expected {expected[metric]:.4f}'
                            print(f'    {metric:7}: {score:.4f} {result}')
                            table[name][find_table_topic_set_key(topic_key)][metric] = score
                        else:
                            table[name][find_table_topic_set_key(topic_key)][metric] = expected[metric]

                print('')

    print(' ' * 49 + 'TREC 2019' + ' ' * 16 + 'TREC 2020' + ' ' * 12 + 'MS MARCO dev')
    print(' ' * 45 + 'MAP nDCG@10    R@1K       MAP nDCG@10    R@1K    MRR@10    R@1K')
    print(' ' * 42 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14)
    for name in models:
        if not name:
            print('')
            continue
        print(f'{table_keys[name]:40}' +
              f'{table[name]["dl19"]["MAP"]:8.4f}{table[name]["dl19"]["nDCG@10"]:8.4f}{table[name]["dl19"]["R@1K"]:8.4f}  ' +
              f'{table[name]["dl20"]["MAP"]:8.4f}{table[name]["dl20"]["nDCG@10"]:8.4f}{table[name]["dl20"]["R@1K"]:8.4f}  ' +
              f'{table[name]["msmarco"]["MRR@10"]:8.4f}{table[name]["msmarco"]["R@1K"]:8.4f}')
