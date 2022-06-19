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

from scripts.repro_matrix.defs_mrtydi import models, languages, trec_eval_metric_definitions


def format_run_command(raw):
    return raw.replace('--lang', '\\\n  --lang')\
        .replace('--encoder', '\\\n  --encoder')\
        .replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--output ', '\\\n  --output ')\
        .replace('--batch ', '\\\n  --batch ') \
        .replace('--threads 12', '--threads 12 \\\n ')


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
    commands = defaultdict(lambda: '')
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

                runfile = f'run.mrtydi.{name}.{split}.txt'
                cmd = Template(cmd_template).substitute(split=split, output=runfile)
                commands[name] = format_run_command(cmd)

                for expected in splits['scores']:
                    for metric in expected:
                        table[name][split][metric] = expected[metric]

                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[metric]} {eval_key}-{split} {runfile}'
                        eval_commands[name][metric] = format_eval_command(eval_cmd)

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
                             cmd1=f'{commands[keys["ar"]]}',
                             cmd2=f'{commands[keys["bn"]]}',
                             cmd3=f'{commands[keys["en"]]}',
                             cmd4=f'{commands[keys["fi"]]}',
                             cmd5=f'{commands[keys["id"]]}',
                             cmd6=f'{commands[keys["ja"]]}',
                             cmd7=f'{commands[keys["ko"]]}',
                             cmd8=f'{commands[keys["ru"]]}',
                             cmd9=f'{commands[keys["sw"]]}',
                             cmd10=f'{commands[keys["te"]]}',
                             cmd11=f'{commands[keys["th"]]}',
                             eval_cmd1=f'{eval_commands[keys["ar"]]["MRR@100"]}',
                             eval_cmd2=f'{eval_commands[keys["bn"]]["MRR@100"]}',
                             eval_cmd3=f'{eval_commands[keys["en"]]["MRR@100"]}',
                             eval_cmd4=f'{eval_commands[keys["fi"]]["MRR@100"]}',
                             eval_cmd5=f'{eval_commands[keys["id"]]["MRR@100"]}',
                             eval_cmd6=f'{eval_commands[keys["ja"]]["MRR@100"]}',
                             eval_cmd7=f'{eval_commands[keys["ko"]]["MRR@100"]}',
                             eval_cmd8=f'{eval_commands[keys["ru"]]["MRR@100"]}',
                             eval_cmd9=f'{eval_commands[keys["sw"]]["MRR@100"]}',
                             eval_cmd10=f'{eval_commands[keys["te"]]["MRR@100"]}',
                             eval_cmd11=f'{eval_commands[keys["th"]]["MRR@100"]}'
                             )

            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        print(Template(html_template).substitute(title='Mr.TyDi', rows=all_rows))
