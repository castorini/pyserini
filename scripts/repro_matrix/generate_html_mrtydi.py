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

import yaml

from scripts.repro_matrix.defs_mrtydi import models, languages

def format_run_command(raw):
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

    html_template = read_file('scripts/repro_matrix/mrtydi_html.template')
    row_template = read_file('scripts/repro_matrix/mrtydi_html_row.template')

    with open('pyserini/resources/mrtydi.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            eval_key = condition['eval_key']
            cmd_template = condition['command']

            for splits in condition['splits']:
                split = splits['split']

                runfile = f'runs/run.mrtydi.{name}.{split}.txt'
                cmd = Template(cmd_template).substitute(split=split, output=runfile)

                for expected in splits['scores']:
                    for metric in expected:
                        table[name][split][metric] = expected[metric]

        row_cnt = 1
        html_rows = []
        for model in models:
            s = Template(row_template)

            keys = {}
            for lang in languages:
                keys[lang[0]] = f'{model}.{lang[0]}'

            s = s.substitute(row_cnt=row_cnt,
                             model=model,
                             ar=f'{table[keys["ar"]]["test"]["MRR@100"]:.3f}',
                             bn=f'{table[keys["bn"]]["test"]["MRR@100"]:.3f}',
                             en=f'{table[keys["en"]]["test"]["MRR@100"]:.3f}',
                             fi=f'{table[keys["fi"]]["test"]["MRR@100"]:.3f}',
                             id=f'{table[keys["id"]]["test"]["MRR@100"]:.3f}',
                             ja=f'{table[keys["ja"]]["test"]["MRR@100"]:.3f}',
                             ko=f'{table[keys["ko"]]["test"]["MRR@100"]:.3f}',
                             ru=f'{table[keys["ru"]]["test"]["MRR@100"]:.3f}',
                             sw=f'{table[keys["sw"]]["test"]["MRR@100"]:.3f}',
                             te=f'{table[keys["te"]]["test"]["MRR@100"]:.3f}',
                             th=f'{table[keys["th"]]["test"]["MRR@100"]:.3f}',
                             cmd1='',
                             cmd2='',
                             cmd3='',
                             eval_cmd1='',
                             eval_cmd2='',
                             eval_cmd3=''
                             )

            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        print(Template(html_template).substitute(title='Mr.TyDi', rows=all_rows))
