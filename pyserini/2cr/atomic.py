import argparse
import os
import sys
from collections import defaultdict
from string import Template
import importlib.resources
import time
import yaml
import math
from ._base import run_eval_and_return_metric, ok_str, fail_str


atomic_models = [
    'ViT-L-14.laion2b_s32b_b82k',
    'ViT-H-14.laion2b_s32b_b79k', 
    'ViT-bigG-14.laion2b_s39b_b160k', 
    'ViT-B-32.laion2b_e16', 
    'ViT-B-32.laion400m_e32', 
    'openai.clip-vit-base-patch32', 
    'openai.clip-vit-large-patch14', 
    'Salesforce.blip-itm-base-coco', 
    'Salesforce.blip-itm-large-coco', 
    'facebook.flava-full',
]

trec_eval_metric_definitions = {
    'MRR@10': '-c -m recip_rank -M 10',
    'R@10': '-c -m recall.10',
    'R@1000': '-c -m recall.1000'
}

def format_run_command(raw):
    return raw.replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--encoded-queries', '\\\n  --encoded-queries')\
        .replace('--output ', '\\\n  --output ')\
        .replace('--hits ', '\\\n  --hits ')


def format_eval_command(raw):
    return raw.replace('-c ', '\\\n  -c ')\
        .replace('run.', '\\\n  run.')

def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr")/f, 'r')
    text = fin.read()
    fin.close()

    return text

def list_models():
    for model in atomic_models:
        print(model)

def get_conditions():
    with open(importlib.resources.files("pyserini.2cr")/'atomic.yaml') as f:
        yaml_data = yaml.safe_load(f)
    
    return [condition['name'] for condition in yaml_data['conditions']]

def list_conditions():
    with open(importlib.resources.files("pyserini.2cr")/'atomic.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            print(condition['name'])
    

def print_results(table, metric):
    print(f'Metric = {metric}')
    print(' ' * 35, end='')
    conditions = get_conditions()
    for condition in conditions:
        print(f'{condition}' + ' ' * 5, end='')
    print('')
    for model in atomic_models:
        print(f'{model:35}', end='')
        for condition in conditions:
            print(f'{table[model][condition][metric]:.3f}' + ' ' * len(condition), end='')
        print('')
    print('')

def generate_report(args):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('atomic_html.template')
    row_template = read_file('atomic_html_row.template')

    with open(importlib.resources.files("pyserini.2cr")/'atomic.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            retrieval_type = name.split('-')[1] # t2i or i2t
            cmd_template = condition['command']

            for models in condition['models']:
                model = models['model']

                runfile = os.path.join(args.directory, f'run.atomic.{model}.{name}.trec')
                cmd = Template(cmd_template).substitute(model=model, output=runfile)
                commands[model][name] = format_run_command(cmd)

                for expected in models['scores']:
                    for metric in expected:
                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[metric]} atomic.validation.{retrieval_type} {runfile}'
                        eval_commands[model][name] += format_eval_command(eval_cmd) + '\n\n'

                        table[model][name][metric] = expected[metric]
        
        row_cnt = 1
        html_rows = []
        for model in atomic_models:
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             model=model,
                             s1=f'{table[model]["large-t2i"]["MRR@10"]:8.4f}',
                             s2=f'{table[model]["large-t2i"]["R@10"]:8.4f}',
                             s3=f'{table[model]["large-t2i"]["R@1000"]:8.4f}',
                             s4=f'{table[model]["large-i2t"]["MRR@10"]:8.4f}',
                             s5=f'{table[model]["large-i2t"]["R@10"]:8.4f}',
                             s6=f'{table[model]["large-i2t"]["R@1000"]:8.4f}',
                             s7=f'{table[model]["base-t2i"]["MRR@10"]:8.4f}',
                             s8=f'{table[model]["base-t2i"]["R@10"]:8.4f}',
                             s9=f'{table[model]["base-t2i"]["R@1000"]:8.4f}',
                             s10=f'{table[model]["base-i2t"]["MRR@10"]:8.4f}',
                             s11=f'{table[model]["base-i2t"]["R@10"]:8.4f}',
                             s12=f'{table[model]["base-i2t"]["R@1000"]:8.4f}',
                             s13=f'{table[model]["small-t2i"]["MRR@10"]:8.4f}',
                             s14=f'{table[model]["small-t2i"]["R@10"]:8.4f}',
                             s15=f'{table[model]["small-t2i"]["R@1000"]:8.4f}',
                             s16=f'{table[model]["small-i2t"]["MRR@10"]:8.4f}',
                             s17=f'{table[model]["small-i2t"]["MRR@10"]:8.4f}',
                             s18=f'{table[model]["small-i2t"]["R@1000"]:8.4f}',
                             cmd1=commands[model]["large-t2i"],
                             cmd2=commands[model]["large-i2t"],
                             cmd3=commands[model]["base-t2i"],
                             cmd4=commands[model]["base-i2t"],
                             cmd5=commands[model]["small-t2i"],
                             cmd6=commands[model]["small-i2t"],
                             eval_cmd1=eval_commands[model]["large-t2i"].rstrip(),
                             eval_cmd2=eval_commands[model]["large-i2t"].rstrip(),
                             eval_cmd3=eval_commands[model]["base-t2i"].rstrip(),
                             eval_cmd4=eval_commands[model]["base-i2t"].rstrip(),
                             eval_cmd5=eval_commands[model]["small-t2i"].rstrip(),
                             eval_cmd6=eval_commands[model]["small-i2t"].rstrip(),
                             )

            s = s.replace("0.0000", "----")
            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title='AToMiC', rows=all_rows))

def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open(importlib.resources.files("pyserini.2cr")/'atomic.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            retrieval_type = name.split('-')[1] # t2i or i2t
            cmd_template = condition['command']

            if args.all or args.condition == name:
                print(f'condition {name}:')
            else:
                continue

            for models in condition['models']:
                model = models['model']
                
                if args.all:
                    pass
                elif args.condition != name:
                    continue
                elif args.model and args.model != model:
                    continue

                print(f'  - Model: {model}')

                runfile = os.path.join(args.directory, f'run.atomic.{model}.{name}.txt')
                cmd = Template(cmd_template).substitute(model=model, output=runfile)
                
                if args.display_commands:
                    print(f'\n```bash\n{format_run_command(cmd)}\n```\n')

                if not os.path.exists(runfile):
                    if not args.dry_run:
                        os.system(cmd)

                for expected in models['scores']:
                    for metric in expected:
                        if not args.skip_eval:
                            if not os.path.exists(runfile):
                                continue
                            
                            score = float(run_eval_and_return_metric(metric, f'atomic.validation.{retrieval_type}',
                                                                     trec_eval_metric_definitions[metric], runfile))
                            result = ok_str if math.isclose(score, float(expected[metric])) \
                                else fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result}')

                            table[model][name][metric] = score
                        else:
                            table[model][name][metric] = expected[metric]

            print('')

    for metric in trec_eval_metric_definitions:
        print_results(table, metric)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for AToMiC.')
    # To list all conditions/models
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    parser.add_argument('--list-models', action='store_true', default=False, help='List available datasets.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--all', action='store_true', default=False, help='Run all conditions.')
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)
    parser.add_argument('--model', type=str, help='Model to run.', required=False)
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)
    parser.add_argument('--dry-run', action='store_true', default=False, help='Print out commands but do not execute.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    parser.add_argument('--display-commands', action='store_true', default=False, help='Display command.')
    args = parser.parse_args()

    if args.list_conditions:
        list_conditions()
        sys.exit()
    
    if args.list_models:
        list_models()
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
        
    if args.all and (args.condition or args.model):
        print('Specifying --all will run all conditions and models')
        sys.exit()

    run_conditions(args)
        
