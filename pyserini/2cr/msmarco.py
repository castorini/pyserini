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
import importlib.resources
import os
import re
import sys
import time
from collections import defaultdict
from datetime import UTC, datetime
from html import escape
from shlex import quote
from string import Template

import yaml
from pyserini.util import run_command

from ._base import (
    compare_reproduction_score,
    format_reproduction_status,
    read_file,
    run_eval_and_return_metric,
)

dense_threads = 16
dense_batch_size = 512
sparse_threads = 16
sparse_batch_size = 128

# The models: the rows of the results table will be ordered this way.
models = {
    # MS MARCO v1 passage
    'msmarco-v1-passage': [
        'bm25-default',
        'bm25-rm3-default',
        'bm25-rocchio-default',
        '',
        'bm25-tuned',
        'bm25-rm3-tuned',
        'bm25-rocchio-tuned',
        '',
        'bm25-d2q-t5-default',
        'bm25-rm3-d2q-t5-default',
        'bm25-rocchio-d2q-t5-default',
        '',
        'bm25-d2q-t5-tuned',
        'bm25-rm3-d2q-t5-tuned',
        'bm25-rocchio-d2q-t5-tuned',
        '',
        'unicoil-noexp-pytorch',
        'unicoil-noexp-onnx',
        'unicoil-pytorch',
        'unicoil-onnx',
        '',
        'splade-pp-ed-pytorch',
        'splade-pp-ed-onnx',
        'splade-pp-ed-rocchio-pytorch',
        'splade-pp-ed-rocchio-onnx',
        'splade-pp-sd-pytorch',
        'splade-pp-sd-onnx',
        'splade-pp-sd-rocchio-pytorch',
        'splade-pp-sd-rocchio-onnx',
        'splade-v3-pytorch',
        'splade-v3-rocchio-pytorch',
        '',
        'slideon-pytorch',
        'slideon-onnx',
        '',
        'ance-pytorch',
        'ance-avg-prf-pytorch',
        'ance-rocchio-prf-pytorch',
        '',
        'sbert-pytorch',
        'sbert-avg-prf-pytorch',
        'sbert-rocchio-prf-pytorch',
        '',
        'distilbert-kd-pytorch',
        'distilbert-kd-tasb-pytorch',
        'distilbert-kd-tasb-avg-prf-pytorch',
        'distilbert-kd-tasb-rocchio-prf-pytorch',
        '',
        'tct_colbert-v2-hnp-pytorch',
        'tct_colbert-v2-hnp-avg-prf-pytorch',
        'tct_colbert-v2-hnp-rocchio-prf-pytorch',
        '',
        'tct_colbert-v2-hnp-bm25-pytorch',
        'tct_colbert-v2-hnp-bm25d2q-pytorch',
        '',
        'slimr',
        'slimr-pp',
        '',
        'aggretriever-distilbert-pytorch',
        'aggretriever-cocondenser-pytorch',
        '',
        'openai-ada2',
        'openai-ada2-hyde',
        'openai-text-embedding-3-large',
        '',
        'cohere-embed-english-v3.0',
        '',
        'cosdpr-distil.faiss-flat.pytorch',
        'cosdpr-distil.lucene-hnsw.onnx',
        'cosdpr-distil.lucene-hnsw-int8.onnx',
        '',
        'bge-base-en-v1.5.faiss-flat.pytorch',
        'bge-base-en-v1.5.lucene-hnsw.onnx',
        'bge-base-en-v1.5.lucene-hnsw-int8.onnx',
    ],
    # MS MARCO v1 doc
    'msmarco-v1-doc': [
        'bm25-doc-default',
        'bm25-doc-segmented-default',
        'bm25-rm3-doc-default',
        'bm25-rm3-doc-segmented-default',
        'bm25-rocchio-doc-default',
        'bm25-rocchio-doc-segmented-default',
        '',
        'bm25-doc-tuned',
        'bm25-doc-segmented-tuned',
        'bm25-rm3-doc-tuned',
        'bm25-rm3-doc-segmented-tuned',
        'bm25-rocchio-doc-tuned',
        'bm25-rocchio-doc-segmented-tuned',
        '',
        'bm25-d2q-t5-doc-default',
        'bm25-d2q-t5-doc-segmented-default',
        'bm25-rm3-d2q-t5-doc-default',
        'bm25-rm3-d2q-t5-doc-segmented-default',
        '',
        'bm25-d2q-t5-doc-tuned',
        'bm25-d2q-t5-doc-segmented-tuned',
        'bm25-rm3-d2q-t5-doc-tuned',
        'bm25-rm3-d2q-t5-doc-segmented-tuned',
        '',
        'unicoil-noexp-pytorch',
        'unicoil-pytorch',
    ],
    # MS MARCO v2 passage
    'msmarco-v2-passage': [
        'bm25-default',
        'bm25-augmented-default',
        'bm25-rm3-default',
        'bm25-rm3-augmented-default',
        '',
        'bm25-d2q-t5-default',
        'bm25-d2q-t5-augmented-default',
        'bm25-rm3-d2q-t5-default',
        'bm25-rm3-d2q-t5-augmented-default',
        '',
        'unicoil-noexp-pytorch',
        'unicoil-pytorch',
        '',
        'slimr-pp',
    ],
    # MS MARCO v2 doc
    'msmarco-v2-doc': [
        'bm25-doc-default',
        'bm25-doc-segmented-default',
        'bm25-rm3-doc-default',
        'bm25-rm3-doc-segmented-default',
        '',
        'bm25-d2q-t5-doc-default',
        'bm25-d2q-t5-doc-segmented-default',
        'bm25-rm3-d2q-t5-doc-default',
        'bm25-rm3-d2q-t5-doc-segmented-default',
        '',
        'unicoil-noexp-pytorch',
        'unicoil-pytorch',
    ],
    # MS MARCO v2.1 doc
    'msmarco-v2.1-doc': [
        'bm25-doc',
        '',
        'bm25-segmented-doc',
    ],
    # MS MARCO v2.1 segmented doc
    'msmarco-v2.1-doc-segmented': [
        'bm25',
        '',
        'splade-v3.onnx',
        '',
        *[f'shard{i:02d}.arctic-l.hnsw-int8.onnx' for i in range(10)],
    ],
}



def find_msmarco_table_topic_set_key_v1(topic_key):
    # E.g., we want to map variants like 'dl19-passage-unicoil' and 'dl19-passage' both into 'dl19'
    key = ''
    if topic_key.startswith('dl19'):
        key = 'dl19'
    elif topic_key.startswith('dl20'):
        key = 'dl20'
    elif topic_key.startswith('msmarco'):
        key = 'dev'

    return key


def find_msmarco_table_topic_set_key_v2(topic_key):
    key = ''
    if topic_key.endswith(('dev', 'dev-unicoil', 'dev-unicoil-noexp')):
        key = 'dev'
    elif topic_key.endswith(('dev2', 'dev2-unicoil', 'dev2-unicoil-noexp')):
        key = 'dev2'
    elif topic_key.startswith('dl21'):
        key = 'dl21'
    elif topic_key.startswith('dl22'):
        key = 'dl22'
    elif topic_key.startswith('dl23'):
        key = 'dl23'

    return key


def format_eval_command(raw):
    return raw.replace('run.', '\\\n  run.')


def get_topic_set_key(collection, topic_key):
    if collection.startswith('msmarco-v2.1-'):
        # Preserve RAG years and splits; the v2 helper only knows dev/dev2/DL21–23.
        return topic_key
    if collection.startswith('msmarco-v1-'):
        return find_msmarco_table_topic_set_key_v1(topic_key)
    return find_msmarco_table_topic_set_key_v2(topic_key)


def get_metric_definitions(collection, topic_set):
    return topic_set['metric_definitions']


def get_run_command(collection, condition, topic_set, directory=''):
    topic_key = topic_set['topic_key']
    runfile = os.path.join(directory,
                          f'run.{collection}.{condition["name"]}.{get_topic_set_key(collection, topic_key)}.txt')
    command = Template(condition['command']).substitute(
        topics=quote(topic_key), output=quote(runfile),
        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
        dense_threads=dense_threads, dense_batch_size=dense_batch_size)
    return runfile, command


def format_command(raw):
    # Format hybrid commands differently.
    if 'pyserini.search.hybrid' in raw:
        return raw.replace('dense', '\\\n  dense ') \
                .replace('--encoder', '\\\n         --encoder') \
                .replace('sparse', '\\\n  sparse') \
                .replace('fusion', '\\\n  fusion') \
                .replace('run --', '\\\n  run    --') \
                .replace('--topics ', '\\\n         --topics ') \
                .replace('--output ', '\\\n         --output ')

    # After "--output foo.txt" are additional options like "--hits 1000 --impact".
    # We want these on a separate line for better readability, but note that sometimes that might
    # be the end of the command, in which case we don't want to add an extra line break.
    return raw.replace('--topics', '\\\n  --topics') \
        .replace('--threads', '\\\n  --threads') \
        .replace('--index', '\\\n  --index') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--encoder', '\\\n  --encoder') \
        .replace('--onnx-encoder', '\\\n  --onnx-encoder') \
        .replace('--encoded-corpus', '\\\n  --encoded-corpus') \
        .replace('--encoded-queries', '\\\n  --encoded-queries') \
        .replace('.txt ', '.txt \\\n  ')


def list_conditions(args):
    for condition in models[args.collection]:
        if condition == '':
            continue
        print(condition)


def _get_display_num(num: float) -> str:
    return f'{num:.4f}' if num != 0 else '-'


def _remove_commands(table, name, s, v1):
    v1_unavailable_dict = {
        ('dl19', 'MAP'): 'Command to generate run on TREC 2019 queries:.*?</div>',
        ('dl20', 'MAP'): 'Command to generate run on TREC 2020 queries:.*?</div>',
        ('dev', 'MRR@10'): 'Command to generate run on dev queries:.*?</div>',
    }
    v2_unavailable_dict = {
        ('dl21', 'MAP@100'): 'Command to generate run on TREC 2021 queries:.*?</div>',
        ('dl22', 'MAP@100'): 'Command to generate run on TREC 2022 queries:.*?</div>',
        ('dl23', 'MAP@100'): 'Command to generate run on TREC 2023 queries:.*?</div>',
        ('dev', 'MRR@100'): 'Command to generate run on dev queries:.*?</div>',
        ('dev2', 'MRR@100'): 'Command to generate run on dev2 queries:.*?</div>',
    }
    unavailable_dict = v1_unavailable_dict if v1 else v2_unavailable_dict
    for k, v in unavailable_dict.items():
        if table[name][k[0]][k[1]] == 0:
            s = re.sub(re.compile(v, re.MULTILINE | re.DOTALL), 'Not available.</div>', s)
    return s


def generate_report_v21(args):
    """Render the V2.1 reproduction matrices and commands."""
    config = yaml.safe_load(read_file(f'{args.collection}.yaml'))
    conditions = {condition['name']: condition for condition in config['conditions']}
    def topic_order(topic_set):
        key = topic_set['topic_key']
        return (key.endswith('.dev'), key.endswith('.dev2'), key)

    def topic_label(topic_set):
        key = topic_set['eval_key']
        if key.startswith('dl'):
            return f'TREC 20{key[2:4]}'
        if key.startswith('rag'):
            year = key[3:5]
            split = 'dev' if 'dev' in key else 'test'
            judgments = 'Umbrela' if 'umbrela' in key else 'NIST'
            return f'RAG 20{year} {split} ({judgments})'
        return key.rsplit('.', 1)[-1]

    def report_metrics(topic_set):
        scores = {metric: score for group in topic_set['scores'] for metric, score in group.items()}
        if args.collection == 'msmarco-v2.1-doc-segmented':
            metric = 'nDCG@20' if topic_set['topic_key'].startswith('rag24') else 'nDCG@30'
            return {metric: scores[metric], 'R@100': scores['R@100']}
        if args.collection == 'msmarco-v2.1-doc' and 'MAP@100' in scores:
            return {metric: scores[metric] for metric in ('MAP@100', 'nDCG@10', 'R@1K')}
        return scores

    def report_topics(condition):
        topics = condition['topics']
        if args.collection == 'msmarco-v2.1-doc':
            topics = [topic for topic in topics if topic['topic_key'] in ('dl21-doc', 'dl22-doc', 'dl23-doc')]
        return sorted(topics, key=topic_order)

    topic_sets = report_topics(config['conditions'][0])
    group_headers = []
    metric_headers = []
    for topic_set in topic_sets:
        metrics = report_metrics(topic_set)
        group_headers.append(f'<th class="headertop" colspan="{len(metrics) + 1}"><b>{escape(topic_label(topic_set))}</b></th>')
        metric_headers.extend(f'<th class="headerbottom" scope="col">{escape('AP' if args.collection == 'msmarco-v2.1-doc' and metric == 'MAP@100' else metric)}</th>' for metric in metrics)
        metric_headers.append('<th class="headerbottom"></th>')
    headers = ('<tr>' + '<th class="headertop"></th>' * 3 + ''.join(group_headers)
               + '</tr>\n<tr>' + '<th class="headerbottom"></th>' * 3
               + ''.join(metric_headers) + '</tr>')

    command_template = Template(read_file('msmarco_html_commands_v21.template'))
    row_template = Template(read_file('msmarco_html_row_v21.template'))
    rows = []
    row_num = 0
    for name in models[args.collection]:
        if not name:
            rows.append('<tr><td style="border-bottom: 0"></td></tr>')
            continue
        row_num += 1
        condition = conditions[name]
        cells = []
        commands = []
        tabs = []
        for tab_num, topic_set in enumerate(report_topics(condition), 1):
            runfile, command = get_run_command(args.collection, condition, topic_set)
            definitions = get_metric_definitions(args.collection, topic_set)
            eval_commands = []
            for metric, score in report_metrics(topic_set).items():
                cells.append(f'<td>{score:.4f}</td>')
                eval_commands.append(
                    f'python -m pyserini.eval.trec_eval {definitions[metric]} '
                    f'{topic_set["eval_key"]} {runfile}')
            cells.append('<td></td>')
            tab_id = f'row{row_num}-tab{tab_num}'
            active = ' active' if tab_num == 1 else ''
            tabs.append(
                f'<li class="nav-item" role="presentation"><a class="nav-link{active}" '
                f'id="{tab_id}-header" data-mdb-toggle="tab" href="#{tab_id}" role="tab" '
                f'aria-controls="{tab_id}" aria-selected="{str(tab_num == 1).lower()}" '
                f'style="text-transform:none">{escape(topic_label(topic_set))}</a></li>')
            commands.append(command_template.substitute(
                tab_id=tab_id, active=' show active' if tab_num == 1 else '',
                topics=escape(topic_set['topic_key']), qrels=escape(topic_set['eval_key']),
                command=escape(format_command(command)),
                eval_commands=escape('\n'.join(eval_commands))))
        rows.append(row_template.substitute(
            row_num=row_num, name=escape(name), display=condition['display-html'],
            cells=''.join(cells), colspan=len(metric_headers) + 2,
            tabs='\n'.join(tabs), commands='\n'.join(commands)))

    title = ('Pyserini: MS MARCO V2.1 Segmented Doc' if args.collection.endswith('-segmented')
             else 'Pyserini: MS MARCO V2.1 Doc')
    template = ('msmarco_html_v21_doc_segmented.template' if args.collection.endswith('-segmented')
                else 'msmarco_html_v21_doc.template')
    with open(args.output, 'w') as out:
        out.write(Template(read_file(template)).substitute(
            title=title, collection=args.collection.removeprefix('msmarco-'),
            corpus=args.collection, headers=headers, rows='\n'.join(rows),
            example_condition=models[args.collection][0]))


def generate_report(args):
    if args.collection.startswith('msmarco-v2.1-'):
        generate_report_v21(args)
        return

    yaml_file = importlib.resources.files('pyserini.2cr').joinpath(f'{args.collection}.yaml')

    if args.collection == 'msmarco-v1-passage':
        html_template = read_file('msmarco_html_v1_passage.template')
        row_template = read_file('msmarco_html_row_v1.template')
    elif args.collection == 'msmarco-v1-doc':
        html_template = read_file('msmarco_html_v1_doc.template')
        row_template = read_file('msmarco_html_row_v1.template')
    elif args.collection == 'msmarco-v2-passage':
        html_template = read_file('msmarco_html_v2_passage.template')
        row_template = read_file('msmarco_html_row_v2.template')
    elif args.collection == 'msmarco-v2-doc':
        html_template = read_file('msmarco_html_v2_doc.template')
        row_template = read_file('msmarco_html_row_v2.template')
    else:
        raise ValueError(f'Unknown corpus: {args.collection}')

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))

    table_keys = {}
    row_ids = {}

    with yaml_file.open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            display = condition['display-html']
            row_id = condition.get('display-row', '')
            cmd_template = condition['command']

            row_ids[name] = row_id
            table_keys[name] = display

            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
                    short_topic_key = find_msmarco_table_topic_set_key_v1(topic_key)
                else:
                    short_topic_key = find_msmarco_table_topic_set_key_v2(topic_key)

                runfile = f'run.{args.collection}.{name}.{short_topic_key}.txt'
                cmd = Template(cmd_template).substitute(topics=topic_key, output=runfile,
                                                        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                                        dense_threads=dense_threads, dense_batch_size=dense_batch_size)
                commands[name][short_topic_key] = cmd

                for expected in topic_set['scores']:
                    for metric in expected:
                        eval_cmd = f'python -m pyserini.eval.trec_eval {get_metric_definitions(args.collection, topic_set)[metric]} {eval_key} {runfile}'
                        eval_commands[name][short_topic_key] += eval_cmd + '\n'
                        table[name][short_topic_key][metric] = expected[metric]

    if args.collection == 'msmarco-v1-passage' or args.collection == 'msmarco-v1-doc':
        row_cnt = 1

        html_rows = []
        for name in models[args.collection]:
            if not name:
                # Add blank row for spacing
                html_rows.append('<tr><td style="border-bottom: 0"></td></tr>')
                continue
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             condition_name=table_keys[name],
                             row=row_ids[name],
                             s1=_get_display_num(table[name]["dl19"]["MAP"]),
                             s2=_get_display_num(table[name]["dl19"]["nDCG@10"]),
                             s3=_get_display_num(table[name]["dl19"]["R@1K"]),
                             s4=_get_display_num(table[name]["dl20"]["MAP"]),
                             s5=_get_display_num(table[name]["dl20"]["nDCG@10"]),
                             s6=_get_display_num(table[name]["dl20"]["R@1K"]),
                             s7=_get_display_num(table[name]["dev"]["MRR@10"]),
                             s8=_get_display_num(table[name]["dev"]["R@1K"]),
                             cmd1=format_command(commands[name]['dl19']),
                             cmd2=format_command(commands[name]['dl20']),
                             cmd3=format_command(commands[name]['dev']),
                             eval_cmd1=format_eval_command(eval_commands[name]['dl19']),
                             eval_cmd2=format_eval_command(eval_commands[name]['dl20']),
                             eval_cmd3=format_eval_command(eval_commands[name]['dev']))

            # If we don't have scores, we want to remove the commands also. Use simple regexp substitution.
            s = _remove_commands(table, name, s, v1=True)

            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        if args.collection == 'msmarco-v1-passage':
            full_name = 'Pyserini: MS MARCO V1 Passage'
        else:
            full_name = 'Pyserini: MS MARCO V1 Doc'

        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title=full_name, rows=all_rows))
    else:
        row_cnt = 1

        html_rows = []
        for name in models[args.collection]:
            if not name:
                # Add blank row for spacing
                html_rows.append('<tr><td style="border-bottom: 0"></td></tr>')
                continue
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             condition_name=table_keys[name],
                             row=row_ids[name],
                             s1=_get_display_num(table[name]["dl21"]["MAP@100"]),
                             s2=_get_display_num(table[name]["dl21"]["nDCG@10"]),
                             s3=_get_display_num(table[name]["dl21"]["R@1K"]),
                             s4=_get_display_num(table[name]["dl22"]["MAP@100"]),
                             s5=_get_display_num(table[name]["dl22"]["nDCG@10"]),
                             s6=_get_display_num(table[name]["dl22"]["R@1K"]),
                             s7=_get_display_num(table[name]["dl23"]["MAP@100"]),
                             s8=_get_display_num(table[name]["dl23"]["nDCG@10"]),
                             s9=_get_display_num(table[name]["dl23"]["R@1K"]),
                             s10=_get_display_num(table[name]["dev"]["MRR@100"]),
                             s11=_get_display_num(table[name]["dev"]["R@1K"]),
                             s12=_get_display_num(table[name]["dev2"]["MRR@100"]),
                             s13=_get_display_num(table[name]["dev2"]["R@1K"]),
                             cmd1=format_command(commands[name]['dl21']),
                             cmd2=format_command(commands[name]['dl22']),
                             cmd3=format_command(commands[name]['dl23']),
                             cmd4=format_command(commands[name]['dev']),
                             cmd5=format_command(commands[name]['dev2']),
                             eval_cmd1=eval_commands[name]['dl21'],
                             eval_cmd2=eval_commands[name]['dl22'],
                             eval_cmd3=eval_commands[name]['dl23'],
                             eval_cmd4=eval_commands[name]['dev'],
                             eval_cmd5=eval_commands[name]['dev2']
                             )

            # If we don't have scores, we want to remove the commands also. Use simple regexp substitution.
            s = _remove_commands(table, name, s, v1=False)

            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        if args.collection == 'msmarco-v2-passage':
            full_name = 'Pyserini: MS MARCO V2 Passage'
        else:
            full_name = 'Pyserini: MS MARCO V2 Doc'

        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title=full_name, rows=all_rows))


def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    table_keys = {}
    v21 = args.collection.startswith('msmarco-v2.1-')

    with importlib.resources.files('pyserini.2cr').joinpath(f'{args.collection}.yaml').open('r') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            # Either we're running all conditions, or running only the condition specified in --condition
            if not args.all and condition['name'] != args.condition:
                continue

            name = condition['name']
            display = condition['display']
            print(f'# Running condition "{name}": {display}\n')
            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                short_topic_key = get_topic_set_key(args.collection, topic_key)
                # A retrieval run can have several qrels sets (e.g., RAG NIST and Umbrela).
                result_key = (topic_key, eval_key) if v21 else short_topic_key
                definitions = get_metric_definitions(args.collection, topic_set)

                print(f'  - topic_key: {topic_key}')
                if v21:
                    print(f'  - eval_key: {eval_key}')

                runfile, cmd = get_run_command(args.collection, condition, topic_set, args.directory)

                if args.display_commands:
                    print(f'\n```bash\n{format_command(cmd)}\n```\n')

                if not os.path.exists(runfile) and not args.dry_run:
                    os.makedirs(os.path.dirname(runfile) or '.', exist_ok=True)
                    run_command(cmd, capture_output=False, check=True)

                for expected in topic_set['scores']:
                    for metric in expected:
                        table_keys[name] = display
                        if args.dry_run:
                            if args.display_commands and not args.skip_eval:
                                eval_cmd = (f'python -m pyserini.eval.trec_eval {definitions[metric]} '
                                            f'{eval_key} {quote(runfile)}')
                                print(f'\n```bash\n{eval_cmd}\n```\n')
                            if args.skip_eval:
                                table[name][result_key][metric] = expected[metric]
                            continue
                        if not args.skip_eval:
                            # If the runfile doesn't exist, we can't evaluate.
                            if not os.path.exists(runfile):
                                continue

                            score = float(run_eval_and_return_metric(metric, eval_key,
                                    definitions[metric], quote(runfile), display_command=args.display_commands))

                            expected_score = float(expected[metric])
                            status = compare_reproduction_score(score, expected_score)
                            result_str = format_reproduction_status(status, expected_score)
                            print(f'    {metric:7}: {score:.4f} {result_str}')
                            table[name][result_key][metric] = score
                        else:
                            table[name][result_key][metric] = expected[metric]

                if not args.skip_eval:
                    print()

    end = time.time()
    start_str = datetime.fromtimestamp(start, tz=UTC).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.fromtimestamp(end, tz=UTC).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO corpora.')
    parser.add_argument('--collection', type=str, choices=[collection.removeprefix('msmarco-') for collection in models], required=True)
    # To list all conditions
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--all', action='store_true', default=False, help='Run all conditions.')
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)
    parser.add_argument('--dry-run', action='store_true', default=False, help='Print out commands but do not execute.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    parser.add_argument('--display-commands', action='store_true', default=False, help='Display command.')
    args = parser.parse_args()

    args.collection = f'msmarco-{args.collection}'
    if args.condition and args.condition not in models[args.collection]:
        parser.error(f'Unknown condition for {args.collection}: {args.condition}')

    if args.list_conditions:
        list_conditions(args)
        sys.exit()

    if args.generate_report:
        if not args.output:
            print('Must specify report filename with --output.')
            sys.exit()

        generate_report(args)
        sys.exit()

    if not args.all and not args.condition:
        print('Must specify a specific condition using --condition or use --all to run all conditions.')
        sys.exit()

    run_conditions(args)
