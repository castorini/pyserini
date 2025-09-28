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

from ._base import fail_str, ok_str, okish_str, run_eval_and_return_metric

trec_eval_metric_definitions = {
    # Default metrics for most datasets
    "default": {
        "R@1": "-c -m recall.1",
        "R@5": "-c -m recall.5",
        "R@10": "-c -m recall.10",
    },
    # Special metrics for fashion datasets
    "fashion200k_task0": {
        "R@10": "-c -m recall.10",
        "R@20": "-c -m recall.20",
        "R@50": "-c -m recall.50",
    },
    "fashion200k_task3": {
        "R@10": "-c -m recall.10",
        "R@20": "-c -m recall.20",
        "R@50": "-c -m recall.50",
    },
    "fashioniq_task7": {
        "R@10": "-c -m recall.10",
        "R@20": "-c -m recall.20",
        "R@50": "-c -m recall.50",
    },
}


def format_run_command(raw):
    return (
        raw.replace("--topics", "\\\n  --topics")
        .replace('--encoder', '\\\n  --encoder')
        .replace("--index", "\\\n  --index")
        .replace("--output-format", "\\\n  --output-format")
        .replace("--output ", "\\\n  --output ")
        .replace("--hits ", "\\\n  --hits ")
        .replace("--remove-query", "\\\n  --remove-query")
        .replace("--fp16", "\\\n  --fp16")
        .replace("--device", "\\\n  --device")
    )

def format_eval_command(raw):
    return raw.replace("-c ", "\\\n  -c ").replace("run.", "\\\n  run.")

def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr") / f, "r")
    text = fin.read()
    fin.close()
    return text


def get_metrics_for_dataset(dataset_name):
    if dataset_name in ["fashion200k_task0", "fashion200k_task3", "fashioniq_task7"]:
        return trec_eval_metric_definitions[dataset_name]
    else:
        return trec_eval_metric_definitions["default"]

def fix_qrels(dataset_name):
    qrels_file = f'qrels/test/mbeir_{dataset_name}_test_qrels.txt'
    fixed_qrels_file = f'qrels/test/mbeir_{dataset_name}_test_fixed_qrels.txt'
    with open(qrels_file, 'r') as infile, open(fixed_qrels_file, 'w') as outfile:
        for line in infile:
            fields = line.strip().split(' ')[:4]
            outfile.write(' '.join(fields) + '\n')
    return fixed_qrels_file

def list_conditions():  
    with importlib.resources.files('pyserini.2cr').joinpath('m-beir.yaml').open('r') as f:  
        yaml_data = yaml.safe_load(f)  
        for condition in yaml_data['conditions']:  
            print(condition['name'])

def print_results_by_metric_position(table, position, metric_name):
    print(f'Metric = {metric_name}')
    print(' ' * 20, end='')
    conditions = ['clip-sf-large', 'blip-ff-large']
    for condition in conditions:
        print(f'{condition:15}', end='')
    print('')

    for dataset in sorted(table.keys()):
        print(f'{dataset:20}', end='')
        dataset_metrics = get_metrics_for_dataset(dataset)
        metric_list = list(dataset_metrics.keys())

        actual_metric = metric_list[position] if position < len(metric_list) else None

        for condition in conditions:
            if actual_metric and actual_metric in table[dataset][condition]:
                score = table[dataset][condition][actual_metric]
            else:
                score = 0.0
            print(f'{score:8.4f}' + ' ' * 7, end='')
        print('')
    print('')

def run_conditions(args):  
    start = time.time()  
      
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))  
      
    with importlib.resources.files('pyserini.2cr').joinpath('m-beir.yaml').open('r') as f:  
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
                  
                if args.dataset and args.dataset != dataset:  
                    continue  
                      
                print(f'  - Dataset: {dataset}')  
                  
                runfile = os.path.join(args.directory, f'run.m-beir-{dataset}.{name}.txt')  
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile)  
                  
                if args.display_commands:  
                    print(f'\n```bash\n{format_run_command(cmd)}\n```\n')  
                      
                if not os.path.exists(runfile):  
                    if not args.dry_run:  
                        os.system(cmd)  
                          
                dataset_metrics = get_metrics_for_dataset(dataset)
                fixed_qrels = fix_qrels(dataset)
                  
                for expected in datasets['scores']:  
                    for metric in expected:  
                        if not args.skip_eval and not args.dry_run:
                            if not os.path.exists(runfile):  
                                continue  
                                  
                            score = float(run_eval_and_return_metric(  
                                metric, fixed_qrels,
                                dataset_metrics[metric], runfile))  
                                  
                            if math.isclose(score, float(expected[metric])):  
                                result = ok_str  
                            elif abs(score - float(expected[metric])) <= 0.0005:  
                                result = okish_str + f' expected {expected[metric]:.4f}'  
                            else:  
                                result = fail_str + f' expected {expected[metric]:.4f}'  
                            print(f'      {metric:7}: {score:.4f} {result}')  
                              
                            table[dataset][name][metric] = score  
                        else:  
                            table[dataset][name][metric] = expected[metric]  
                              
            print('')  
    
    print_results_by_metric_position(table, 0, 'Metric 1 (R@1 for most datasets, R@10 for fashion datasets)')
    print_results_by_metric_position(table, 1, 'Metric 2 (R@5 for most datasets, R@20 for fashion datasets)')
    print_results_by_metric_position(table, 2, 'Metric 3 (R@10 for most datasets, R@50 for fashion datasets)')

    end = time.time()  
    start_str = datetime.fromtimestamp(start, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')  
    end_str = datetime.fromtimestamp(end, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')  
      
    print('\n')  
    print(f'Start time: {start_str}')  
    print(f'End time: {end_str}')  
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


def generate_report(args):    
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))    
    commands = defaultdict(lambda: defaultdict(lambda: ''))    
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))    
        
    html_template = read_file('m-beir_html.template')    
    row_template = read_file('m-beir_html_row.template')    
        
    with importlib.resources.files('pyserini.2cr').joinpath('m-beir.yaml').open('r') as f:    
        yaml_data = yaml.safe_load(f)    
        for condition in yaml_data['conditions']:    
            name = condition['name']    
            cmd_template = condition['command']    
                
            for datasets in condition['datasets']:    
                dataset = datasets['dataset']    
                    
                runfile = os.path.join(args.directory, f'run.m-beir-{dataset}.{name}.txt')    
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile)    
                commands[dataset][name] = format_run_command(cmd)    
                    
                dataset_metrics = get_metrics_for_dataset(dataset)    
                fixed_qrels = f'qrels/test/mbeir_{dataset}_test_fixed_qrels.txt' 

                for expected in datasets['scores']:    
                    for metric in expected:    
                        eval_cmd = f'python -m pyserini.eval.trec_eval {dataset_metrics[metric]} {fixed_qrels} {runfile}'  
                        eval_commands[dataset][name] += format_eval_command(eval_cmd) + '\n\n'    
                            
                        table[dataset][name][metric] = expected[metric]    
        
    # Generate HTML rows based on your datasets    
    html_rows = []    
    row_cnt = 1    
        
    for dataset in sorted(table.keys()):  
        # Get dataset-specific metrics to determine the order  
        dataset_metrics = get_metrics_for_dataset(dataset)  
        metric_names = list(dataset_metrics.keys())  
          
        s = Template(row_template)    
        s = s.substitute(    
            row_cnt=row_cnt,    
            dataset=dataset,  
            # CLIP-SF-Large metrics (s1, s2, s3)  
            s1=f'{table[dataset]["clip-sf-large"].get(metric_names[0], 0.0):.4f}',  
            s2=f'{table[dataset]["clip-sf-large"].get(metric_names[1], 0.0):.4f}',  
            s3=f'{table[dataset]["clip-sf-large"].get(metric_names[2], 0.0):.4f}',  
            # BLIP-FF-Large metrics (s4, s5, s6)  
            s4=f'{table[dataset]["blip-ff-large"].get(metric_names[0], 0.0):.4f}',  
            s5=f'{table[dataset]["blip-ff-large"].get(metric_names[1], 0.0):.4f}',  
            s6=f'{table[dataset]["blip-ff-large"].get(metric_names[2], 0.0):.4f}',  
            # Commands for tabbed display  
            cmd1=commands[dataset].get('clip-sf-large', ''),    
            cmd2=commands[dataset].get('blip-ff-large', ''),    
            eval_cmd1=eval_commands[dataset].get('clip-sf-large', '').rstrip(),    
            eval_cmd2=eval_commands[dataset].get('blip-ff-large', '').rstrip()    
        )    
        html_rows.append(s)    
        row_cnt += 1    
        
    all_rows = '\n'.join(html_rows)    
    with open(args.output, 'w') as out:    
        out.write(Template(html_template).substitute(title='M-BEIR Datasets Regressions', rows=all_rows))


if __name__ == '__main__':  
    parser = argparse.ArgumentParser(description='Generate regression matrix for UniIR datasets.')  
      
    parser.add_argument('--list-conditions', action='store_true', default=False,   
                        help='List available conditions.')  
      
    parser.add_argument('--generate-report', action='store_true', default=False,   
                        help='Generate report.')  
    parser.add_argument('--output', type=str, help='File to store report.', required=False)  
      
    parser.add_argument('--all', action='store_true', default=False,   
                        help='Run all conditions.')  
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)  
    parser.add_argument('--dataset', type=str, help='Dataset to run.', required=False)  
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)  
      
    parser.add_argument('--dry-run', action='store_true', default=False,   
                        help='Print out commands but do not execute.')  
    parser.add_argument('--skip-eval', action='store_true', default=False,   
                        help='Skip running trec_eval.')  
    parser.add_argument('--display-commands', action='store_true', default=False,   
                        help='Display command.')  
      
    args = parser.parse_args()  
  
    if args.list_conditions:  
        list_conditions()  
        sys.exit()  
  
    if args.generate_report:  
        if not args.output:  
            print('Must specify report filename with --output.')  
            sys.exit()  
        generate_report(args)  
        sys.exit()  
  
    if not args.all and not args.condition:  
        print('Must specify a specific condition using --condition or use --all to run all conditions.')  
        sys.exit()  
          
    if args.all and (args.condition or args.dataset):  
        print('Specifying --all will run all conditions and datasets')  
        sys.exit()  
  
    run_conditions(args)
