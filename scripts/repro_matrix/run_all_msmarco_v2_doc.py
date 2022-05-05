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
import yaml

from collections import defaultdict
from scripts.repro_matrix.utils import run_eval_and_return_metric


collection = 'msmarco-v2-doc'

# The models: the rows of the results table will be ordered this way.
models = ['bm25-doc-default',
          'bm25-doc-segmented-default']

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK] '

trec_eval_metric_definitions = {
    'msmarco-v2-doc-dev': {
        'MRR@100': '-c -M 100 -m recip_rank',
        'R@1K': '-c -m recall.1000'
    },
    'msmarco-v2-doc-dev2': {
        'MRR@100': '-c -M 100 -m recip_rank',
        'R@1K': '-c -m recall.1000'
    },
    'dl21-doc': {
        'MAP@100': '-c -M 100 -m map',
        'nDCG@10': '-c -m ndcg_cut.10',
        'R@1K': '-c -m recall.1000'
    }
}

table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
table_keys = {}


def find_table_topic_set_key(topic_key):
    key = ''
    if topic_key.endswith('dev'):
        key = 'dev'
    elif topic_key.endswith('dev2'):
        key = 'dev2'
    elif topic_key.startswith('dl21'):
        key = 'dl21'

    return key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO V2 doc corpus.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    args = parser.parse_args()

    with open('pyserini/resources/msmarco-v2-doc.yaml') as f:
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
                            score = float(run_eval_and_return_metric(metric, eval_key, trec_eval_metric_definitions, runfile))
                            result = ok_str if math.isclose(score, float(expected[metric])) else fail_str + f' expected {expected[metric]:.4f}'
                            print(f'    {metric:7}: {score:.4f} {result}')
                            table[name][find_table_topic_set_key(topic_key)][metric] = score
                        else:
                            table[name][find_table_topic_set_key(topic_key)][metric] = expected[metric]

                print('')

    print(' ' * 54 + 'TREC 2021' + ' ' * 11 + 'MS MARCO dev' + ' ' * 6 + 'MS MARCO dev2')
    print(' ' * 47 + 'MAP@100 nDCG@10  R@1K     MRR@100   R@1K    MRR@100   R@1K')
    print(' ' * 47 + '-' * 22 + '    ' + '-' * 14 + '    ' + '-' * 14)
    for name in models:
        if not name:
            print('')
            continue
        print(f'{table_keys[name]:45}' +
              f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
              f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
              f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}')
