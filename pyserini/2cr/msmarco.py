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
from collections import defaultdict
from string import Template

import pkg_resources
import yaml

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str

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
     'splade-pp-ed-onnx',
     'splade-pp-ed-rocchio-onnx',
     'splade-pp-sd-onnx',
     'splade-pp-sd-rocchio-onnx',
     '',
     'ance',
     'ance-pytorch',
     '',
     'distilbert-kd',
     'distilbert-kd-pytorch',
     'distilbert-kd-tasb',
     'distilbert-kd-tasb-pytorch',
     '',
     'tct_colbert-v2-hnp',
     'tct_colbert-v2-hnp-pytorch',
     '',
     'slimr',
     'slimr-pp',
     '',
     'aggretriever-distilbert-pytorch',
     'aggretriever-cocondenser-pytorch',
     '',
     'openai-ada2',
     'openai-ada2-hyde'],

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
     'unicoil-otf'],

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

    return key


def format_command(raw):
    # After "--output foo.txt" are additional options like "--hits 1000 --impact".
    # We want these on a separate line for better readability, but note that sometimes that might
    # be the end of the command, in which case we don't want to add an extra line break.
    return raw.replace('--topics', '\\\n  --topics') \
        .replace('--threads', '\\\n  --threads')\
        .replace('--index', '\\\n  --index')\
        .replace('--output ', '\\\n  --output ')\
        .replace('--encoder', '\\\n  --encoder')\
        .replace('--onnx-encoder', '\\\n  --onnx-encoder')\
        .replace('--encoded-corpus', '\\\n  --encoded-corpus')\
        .replace('.txt ', '.txt \\\n  ')


def read_file(f):
    fin = open(f, 'r')
    text = fin.read()
    fin.close()

    return text


def list_conditions(args):
    for condition in models[args.collection]:
        if condition == '':
            continue
        print(condition)


def generate_report(args):
    yaml_file = pkg_resources.resource_filename(__name__, f'{args.collection}.yaml')

    if args.collection == 'msmarco-v1-passage':
        html_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_v1_passage.template'))
        row_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_row_v1.template'))
    elif args.collection == 'msmarco-v1-doc':
        html_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_v1_doc.template'))
        row_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_row_v1.template'))
    elif args.collection == 'msmarco-v2-passage':
        html_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_v2_passage.template'))
        row_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_row_v2.template'))
    elif args.collection == 'msmarco-v2-doc':
        html_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_v2_doc.template'))
        row_template = read_file(pkg_resources.resource_filename(__name__, 'msmarco_html_row_v2.template'))
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

            row_ids[name] =row_id
            table_keys[name] = display

            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
                    short_topic_key = find_msmarco_table_topic_set_key_v1(topic_key)
                else:
                    short_topic_key = find_msmarco_table_topic_set_key_v2(topic_key)

                runfile = f'run.{args.collection}.{name}.{short_topic_key}.txt'
                cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile)
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
                             s1=f'{table[name]["dl19"]["MAP"]:.4f}' if table[name]['dl19']['MAP'] != 0 else '-',
                             s2=f'{table[name]["dl19"]["nDCG@10"]:.4f}' if table[name]['dl19']['nDCG@10'] != 0 else '-',
                             s3=f'{table[name]["dl19"]["R@1K"]:.4f}' if table[name]['dl19']['R@1K'] != 0 else '-',
                             s4=f'{table[name]["dl20"]["MAP"]:.4f}' if table[name]['dl20']['MAP'] != 0 else '-',
                             s5=f'{table[name]["dl20"]["nDCG@10"]:.4f}' if table[name]['dl20']['nDCG@10'] != 0 else '-',
                             s6=f'{table[name]["dl20"]["R@1K"]:.4f}' if table[name]['dl20']['R@1K'] != 0 else '-',
                             s7=f'{table[name]["dev"]["MRR@10"]:.4f}' if table[name]['dev']['MRR@10'] != 0 else '-',
                             s8=f'{table[name]["dev"]["R@1K"]:.4f}' if table[name]['dev']['R@1K'] != 0 else '-',
                             cmd1=format_command(commands[name]['dl19']),
                             cmd2=format_command(commands[name]['dl20']),
                             cmd3=format_command(commands[name]['dev']),
                             eval_cmd1=eval_commands[name]['dl19'],
                             eval_cmd2=eval_commands[name]['dl20'],
                             eval_cmd3=eval_commands[name]['dev']
                             )

            # If we don't have scores, we want to remove the commands also. Use simple regexp substitution.
            if table[name]['dl19']['MAP'] == 0:
                s = re.sub(re.compile('Command to generate run on TREC 2019 queries:.*?</div>',
                                      re.MULTILINE | re.DOTALL),
                           'Not available.</div>', s)
            if table[name]['dl20']['MAP'] == 0:
                s = re.sub(re.compile('Command to generate run on TREC 2020 queries:.*?</div>',
                                      re.MULTILINE | re.DOTALL),
                           'Not available.</div>', s)
            if table[name]['dev']['MRR@10'] == 0:
                s = re.sub(re.compile('Command to generate run on dev queries:.*?</div>',
                                      re.MULTILINE | re.DOTALL),
                           'Not available.</div>', s)

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
                             s1=f'{table[name]["dl21"]["MAP@100"]:.4f}',
                             s2=f'{table[name]["dl21"]["nDCG@10"]:.4f}',
                             s3=f'{table[name]["dl21"]["MRR@100"]:.4f}',
                             s4=f'{table[name]["dl21"]["R@100"]:.4f}',
                             s5=f'{table[name]["dl21"]["R@1K"]:.4f}',
                             s6=f'{table[name]["dev"]["MRR@100"]:.4f}',
                             s7=f'{table[name]["dev"]["R@1K"]:.4f}',
                             s8=f'{table[name]["dev2"]["MRR@100"]:.4f}',
                             s9=f'{table[name]["dev2"]["R@1K"]:.4f}',
                             cmd1=format_command(commands[name]['dl21']),
                             cmd2=format_command(commands[name]['dev']),
                             cmd3=format_command(commands[name]['dev2']),
                             eval_cmd1=eval_commands[name]['dl21'],
                             eval_cmd2=eval_commands[name]['dev'],
                             eval_cmd3=eval_commands[name]['dev2']
                             )
            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        if args.collection == 'msmarco-v2-passage':
            full_name = 'MS MARCO V2 Passage'
        else:
            full_name = 'MS MARCO V2 Document'

        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title=full_name, rows=all_rows))


def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    table_keys = {}

    yaml_file = pkg_resources.resource_filename(__name__, f'{args.collection}.yaml')

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

                short_topic_key = ''
                if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
                    short_topic_key = find_msmarco_table_topic_set_key_v1(topic_key)
                else:
                    short_topic_key = find_msmarco_table_topic_set_key_v2(topic_key)

                print(f'  - topic_key: {topic_key}')

                runfile = os.path.join(args.directory, f'run.{args.collection}.{name}.{short_topic_key}.txt')
                cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile)

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
                            # Flaky tests
                            elif args.collection == 'msmarco-v1-passage' \
                                    and topic_key == 'msmarco-passage-dev-subset' and name == 'ance-pytorch' \
                                    and metric == 'MRR@10' and abs(score-float(expected[metric])) <= 0.0001:
                                result_str = okish_str
                            else:
                                result_str = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'    {metric:7}: {score:.4f} {result_str}')
                            table[name][short_topic_key][metric] = score
                        else:
                            table[name][short_topic_key][metric] = expected[metric]

                if not args.skip_eval:
                    print('')

    if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
        print(' ' * 69 + 'TREC 2019' + ' ' * 16 + 'TREC 2020' + ' ' * 12 + 'MS MARCO dev')
        print(' ' * 62 + 'MAP    nDCG@10    R@1K       MAP nDCG@10    R@1K    MRR@10    R@1K')
        print(' ' * 62 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14)

        if args.condition:
            # If we've used --condition to specify a specific condition, print out only that row.
            name = args.condition
            print(f'{table_keys[name]:60}' +
                  f'{table[name]["dl19"]["MAP"]:8.4f}{table[name]["dl19"]["nDCG@10"]:8.4f}{table[name]["dl19"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dl20"]["MAP"]:8.4f}{table[name]["dl20"]["nDCG@10"]:8.4f}{table[name]["dl20"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev"]["MRR@10"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}')
        else:
            # Otherwise, print out all rows
            for name in models[args.collection]:
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

        if args.condition:
            # If we've used --condition to specify a specific condition, print out only that row.
            name = args.condition
            print(f'{table_keys[name]:60}' +
                  f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}' +
                  f'{table[name]["dl21"]["MRR@100"]:8.4f}{table[name]["dl21"]["R@100"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}')
        else:
            # Otherwise, print out all rows
            for name in models[args.collection]:
                if not name:
                    print('')
                    continue
                print(f'{table_keys[name]:60}' +
                      f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}' +
                      f'{table[name]["dl21"]["MRR@100"]:8.4f}{table[name]["dl21"]["R@100"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
                      f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
                      f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}')

    end = time.time()

    print('\n')
    print(f'Total elapsed time: {end - start:.0f}s')


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
