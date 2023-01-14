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

from collections import defaultdict
from string import Template
import argparse

import yaml

# from scripts.repro_matrix.defs_odqa import models
from defs_odqa import models

# global vars
TQA_TOPICS = 'dpr-trivia-test'
NQ_TOPICS = 'nq-test'
PRINT_TQA_TOPICS = 'TriviaQA'
PRINT_NQ_TOPICS = 'Natural Question'
TQA_DKRR_RUN = f'runs/run.odqa.DPR-DKRR.{TQA_TOPICS}.hits=100.txt'
NQ_DKRR_RUN = f'runs/run.odqa.DPR-DKRR.{NQ_TOPICS}.hits=100.txt'
HITS_1K = set(['GarT5-RRF', 'DPR-DKRR'])


def format_run_command(raw):
    return raw.replace('--encoded-queries', '\\\n  --encoded-queries')\
        .replace('--encoder', '\\\n  --encoder')\
        .replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--output', '\\\n  --output')\
        .replace('--batch', '\\\n  --batch') \
        .replace('--threads', '\\\n  --threads')\
        .replace('--hits 100', '\\\n  --hits 100')

def format_hybrid_search_command(raw):
    return raw.replace('--encoder', '\\\n\t--encoder')\
        .replace(' dense', '\\\n dense ')\
        .replace(' sparse', '\\\n sparse')\
        .replace(' fusion', '\\\n fusion')\
        .replace(' run ', '\\\n run\t')\
        .replace('--output', '\\\n\t--output')\
        .replace('--batch', '\\\n\t--batch') \
        .replace('--threads', '\\\n\t--threads')\
        .replace('--lang', '\\\n\t--lang')\
        .replace('--hits 100', '\\\n\t--hits 100')

def format_convert_command(raw):
    return raw.replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--input', '\\\n  --input')\
        .replace('--output', '\\\n  --output')\


def format_eval_command(raw):
    return raw.replace('--retrieval ', '\\\n  --retrieval ')\
        .replace('--topk', '\\\n  --topk')


def read_file(f):
    fin = open(f, 'r')
    text = fin.read()
    fin.close()

    return text


def generate_table_rows(table_id):
    row_cnt = 1
    html_rows = []

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
                            eval_cmd2=f'{eval_commands[model][NQ_TOPICS]}'
                            )
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
                            eval_cmd2=f'{eval_commands[model][NQ_TOPICS]}'
                            )
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
                            eval_cmd2=f'{eval_commands[model][NQ_TOPICS]}'
                            )
        html_rows.append(s)
        row_cnt += 1

    return html_rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Generate HTML rendering of regression matrix for MS MARCO corpora.')
    args = parser.parse_args()
    
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: []))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))
    convert_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('scripts/repro_matrix/odqa_html.template')
    table_template = read_file('scripts/repro_matrix/odqa_html_table.template')
    row_template = read_file('scripts/repro_matrix/odqa_html_table_row.template')
    row_template_garrrf = read_file('scripts/repro_matrix/odqa_html_table_row_gar-rrf.template')
    row_template_rrf = read_file('scripts/repro_matrix/odqa_html_table_row_rrf.template')
    tqa_yaml_path = 'pyserini/resources/triviaqa.yaml'
    nq_yaml_path = 'pyserini/resources/naturalquestion.yaml'

    garrrf_ls = ['answers','titles','sentences']
    prefusion_runfile_tqa = []
    prefusion_runfile_nq = []
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
                    runfile_tqa = [f'runs/run.odqa.{name}.{TQA_TOPICS}.{garrrf_ls[i]}.hits=1000.txt' for i in range(len(cmd_template_tqa))]
                    runfile_nq = [f'runs/run.odqa.{name}.{NQ_TOPICS}.{garrrf_ls[i]}.hits=1000.txt' for i in range(len(cmd_template_nq))]
                    tqa_fused_run.update({name: runfile_tqa[0].replace('.answers.hits=1000.txt', '.hits=100.fusion.txt')})
                    nq_fused_run.update({name: runfile_nq[0].replace('.answers.hits=1000.txt', '.hits=100.fusion.txt')})
                    jsonfile_tqa = tqa_fused_run[name].replace('.txt', '.json').replace('.hits=1000', '')
                    jsonfile_nq = nq_fused_run[name].replace('.txt', '.json').replace('.hits=1000', '')
                elif name == 'GarT5RRF-DKRR-RRF':
                    jsonfile_tqa = f'runs/run.odqa.{name}.{TQA_TOPICS}.json'
                    jsonfile_nq = f'runs/run.odqa.{name}.{TQA_TOPICS}.json'
                    tqa_fused_run.update({name: jsonfile_tqa.replace('.json','.txt')})
                    nq_fused_run.update({name: jsonfile_nq.replace('.json','.txt')})
                else:
                    raise NameError('Wrong model name in yaml config')
            else:
                if 'dpr-topics' in name:
                    runfile_nq = [f'runs/run.odqa.{name}.dpr-nq-test.hits=100.txt']
                else:
                    runfile_nq = [f'runs/run.odqa.{name}.{NQ_TOPICS}.hits=100.txt']
                runfile_tqa = [f'runs/run.odqa.{name}.{TQA_TOPICS}.hits=100.txt']   
                jsonfile_tqa = runfile_tqa[0].replace('.answers', '').replace('.txt', '.json')
                jsonfile_nq = runfile_nq[0].replace('.answers', '').replace('.txt', '.json')
            
            display_runfile_tqa = jsonfile_tqa.replace('.json','.txt')
            display_runfile_nq = jsonfile_nq.replace('.json','.txt')

            # fusion commands
            if "RRF" in name:
                if name == "GarT5RRF-DKRR-RRF":
                    nq_runs = ' \\\n\t '.join([NQ_DKRR_RUN, nq_fused_run['GarT5-RRF']])
                    tqa_runs = ' \\\n\t '.join([TQA_DKRR_RUN, tqa_fused_run['GarT5-RRF']])
                else:
                    tqa_runs = ' \\\n\t '.join(runfile_tqa)
                    nq_runs = ' \\\n\t '.join(runfile_nq)
                
                fusion_cmd_tqa.append(f'python -m pyserini.fusion \\\n' + \
                    f'  --runs {tqa_runs} \\\n' + \
                    f'  --output {tqa_fused_run[name]}\\\n'
                    f'  --k 100')
                fusion_cmd_nq.append(f'python -m pyserini.fusion \\\n' + \
                    f'  --runs {nq_runs} \\\n' + \
                    f'  --output {nq_fused_run[name]} \\\n' + \
                    f'  --k 100')

            if name != "GarT5RRF-DKRR-RRF":
                hits = 100 if name not in HITS_1K else 1000
                cmd_tqa = [Template(cmd_template_tqa[i]).substitute(
                    output=runfile_tqa[i]) + f" --hits {hits}" for i in range(len(cmd_template_tqa))]
                cmd_nq = [Template(cmd_template_nq[i]).substitute(output=runfile_nq[i]) + f" --hits {hits}" for i in range(len(cmd_template_nq))]
                if name == 'DPR-Hybrid':
                    commands[name][TQA_TOPICS].extend([format_hybrid_search_command(i) for i in cmd_tqa])
                    commands[name][NQ_TOPICS].extend([format_hybrid_search_command(i) for i in cmd_nq])
                else:
                    commands[name][TQA_TOPICS].extend([format_run_command(i) for i in cmd_tqa])
                    commands[name][NQ_TOPICS].extend([format_run_command(i) for i in cmd_nq])
            
            # convertion commands:
            if 'dpr-topics' in name:
                temp_nq_topics = 'dpr-nq-test'
            else:
                temp_nq_topics = NQ_TOPICS

            convert_cmd_tqa = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run ' + \
                f'--topics {TQA_TOPICS} ' + \
                f'--index wikipedia-dpr ' +\
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

        html_rows = generate_table_rows(1)
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc='Models', rows=all_rows))

        print(Template(html_template).substitute(
            title=f'Retrieval for Open-Domain QA Datasets', tables=' '.join(tables_html)))
