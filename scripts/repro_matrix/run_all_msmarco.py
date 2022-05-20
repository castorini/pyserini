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


# The models: the rows of the results table will be ordered this way.
models = {
    'msmarco-v1-passage':
    ['bm25-tuned',
     'bm25-rm3-tuned',
     '',
     'bm25-d2q-t5-tuned',
     '',
     'bm25-default',
     'bm25-rm3-default',
     '',
     'bm25-d2q-t5-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf',
     '',
     'tct_colbert-v2-hnp',
     'tct_colbert-v2-hnp-otf'],
    'msmarco-v1-doc':
    ['bm25-doc-tuned',
     'bm25-doc-segmented-tuned',
     'bm25-rm3-doc-tuned',
     'bm25-rm3-doc-segmented-tuned',
     '',
     'bm25-d2q-t5-doc-tuned',
     'bm25-d2q-t5-doc-segmented-tuned',
     '',
     'bm25-doc-default',
     'bm25-doc-segmented-default',
     'bm25-rm3-doc-default',
     'bm25-rm3-doc-segmented-default',
     '',
     'bm25-d2q-t5-doc-default',
     'bm25-d2q-t5-doc-segmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'],
    'msmarco-v2-passage':
    ['bm25-default',
     'bm25-augmented-default',
     'bm25-rm3-default',
     'bm25-rm3-augmented-default',
     '',
     'bm25-d2q-t5-default',
     'bm25-d2q-t5-augmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'],
    'msmarco-v2-doc':
    ['bm25-doc-default',
     'bm25-doc-segmented-default',
     'bm25-rm3-doc-default',
     'bm25-rm3-doc-segmented-default',
     '',
     'bm25-d2q-t5-doc-default',
     'bm25-d2q-t5-doc-segmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'
     ]
}

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK] '

trec_eval_metric_definitions = {
    'msmarco-v1-passage': {
        'msmarco-passage-dev-subset': {
            'MRR@10': '-c -M 10 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'dl19-passage': {
            'MAP': '-c -l 2 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -l 2 -m recall.1000'
        },
        'dl20-passage': {
            'MAP': '-c -l 2 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -l 2 -m recall.1000'
        }
    },
    'msmarco-v1-doc': {
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
    },
    'msmarco-v2-passage': {
        'msmarco-v2-passage-dev': {
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'msmarco-v2-passage-dev2': {
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'dl21-passage': {
            'MAP@100': '-c -l 2 -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'MRR@100': '-c -l 2 -M 100 -m recip_rank',
            'R@100': '-c -l 2 -m recall.100',
            'R@1K': '-c -l 2 -m recall.1000'
        }
    },
    'msmarco-v2-doc': {
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
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@100': '-c -m recall.100',
            'R@1K': '-c -m recall.1000'
        }
    }
}

table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
table_keys = {}


def find_table_topic_set_key_v1(topic_key):
    # E.g., we want to map variants like 'dl19-passage-unicoil' and 'dl19-passage' both into 'dl19'
    key = ''
    if topic_key.startswith('dl19'):
        key = 'dl19'
    elif topic_key.startswith('dl20'):
        key = 'dl20'
    elif topic_key.startswith('msmarco'):
        key = 'msmarco'

    return key


def find_table_topic_set_key_v2(topic_key):
    key = ''
    if topic_key.endswith('dev') or topic_key.endswith('dev-unicoil') or topic_key.endswith('dev-unicoil-noexp'):
        key = 'dev'
    elif topic_key.endswith('dev2') or topic_key.endswith('dev2-unicoil') or topic_key.endswith('dev2-unicoil-noexp'):
        key = 'dev2'
    elif topic_key.startswith('dl21'):
        key = 'dl21'

    return key


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO V1 passage corpus.')
    parser.add_argument('--collection', type=str, help='Collection = {v1-passage, v1-doc, v2-passage, v2-doc}.', required=True)
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    args = parser.parse_args()

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

                if not args.skip_eval:
                    print(f'  - topic_key: {topic_key}')

                runfile = f'run.{collection}.{topic_key}.{name}.txt'
                cmd = cmd_template.replace('_R_', f'runs/{runfile}').replace('_T_', topic_key)

                if not args.skip_eval:
                    if not os.path.exists(f'runs/{runfile}'):
                        print(f'    Running: {cmd}')
                        os.system(cmd)

                if not args.skip_eval:
                    print('')

                for expected in topic_set['scores']:
                    for metric in expected:
                        table_keys[name] = display
                        if not args.skip_eval:
                            score = float(run_eval_and_return_metric(metric, eval_key, trec_eval_metric_definitions[collection], runfile))
                            result = ok_str if math.isclose(score, float(expected[metric])) else fail_str + f' expected {expected[metric]:.4f}'
                            print(f'    {metric:7}: {score:.4f} {result}')
                            if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
                                table[name][find_table_topic_set_key_v1(topic_key)][metric] = score
                            else:
                                table[name][find_table_topic_set_key_v2(topic_key)][metric] = score
                        else:
                            if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
                                table[name][find_table_topic_set_key_v1(topic_key)][metric] = expected[metric]
                            else:
                                table[name][find_table_topic_set_key_v2(topic_key)][metric] = expected[metric]

                if not args.skip_eval:
                    print('')

    if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
        print(' ' * 64 + 'TREC 2019' + ' ' * 16 + 'TREC 2020' + ' ' * 12 + 'MS MARCO dev')
        print(' ' * 57 + 'MAP    nDCG@10    R@1K       MAP nDCG@10    R@1K    MRR@10    R@1K')
        print(' ' * 57 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14)
        for name in models[collection]:
            if not name:
                print('')
                continue
            print(f'{table_keys[name]:55}' +
                  f'{table[name]["dl19"]["MAP"]:8.4f}{table[name]["dl19"]["nDCG@10"]:8.4f}{table[name]["dl19"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dl20"]["MAP"]:8.4f}{table[name]["dl20"]["nDCG@10"]:8.4f}{table[name]["dl20"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["msmarco"]["MRR@10"]:8.4f}{table[name]["msmarco"]["R@1K"]:8.4f}')
    else:
        print(' ' * 72 + 'TREC 2021' + ' ' * 18 + 'MS MARCO dev' + ' ' * 6 + 'MS MARCO dev2')
        print(' ' * 57 + 'MAP@100 nDCG@10 MRR@100 R@100   R@1K     MRR@100   R@1K    MRR@100   R@1K')
        print(' ' * 57 + '-' * 38 + '    ' + '-' * 14 + '    ' + '-' * 14)
        for name in models[collection]:
            if not name:
                print('')
                continue
            print(f'{table_keys[name]:55}' +
                  f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}' +
                  f'{table[name]["dl21"]["MRR@100"]:8.4f}{table[name]["dl21"]["R@100"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}')
