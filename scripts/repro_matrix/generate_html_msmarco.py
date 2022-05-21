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
from collections import defaultdict
from string import Template

import yaml

from scripts.repro_matrix.defs import models, trec_eval_metric_definitions
from scripts.repro_matrix.utils import find_table_topic_set_key_v1, find_table_topic_set_key_v2


def format_command(raw):
    return raw.replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--output', '\\\n  --output')\
        .replace('.txt', '.txt \\\n ')


def read_file(f):
    fin = open(f, 'r')
    text = fin.read()
    fin.close()

    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate HTML rendering of regression matrix for MS MARCO corpora.')
    parser.add_argument('--collection', type=str, help='Collection = {v1-passage, v1-doc, v2-passage, v2-doc}.', required=True)
    args = parser.parse_args()

    if args.collection == 'v1-passage':
        collection = 'msmarco-v1-passage'
        yaml_file = 'pyserini/resources/msmarco-v1-passage.yaml'
        html_template = read_file('scripts/repro_matrix/msmarco_html_v1_passage.template')
        row_template = read_file('scripts/repro_matrix/msmarco_html_row_v1.template')
    elif args.collection == 'v1-doc':
        collection = 'msmarco-v1-doc'
        yaml_file = 'pyserini/resources/msmarco-v1-doc.yaml'
        html_template = read_file('scripts/repro_matrix/msmarco_html_v1_doc.template')
        row_template = read_file('scripts/repro_matrix/msmarco_html_row_v1.template')
    elif args.collection == 'v2-passage':
        collection = 'msmarco-v2-passage'
        yaml_file = 'pyserini/resources/msmarco-v2-passage.yaml'
        html_template = read_file('scripts/repro_matrix/msmarco_html_v2.template')
        row_template = read_file('scripts/repro_matrix/msmarco_html_row_v2.template')
    elif args.collection == 'v2-doc':
        collection = 'msmarco-v2-doc'
        yaml_file = 'pyserini/resources/msmarco-v2-doc.yaml'
        html_template = read_file('scripts/repro_matrix/msmarco_html_v2.template')
        row_template = read_file('scripts/repro_matrix/msmarco_html_row_v2.template')
    else:
        raise ValueError(f'Unknown corpus: {args.collection}')

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    table_keys = {}

    with open(yaml_file) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            display = condition['display']
            cmd_template = condition['command']

            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                short_topic_key = ''
                if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
                    short_topic_key = find_table_topic_set_key_v1(topic_key)
                else:
                    short_topic_key = find_table_topic_set_key_v2(topic_key)

                runfile = f'run.{collection}.{name}.{short_topic_key}.txt'
                cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile)
                commands[name][short_topic_key] = cmd

                for expected in topic_set['scores']:
                    for metric in expected:
                        table_keys[name] = display
                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[collection][eval_key][metric]} {eval_key} {runfile}'
                        eval_commands[name][short_topic_key] += eval_cmd + '\n'
                        table[name][short_topic_key][metric] = expected[metric]

    if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
        row_cnt = 1

        html_rows = []
        for name in models[collection]:
            if not name:
                continue
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             condition_name=table_keys[name],
                             s1=f'{table[name]["dl19"]["MAP"]:8.4f}',
                             s2=f'{table[name]["dl19"]["nDCG@10"]:8.4f}',
                             s3=f'{table[name]["dl19"]["R@1K"]:8.4f}',
                             s4=f'{table[name]["dl20"]["MAP"]:8.4f}',
                             s5=f'{table[name]["dl20"]["nDCG@10"]:8.4f}',
                             s6=f'{table[name]["dl20"]["R@1K"]:8.4f}',
                             s7=f'{table[name]["msmarco"]["MRR@10"]:8.4f}',
                             s8=f'{table[name]["msmarco"]["R@1K"]:8.4f}',
                             cmd1=format_command(commands[name]['dl19']),
                             cmd2=format_command(commands[name]['dl20']),
                             cmd3=format_command(commands[name]['dev']),
                             eval_cmd1=eval_commands[name]['dl19'],
                             eval_cmd2=eval_commands[name]['dl20'],
                             eval_cmd3=eval_commands[name]['dev']
                             )
            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        if collection == 'msmarco-v1-passage':
            full_name = 'MS MARCO V1 Passage'
        else:
            full_name = 'MS MARCO V1 Document'
        print(Template(html_template).substitute(title=full_name, rows=all_rows))
    else:
        row_cnt = 1

        html_rows = []
        for name in models[collection]:
            if not name:
                continue
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             condition_name=table_keys[name],
                             s1=f'{table[name]["dl21"]["MAP@100"]:8.4f}',
                             s2=f'{table[name]["dl21"]["nDCG@10"]:8.4f}',
                             s3=f'{table[name]["dl21"]["MRR@100"]:8.4f}',
                             s4=f'{table[name]["dl21"]["R@100"]:8.4f}',
                             s5=f'{table[name]["dl21"]["R@1K"]:8.4f}',
                             s6=f'{table[name]["dev"]["MRR@100"]:8.4f}',
                             s7=f'{table[name]["dev"]["R@1K"]:8.4f}',
                             s8=f'{table[name]["dev2"]["MRR@100"]:8.4f}',
                             s9=f'{table[name]["dev2"]["R@1K"]:8.4f}',
                             cmd1=format_command(commands[name]['dl21']),
                             cmd2=format_command(commands[name]['dev']),
                             cmd3=format_command(commands[name]['dev2']),
                             eval_cmd1=eval_commands[name]['dl21'],
                             eval_cmd2=eval_commands[name]['dev'],
                             eval_cmd3=eval_commands[name]['dev2']
                             )
            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        if collection == 'msmarco-v2-passage':
            full_name = 'MS MARCO V2 Passage'
        else:
            full_name = 'MS MARCO V2 Document'
        print(Template(html_template).substitute(title=full_name, rows=all_rows))
