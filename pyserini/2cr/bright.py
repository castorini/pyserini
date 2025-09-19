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
import importlib.resources
import math
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone
from string import Template

import yaml

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str

metrics = ['nDCG@10', 'R@100', 'R@1000']

trec_eval_metric_definitions = {
    'nDCG@10': '-c -m ndcg_cut.10',
    'R@100': '-c -m recall.100',
    'R@1000': '-c -m recall.1000'
}

bright_keys = ['biology', 
             'earth-science', 
             'economics', 
             'psychology', 
             'robotics', 
             'stackoverflow', 
             'sustainable-living', 
             'pony', 
             'leetcode', 
             'aops', 
             'theoremqa-theorems', 
             'theoremqa-questions'
             ]

models = ['bm25', 
          'bm25qs', 
          'splade-v3', 
          'bge-large-en-v1.5.flat']


def format_run_command(raw):
    return raw.replace('--topics', '\\\n  --topics') \
        .replace('--index', '\\\n  --index') \
        .replace('--onnx-encoder', '\\\n  --onnx-encoder') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--output-format trec ', '\\\n  --output-format trec ') \
        .replace('--hits ', '\\\n  --hits ') \


def format_eval_command(raw):
    return raw.replace('-c ', '\\\n  -c ') \
        .replace('run.', '\\\n  run.')


def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr")/f, 'r')
    text = fin.read()
    fin.close()

    return text


def list_conditions():
    with importlib.resources.files('pyserini.2cr').joinpath('bright.yaml').open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            print(condition['name'])


def list_datasets():
    for dataset in bright_keys:
        print(dataset)


def generate_report(args):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('bright_html.template')
    row_template = read_file('bright_html_row.template')

    with importlib.resources.files('pyserini.2cr').joinpath('bright.yaml').open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            cmd_template = condition['command']

            for datasets in condition['datasets']:
                dataset = datasets['dataset']
                runfile = os.path.join(args.directory, f'run.bright.{name}.{dataset}.txt')
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile)
                commands[dataset][name] = format_run_command(cmd)

                for expected in datasets['scores']:
                    for metric in expected:
                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[metric]} bright-{dataset} {runfile}'
                        eval_commands[dataset][name] += format_eval_command(eval_cmd) + '\n\n'
                        
                        table[dataset][name][metric] = expected[metric]

        row_cnt = 1
        main_rows = []
        
        for dataset in bright_keys:
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             dataset=dataset,
                             s1=f'{table[dataset]["bm25"]["nDCG@10"]:8.3f}',
                             s2=f'{table[dataset]["bm25"]["R@100"]:8.3f}',
                             s3=f'{table[dataset]["bm25qs"]["nDCG@10"]:8.3f}',
                             s4=f'{table[dataset]["bm25qs"]["R@100"]:8.3f}',
                             s5=f'{table[dataset]["splade-v3"]["nDCG@10"]:8.3f}',
                             s6=f'{table[dataset]["splade-v3"]["R@100"]:8.3f}',
                             s7=f'{table[dataset]["bge-large-en-v1.5.flat"]["nDCG@10"]:8.3f}',
                             s8=f'{table[dataset]["bge-large-en-v1.5.flat"]["R@100"]:8.3f}',
                             cmd1=commands[dataset]["bm25"],
                             cmd2=commands[dataset]["bm25qs"],
                             cmd3=commands[dataset]["splade-v3"],
                             cmd4=commands[dataset]["bge-large-en-v1.5.flat"],
                             eval_cmd1=eval_commands[dataset]["bm25"].rstrip(),
                             eval_cmd2=eval_commands[dataset]["bm25qs"].rstrip(),
                             eval_cmd3=eval_commands[dataset]["splade-v3"].rstrip(),
                             eval_cmd4=eval_commands[dataset]["bge-large-en-v1.5.flat"].rstrip())
            main_rows.append(s)
            row_cnt += 1
            
        main_rows = '\n'.join(main_rows)
        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title='Pyserini BRIGHT Regressions', main_rows=main_rows))


def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with importlib.resources.files('pyserini.2cr').joinpath('bright.yaml').open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            cmd_template = condition['command']

            if args.all or args.condition == name:
                print(f'condition {name}:')
            else:
                continue

            for datasets in condition['datasets']:
                dataset = datasets['dataset']
                if args.all:
                    pass
                elif args.condition != name:
                    continue
                elif args.dataset and args.dataset != dataset:
                    continue

                print(f'  - dataset: {dataset}')

                runfile = os.path.join(args.directory, f'run.bright.{name}.{dataset}.txt')
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile)
                
                if args.display_commands:
                    print(f'\n```bash\n{format_run_command(cmd)}\n```\n')

                if not os.path.exists(runfile):
                    if not args.dry_run:
                        os.system(cmd)

                for expected in datasets['scores']:
                    for metric in expected:
                        if not args.skip_eval and not args.dry_run:
                            if not os.path.exists(runfile):
                                continue

                            score = float(run_eval_and_return_metric(metric, f'bright-{dataset}',
                                                                     trec_eval_metric_definitions[metric], runfile))
                            if math.isclose(score, float(expected[metric])):
                                result = ok_str
                            # If results are within 0.0005, just call it "OKish".
                            elif abs(score - float(expected[metric])) <= 0.0005:
                                result = okish_str + f' expected {expected[metric]:.4f}'
                            else:
                                result = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result}')

                            table[dataset][name][metric] = score
                        else:
                            table[dataset][name][metric] = expected[metric]
                    print('')

            print('')

    top_level_sums = defaultdict(lambda: defaultdict(float))
    final_scores = defaultdict(lambda: defaultdict(float))

    # Compute the running sums to compute the final mean scores
    for key in bright_keys:
        for model in models:
            for metric in metrics:
                    top_level_sums[model][metric] += table[key][model][metric]

    # Compute the final mean
    for model in models:
        for metric in metrics:
            final_score = top_level_sums[model][metric] / 12
            final_scores[model][metric] = final_score

    print(' ' * 33 + 'BM25' + ' ' * 14 + 'BM25QS' + ' ' * 12 + 'SPLADE' + ' ' * 15 + 'BGE')
    print(' ' * 28 + 'nDCG    R@100      ' * 4)
    print(' ' * 28 + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ')
    for dataset in bright_keys:
        print(f'{dataset:25}' +
              f'{table[dataset]["bm25"]["nDCG@10"]:8.3f}{table[dataset]["bm25"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bm25qs"]["nDCG@10"]:8.3f}{table[dataset]["bm25qs"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["splade-v3"]["nDCG@10"]:8.3f}{table[dataset]["splade-v3"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bge-large-en-v1.5.flat"]["nDCG@10"]:8.3f}{table[dataset]["bge-large-en-v1.5.flat"]["R@100"]:8.3f}   ')
    print(' ' * 28 + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ')
    print('avg' + ' ' * 22 + f'{final_scores["bm25"]["nDCG@10"]:8.3f}{final_scores["bm25"]["R@100"]:8.3f}   ' +
          f'{final_scores["bm25qs"]["nDCG@10"]:8.3f}{final_scores["bm25qs"]["R@100"]:8.3f}   ' +
          f'{final_scores["splade-v3"]["nDCG@10"]:8.3f}{final_scores["splade-v3"]["R@100"]:8.3f}   ' +
          f'{final_scores["bge-large-en-v1.5.flat"]["nDCG@10"]:8.3f}{final_scores["bge-large-en-v1.5.flat"]["R@100"]:8.3f}   ')

    print('\n')

    end = time.time()
    start_str = datetime.fromtimestamp(start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.fromtimestamp(start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for BRIGHT corpora.')
    # To list all conditions/datasets
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    parser.add_argument('--list-datasets', action='store_true', default=False, help='List available datasets.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--all', action='store_true', default=False, help='Run all conditions.')
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)
    parser.add_argument('--dataset', type=str, help='Dataset to run.', required=False)
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)
    parser.add_argument('--dry-run', action='store_true', default=False, help='Print out commands but do not execute.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    parser.add_argument('--display-commands', action='store_true', default=False, help='Display command.')
    args = parser.parse_args()

    if args.list_conditions:
        list_conditions()
        sys.exit()
    
    if args.list_datasets:
        list_datasets()
        sys.exit()

    if args.generate_report:
        if not args.output:
            print(f'Must specify report filename with --output.')
            sys.exit()

        generate_report(args)
        sys.exit()

    if args.condition and args.condition not in models:
        print(f'Invalid condition: {args.condition}')
        sys.exit()

    if not args.all and not args.condition:
        print(f'Must specify a specific condition using --condition or use --all to run all conditions.')
        sys.exit()
        
    if args.all and (args.condition or args.dataset):
        print('Specifying --all will run all conditions and datasets')
        sys.exit()

    run_conditions(args)
