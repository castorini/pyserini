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
import importlib.resources
from collections import defaultdict, OrderedDict
from datetime import datetime
from string import Template

import yaml

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str

dense_threads = 16
dense_batch_size = 512
sparse_threads = 16
sparse_batch_size = 128
fusion_tag="rrf-afridpr-bmdt"

languages = [
    ['ha', 'hausa'],
    ['so', 'somali'],
    ['sw', 'swahili'],
    ['yo', 'yoruba']
]

all_splits = {
    'test-a': 'Test Set A',
    'test-a-pools': 'Test Set A (Pools)',
    'test-b': 'Test Set B'
}

html_display = OrderedDict()
# html_display['bm25-mono'] = 'BM25 Monolingual (Human QT)'
html_display['bm25-qt'] = 'BM25 Human QT'
html_display['bm25-dt'] = 'BM25 Machine DT'
html_display['mdpr-tied-pft-msmarco'] = 'mDPR (tied encoders), pre-FT w/ MS MARCO'
html_display['afriberta-pft-msmarco-ft-mrtydi'] = 'AfriBERTa, pre-FT w/ MS MARCO FT w/ latin Mr. TyDi'
html_display['bm25-dt-afriberta-dpr-fusion'] = 'RRF Fusion of BM25 Machine DT and AfriBERTa-DPR'

models = list(html_display)

trec_eval_metric_definitions = {
    'nDCG@20': '-c -m ndcg_cut.20',
    'R@100': '-c -m recall.100',
}


def format_run_command(raw):
    return raw.replace('--lang', '\\\n  --lang') \
        .replace('--encoder', '\\\n  --encoder') \
        .replace('--topics', '\\\n  --topics') \
        .replace('--index', '\\\n  --index') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--runs', '\\\n  --runs ') \
        .replace('--runtag', '\\\n  --runtag ') \
        .replace('--batch ', '\\\n  --batch ') \
        .replace('--threads 12', '--threads 12 \\\n ')


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
    for condition, _ in html_display.items():
        print(condition)
    print('\nLanguages\n---------')
    for language in languages:
        print(language[1])


def print_results(table, metric, split):
    print(f'Metric = {metric}, Split = {split}')
    print(' ' * 32, end='')
    for lang in languages:
        print(f' {lang[1]:4}   ', end='')
    print('')
    for model in models:
        print(f'{model:32}', end='')
        for lang in languages:
            key = f'{model}.{lang[0]}'
            print(f'{table[key][split][metric]:7.4f}', end='   ')
        print('')
    print('')


def generate_table_rows(table, row_template, commands, eval_commands, table_id, split, metric):
    row_cnt = 1
    html_rows = []

    for model in models:
        s = Template(row_template)

        keys = {}
        used_langs = 0
        for lang in languages:
            keys[lang[0]] = f'{model}.{lang[0]}'
            used_langs += 1 if table[keys[lang[0]]][split][metric] != 0 else 0

        sum = table[keys["ha"]][split][metric] + \
              table[keys["so"]][split][metric] + \
              table[keys["sw"]][split][metric] + \
              table[keys["yo"]][split][metric]
        avg = sum / used_langs

        s = s.substitute(table_cnt=table_id,
                         row_cnt=row_cnt,
                         model=html_display[model],
                         Hausa=f'{table[keys["ha"]][split][metric]:.4f}',
                         Somali=f'{table[keys["so"]][split][metric]:.4f}',
                         Swahili=f'{table[keys["sw"]][split][metric]:.4f}',
                         Yoruba=f'{table[keys["yo"]][split][metric]:.4f}',
                         Avg=f'{avg:.4f}',
                         cmd1=f'{commands[keys["ha"]]}',
                         cmd2=f'{commands[keys["so"]]}',
                         cmd3=f'{commands[keys["sw"]]}',
                         cmd4=f'{commands[keys["yo"]]}',
                         eval_cmd1=f'{eval_commands[keys["ha"]][metric]}',
                         eval_cmd2=f'{eval_commands[keys["so"]][metric]}',
                         eval_cmd3=f'{eval_commands[keys["sw"]][metric]}',
                         eval_cmd4=f'{eval_commands[keys["yo"]][metric]}'
                         )

        s = s.replace("0.0000", "--")
        html_rows.append(s)
        row_cnt += 1

    return html_rows


def extract_topic_fn_from_cmd(cmd):
    cmd = cmd.split()
    topic_idx = cmd.index('--topics')
    return cmd[topic_idx + 1]


def generate_report(args):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: '')
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('ciral_html.template')
    table_template = read_file('ciral_html_table.template')
    row_template = read_file('ciral_html_table_row.template')

    with open(importlib.resources.files("pyserini.2cr")/'ciral.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            lang = name.split('.')[-1]
            eval_key = condition['eval_key']
            cmd_template = condition['command']
            is_fusion = 'fusion' in name
            
            display_split = args.display_split

            runfile = os.path.join(args.directory, f'run.ciral.{name}.{display_split}.txt')
            if is_fusion:
                bm25_dt_output = os.path.join(args.directory,
                                            f'run.ciral.bm25-dt.{lang}.{display_split}.txt')
                afriberta_dpr_output = os.path.join(args.directory,
                                            f'run.ciral.afriberta-pft-msmarco-ft-mrtydi.{lang}.{display_split}.txt')
                expected_args = dict(output=runfile, bm25_dt_output=bm25_dt_output, 
                                     afriberta_dpr_output=afriberta_dpr_output, fusion_tag=fusion_tag)
            else:
                expected_args = dict(split=display_split, output=runfile,
                                     sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                     dense_threads=dense_threads, dense_batch_size=dense_batch_size)

            cmd = Template(cmd_template).substitute(**expected_args)
            commands[name] = format_run_command(cmd)

            # for expected in condition['splits'][0]['scores']:
            for split in condition['splits']:
                if split['split'] == display_split:
                    for scores in split['scores']:
                        for metric in scores:
                            table[name][display_split][metric] = scores[metric]

                            eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                    f'{trec_eval_metric_definitions[metric]} {eval_key}-{display_split} {runfile}'
                            eval_commands[name][metric] = format_eval_command(eval_cmd)

        tables_html = []

        # Build the table for nDCG@20, dev queries
        html_rows = generate_table_rows(table, row_template, commands, eval_commands, 1, display_split, 'nDCG@20')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc=f'nDCG@20, {all_splits[display_split]}', 
                                                               rows=all_rows))

        # Build the table for R@100, dev queries
        html_rows = generate_table_rows(table, row_template, commands, eval_commands, 3, display_split, 'R@100')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc=f'Recall@100, {all_splits[display_split]}', 
                                                               rows=all_rows))

    with open(args.output, 'w') as out:
        out.write(Template(html_template).substitute(title='CIRAL', tables=' '.join(tables_html)))


def run_conditions(args):

    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open(importlib.resources.files("pyserini.2cr")/'ciral.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            encoder = name.split('.')[0]
            lang = name.split('.')[-1]

            lang_name = [item[1] for item in languages 
                         if item[0] == lang][0]
            if args.all:
                pass
            elif args.condition != encoder:
                continue
            elif args.language and args.language != lang_name:
                continue
            eval_key = condition['eval_key']
            cmd_template = condition['command']

            # split = "dev"
            print(f'condition {name}:')
            is_fusion = 'fusion' in name

            for splits in condition['splits']:
                split = splits['split']
                print(f'  - split: {split}')
                
                if split.endswith('pools'):
                    test_split = "test-a"
                else:
                    test_split = split
                runfile = os.path.join(args.directory, f'run.ciral.{name}.{split}.txt')
                if is_fusion:
                    bm25_dt_output = os.path.join(args.directory,
                                                f'run.ciral.bm25-dt.{lang}.{split}.txt')
                    afriberta_dpr_output = os.path.join(args.directory,
                                                f'run.ciral.afriberta-pft-msmarco-ft-mrtydi.{lang}.{split}.txt')
                    cmd = Template(cmd_template).substitute(split=test_split, output=runfile, 
                                                            bm25_dt_output=bm25_dt_output, afriberta_dpr_output=afriberta_dpr_output, fusion_tag=fusion_tag)
                else:
                    cmd = Template(cmd_template).substitute(split=test_split, output=runfile,
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
                            else:
                                result_str = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result_str}')
                            table[name][split][metric] = score
                        else:
                            table[name][split][metric] = expected[metric]

                print('')

    for metric in ['nDCG@20', 'R@100']:
        for split in ['test-a', 'test-b']: # To add test later 
            print_results(table, metric, split)

    end = time.time()

    start_str = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.utcfromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for CIRAL.')
    parser.add_argument('--condition', type=str, help='Condition to run', required=False)
    # To list all conditions
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--display-split', type=str, help='Split to generate report on.', default='test-b', required=False)
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
