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

from scripts.repro_matrix.defs_mrtydi import models, languages, html_display, trec_eval_metric_definitions


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


def generate_table_rows(table_id, split, metric):
    row_cnt = 1
    html_rows = []

    for model in models:
        s = Template(row_template)

        keys = {}
        for lang in languages:
            keys[lang[0]] = f'{model}.{lang[0]}'

        sum = table[keys["ar"]][split][metric] + \
              table[keys["bn"]][split][metric] + \
              table[keys["en"]][split][metric] + \
              table[keys["fi"]][split][metric] + \
              table[keys["id"]][split][metric] + \
              table[keys["ja"]][split][metric] + \
              table[keys["ko"]][split][metric] + \
              table[keys["ru"]][split][metric] + \
              table[keys["sw"]][split][metric] + \
              table[keys["te"]][split][metric] + \
              table[keys["th"]][split][metric]
        avg = sum / 11

        s = s.substitute(table_cnt=table_id,
                         row_cnt=row_cnt,
                         model=html_display[model],
                         ar=f'{table[keys["ar"]][split][metric]:.3f}',
                         bn=f'{table[keys["bn"]][split][metric]:.3f}',
                         en=f'{table[keys["en"]][split][metric]:.3f}',
                         fi=f'{table[keys["fi"]][split][metric]:.3f}',
                         id=f'{table[keys["id"]][split][metric]:.3f}',
                         ja=f'{table[keys["ja"]][split][metric]:.3f}',
                         ko=f'{table[keys["ko"]][split][metric]:.3f}',
                         ru=f'{table[keys["ru"]][split][metric]:.3f}',
                         sw=f'{table[keys["sw"]][split][metric]:.3f}',
                         te=f'{table[keys["te"]][split][metric]:.3f}',
                         th=f'{table[keys["th"]][split][metric]:.3f}',
                         avg=f'{avg:.3f}',
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
                         eval_cmd1=f'{eval_commands[keys["ar"]][metric]}',
                         eval_cmd2=f'{eval_commands[keys["bn"]][metric]}',
                         eval_cmd3=f'{eval_commands[keys["en"]][metric]}',
                         eval_cmd4=f'{eval_commands[keys["fi"]][metric]}',
                         eval_cmd5=f'{eval_commands[keys["id"]][metric]}',
                         eval_cmd6=f'{eval_commands[keys["ja"]][metric]}',
                         eval_cmd7=f'{eval_commands[keys["ko"]][metric]}',
                         eval_cmd8=f'{eval_commands[keys["ru"]][metric]}',
                         eval_cmd9=f'{eval_commands[keys["sw"]][metric]}',
                         eval_cmd10=f'{eval_commands[keys["te"]][metric]}',
                         eval_cmd11=f'{eval_commands[keys["th"]][metric]}'
                         )

        html_rows.append(s)
        row_cnt += 1

    return html_rows


if __name__ == '__main__':
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: '')
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file('scripts/repro_matrix/mrtydi_html.template')
    table_template = read_file('scripts/repro_matrix/mrtydi_html_table.template')
    row_template = read_file('scripts/repro_matrix/mrtydi_html_table_row.template')

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

        tables_html = []

        # Build the table for MRR@100, test queries
        html_rows = generate_table_rows(1, 'test', 'MRR@100')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc='MRR@100, test queries', rows=all_rows))

        # Build the table for R@100, test queries
        html_rows = generate_table_rows(2, 'test', 'R@100')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc='Recall@100, test queries', rows=all_rows))

        print(Template(html_template).substitute(title='Mr.TyDi', tables=' '.join(tables_html)))
