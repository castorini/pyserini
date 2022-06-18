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
import re
from collections import defaultdict
from string import Template

import yaml

from scripts.repro_matrix.defs import models, trec_eval_metric_definitions
from scripts.repro_matrix.utils import find_table_topic_set_key_v1, find_table_topic_set_key_v2

beir_keys = ['trec-covid',
             'bioasq',
             'nfcorpus',
             'nq',
             'hotpotqa',
             'fiqa',
             'signal1m',
             'trec-news',
             'robust04',
             'arguana',
             'webis-touche2020',
             'cqadupstack-android',
             'cqadupstack-english',
             'cqadupstack-gaming',
             'cqadupstack-gis',
             'cqadupstack-mathematica',
             'cqadupstack-physics',
             'cqadupstack-programmers',
             'cqadupstack-stats',
             'cqadupstack-tex',
             'cqadupstack-unix',
             'cqadupstack-webmasters',
             'cqadupstack-wordpress',
             'quora',
             'dbpedia-entity',
             'scidocs',
             'fever',
             'climate-fever',
             'scifact'
             ]

trec_eval_metric_definitions = {
    'nDCG@10': '-c -m ndcg_cut.10',
    'R@100': '-c -m recall.100',
    'R@1000': '-c -m recall.1000'
}


def format_command(raw):
    return raw.replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--output ', '\\\n  --output ')\
        .replace('--output-format trec', '\\\n  --output-format trec \\\n ') \
        .replace('--hits ', '\\\n  --hits ')


def format_eval_command(raw):
    return raw.replace('-c ', '\\\n  -c ')\
        .replace('run.', '\\\n  run.')


def read_file(f):
    fin = open(f, 'r')
    text = fin.read()
    fin.close()

    return text


if __name__ == '__main__':
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('scripts/repro_matrix/beir_html.template')
    row_template = read_file('scripts/repro_matrix/beir_html_row.template')

    with open('pyserini/resources/beir.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            cmd_template = condition['command']

            for datasets in condition['datasets']:
                dataset = datasets['dataset']

                runfile = f'run.beir-{name}.{dataset}.txt'
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile)
                commands[dataset][name] = format_command(cmd)

                for expected in datasets['scores']:
                    for metric in expected:
                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[metric]} beir-v1.0.0-{dataset}-test {runfile}'
                        eval_commands[dataset][name] += format_eval_command(eval_cmd) + '\n\n'

                        table[dataset][name][metric] = expected[metric]

        row_cnt = 1
        html_rows = []
        for dataset in beir_keys:
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             dataset=dataset,
                             s1=f'{table[dataset]["flat"]["nDCG@10"]:8.4f}',
                             s2=f'{table[dataset]["flat"]["R@100"]:8.4f}',
                             s3=f'{table[dataset]["multifield"]["nDCG@10"]:8.4f}',
                             s4=f'{table[dataset]["multifield"]["R@100"]:8.4f}',
                             s5=f'{table[dataset]["splade-distil-cocodenser-medium"]["nDCG@10"]:8.4f}',
                             s6=f'{table[dataset]["splade-distil-cocodenser-medium"]["R@100"]:8.4f}',
                             cmd1=commands[dataset]["flat"],
                             cmd2=commands[dataset]["multifield"],
                             cmd3=commands[dataset]["splade-distil-cocodenser-medium"],
                             eval_cmd1=eval_commands[dataset]["flat"].rstrip(),
                             eval_cmd2=eval_commands[dataset]["multifield"].rstrip(),
                             eval_cmd3=eval_commands[dataset]["splade-distil-cocodenser-medium"].rstrip(),
                             )

            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        print(Template(html_template).substitute(title='BEIR', rows=all_rows))
