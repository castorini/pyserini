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
import sys
import time
from collections import defaultdict
from datetime import datetime
from string import Template

import importlib.resources
import yaml

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str

dense_threads = 16
dense_batch_size = 512
sparse_threads = 16
sparse_batch_size = 128

languages = [
    ['ar', 'arabic'],
    ['bn', 'bengali'],
    ['en', 'english'],
    ['fi', 'finnish'],
    ['id', 'indonesian'],
    ['ja', 'japanese'],
    ['ko', 'korean'],
    ['ru', 'russian'],
    ['sw', 'swahili'],
    ['te', 'telugu'],
    ['th', 'thai']
]

models = ['bm25', 'mdpr-split-pft-nq', 'mdpr-tied-pft-nq', 'mdpr-tied-pft-msmarco', 'mdpr-tied-pft-msmarco-ft-all']

html_display = {
    'bm25': 'BM25',
    'mdpr-split-pft-nq': 'mDPR (split) pFT NQ',
    'mdpr-tied-pft-nq': 'mDPR (tied) pFT NQ',
    'mdpr-tied-pft-msmarco': 'mDPR (tied) pFT MS MARCO',
    'mdpr-tied-pft-msmarco-ft-all': 'mDPR (tied) pFT MS MARCO + FT all'
}

trec_eval_metric_definitions = {
    'MRR@100': '-c -M 100 -m recip_rank',
    'R@100': '-c -m recall.100',
}


def format_run_command(raw):
    return raw.replace('--lang', '\\\n  --lang') \
        .replace('--encoder', '\\\n  --encoder') \
        .replace('--topics', '\\\n  --topics') \
        .replace('--index', '\\\n  --index') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--threads ', '\\\n  --threads ')


def format_eval_command(raw):
    return raw.replace('-c ', '\\\n  -c ') \
        .replace(raw.split()[-1], f'\\\n  {raw.split()[-1]}')


def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr")/f, 'r')
    text = fin.read()
    fin.close()

    return text


def list_conditions():
    print('Conditions:\n-----------')
    for condition in models:
        print(condition)
    print('\nLanguages\n---------')
    for language in languages:
        print(language[0])


def print_results(table, metric, split):
    print(f'Metric = {metric}, Split = {split}')
    print(' ' * 32, end='')
    for lang in languages:
        print(f'{lang[0]:3}    ', end='')
    print('')
    for model in models:
        print(f'{model:30}', end='')
        for lang in languages:
            key = f'{model}.{lang[0]}'
            print(f'{table[key][split][metric]:7.3f}', end='')
        print('')
    print('')


def generate_table_rows(table, row_template, commands, eval_commands, table_id, split, metric):
    row_cnt = 1
    html_rows = []

    for model in models:
        s = Template(row_template)

        keys = {}
        for lang in languages:
            keys[lang[0]] = f'{model}.{lang[0]}'

        sum = table[keys["ar"]][split][metric] + \
              table[keys["bn"]][split][metric] + \
              table[keys["en"]][split][metric] + \
              table[keys["fi"]][split][metric] + \
              table[keys["id"]][split][metric] + \
              table[keys["ja"]][split][metric] + \
              table[keys["ko"]][split][metric] + \
              table[keys["ru"]][split][metric] + \
              table[keys["sw"]][split][metric] + \
              table[keys["te"]][split][metric] + \
              table[keys["th"]][split][metric]
        avg = sum / 11

        s = s.substitute(table_cnt=table_id,
                         row_cnt=row_cnt,
                         model=html_display[model],
                         ar=f'{table[keys["ar"]][split][metric]:.3f}',
                         bn=f'{table[keys["bn"]][split][metric]:.3f}',
                         en=f'{table[keys["en"]][split][metric]:.3f}',
                         fi=f'{table[keys["fi"]][split][metric]:.3f}',
                         id=f'{table[keys["id"]][split][metric]:.3f}',
                         ja=f'{table[keys["ja"]][split][metric]:.3f}',
                         ko=f'{table[keys["ko"]][split][metric]:.3f}',
                         ru=f'{table[keys["ru"]][split][metric]:.3f}',
                         sw=f'{table[keys["sw"]][split][metric]:.3f}',
                         te=f'{table[keys["te"]][split][metric]:.3f}',
                         th=f'{table[keys["th"]][split][metric]:.3f}',
                         avg=f'{avg:.3f}',
                         cmd1=f'{commands[keys["ar"]]}',
                         cmd2=f'{commands[keys["bn"]]}',
                         cmd3=f'{commands[keys["en"]]}',
                         cmd4=f'{commands[keys["fi"]]}',
                         cmd5=f'{commands[keys["id"]]}',
                         cmd6=f'{commands[keys["ja"]]}',
                         cmd7=f'{commands[keys["ko"]]}',
                         cmd8=f'{commands[keys["ru"]]}',
                         cmd9=f'{commands[keys["sw"]]}',
                         cmd10=f'{commands[keys["te"]]}',
                         cmd11=f'{commands[keys["th"]]}',
                         eval_cmd1=f'{eval_commands[keys["ar"]][metric]}',
                         eval_cmd2=f'{eval_commands[keys["bn"]][metric]}',
                         eval_cmd3=f'{eval_commands[keys["en"]][metric]}',
                         eval_cmd4=f'{eval_commands[keys["fi"]][metric]}',
                         eval_cmd5=f'{eval_commands[keys["id"]][metric]}',
                         eval_cmd6=f'{eval_commands[keys["ja"]][metric]}',
                         eval_cmd7=f'{eval_commands[keys["ko"]][metric]}',
                         eval_cmd8=f'{eval_commands[keys["ru"]][metric]}',
                         eval_cmd9=f'{eval_commands[keys["sw"]][metric]}',
                         eval_cmd10=f'{eval_commands[keys["te"]][metric]}',
                         eval_cmd11=f'{eval_commands[keys["th"]][metric]}')

        html_rows.append(s)
        row_cnt += 1

    return html_rows


def generate_report(args):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: '')
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('mrtydi_html.template')
    table_template = read_file('mrtydi_html_table.template')
    row_template = read_file('mrtydi_html_table_row.template')

    with open(importlib.resources.files("pyserini.2cr")/'mrtydi.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            eval_key = condition['eval_key']
            cmd_template = condition['command']

            for splits in condition['splits']:
                split = splits['split']

                runfile = os.path.join(args.directory, f'run.mrtydi.{name}.{split}.txt')
                cmd = Template(cmd_template).substitute(split=split, output=runfile,
                                                        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                                        dense_threads=dense_threads, dense_batch_size=dense_batch_size)
                commands[name] = format_run_command(cmd)

                for expected in splits['scores']:
                    for metric in expected:
                        table[name][split][metric] = expected[metric]

                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[metric]} {eval_key}-{split} {runfile}'
                        eval_commands[name][metric] = format_eval_command(eval_cmd)

        tables_html = []

        # Build the table for MRR@100, test queries
        html_rows = generate_table_rows(table, row_template, commands, eval_commands, 1, 'test', 'MRR@100')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc='MRR@100, test queries', rows=all_rows))

        # Build the table for R@100, test queries
        html_rows = generate_table_rows(table, row_template, commands, eval_commands, 2, 'test', 'R@100')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc='Recall@100, test queries', rows=all_rows))

    with open(args.output, 'w') as out:
        out.write(Template(html_template).substitute(title='Mr.TyDi', tables=' '.join(tables_html)))


def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open(importlib.resources.files("pyserini.2cr")/'mrtydi.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            encoder = name.split('.')[0]
            lang = name.split('.')[-1]
            if args.all:
                pass
            elif args.condition != encoder:
                continue
            elif args.language and args.language != lang:
                continue
            eval_key = condition['eval_key']
            cmd_template = condition['command']

            print(f'condition {name}:')

            for splits in condition['splits']:
                split = splits['split']

                print(f'  - split: {split}')

                runfile = os.path.join(args.directory, f'run.mrtydi.{name}.{split}.txt')
                cmd = Template(cmd_template).substitute(split=split, output=runfile,
                                                        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                                        dense_threads=dense_threads, dense_batch_size=dense_batch_size)

                if args.display_commands:
                    print(f'\n```bash\n{format_run_command(cmd)}\n```\n')

                if not os.path.exists(runfile):
                    if not args.dry_run:
                        os.system(cmd)

                for expected in splits['scores']:
                    for metric in expected:
                        if not args.skip_eval:
                            if not os.path.exists(runfile):
                                continue

                            score = float(run_eval_and_return_metric(metric, f'{eval_key}-{split}',
                                                                     trec_eval_metric_definitions[metric], runfile))

                            if math.isclose(score, float(expected[metric])):
                                result_str = ok_str
                            # If results are within 0.0005, just call it "OKish".
                            elif math.isclose(score, float(expected[metric]), abs_tol=5e-4):
                                result_str = okish_str + f' expected {expected[metric]:.4f}'
                            else:
                                result_str = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result_str}')
                            table[name][split][metric] = score
                        else:
                            table[name][split][metric] = expected[metric]

            print('')

    for metric in ['MRR@100', 'R@100']:
        for split in ['test', 'dev', 'train']:
            print_results(table, metric, split)

    end = time.time()
    start_str = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.utcfromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MIRACL.')
    parser.add_argument('--condition', type=str,
                        help='Condition to run', required=False)
    # To list all conditions
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--all', action='store_true', default=False, help='Run using all languages.')
    parser.add_argument('--language', type=str, help='Language to run.', required=False)
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)
    parser.add_argument('--dry-run', action='store_true', default=False, help='Print out commands but do not execute.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    parser.add_argument('--display-commands', action='store_true', default=False, help='Display command.')
    args = parser.parse_args()

    if args.list_conditions:
        list_conditions()
        sys.exit()

    if args.generate_report:
        if not args.output:
            print(f'Must specify report filename with --output.')
            sys.exit()

        generate_report(args)
        sys.exit()

    if args.all and (args.condition or args.language):
        print('Specifying --all will run all conditions and languages')
        sys.exit()

    run_conditions(args)
