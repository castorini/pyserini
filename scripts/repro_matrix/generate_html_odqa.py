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


def format_run_command(raw):
    return raw.replace('--encoded-queries', '\\\n  --lang')\
        .replace('--encoder', '\\\n  --encoder')\
        .replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--output ', '\\\n  --output')\
        .replace('--batch ', '\\\n  --batch') \
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


def generate_table_rows(table_id, topics, table):
    row_cnt = 1
    html_rows = []

    for model in models['models']:
        s = Template(row_template)
        s = s.substitute(table_cnt=table_id,
                         row_cnt=row_cnt,
                         model=model,
                         Top5=f'{table[model][topics]["Top5"]}',
                         Top20=f'{table[model][topics]["Top20"]}',
                         Top100=f'{table[model][topics]["Top100"]}',
                         Top500=f'{table[model][topics]["Top500"]}',
                         Top1000=f'{table[model][topics]["Top1000"]}',
                         cmd1=f'{commands[model]}',
                         cmd2=f'{commands[model]}',
                         cmd3=f'{commands[model]}',
                         cmd4=f'{commands[model]}',
                         cmd5=f'{commands[model]}',
                         convert_cmd1=f'{convert_commands[model]["Top5"]}',
                         convert_cmd2=f'{convert_commands[model]["Top20"]}',
                         convert_cmd3=f'{convert_commands[model]["Top100"]}',
                         convert_cmd4=f'{convert_commands[model]["Top500"]}',
                         convert_cmd5=f'{convert_commands[model]["Top1000"]}',
                         eval_cmd1=f'{eval_commands[model]["Top5"]}',
                         eval_cmd2=f'{eval_commands[model]["Top20"]}',
                         eval_cmd3=f'{eval_commands[model]["Top100"]}',
                         eval_cmd4=f'{eval_commands[model]["Top500"]}',
                         eval_cmd5=f'{eval_commands[model]["Top1000"]}',
                         )

        html_rows.append(s)
        row_cnt += 1

    return html_rows


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate HTML rendering of regression matrix for MS MARCO corpora.')
    parser.add_argument('--topics', choices=['triviaqa','naturalquestion'], help='Topics to be run [triviaqa, naturalquestion]', required=True)
    args = parser.parse_args()
    topics = 'dpr-trivia-test' if args.topics == 'triviaqa' else 'nq-test'

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: '')
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))
    convert_commands = defaultdict(lambda : defaultdict(lambda: ''))

    html_template = read_file('scripts/repro_matrix/odqa_html.template')
    table_template = read_file('scripts/repro_matrix/odqa_html_table.template')
    row_template = read_file('scripts/repro_matrix/odqa_html_table_row.template')
    yaml_path = 'pyserini/resources/triviaqa.yaml' if args.topics == "triviaqa" else 'pyserini/resources/naturalquestion.yaml'

    with open(yaml_path) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['model_name']
            cmd_template = condition['command']
            runfile = f'run.odqa.{name}.{topics}.txt'
            jsonfile = runfile.replace('.txt','.json')
            cmd = Template(cmd_template).substitute(output=runfile)
            commands[name] = format_run_command(cmd)

            for expected in condition['scores']:
                for metric in expected:
                    table[name][topics][metric] = expected[metric]
                    convert_cmd = f'python -m pyserini.eval.convert_trec_run_to_dpr_retrieval_run ' + \
                                f'--topics {topics} ' + \
                                f'--index wikipedia-dpr ' +\
                                f'--input {runfile} ' + \
                                f'--output {jsonfile}'
                    convert_commands[name][metric] = format_convert_command(convert_cmd)

                    eval_cmd = f'python -m pyserini.eval.evaluate_dpr_retrieval ' + \
                                f'--retrieval {jsonfile} ' + \
                                f'{evaluate_dpr_retrieval_metric_definitions[metric]}'
                    eval_commands[name][metric] = format_eval_command(eval_cmd)
        tables_html = []

        # Build the table for MRR@100, test queries
        html_rows = generate_table_rows(1, topics, table)
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc='Models', rows=all_rows))

        # # Build the table for R@100, test queries
        # html_rows = generate_table_rows(2, topics)
        # all_rows = '\n'.join(html_rows)
        # tables_html.append(Template(table_template).substitute(desc='Recall@100, test queries', rows=all_rows))

        print(Template(html_template).substitute(title='ODQA Retrieval', tables=' '.join(tables_html)))
