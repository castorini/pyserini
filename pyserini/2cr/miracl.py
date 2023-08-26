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
import subprocess
import pkg_resources
from collections import defaultdict, OrderedDict
from string import Template

import yaml

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str

languages = [
    ['ar', 'arabic'],
    ['bn', 'bengali'],
    ['en', 'english'],
    ['es', 'spanish'],
    ['fa', 'persian'],
    ['fi', 'finnish'],
    ['fr', 'french'],
    ['hi', 'hindi'],
    ['id', 'indonesian'],
    ['ja', 'japanese'],
    ['ko', 'korean'],
    ['ru', 'russian'],
    ['sw', 'swahili'],
    ['te', 'telugu'],
    ['th', 'thai'],
    ['zh', 'chinese'],
    ['de', 'german'],
    ['yo', 'yoruba']
]

html_display = OrderedDict()
html_display['bm25'] = 'BM25'
html_display['mdpr-tied-pft-msmarco'] = 'mDPR (tied encoders), pre-FT w/ MS MARCO'
html_display['mdpr-tied-pft-msmarco-ft-all'] = 'mDPR (tied encoders), pre-FT w/ MS MARCO then FT w/ all Mr. TyDi'
html_display['bm25-mdpr-tied-pft-msmarco-hybrid'] = 'Hybrid of `bm25` and `mdpr-tied-pft-msmarco`'
html_display['mdpr-tied-pft-msmarco-ft-miracl'] = 'mDPR (tied encoders), pre-FT w/ MS MARCO then in-lang FT w/ MIRACL'
html_display['mcontriever-tied-pft-msmarco'] = 'mContriever (tied encoders), pre-FT w/ MS MARCO'

models = list(html_display)

trec_eval_metric_definitions = {
    'nDCG@10': '-c -M 100 -m ndcg_cut.10',
    'R@100': '-c -m recall.100',
}


def format_run_command(raw):
    return raw.replace('--lang', '\\\n  --lang') \
        .replace('--encoder', '\\\n  --encoder') \
        .replace('--topics', '\\\n  --topics') \
        .replace('--index', '\\\n  --index') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--runs', '\\\n  --runs ') \
        .replace('--batch ', '\\\n  --batch ') \
        .replace('--threads 12', '--threads 12 \\\n ')


def format_eval_command(raw):
    return raw.replace('-c ', '\\\n  -c ') \
        .replace(raw.split()[-1], f'\\\n  {raw.split()[-1]}')


def read_file(f):
    fin = open(f, 'r')
    text = fin.read()
    fin.close()

    return text


def list_conditions():
    print('Conditions:\n-----------')
    for condition, _ in html_display.items():
        print(condition)
    print('\nLanguages\n---------')
    for language in languages:
        print(language[0])


def generate_table_rows(table, row_template, commands, eval_commands, table_id, split, metric):
    row_cnt = 1
    html_rows = []

    for model in models:
        s = Template(row_template)

        keys = {}
        used_langs = 0
        for lang in languages:
            keys[lang[0]] = f'{model}.{lang[0]}'
            used_langs += 1 if table[keys[lang[0]]][split][metric] != 0 else 0

        sum = table[keys["ar"]][split][metric] + \
              table[keys["bn"]][split][metric] + \
              table[keys["en"]][split][metric] + \
              table[keys["es"]][split][metric] + \
              table[keys["fa"]][split][metric] + \
              table[keys["fi"]][split][metric] + \
              table[keys["fr"]][split][metric] + \
              table[keys["hi"]][split][metric] + \
              table[keys["id"]][split][metric] + \
              table[keys["ja"]][split][metric] + \
              table[keys["ko"]][split][metric] + \
              table[keys["ru"]][split][metric] + \
              table[keys["sw"]][split][metric] + \
              table[keys["te"]][split][metric] + \
              table[keys["th"]][split][metric] + \
              table[keys["zh"]][split][metric] + \
              table[keys["de"]][split][metric] + \
              table[keys["yo"]][split][metric]
        avg = sum / used_langs

        s = s.substitute(table_cnt=table_id,
                         row_cnt=row_cnt,
                         model=html_display[model],
                         ar=f'{table[keys["ar"]][split][metric]:.3f}',
                         bn=f'{table[keys["bn"]][split][metric]:.3f}',
                         en=f'{table[keys["en"]][split][metric]:.3f}',
                         es=f'{table[keys["es"]][split][metric]:.3f}',
                         fa=f'{table[keys["fa"]][split][metric]:.3f}',
                         fi=f'{table[keys["fi"]][split][metric]:.3f}',
                         fr=f'{table[keys["fr"]][split][metric]:.3f}',
                         hi=f'{table[keys["hi"]][split][metric]:.3f}',
                         id=f'{table[keys["id"]][split][metric]:.3f}',
                         ja=f'{table[keys["ja"]][split][metric]:.3f}',
                         ko=f'{table[keys["ko"]][split][metric]:.3f}',
                         ru=f'{table[keys["ru"]][split][metric]:.3f}',
                         sw=f'{table[keys["sw"]][split][metric]:.3f}',
                         te=f'{table[keys["te"]][split][metric]:.3f}',
                         th=f'{table[keys["th"]][split][metric]:.3f}',
                         zh=f'{table[keys["zh"]][split][metric]:.3f}',
                         de=f'{table[keys["de"]][split][metric]:.3f}',
                         yo=f'{table[keys["yo"]][split][metric]:.3f}',
                         avg=f'{avg:.3f}',
                         cmd1=f'{commands[keys["ar"]]}',
                         cmd2=f'{commands[keys["bn"]]}',
                         cmd3=f'{commands[keys["en"]]}',
                         cmd4=f'{commands[keys["es"]]}',
                         cmd5=f'{commands[keys["fa"]]}',
                         cmd6=f'{commands[keys["fi"]]}',
                         cmd7=f'{commands[keys["fr"]]}',
                         cmd8=f'{commands[keys["hi"]]}',
                         cmd9=f'{commands[keys["id"]]}',
                         cmd10=f'{commands[keys["ja"]]}',
                         cmd11=f'{commands[keys["ko"]]}',
                         cmd12=f'{commands[keys["ru"]]}',
                         cmd13=f'{commands[keys["sw"]]}',
                         cmd14=f'{commands[keys["te"]]}',
                         cmd15=f'{commands[keys["th"]]}',
                         cmd16=f'{commands[keys["zh"]]}',
                         cmd17=f'{commands[keys["de"]]}',
                         cmd18=f'{commands[keys["yo"]]}',
                         eval_cmd1=f'{eval_commands[keys["ar"]][metric]}',
                         eval_cmd2=f'{eval_commands[keys["bn"]][metric]}',
                         eval_cmd3=f'{eval_commands[keys["en"]][metric]}',
                         eval_cmd4=f'{eval_commands[keys["es"]][metric]}',
                         eval_cmd5=f'{eval_commands[keys["fa"]][metric]}',
                         eval_cmd6=f'{eval_commands[keys["fi"]][metric]}',
                         eval_cmd7=f'{eval_commands[keys["fr"]][metric]}',
                         eval_cmd8=f'{eval_commands[keys["hi"]][metric]}',
                         eval_cmd9=f'{eval_commands[keys["id"]][metric]}',
                         eval_cmd10=f'{eval_commands[keys["ja"]][metric]}',
                         eval_cmd11=f'{eval_commands[keys["ko"]][metric]}',
                         eval_cmd12=f'{eval_commands[keys["ru"]][metric]}',
                         eval_cmd13=f'{eval_commands[keys["sw"]][metric]}',
                         eval_cmd14=f'{eval_commands[keys["te"]][metric]}',
                         eval_cmd15=f'{eval_commands[keys["th"]][metric]}',
                         eval_cmd16=f'{eval_commands[keys["zh"]][metric]}',
                         eval_cmd17=f'{eval_commands[keys["de"]][metric]}',
                         eval_cmd18=f'{eval_commands[keys["yo"]][metric]}'
                         )

        s = s.replace("0.000", "--")
        html_rows.append(s)
        row_cnt += 1

    return html_rows


def print_results(table, metric, split):
    print(f'Metric = {metric}, Split = {split}')
    print(' ' * 35, end='')
    for lang in languages:
        print(f'{lang[0]:3}    ', end='')
    print('')
    for model in models:
        print(f'{model:33}', end='')
        for lang in languages:
            key = f'{model}.{lang[0]}'
            print(f'{table[key][split][metric]:7.3f}', end='')
        print('')
    print('')


def extract_topic_fn_from_cmd(cmd):
    cmd = cmd.split()
    topic_idx = cmd.index('--topics')
    return cmd[topic_idx + 1]


def generate_report(args):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: '')
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    html_template = read_file(pkg_resources.resource_filename(__name__, 'miracl_html.template'))
    table_template = read_file(pkg_resources.resource_filename(__name__, 'miracl_html_table.template'))
    row_template = read_file(pkg_resources.resource_filename(__name__, 'miracl_html_table_row.template'))

    with open(pkg_resources.resource_filename(__name__, 'miracl.yaml')) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            eval_key = condition['eval_key']
            cmd_template = condition['command']
            cmd_lst = cmd_template.split()
            lang = name.split('.')[-1]
            is_hybrid_run = 'hybrid' in name

            for splits in condition['splits']:
                split = splits['split']
                if is_hybrid_run:
                    hits = int(cmd_lst[cmd_lst.index('--k') + 1])
                else:
                    hits = int(cmd_lst[cmd_lst.index('--hits') + 1])

                runfile = os.path.join(args.directory, f'run.miracl.{name}.{split}.txt')
                if is_hybrid_run:
                    bm25_output = os.path.join(args.directory,
                                               f'run.miracl.bm25.{lang}.{split}.top{hits}.txt')
                    mdpr_output = os.path.join(args.directory,
                                               f'run.miracl.mdpr-tied-pft-msmarco.{lang}.{split}.top{hits}.txt')
                    expected_args = dict(output=runfile, bm25_output=bm25_output, mdpr_output=mdpr_output)
                else:
                    expected_args = dict(split=split, output=runfile)

                if not all([f"${k}" in cmd_template or f"${{{k}}}" in cmd_template for k in expected_args]):
                    raise ValueError(f"Not all arguements {list(expected_args)} detected from inputs: {cmd_template}.")
                cmd = Template(cmd_template).substitute(**expected_args)
                commands[name] = format_run_command(cmd)

                for expected in splits['scores']:
                    for metric in expected:
                        if str(expected[metric])[-1] == "5":
                            # without adding espilon, there is a chance that f-string would round 0.5 to 0 rather than 1
                            # e.g., 0.8885 -> 0.888 rather than 0.889
                            # add a espilon to the expected score to avoid rounding error
                            expected[metric] += 1e-5
                        table[name][split][metric] = expected[metric]

                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[metric]} {eval_key}-{split} {runfile}'
                        eval_commands[name][metric] = format_eval_command(eval_cmd)

        tables_html = []

        split = 'dev'

        # Build the table for MRR@100, test queries
        html_rows = generate_table_rows(table, row_template, commands, eval_commands, 1, split, 'nDCG@10')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc=f'nDCG@10, {split} queries', rows=all_rows))

        # Build the table for R@100, test queries
        html_rows = generate_table_rows(table, row_template, commands, eval_commands, 2, split, 'R@100')
        all_rows = '\n'.join(html_rows)
        tables_html.append(Template(table_template).substitute(desc=f'Recall@100, {split} queries', rows=all_rows))

    with open(args.output, 'w') as out:
        out.write(Template(html_template).substitute(title='MIRACL', tables=' '.join(tables_html)))


def run_conditions(args):
    if args.condition == 'mdpr-tied-pft-msmarco-ft-miracl' and args.language in ['de', 'yo']:
        print('MIRACL de and yo datasets do not have train splits to finetune with')
        return

    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open(pkg_resources.resource_filename(__name__, 'miracl.yaml')) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            encoder = name.split('.')[0]
            lang = name.split('.')[-1]
            if args.all:
                pass
            elif args.condition != encoder:
                continue
            elif args.language and args.language != lang:
                continue
            eval_key = condition['eval_key']
            cmd_template = condition['command']
            cmd_lst = cmd_template.split()

            print(f'condition {name}:')
            is_hybrid_run = 'hybrid' in name

            for splits in condition['splits']:
                split = splits['split']
                if is_hybrid_run:
                    hits = int(cmd_lst[cmd_lst.index('--k') + 1])
                else:
                    hits = int(cmd_lst[cmd_lst.index('--hits') + 1])

                print(f'  - split: {split}')

                runfile = os.path.join(args.directory, f'run.miracl.{name}.{split}.top{hits}.txt')
                if is_hybrid_run:
                    bm25_output = os.path.join(args.directory,
                                               f'run.miracl.bm25.{lang}.{split}.top{hits}.txt')
                    mdpr_output = os.path.join(args.directory,
                                               f'run.miracl.mdpr-tied-pft-msmarco.{lang}.{split}.top{hits}.txt')
                    if not os.path.exists(bm25_output):
                        print(f'Missing BM25 file: {bm25_output}')
                        continue
                    if not os.path.exists(mdpr_output):
                        print(f'Missing mDPR file: {mdpr_output}')
                        continue
                    cmd = Template(cmd_template).substitute(split=split, output=runfile, bm25_output=bm25_output,
                                                            mdpr_output=mdpr_output)
                else:
                    cmd = Template(cmd_template).substitute(split=split, output=runfile)

                # In the yaml file, the topics are written as something like '--topics miracl-v1.0-ar-${split}'
                # This works for the dev split because the topics are directly included in Anserini/Pyserini.
                # For this training split, we have to map the symbol into a file in tools/topics-and-qrels/
                # Here, we assume that the developer has cloned the miracl repo and placed the topics there.
                if split == 'train':
                    cmd = cmd.replace(f'--topics miracl-v1.0-{lang}-{split}',
                                      f'--topics tools/topics-and-qrels/topics.miracl-v1.0-{lang}-{split}.tsv')

                if args.display_commands:
                    print(f'\n```bash\n{format_run_command(cmd)}\n```\n')

                if not os.path.exists(runfile):
                    if not args.dry_run:
                        rtn = subprocess.run(cmd.split(), capture_output=True)
                        stderr = rtn.stderr.decode()
                        if '--topics' in cmd:
                            topic_fn = extract_topic_fn_from_cmd(cmd)
                            if f'ValueError: Topic {topic_fn} Not Found' in stderr:
                                print(f'Skipping {topic_fn}: file not found.')
                                continue

                for expected in splits['scores']:
                    for metric in expected:
                        if not args.skip_eval:
                            # We have the translate the training qrels into a file located in tools/topics-and-qrels/
                            # because they are not included with Anserini/Pyserini by default.
                            # Here, we assume that the developer has cloned the miracl repo and placed the qrels there.
                            if split == 'train':
                                qrels = f'tools/topics-and-qrels/qrels.{eval_key}-train.tsv'
                            else:
                                qrels = f'{eval_key}-{split}'
                            score = float(run_eval_and_return_metric(metric, qrels,
                                                                     trec_eval_metric_definitions[metric], runfile))
                            if math.isclose(score, float(expected[metric])):
                                result_str = ok_str
                            # Flaky tests
                            elif (name == 'mdpr-tied-pft-msmarco.hi' and split == 'train'
                                  and math.isclose(score, float(expected[metric]), abs_tol=2e-4)) or \
                                 (name == 'bm25-mdpr-tied-pft-msmarco-hybrid.zh'
                                  and split == 'dev' and metric == 'nDCG@10'
                                  and math.isclose(score, float(expected[metric]), abs_tol=2e-4)) or \
                                 (name == 'mdpr-tied-pft-msmarco-ft-all.ru'
                                 # Flaky on Jimmy's Mac Studio (Apple M1 Ultra), nDCG@10: 0.3932 -> expected 0.3933
                                  and split == 'dev' and metric == 'nDCG@10'
                                  and math.isclose(score, float(expected[metric]), abs_tol=2e-4)) or \
                                 (name == 'bm25-mdpr-tied-pft-msmarco-hybrid.te'
                                 # Flaky on Jimmy's Mac Studio (Apple M1 Ultra), nDCG@10: 0.6000 -> expected 0.5999
                                  and split == 'train' and metric == 'nDCG@10'
                                  and math.isclose(score, float(expected[metric]), abs_tol=2e-4)) or \
                                 (name == 'mcontriever-tied-pft-msmarco.id'
                                 # Flaky on Jimmy's Mac Studio (Apple M1 Ultra), nDCG@10: 0.3748 -> expected 0.3749
                                  and split == 'train' and metric == 'nDCG@10'
                                  and math.isclose(score, float(expected[metric]), abs_tol=2e-4)):
                                result_str = okish_str
                            else:
                                result_str = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result_str}')
                            table[name][split][metric] = score
                        else:
                            table[name][split][metric] = expected[metric]

            print('')

    for metric in ['nDCG@10', 'R@100']:
        for split in ['dev', 'train']:
            print_results(table, metric, split)

    end = time.time()
    print(f'Total elapsed time: {end - start:.0f}s')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MIRACL.')
    parser.add_argument('--condition', type=str,
                        help='Condition to run', required=False)
    # To list all conditions
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--all', action='store_true', default=False, help='Run using all languages.')
    parser.add_argument('--language', type=str, help='Language to run.', required=False)
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

    if args.all and (args.condition or args.language):
        print('Specifying --all will run all conditions and languages')
        sys.exit()

    run_conditions(args)
