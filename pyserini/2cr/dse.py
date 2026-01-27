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

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str, run_command

def format_run_command(raw):
    return raw.replace('--topics', '\\\n  --topics') \
        .replace('--encoder-class', '\\\n  --encoder-class') \
        .replace('--encoder ', '\\\n  --encoder ') \
        .replace('--pooling', '\\\n  --pooling') \
        .replace('--index', '\\\n  --index') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--hits ', '\\\n  --hits ') \
        .replace('--device', '\\\n  --device') \
        .replace('--batch-size', '\\\n  --batch-size')

def list_conditions():
    with importlib.resources.files('pyserini.2cr').joinpath('dse.yaml').open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            print(condition['name'])

def list_datasets():
    with importlib.resources.files('pyserini.2cr').joinpath('dse.yaml').open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            for dataset in condition['datasets']:
                print(dataset['dataset'])

def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with importlib.resources.files('pyserini.2cr').joinpath('dse.yaml').open('r') as f:
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

                runfile = os.path.join(args.directory, f'run.dse.{name}.{dataset}.txt')

                index_name = datasets.get('index', f'indexes/{dataset}.dse')
                topics_name = datasets.get('topics', dataset)
                cmd = Template(cmd_template).substitute(dataset=dataset, index=index_name, topics=topics_name, output=runfile)

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
                            
                            score = 0
                            if dataset == 'wiki-ss-nq':
                                # Custom evaluation for Wiki-SS
                                k = int(metric.split('-')[1])
                                eval_cmd = f'python scripts/dse/evaluate_wiki_ss_run.py --run_file {runfile} --k {k}'
                                out, err = run_command(eval_cmd)
                                # Parse "Top-k Accuracy: 0.43"
                                for line in out.split('\n'):
                                    if "Top-k Accuracy:" in line:
                                        score = float(line.split(':')[-1].strip()) * 100
                                        break
                            
                            else:
                                # Standard trec_eval
                                trec_eval_metric = ''
                                if metric == 'nDCG@10':
                                    trec_eval_metric = '-c -m ndcg_cut.10'
                                elif metric == 'Recall@10':
                                    trec_eval_metric = '-c -m recall.10'
                                
                                score = float(run_eval_and_return_metric(metric, dataset, trec_eval_metric, runfile)) * 100


                            if math.isclose(score, float(expected[metric]), abs_tol=0.1): 
                                result = ok_str
                            elif abs(score - float(expected[metric])) <= 0.5:
                                result = okish_str + f' expected {expected[metric]:.1f}'
                            else:
                                result = fail_str + f' expected {expected[metric]:.1f}'
                            
                            print(f'      {metric:10}: {score:6.2f} {result}')
                            table[dataset][name][metric] = score
                        else:
                            table[dataset][name][metric] = expected[metric]
                    print('')

            print('')

    end = time.time()
    start_str = datetime.fromtimestamp(start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.fromtimestamp(end, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr")/f, 'r')
    text = fin.read()
    fin.close()

    return text

def generate_report(args):
    
    html_template = read_file('dse_html.template')
    row_template = read_file('dse_html_row.template')

    wiki_rows = []
    slide_rows = []
    
    row_cnt = 1

    with importlib.resources.files('pyserini.2cr').joinpath('dse.yaml').open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name'] # dse
            cmd_template = condition['command']

            for datasets in condition['datasets']:
                dataset = datasets['dataset']
                
                runfile = os.path.join(args.directory, f'run.dse.{name}.{dataset}.txt')
                index_name = datasets.get('index', f'indexes/{dataset}.dse')
                topics_name = datasets.get('topics', dataset)
                cmd = Template(cmd_template).substitute(dataset=dataset, index=index_name, topics=topics_name, output=runfile)
                
                cmd = format_run_command(cmd)

                # Eval command generation
                eval_cmds = []
                score_cells = ""
                
                for expected_map in datasets['scores']:
                     
                     if dataset == 'wiki-ss-nq':
                         metrics_order = ['Top-1', 'Top-5', 'Top-10', 'Top-20']
                     else:
                         metrics_order = ['nDCG@10', 'Recall@10']

                     for metric in metrics_order:
                         score = expected_map.get(metric, 0.0)
                         score_cells += f'<td>{score:.1f}</td>\n'
                         
                         if dataset == 'wiki-ss-nq':
                            k = int(metric.split('-')[1])
                            eval_cmd = f'python scripts/dse/evaluate_wiki_ss_run.py --run_file {runfile} --k {k}'
                         else:
                            trec_eval_metric = ''
                            if metric == 'nDCG@10':
                                trec_eval_metric = '-c -m ndcg_cut.10'
                            elif metric == 'Recall@10':
                                trec_eval_metric = '-c -m recall.10'
                            eval_cmd = f'python -m pyserini.eval.trec_eval {trec_eval_metric} {dataset} {runfile}'
                         
                         eval_cmds.append(eval_cmd)

                # Format eval commands
                eval_cmds_str = '\n'.join(eval_cmds)

                s = Template(row_template)
                s = s.substitute(row_cnt=row_cnt,
                                 dataset=dataset,
                                 score_cells=score_cells,
                                 cmd=cmd,
                                 eval_cmd=eval_cmds_str)

                if dataset == 'wiki-ss-nq':
                    wiki_rows.append(s)
                else:
                    slide_rows.append(s)
                
                row_cnt += 1

    with open(args.output, 'w') as out:
        out.write(Template(html_template).substitute(title='Pyserini DSE Reproductions', 
                                                     wiki_rows='\n'.join(wiki_rows), 
                                                     slide_rows='\n'.join(slide_rows)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run DSE 2CR experiments.')
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    parser.add_argument('--list-datasets', action='store_true', default=False, help='List available datasets.')
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    parser.add_argument('--all', action='store_true', default=False, help='Run all conditions.')
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)
    parser.add_argument('--dataset', type=str, help='Dataset to run.', required=False)
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)
    parser.add_argument('--dry-run', action='store_true', default=False, help='Print out commands but do not execute.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running evaluation.')
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

    if not args.all and not args.condition:
        print(f'Must specify a specific condition using --condition or use --all to run all conditions.')
        sys.exit()

    if args.all and (args.condition or args.dataset):
        print('Specifying --all will run all conditions and datasets')
        sys.exit()

    run_conditions(args)
