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

from scripts.repro_matrix.defs_odqa import models, evaluate_dpr_retrieval_metric_definitions

# global vars
TQA_TOPICS = 'dpr-trivia-test'
NQ_TOPICS = 'nq-test'
PRINT_TQA_TOPICS = 'TriviaQA'
PRINT_NQ_TOPICS = 'Natural Question'


def format_run_command(raw):
    return raw.replace('--encoded-queries', '\\\n  --lang')\
        .replace('--encoder', '\\\n  --encoder')\
        .replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--output', '\\\n  --output')\
        .replace('--batch', '\\\n  --batch') \
        .replace('--threads 12', '--threads 12 \\\n')


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
        s = Template(row_template)
        s = s.substitute(table_cnt=table_id,
                         row_cnt=row_cnt,
                         model=model,
                         TQA_Top20=table[model][TQA_TOPICS]["Top20"],
                         TQA_Top100=table[model][TQA_TOPICS]["Top100"],
                         NQ_Top20=table[model][NQ_TOPICS]["Top20"],
                         NQ_Top100=table[model][NQ_TOPICS]["Top100"],
                         cmd1=f'{commands[model][TQA_TOPICS]}',
                         cmd2=f'{commands[model][NQ_TOPICS]}',
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
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))
    convert_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('scripts/repro_matrix/odqa_html.template')
    table_template = read_file('scripts/repro_matrix/odqa_html_table.template')
    row_template = read_file(
        'scripts/repro_matrix/odqa_html_table_row.template')
    tqa_yaml_path = 'pyserini/resources/triviaqa.yaml'
    nq_yaml_path = 'pyserini/resources/naturalquestion.yaml'

    with open(tqa_yaml_path) as f_tqa, open(nq_yaml_path) as f_nq:
        tqa_yaml_data = yaml.safe_load(f_tqa)
        nq_yaml_data = yaml.safe_load(f_nq)
        for condition_tqa, condition_nq in zip(tqa_yaml_data['conditions'], nq_yaml_data['conditions']):
            name = condition_tqa['model_name']
            cmd_template_tqa = condition_tqa['command']
            cmd_template_nq = condition_nq['command']
            runfile_tqa = f'runs/run.odqa.{name}.{TQA_TOPICS}.txt'
            runfile_nq = f'runs/run.odqa.{name}.{NQ_TOPICS}.txt'
            jsonfile_tqa = runfile_tqa.replace('.txt', '.json')
            jsonfile_nq = runfile_nq.replace('.txt', '.json')
            cmd_tqa = Template(cmd_template_tqa).substitute(
                output=runfile_tqa)
            cmd_nq = Template(cmd_template_nq).substitute(output=runfile_nq)
            commands[name][TQA_TOPICS] = format_run_command(cmd_tqa)
            commands[name][NQ_TOPICS] = format_run_command(cmd_nq)
            convert_cmd_tqa = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run ' + \
                f'--topics {TQA_TOPICS} ' + \
                f'--index wikipedia-dpr ' +\
                f'--input {runfile_tqa} ' + \
                f'--output {jsonfile_tqa}'
            convert_cmd_nq = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run ' + \
                f'--topics {NQ_TOPICS} ' + \
                f'--index wikipedia-dpr ' +\
                f'--input {runfile_nq} ' + \
                f'--output {jsonfile_nq}'
            convert_commands[name][TQA_TOPICS] = format_convert_command(
                convert_cmd_tqa)
            convert_commands[name][NQ_TOPICS] = format_convert_command(
                convert_cmd_nq)

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
        tables_html.append(Template(table_template).substitute(
            desc='Models', rows=all_rows))

        print(Template(html_template).substitute(
            title=f'Retrieval for Open-Domain QA Datasets', tables=' '.join(tables_html)))
