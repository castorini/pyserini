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
import re
import sys
import time
from collections import defaultdict, namedtuple
from datetime import datetime
from string import Template

import importlib.resources
import yaml

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str

dense_threads = 16
dense_batch_size = 512
sparse_threads = 16
sparse_batch_size = 128

# The models: the rows of the results table will be ordered this way.
models = {
    # MS MARCO v1 passage
    'msmarco-v1-passage':
    ['bm25-default',
     'bm25-rm3-default',
     'bm25-rocchio-default',
     '',
     'bm25-tuned',
     'bm25-rm3-tuned',
     'bm25-rocchio-tuned',
     '',
     'bm25-d2q-t5-default',
     'bm25-rm3-d2q-t5-default',
     'bm25-rocchio-d2q-t5-default',
     '',
     'bm25-d2q-t5-tuned',
     'bm25-rm3-d2q-t5-tuned',
     'bm25-rocchio-d2q-t5-tuned',
     '',
     'unicoil',
     'unicoil-pytorch',
     'unicoil-onnx',
     '',
     'unicoil-noexp',
     'unicoil-noexp-pytorch',
     'unicoil-noexp-onnx',
     '',
     'splade-pp-ed-pytorch',
     'splade-pp-ed-onnx',
     'splade-pp-ed-rocchio-pytorch',
     'splade-pp-ed-rocchio-onnx',
     'splade-pp-sd-pytorch',
     'splade-pp-sd-onnx',
     'splade-pp-sd-rocchio-pytorch',
     'splade-pp-sd-rocchio-onnx',
     '',
     'ance',
     'ance-pytorch',
     'ance-avg-prf-pytorch',
     'ance-rocchio-prf-pytorch',
     '',
     'sbert-pytorch',
     'sbert-avg-prf-pytorch',
     'sbert-rocchio-prf-pytorch',
     '',
     'distilbert-kd',
     'distilbert-kd-pytorch',
     'distilbert-kd-tasb',
     'distilbert-kd-tasb-pytorch',
     'distilbert-kd-tasb-avg-prf-pytorch',
     'distilbert-kd-tasb-rocchio-prf-pytorch',
     '',
     'tct_colbert-v2-hnp',
     'tct_colbert-v2-hnp-pytorch',
     'tct_colbert-v2-hnp-avg-prf-pytorch',
     'tct_colbert-v2-hnp-rocchio-prf-pytorch',
     '',
     'tct_colbert-v2-hnp-bm25-pytorch',
     'tct_colbert-v2-hnp-bm25d2q-pytorch',
     '',
     'slimr',
     'slimr-pp',
     '',
     'aggretriever-distilbert-pytorch',
     'aggretriever-cocondenser-pytorch',
     '',
     'openai-ada2',
     'openai-ada2-hyde',
     'openai-text-embedding-3-large',
     '',
     'cosdpr-distil-pytorch',
     '',
     'bge-base-en-v1.5-pytorch',
     '',
     'cohere-embed-english-v3.0',
     ],

    # MS MARCO v1 doc
    'msmarco-v1-doc':
    ['bm25-doc-default',
     'bm25-doc-segmented-default',
     'bm25-rm3-doc-default',
     'bm25-rm3-doc-segmented-default',
     'bm25-rocchio-doc-default',
     'bm25-rocchio-doc-segmented-default',
     '',
     'bm25-doc-tuned',
     'bm25-doc-segmented-tuned',
     'bm25-rm3-doc-tuned',
     'bm25-rm3-doc-segmented-tuned',
     'bm25-rocchio-doc-tuned',
     'bm25-rocchio-doc-segmented-tuned',
     '',
     'bm25-d2q-t5-doc-default',
     'bm25-d2q-t5-doc-segmented-default',
     'bm25-rm3-d2q-t5-doc-default',
     'bm25-rm3-d2q-t5-doc-segmented-default',
     '',
     'bm25-d2q-t5-doc-tuned',
     'bm25-d2q-t5-doc-segmented-tuned',
     'bm25-rm3-d2q-t5-doc-tuned',
     'bm25-rm3-d2q-t5-doc-segmented-tuned',
     '',
     'unicoil-noexp',
     'unicoil-noexp-pytorch',
     '',
     'unicoil',
     'unicoil-pytorch'],

    # MS MARCO v2 passage
    'msmarco-v2-passage':
    ['bm25-default',
     'bm25-augmented-default',
     'bm25-rm3-default',
     'bm25-rm3-augmented-default',
     '',
     'bm25-d2q-t5-default',
     'bm25-d2q-t5-augmented-default',
     'bm25-rm3-d2q-t5-default',
     'bm25-rm3-d2q-t5-augmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf',
     'slimr-pp'],

    # MS MARCO v2 doc
    'msmarco-v2-doc':
    ['bm25-doc-default',
     'bm25-doc-segmented-default',
     'bm25-rm3-doc-default',
     'bm25-rm3-doc-segmented-default',
     '',
     'bm25-d2q-t5-doc-default',
     'bm25-d2q-t5-doc-segmented-default',
     'bm25-rm3-d2q-t5-doc-default',
     'bm25-rm3-d2q-t5-doc-segmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'
     ]
}

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
            'R@1K': '-c -l 2 -m recall.1000'
        },
        'dl22-passage': {
            'MAP@100': '-c -l 2 -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -l 2 -m recall.1000'
        },
        'dl23-passage': {
            'MAP@100': '-c -l 2 -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
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
            'R@1K': '-c -m recall.1000'
        },
        'dl22-doc': {
            'MAP@100': '-c -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -m recall.1000'
        },
        'dl23-doc': {
            'MAP@100': '-c -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -m recall.1000'
        }
    }
}


def find_msmarco_table_topic_set_key_v1(topic_key):
    # E.g., we want to map variants like 'dl19-passage-unicoil' and 'dl19-passage' both into 'dl19'
    key = ''
    if topic_key.startswith('dl19'):
        key = 'dl19'
    elif topic_key.startswith('dl20'):
        key = 'dl20'
    elif topic_key.startswith('msmarco'):
        key = 'dev'

    return key


def find_msmarco_table_topic_set_key_v2(topic_key):
    key = ''
    if topic_key.endswith('dev') or topic_key.endswith('dev-unicoil') or topic_key.endswith('dev-unicoil-noexp'):
        key = 'dev'
    elif topic_key.endswith('dev2') or topic_key.endswith('dev2-unicoil') or topic_key.endswith('dev2-unicoil-noexp'):
        key = 'dev2'
    elif topic_key.startswith('dl21'):
        key = 'dl21'
    elif topic_key.startswith('dl22'):
        key = 'dl22'
    elif topic_key.startswith('dl23'):
        key = 'dl23'

    return key


def format_eval_command(raw):
    return raw.replace('run.', '\\\n  run.')


def format_command(raw):
    # Format hybrid commands differently.
    if 'pyserini.search.hybrid' in raw:
        return raw.replace('dense', '\\\n  dense ') \
                .replace('--encoder', '\\\n         --encoder') \
                .replace('sparse', '\\\n  sparse') \
                .replace('fusion', '\\\n  fusion') \
                .replace('run --', '\\\n  run    --') \
                .replace('--topics ', '\\\n         --topics ') \
                .replace('--output ', '\\\n         --output ')

    # After "--output foo.txt" are additional options like "--hits 1000 --impact".
    # We want these on a separate line for better readability, but note that sometimes that might
    # be the end of the command, in which case we don't want to add an extra line break.
    return raw.replace('--topics', '\\\n  --topics') \
        .replace('--threads', '\\\n  --threads') \
        .replace('--index', '\\\n  --index') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--encoder', '\\\n  --encoder') \
        .replace('--onnx-encoder', '\\\n  --onnx-encoder') \
        .replace('--encoded-corpus', '\\\n  --encoded-corpus') \
        .replace('.txt ', '.txt \\\n  ')


def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr")/f, 'r')
    text = fin.read()
    fin.close()

    return text


def list_conditions(args):
    for condition in models[args.collection]:
        if condition == '':
            continue
        print(condition)


def _get_display_num(num: int) -> str:
    return f'{num:.4f}' if num != 0 else '-'


def _remove_commands(table, name, s, v1):
    v1_unavilable_dict = {
        ('dl19', 'MAP'): 'Command to generate run on TREC 2019 queries:.*?</div>',
        ('dl20', 'MAP'): 'Command to generate run on TREC 2020 queries:.*?</div>',
        ('dev', 'MRR@10'): 'Command to generate run on dev queries:.*?</div>',
    }
    v2_unavilable_dict = {
        ('dl21', 'MAP@100'): 'Command to generate run on TREC 2021 queries:.*?</div>',
        ('dl22', 'MAP@100'): 'Command to generate run on TREC 2022 queries:.*?</div>',
        ('dl23', 'MAP@100'): 'Command to generate run on TREC 2023 queries:.*?</div>',
        ('dev', 'MRR@100'): 'Command to generate run on dev queries:.*?</div>',
        ('dev2', 'MRR@100'): 'Command to generate run on dev2 queries:.*?</div>',
    }
    unavilable_dict = v1_unavilable_dict if v1 else v2_unavilable_dict
    for k, v in unavilable_dict.items():
        if table[name][k[0]][k[1]] == 0:
            s = re.sub(re.compile(v, re.MULTILINE | re.DOTALL), 'Not available.</div>', s)
    return s


def generate_report(args):
    yaml_file = importlib.resources.files("pyserini.2cr")/f'{args.collection}.yaml'

    if args.collection == 'msmarco-v1-passage':
        html_template = read_file('msmarco_html_v1_passage.template')
        row_template = read_file('msmarco_html_row_v1.template')
    elif args.collection == 'msmarco-v1-doc':
        html_template = read_file('msmarco_html_v1_doc.template')
        row_template = read_file('msmarco_html_row_v1.template')
    elif args.collection == 'msmarco-v2-passage':
        html_template = read_file('msmarco_html_v2_passage.template')
        row_template = read_file('msmarco_html_row_v2.template')
    elif args.collection == 'msmarco-v2-doc':
        html_template = read_file('msmarco_html_v2_doc.template')
        row_template = read_file('msmarco_html_row_v2.template')
    else:
        raise ValueError(f'Unknown corpus: {args.collection}')

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    table_keys = {}
    row_ids = {}

    with open(yaml_file) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            display = condition['display-html']
            row_id = condition['display-row'] if 'display-row' in condition else ''
            cmd_template = condition['command']

            row_ids[name] = row_id
            table_keys[name] = display

            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
                    short_topic_key = find_msmarco_table_topic_set_key_v1(topic_key)
                else:
                    short_topic_key = find_msmarco_table_topic_set_key_v2(topic_key)

                runfile = f'run.{args.collection}.{name}.{short_topic_key}.txt'
                cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile,
                                                        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                                        dense_threads=dense_threads, dense_batch_size=dense_batch_size)
                commands[name][short_topic_key] = cmd

                for expected in topic_set['scores']:
                    for metric in expected:
                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[args.collection][eval_key][metric]} {eval_key} {runfile}'
                        eval_commands[name][short_topic_key] += eval_cmd + '\n'
                        table[name][short_topic_key][metric] = expected[metric]

    if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
        row_cnt = 1

        html_rows = []
        for name in models[args.collection]:
            if not name:
                # Add blank row for spacing
                html_rows.append('<tr><td style="border-bottom: 0"></td></tr>')
                continue
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             condition_name=table_keys[name],
                             row=row_ids[name],
                             s1=_get_display_num(table[name]["dl19"]["MAP"]),
                             s2=_get_display_num(table[name]["dl19"]["nDCG@10"]),
                             s3=_get_display_num(table[name]["dl19"]["R@1K"]),
                             s4=_get_display_num(table[name]["dl20"]["MAP"]),
                             s5=_get_display_num(table[name]["dl20"]["nDCG@10"]),
                             s6=_get_display_num(table[name]["dl20"]["R@1K"]),
                             s7=_get_display_num(table[name]["dev"]["MRR@10"]),
                             s8=_get_display_num(table[name]["dev"]["R@1K"]),
                             cmd1=format_command(commands[name]['dl19']),
                             cmd2=format_command(commands[name]['dl20']),
                             cmd3=format_command(commands[name]['dev']),
                             eval_cmd1=format_eval_command(eval_commands[name]['dl19']),
                             eval_cmd2=format_eval_command(eval_commands[name]['dl20']),
                             eval_cmd3=format_eval_command(eval_commands[name]['dev']))

            # If we don't have scores, we want to remove the commands also. Use simple regexp substitution.
            s = _remove_commands(table, name, s, v1=True)

            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        if args.collection == 'msmarco-v1-passage':
            full_name = 'MS MARCO V1 Passage'
        else:
            full_name = 'MS MARCO V1 Document'

        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title=full_name, rows=all_rows))
    else:
        row_cnt = 1

        html_rows = []
        for name in models[args.collection]:
            if not name:
                # Add blank row for spacing
                html_rows.append('<tr><td style="border-bottom: 0"></td></tr>')
                continue
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             condition_name=table_keys[name],
                             row=row_ids[name],
                             s1=_get_display_num(table[name]["dl21"]["MAP@100"]),
                             s2=_get_display_num(table[name]["dl21"]["nDCG@10"]),
                             s3=_get_display_num(table[name]["dl21"]["R@1K"]),
                             s4=_get_display_num(table[name]["dl22"]["MAP@100"]),
                             s5=_get_display_num(table[name]["dl22"]["nDCG@10"]),
                             s6=_get_display_num(table[name]["dl22"]["R@1K"]),
                             s7=_get_display_num(table[name]["dl23"]["MAP@100"]),
                             s8=_get_display_num(table[name]["dl23"]["nDCG@10"]),
                             s9=_get_display_num(table[name]["dl23"]["R@1K"]),
                             s10=_get_display_num(table[name]["dev"]["MRR@100"]),
                             s11=_get_display_num(table[name]["dev"]["R@1K"]),
                             s12=_get_display_num(table[name]["dev2"]["MRR@100"]),
                             s13=_get_display_num(table[name]["dev2"]["R@1K"]),
                             cmd1=format_command(commands[name]['dl21']),
                             cmd2=format_command(commands[name]['dl22']),
                             cmd3=format_command(commands[name]['dl23']),
                             cmd4=format_command(commands[name]['dev']),
                             cmd5=format_command(commands[name]['dev2']),
                             eval_cmd1=eval_commands[name]['dl21'],
                             eval_cmd2=eval_commands[name]['dl22'],
                             eval_cmd3=eval_commands[name]['dl23'],
                             eval_cmd4=eval_commands[name]['dev'],
                             eval_cmd5=eval_commands[name]['dev2']
                             )

            # If we don't have scores, we want to remove the commands also. Use simple regexp substitution.
            s = _remove_commands(table, name, s, v1=False)

            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        if args.collection == 'msmarco-v2-passage':
            full_name = 'MS MARCO V2 Passage'
        else:
            full_name = 'MS MARCO V2 Document'

        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title=full_name, rows=all_rows))


FlakyKey = namedtuple('FlakyKey', ['collection', 'name', 'topic_key', 'metric'])
flaky_dict = {
    # Score differences between runs on Ubuntu and (Jimmy's) Mac Studio
    FlakyKey('msmarco-v1-passage', 'tct_colbert-v2-hnp-avg-prf-pytorch', 'dl20', 'nDCG@10'): 0.0009,
    FlakyKey('msmarco-v1-passage', 'ance-rocchio-prf-pytorch', 'dl19-passage', 'nDCG@10'): 0.0008,
    # Score differences between tuna and linux.cs
    FlakyKey('msmarco-v1-passage', 'ance-rocchio-prf-pytorch', 'dl20', 'R@1K'): 0.0011,
}


def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    table_keys = {}

    yaml_file = importlib.resources.files("pyserini.2cr")/f'{args.collection}.yaml'

    with open(yaml_file) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            # Either we're running all conditions, or running only the condition specified in --condition
            if not args.all:
                if not condition['name'] == args.condition:
                    continue

            name = condition['name']
            display = condition['display']
            cmd_template = condition['command']

            print(f'# Running condition "{name}": {display}\n')
            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
                    short_topic_key = find_msmarco_table_topic_set_key_v1(topic_key)
                else:
                    short_topic_key = find_msmarco_table_topic_set_key_v2(topic_key)

                print(f'  - topic_key: {topic_key}')

                runfile = os.path.join(args.directory, f'run.{args.collection}.{name}.{short_topic_key}.txt')
                cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile,
                                                        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                                        dense_threads=dense_threads, dense_batch_size=dense_batch_size)

                if args.display_commands:
                    print(f'\n```bash\n{format_command(cmd)}\n```\n')

                if not os.path.exists(runfile):
                    if not args.dry_run:
                        os.system(cmd)

                for expected in topic_set['scores']:
                    for metric in expected:
                        table_keys[name] = display
                        if not args.skip_eval:
                            # If the runfile doesn't exist, we can't evaluate.
                            # This would be the case if --dry-run were set.
                            if not os.path.exists(runfile):
                                continue

                            score = float(
                                run_eval_and_return_metric(
                                    metric,
                                    eval_key,
                                    trec_eval_metric_definitions[args.collection][eval_key][metric],
                                    runfile))
                            if math.isclose(score, float(expected[metric])):
                                result_str = ok_str
                            # If results are within 0.0005, just call it "OKish".
                            elif abs(score-float(expected[metric])) <= 0.0005:
                                result_str = okish_str + f' expected {expected[metric]:.4f}'
                            # If there are bigger differences, deal with on a case-by-case basis.
                            elif abs(score-float(expected[metric])) <= \
                                    flaky_dict.get(FlakyKey(collection=args.collection, name=name, topic_key=topic_key, metric=metric), 0):
                                result_str = okish_str + f' expected {expected[metric]:.4f}'
                            else:
                                result_str = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'    {metric:7}: {score:.4f} {result_str}')
                            table[name][short_topic_key][metric] = score
                        else:
                            table[name][short_topic_key][metric] = expected[metric]

                if not args.skip_eval:
                    print('')

    if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
        print(' ' * 74 + 'TREC 2019' + ' ' * 16 + 'TREC 2020' + ' ' * 12 + 'MS MARCO dev')
        print(' ' * 67 + 'MAP    nDCG@10    R@1K    MAP    nDCG@10    R@1K    MRR@10    R@1K')
        print(' ' * 67 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14)

        if args.condition:
            # If we've used --condition to specify a specific condition, print out only that row.
            names = [ args.condition ]
        else:
            # Otherwise, print out all rows
            names = models[args.collection]

        for name in names:
            if not name:
                print('')
                continue
            print(f'{table_keys[name]:65}' +
                  f'{table[name]["dl19"]["MAP"]:8.4f}{table[name]["dl19"]["nDCG@10"]:8.4f}{table[name]["dl19"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dl20"]["MAP"]:8.4f}{table[name]["dl20"]["nDCG@10"]:8.4f}{table[name]["dl20"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev"]["MRR@10"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}')
    else:
        print(' ' * 69 + 'TREC 2021' + ' ' * 16 + 'TREC 2022' +  ' ' * 16 + 'TREC 2023' + ' ' * 12 + 'MS MARCO dev' + ' ' * 5 + 'MS MARCO dev2')
        print(' ' * 62 + 'MAP    nDCG@10    R@1K    MAP    nDCG@10    R@1K    MAP    nDCG@10    R@1K    MRR@100   R@1K    MRR@100   R@1K')
        print(' ' * 62 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14 + '    ' + '-' * 14)

        if args.condition:
            # If we've used --condition to specify a specific condition, print out only that row.
            names = [args.condition]
        else:
            # Otherwise, print out all rows
            names =  models[args.collection]

        for name in names:
            if not name:
                print('')
                continue
            print(f'{table_keys[name]:60}' +
                  f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dl22"]["MAP@100"]:8.4f}{table[name]["dl22"]["nDCG@10"]:8.4f}{table[name]["dl22"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dl23"]["MAP@100"]:8.4f}{table[name]["dl23"]["nDCG@10"]:8.4f}{table[name]["dl23"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}')

    end = time.time()
    start_str = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.utcfromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO corpora.')
    parser.add_argument('--collection', type=str,
                        help='Collection = {v1-passage, v1-doc, v2-passage, v2-doc}.', required=True)
    # To list all conditions
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--all', action='store_true', default=False, help='Run all conditions.')
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)
    parser.add_argument('--dry-run', action='store_true', default=False, help='Print out commands but do not execute.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    parser.add_argument('--display-commands', action='store_true', default=False, help='Display command.')
    args = parser.parse_args()

    if args.collection == 'v1-passage':
        args.collection = 'msmarco-v1-passage'
    elif args.collection == 'v1-doc':
        args.collection = 'msmarco-v1-doc'
    elif args.collection == 'v2-passage':
        args.collection = 'msmarco-v2-passage'
    elif args.collection == 'v2-doc':
        args.collection = 'msmarco-v2-doc'
    else:
        raise ValueError(f'Unknown corpus: {args.collection}')

    if args.list_conditions:
        list_conditions(args)
        sys.exit()

    if args.generate_report:
        if not args.output:
            print(f'Must specify report filename with --output.')
            sys.exit()

        generate_report(args)
        sys.exit()

    if not args.all and not args.condition:
        print(f'Must specify a specific condition using --condition or use --all to run all conditions.')
        sys.exit()

    run_conditions(args)
