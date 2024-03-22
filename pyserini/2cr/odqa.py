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

from ._base import run_dpr_retrieval_eval_and_return_metric, convert_trec_run_to_dpr_retrieval_json, run_fusion, ok_str, \
    fail_str

dense_threads = 16
dense_batch_size = 512
sparse_threads = 16
sparse_batch_size = 128

# The models: the rows of the results table will be ordered this way.
models = {
    'models':
    ['BM25-k1_0.9_b_0.4',
     'BM25-k1_0.9_b_0.4_dpr-topics',
     'GarT5-RRF',
     'DPR',
     'DPR-DKRR',
     'DPR-Hybrid',
     'GarT5RRF-DKRR-RRF'
     ]
}

evaluate_dpr_retrieval_metric_definitions = {
        'Top5-1000': '--topk 5 20 100 500 1000',
        'Top5-100': '--topk 5 20 100'
}

# global vars
TQA_TOPICS = 'dpr-trivia-test'
NQ_TOPICS = 'nq-test'
PRINT_TQA_TOPICS = 'TriviaQA'
PRINT_NQ_TOPICS = 'Natural Question'
TQA_DKRR_RUN = f'run.odqa.DPR-DKRR.{TQA_TOPICS}.hits-100.txt'
NQ_DKRR_RUN = f'run.odqa.DPR-DKRR.{NQ_TOPICS}.hits-100.txt'

GARRRF_LS = ['answers', 'titles', 'sentences']
HITS_1K = {'GarT5-RRF', 'DPR-DKRR', 'DPR-Hybrid'}


def print_results(table, metric, topics):
    print(f'Metric = {metric}, Topics = {topics}')
    for model in models['models']:
        print(' ' * 32, end='')
        print(f'{model:30}', end='')
        key = f'{model}'
        print(f'{table[key][metric]:7.2f}', end='\n')
    print('')


def format_run_command(raw):
    return raw.replace('--encoded-queries', '\\\n  --encoded-queries') \
        .replace('--encoder', '\\\n  --encoder') \
        .replace('--topics', '\\\n  --topics') \
        .replace('--index', '\\\n  --index') \
        .replace('--output', '\\\n  --output') \
        .replace('--threads', '\\\n  --threads') \
        .replace('--bm25', '\\\n  --bm25') \
        .replace('--hits 100', '\\\n  --hits 100')


def format_hybrid_search_command(raw):
    return raw.replace('--encoder', '\\\n\t--encoder') \
        .replace(' dense', ' \\\n dense ') \
        .replace(' sparse', ' \\\n sparse') \
        .replace(' fusion', ' \\\n fusion') \
        .replace(' run ', ' \\\n run\t') \
        .replace('--output', '\\\n\t--output') \
        .replace('--threads', '\\\n\t--threads') \
        .replace('--lang', '\\\n\t--lang') \
        .replace('--hits 100', '\\\n\t--hits 100')


def format_convert_command(raw):
    return raw.replace('--topics', '\\\n  --topics') \
        .replace('--index', '\\\n  --index') \
        .replace('--input', '\\\n  --input') \
        .replace('--output', '\\\n  --output')


def format_eval_command(raw):
    return raw.replace('--retrieval ', '\\\n  --retrieval ') \
        .replace('--topk', '\\\n  --topk')


def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr")/f, 'r')
    text = fin.read()
    fin.close()

    return text


def list_conditions():
    for model in models['models']:
        print(model)


def generate_table_rows(table, table_id, commands, convert_commands, eval_commands, fusion_cmd_tqa, fusion_cmd_nq):
    row_cnt = 1
    html_rows = []

    row_template = read_file('odqa_html_table_row.template')
    row_template_garrrf = read_file('odqa_html_table_row_gar-rrf.template')
    row_template_rrf = read_file('odqa_html_table_row_rrf.template')
    
    for model in models['models']:
        if model == "GarT5-RRF":
            s = Template(row_template_garrrf)
            s = s.substitute(table_cnt=table_id,
                             row_cnt=row_cnt,
                             model=model,
                             TQA_Top20=table[model][TQA_TOPICS]["Top20"],
                             TQA_Top100=table[model][TQA_TOPICS]["Top100"],
                             NQ_Top20=table[model][NQ_TOPICS]["Top20"],
                             NQ_Top100=table[model][NQ_TOPICS]["Top100"],
                             cmd1=f'{commands[model][TQA_TOPICS][0]}',
                             cmd2=f'{commands[model][TQA_TOPICS][1]}',
                             cmd3=f'{commands[model][TQA_TOPICS][2]}',
                             cmd4=f'{commands[model][NQ_TOPICS][0]}',
                             cmd5=f'{commands[model][NQ_TOPICS][1]}',
                             cmd6=f'{commands[model][NQ_TOPICS][2]}',
                             fusion_cmd1=fusion_cmd_tqa[0],
                             fusion_cmd2=fusion_cmd_nq[0],
                             convert_cmd1=f'{convert_commands[model][TQA_TOPICS]}',
                             convert_cmd2=f'{convert_commands[model][NQ_TOPICS]}',
                             eval_cmd1=f'{eval_commands[model][TQA_TOPICS]}',
                             eval_cmd2=f'{eval_commands[model][NQ_TOPICS]}')
        elif model == "GarT5RRF-DKRR-RRF":
            s = Template(row_template_rrf)
            s = s.substitute(table_cnt=table_id,
                             row_cnt=row_cnt,
                             model=model,
                             TQA_Top20=table[model][TQA_TOPICS]["Top20"],
                             TQA_Top100=table[model][TQA_TOPICS]["Top100"],
                             NQ_Top20=table[model][NQ_TOPICS]["Top20"],
                             NQ_Top100=table[model][NQ_TOPICS]["Top100"],
                             fusion_cmd1=fusion_cmd_tqa[1],
                             fusion_cmd2=fusion_cmd_nq[1],
                             convert_cmd1=f'{convert_commands[model][TQA_TOPICS]}',
                             convert_cmd2=f'{convert_commands[model][NQ_TOPICS]}',
                             eval_cmd1=f'{eval_commands[model][TQA_TOPICS]}',
                             eval_cmd2=f'{eval_commands[model][NQ_TOPICS]}')
        else:
            s = Template(row_template)
            s = s.substitute(table_cnt=table_id,
                             row_cnt=row_cnt,
                             model=model,
                             TQA_Top20=table[model][TQA_TOPICS]["Top20"],
                             TQA_Top100=table[model][TQA_TOPICS]["Top100"],
                             NQ_Top20=table[model][NQ_TOPICS]["Top20"],
                             NQ_Top100=table[model][NQ_TOPICS]["Top100"],
                             cmd1=commands[model][TQA_TOPICS][0],
                             cmd2=commands[model][NQ_TOPICS][0],
                             convert_cmd1=f'{convert_commands[model][TQA_TOPICS]}',
                             convert_cmd2=f'{convert_commands[model][NQ_TOPICS]}',
                             eval_cmd1=f'{eval_commands[model][TQA_TOPICS]}',
                             eval_cmd2=f'{eval_commands[model][NQ_TOPICS]}')
        html_rows.append(s)
        row_cnt += 1

    return html_rows


def generate_report(args):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: []))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))
    convert_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('odqa_html.template')
    table_template = read_file('odqa_html_table.template')
    tqa_yaml_path = importlib.resources.files("pyserini.2cr")/'triviaqa.yaml'
    nq_yaml_path = importlib.resources.files("pyserini.2cr")/'naturalquestion.yaml'

    garrrf_ls = ['answers', 'titles', 'sentences']
    fusion_cmd_tqa = []
    fusion_cmd_nq = []
    tqa_fused_run = {}
    nq_fused_run = {}

    with open(tqa_yaml_path) as f_tqa, open(nq_yaml_path) as f_nq:
        tqa_yaml_data = yaml.safe_load(f_tqa)
        nq_yaml_data = yaml.safe_load(f_nq)
        for condition_tqa, condition_nq in zip(tqa_yaml_data['conditions'], nq_yaml_data['conditions']):
            name = condition_tqa['model_name']
            cmd_template_tqa = condition_tqa['command']
            cmd_template_nq = condition_nq['command']
            if 'RRF' in name:
                if name == 'GarT5-RRF':
                    runfile_tqa = \
                        [os.path.join(args.directory, f'run.odqa.{name}.{TQA_TOPICS}.{garrrf_ls[i]}.hits-1000.txt')
                         for i in range(len(cmd_template_tqa))]
                    runfile_nq = \
                        [os.path.join(args.directory, f'run.odqa.{name}.{NQ_TOPICS}.{garrrf_ls[i]}.hits-1000.txt')
                         for i in range(len(cmd_template_nq))]
                    tqa_fused_run.update({name: runfile_tqa[0].replace('.answers.hits-1000.txt', '.hits-100.fusion.txt')})
                    nq_fused_run.update({name: runfile_nq[0].replace('.answers.hits-1000.txt', '.hits-100.fusion.txt')})
                    jsonfile_tqa = tqa_fused_run[name].replace('.txt', '.json').replace('.hits-1000', '')
                    jsonfile_nq = nq_fused_run[name].replace('.txt', '.json').replace('.hits-1000', '')
                elif name == 'GarT5RRF-DKRR-RRF':
                    jsonfile_tqa = os.path.join(args.directory, f'run.odqa.{name}.{TQA_TOPICS}.json')
                    jsonfile_nq = os.path.join(args.directory, f'run.odqa.{name}.{TQA_TOPICS}.json')
                    tqa_fused_run.update({name: jsonfile_tqa.replace('.json', '.txt')})
                    nq_fused_run.update({name: jsonfile_nq.replace('.json', '.txt')})
                else:
                    raise NameError('Wrong model name in yaml config')
            else:
                if 'dpr-topics' in name:
                    runfile_nq = [os.path.join(args.directory, f'run.odqa.{name}.dpr-nq-test.hits-100.txt')]
                else:
                    runfile_nq = [os.path.join(args.directory, f'run.odqa.{name}.{NQ_TOPICS}.hits-100.txt')]
                runfile_tqa = [os.path.join(args.directory, f'run.odqa.{name}.{TQA_TOPICS}.hits-100.txt')]   
                jsonfile_tqa = runfile_tqa[0].replace('.answers', '').replace('.txt', '.json')
                jsonfile_nq = runfile_nq[0].replace('.answers', '').replace('.txt', '.json')
            
            display_runfile_tqa = jsonfile_tqa.replace('.json', '.txt')
            display_runfile_nq = jsonfile_nq.replace('.json', '.txt')

            # fusion commands
            if "RRF" in name:
                if name == "GarT5RRF-DKRR-RRF":
                    nq_runs = ' \\\n\t '.join([NQ_DKRR_RUN, nq_fused_run['GarT5-RRF']])
                    tqa_runs = ' \\\n\t '.join([TQA_DKRR_RUN, tqa_fused_run['GarT5-RRF']])
                else:
                    tqa_runs = ' \\\n\t '.join(runfile_tqa)
                    nq_runs = ' \\\n\t '.join(runfile_nq)
                
                fusion_cmd_tqa.append(f'python -m pyserini.fusion \\\n' +
                                      f'  --runs {tqa_runs} \\\n' +
                                      f'  --output {tqa_fused_run[name]} \\\n' +
                                      f'  --k 100')
                fusion_cmd_nq.append(f'python -m pyserini.fusion \\\n' +
                                     f'  --runs {nq_runs} \\\n' +
                                     f'  --output {nq_fused_run[name]} \\\n' +
                                     f'  --k 100')

            if name != "GarT5RRF-DKRR-RRF":
                hits = 100 if name not in HITS_1K else 1000
                cmd_tqa = [Template(cmd_template_tqa[i])
                           .substitute(output=runfile_tqa[i],
                                       sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                       dense_threads=dense_threads, dense_batch_size=dense_batch_size) +
                           f' --hits {hits}' for i in range(len(cmd_template_tqa))]
                cmd_nq = [Template(cmd_template_nq[i])
                          .substitute(output=runfile_nq[i],
                                      sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                      dense_threads=dense_threads, dense_batch_size=dense_batch_size) +
                          f' --hits {hits}' for i in range(len(cmd_template_nq))]
                if name == 'DPR-Hybrid':
                    commands[name][TQA_TOPICS].extend([format_hybrid_search_command(i) for i in cmd_tqa])
                    commands[name][NQ_TOPICS].extend([format_hybrid_search_command(i) for i in cmd_nq])
                else:
                    commands[name][TQA_TOPICS].extend([format_run_command(i) for i in cmd_tqa])
                    commands[name][NQ_TOPICS].extend([format_run_command(i) for i in cmd_nq])
            
            # conversion commands:
            if 'dpr-topics' in name:
                temp_nq_topics = 'dpr-nq-test'
            else:
                temp_nq_topics = NQ_TOPICS

            convert_cmd_tqa = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run ' + \
                f'--topics {TQA_TOPICS} ' + \
                f'--index wikipedia-dpr ' + \
                f'--input {display_runfile_tqa} ' + \
                f'--output {jsonfile_tqa}'
            convert_cmd_nq = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run ' + \
                f'--topics {temp_nq_topics} ' + \
                f'--index wikipedia-dpr ' +\
                f'--input {display_runfile_nq} ' + \
                f'--output {jsonfile_nq}'
            convert_commands[name][TQA_TOPICS] = format_convert_command(convert_cmd_tqa)
            convert_commands[name][NQ_TOPICS] = format_convert_command(convert_cmd_nq)

            # eval commands
            eval_cmd_tqa = f'python -m pyserini.eval.evaluate_dpr_retrieval ' + \
                f'--retrieval {jsonfile_tqa} ' + \
                f'--topk 20 100'
            eval_cmd_nq = f'python -m pyserini.eval.evaluate_dpr_retrieval ' + \
                f'--retrieval {jsonfile_nq} ' + \
                f'--topk 20 100'
            eval_commands[name][TQA_TOPICS] = format_eval_command(eval_cmd_tqa)
            eval_commands[name][NQ_TOPICS] = format_eval_command(eval_cmd_nq)

            for expected_tqa, expected_nq in zip(condition_tqa['scores'], condition_nq['scores']):
                table[name][TQA_TOPICS].update(expected_tqa)
                table[name][NQ_TOPICS].update(expected_nq)
        tables_html = []

        html_rows = generate_table_rows(table, 1, commands, convert_commands,
                                        eval_commands, fusion_cmd_tqa=fusion_cmd_tqa, fusion_cmd_nq=fusion_cmd_nq)
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc='Models', rows=all_rows))

        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title=f'Retrieval for Open-Domain QA Datasets', tables=' '.join(tables_html)))


def run_conditions(args):
    hits = 1000 if args.full_topk else 100
    yaml_path = importlib.resources.files("pyserini.2cr")/'triviaqa.yaml' \
        if args.topics == "tqa" else importlib.resources.files("pyserini.2cr")/'naturalquestion.yaml'
    topics = 'dpr-trivia-test' if args.topics == 'tqa' else 'nq-test'
    start = time.time()
    table = defaultdict(lambda: defaultdict(lambda: 0.0))

    with open(yaml_path) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['model_name']
            cmd_template = condition['command']
            
            if args.all:
                pass
            elif args.condition != name:
                continue

            if not args.full_topk:
                # if using topk100
                if name in HITS_1K:
                    # if running topk1000 is a must to ensure scores match with the ones in the table
                    hits = 1000
                else:
                    hits = 100

            print(f'model {name}:')
            if topics == 'nq-test' and name == 'BM25-k1_0.9_b_0.4_dpr-topics':
                topics = 'dpr-nq-test'
            elif args.topics == 'nq':
                topics = 'nq-test'
            print(f'  - Topics: {topics}')

            # running retrieval
            if name == "GarT5-RRF":
                runfile = [os.path.join(args.directory, f'run.odqa.{name}.{topics}.{i}.hits-{hits}.txt') for i in GARRRF_LS]
            else:
                runfile = [os.path.join(args.directory, f'run.odqa.{name}.{topics}.hits-{hits}.txt')]

            if name != "GarT5RRF-DKRR-RRF":
                cmd = [Template(cmd_template[i]).substitute(output=runfile[i],
                                                            sparse_threads=sparse_threads,
                                                            sparse_batch_size=sparse_batch_size,
                                                            dense_threads=dense_threads,
                                                            dense_batch_size=dense_batch_size) for i in range(len(runfile))]
                if hits == 100:
                    cmd = [i + ' --hits 100' for i in cmd]

                for i in range(len(runfile)):
                    if args.display_commands:
                        if name == 'DPR-Hybrid':
                            formatted_command = format_hybrid_search_command(cmd[i])
                        else:
                            formatted_command = format_run_command(cmd[i])

                        print(f'\n```bash\n{formatted_command}\n```\n')
                    if not os.path.exists(runfile[i]):
                        if not args.dry_run:
                            os.system(cmd[i])

            # fusion
            if 'RRF' in name:
                if name == 'GarT5-RRF':
                    runs = runfile
                    output = os.path.join(args.directory, f'run.odqa.{name}.{topics}.hits-{hits}.fusion.txt')
                elif name == 'GarT5RRF-DKRR-RRF':
                    runs = [os.path.join(args.directory, f'run.odqa.DPR-DKRR.{topics}.hits-1000.txt'),
                            os.path.join(args.directory, f'run.odqa.GarT5-RRF.{topics}.hits-1000.fusion.txt')]
                    output = runfile[0].replace('.txt', '.fusion.txt')
                else:
                    raise NameError('Unexpected model name')
                if not os.path.exists(output) and not args.dry_run:
                    if not args.full_topk and name != 'GarT5-RRF':
                        # if using topk100, we change it back for methods that require topk1000 to generate runs
                        hits = 100
                    status = run_fusion(runs, output, hits)
                    if status != 0:
                        raise RuntimeError('fusion failed')
                runfile = [output]

            # TREC conversion + evaluation
            if not args.skip_eval:
                if not os.path.exists(runfile[0]):
                    continue
                jsonfile = runfile[0].replace('.txt', '.json')
                runfile = jsonfile.replace('.json', '.txt')
                if not os.path.exists(jsonfile):
                    status = convert_trec_run_to_dpr_retrieval_json(topics, 'wikipedia-dpr-100w', runfile, jsonfile)
                    if status != 0:
                        raise RuntimeError("dpr retrieval conversion failed")
                topk_defs = evaluate_dpr_retrieval_metric_definitions['Top5-100']
                if args.full_topk:
                    topk_defs = evaluate_dpr_retrieval_metric_definitions['Top5-1000']
                score = run_dpr_retrieval_eval_and_return_metric(topk_defs, jsonfile)
            
            # comparing ground truth scores with the generated ones 
            for expected in condition['scores']:
                for metric, expected_score in expected.items():
                    if not args.skip_eval and metric not in score.keys():
                        continue
                    if not args.skip_eval:
                        if math.isclose(score[metric], float(expected_score), abs_tol=2e-2):
                            result_str = ok_str
                        else:
                            result_str = fail_str + f' expected {expected[metric]:.4f}'
                        print(f'      {metric:7}: {score[metric]:.2f} {result_str}')
                        table[name][metric] = score[metric]
                    else:
                        table[name][metric] = expected_score
            print('')
    metric_ls = ['Top5', 'Top20', 'Top100', 'Top500', 'Top1000']
    metric_ls = metric_ls[:3] if not args.full_topk else metric_ls
    for metric in metric_ls:
        print_results(table, metric, topics)

    end = time.time()
    start_str = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.utcfromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


if __name__ == '__main__': 
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO corpora.')
    # To list all conditions
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--full-topk', action='store_true', default=False, help='Run topk 5-1000, default is topk 5-100')
    parser.add_argument('--all', action='store_true', default=False, help='Run all conditions.')
    parser.add_argument('--topics', type=str, help='Topics to run [tqa, nq].', choices=['tqa', 'nq'], required=False)
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)
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
        
    if not args.generate_report and not args.topics:
        print(f"Must specify a topic [tqa, nq] when running an evaluation.")
        sys.exit()

    if not args.all and not args.condition:
        print(f'Must specify a specific condition using --condition or use --all to run all conditions.')
        sys.exit()
    
    if args.all and args.condition:
        print('Specifying --all will run all conditions')
        sys.exit()

    run_conditions(args)
