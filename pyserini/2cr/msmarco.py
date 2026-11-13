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
import os
import sys
import time
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
        'shard00.arctic-l.hnsw-int8.onnx',
        'shard01.arctic-l.hnsw-int8.onnx',
        'shard02.arctic-l.hnsw-int8.onnx',
        'shard03.arctic-l.hnsw-int8.onnx',
        'shard04.arctic-l.hnsw-int8.onnx',
        'shard05.arctic-l.hnsw-int8.onnx',
        'shard06.arctic-l.hnsw-int8.onnx',
        'shard07.arctic-l.hnsw-int8.onnx',
        'shard08.arctic-l.hnsw-int8.onnx',
        'shard09.arctic-l.hnsw-int8.onnx',
    ],
}



def get_runfile_name(collection, condition_name, topic_key):
    """Build a run filename using the full topic key for every collection."""
    return f'run.{collection}.{condition_name}.{topic_key}.txt'


def get_run_command(collection, condition, topic_set, directory=''):
    topic_key = topic_set['topic_key']
    runfile = os.path.join(directory, get_runfile_name(collection, condition['name'], topic_key))
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


def get_condition_names(collection):
    config = yaml.safe_load(read_file(f'{collection}.yaml'))
    return [condition['name'] for condition in config['conditions']]


REPORT_TOPICS = {
    'msmarco-v1-passage': {
        'TREC 2019': ('AP@1K', 'nDCG@10', 'R@1K'),
        'TREC 2020': ('AP@1K', 'nDCG@10', 'R@1K'),
        'MS MARCO dev': ('RR@10', 'R@1K'),
    },
    'msmarco-v1-doc': {
        'TREC 2019': ('AP@100', 'nDCG@10', 'R@1K'),
        'TREC 2020': ('AP@100', 'nDCG@10', 'R@1K'),
        'MS MARCO dev': ('RR@100', 'R@1K'),
    },
    'msmarco-v2-passage': {
        'TREC 2021': ('AP@100', 'nDCG@10', 'R@1K'),
        'TREC 2022': ('AP@100', 'nDCG@10', 'R@1K'),
        'TREC 2023': ('AP@100', 'nDCG@10', 'R@1K'),
    },
    'msmarco-v2-doc': {
        'TREC 2021': ('AP@100', 'nDCG@10', 'R@1K'),
        'TREC 2022': ('AP@100', 'nDCG@10', 'R@1K'),
        'TREC 2023': ('AP@100', 'nDCG@10', 'R@1K'),
    },
    'msmarco-v2.1-doc': {
        'TREC 2021': ('AP@100', 'nDCG@10', 'R@1K'),
        'TREC 2022': ('AP@100', 'nDCG@10', 'R@1K'),
        'TREC 2023': ('AP@100', 'nDCG@10', 'R@1K'),
    },
    'msmarco-v2.1-doc-segmented': {
        'RAG 2024 test (Umbrela)': ('nDCG@20', 'R@100'),
        'RAG 2024 test (NIST)': ('nDCG@20', 'R@100'),
        'RAG 2025 test (Umbrela)': ('nDCG@30', 'R@100'),
        'RAG 2025 test (NIST)': ('nDCG@30', 'R@100'),
    },
}


def generate_report(args):
    """Render all MS MARCO reproduction matrices with shared rows and command tabs."""
    config = yaml.safe_load(read_file(f'{args.collection}.yaml'))
    conditions = {condition['name']: condition for condition in config['conditions']}

    report_topics = REPORT_TOPICS[args.collection]

    def report_metrics(topic_set):
        scores = {metric: score for group in topic_set['scores'] for metric, score in group.items()}
        return {metric: scores[metric] for metric in report_topics[topic_set['display']]}

    topics_by_condition = {}
    for condition in config['conditions']:
        topics = {}
        for topic in condition['topics']:
            label = topic['display']
            if label in topics:
                raise ValueError(f'Duplicate topic display label "{label}" in condition "{condition["name"]}"')
            scores = {metric for group in topic['scores'] for metric in group}
            for metric in report_topics.get(label, ()):
                if metric not in scores or metric not in topic['metric_definitions']:
                    raise ValueError(f'Missing score or metric definition for "{metric}" in "{label}" of condition "{condition["name"]}"')
            topics[label] = topic
        topics_by_condition[condition['name']] = topics

    group_headers = []
    metric_headers = []
    for topic_num, (label, metrics) in enumerate(report_topics.items(), 1):
        spacer = topic_num < len(report_topics)
        group_headers.append(f'<th class="headertop" colspan="{len(metrics) + int(spacer)}"><b>{escape(label)}</b></th>')
        metric_headers.extend(f'<th class="headerbottom" scope="col">{escape(metric)}</th>' for metric in metrics)
        if spacer:
            metric_headers.append('<th class="headerbottom"></th>')
    headers = ('<tr>' + '<th class="headertop"></th>' * 3 + ''.join(group_headers)
               + '</tr>\n<tr>' + '<th class="headerbottom"></th>' * 3
               + ''.join(metric_headers) + '</tr>')

    command_template = Template(read_file('msmarco_html_commands.template'))
    row_template = Template(read_file('msmarco_html_row.template'))
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
        condition_topics = topics_by_condition[name]
        for tab_num, (label, metrics) in enumerate(report_topics.items(), 1):
            topic_set = condition_topics.get(label)
            available = topic_set is not None
            scores = report_metrics(topic_set) if available else {}
            for metric in metrics:
                value = f'{scores[metric]:.4f}' if available else '-'
                cells.append(f'<td>{value}</td>')
            if tab_num < len(report_topics):
                cells.append('<td></td>')
            tab_id = f'row{row_num}-tab{tab_num}'
            active = ' active' if tab_num == 1 else ''
            tabs.append(f'<li class="nav-item" role="presentation"><a class="nav-link{active}" id="{tab_id}-header" data-mdb-toggle="tab" href="#{tab_id}" role="tab" aria-controls="{tab_id}" aria-selected="{str(tab_num == 1).lower()}" style="text-transform:none">{escape(label)}</a></li>')
            if available:
                runfile, command = get_run_command(args.collection, condition, topic_set)
                definitions = topic_set['metric_definitions']
                eval_commands = [f'python -m pyserini.eval.trec_eval {definitions[metric]} {topic_set["eval_key"]} {quote(runfile)}' for metric in metrics]
                panel = command_template.substitute(
                    tab_id=tab_id, active=' show active' if tab_num == 1 else '',
                    topics=escape(topic_set['topic_key']), qrels=escape(topic_set['eval_key']),
                    command=escape(format_command(command)),
                    eval_commands=escape('\n'.join(eval_commands)))
            else:
                panel = f'<div class="tab-pane fade{" show active" if tab_num == 1 else ""}" id="{tab_id}" role="tabpanel" aria-labelledby="{tab_id}-header">Not available.</div>'
            commands.append(panel)
        rows.append(row_template.substitute(
            row_num=row_num,
            name=escape(name), display=condition['display-html'],
            cells=''.join(cells), colspan=len(cells) + 2,
            tabs='\n'.join(tabs), commands='\n'.join(commands)))

    suffix = args.collection.removeprefix('msmarco-')
    title = 'Pyserini: MS MARCO ' + {
        'v1-passage': 'V1 Passage', 'v1-doc': 'V1 Doc',
        'v2-passage': 'V2 Passage', 'v2-doc': 'V2 Doc',
        'v2.1-doc': 'V2.1 Doc', 'v2.1-doc-segmented': 'V2.1 Segmented Doc',
    }[suffix]
    template = 'msmarco_html_' + suffix.replace('-', '_') + '.template'
    with open(args.output, 'w') as out:
        out.write(Template(read_file(template)).substitute(
            title=title, collection=args.collection.removeprefix('msmarco-'),
            corpus=args.collection, headers=headers, rows='\n'.join(rows),
            example_condition=models[args.collection][0]))


def run_conditions(args):
    start = time.time()

    yaml_data = yaml.safe_load(read_file(f'{args.collection}.yaml'))
    for condition in yaml_data['conditions']:
        # Either we're running all conditions, or running only the condition specified in --condition
        if not args.all and condition['name'] != args.condition:
            continue

        name = condition['name']
        display = condition['display']
        print(f'# Running condition "{name}": {display}\n')
        for topic_set in condition['topics']:
            eval_key = topic_set['eval_key']
            definitions = topic_set['metric_definitions']

            print(f'  - {topic_set["display"]}\n')

            runfile, cmd = get_run_command(args.collection, condition, topic_set, args.directory)

            if not os.path.exists(runfile) and not args.dry_run:
                os.makedirs(os.path.dirname(runfile) or '.', exist_ok=True)
                run_command(cmd, capture_output=False, check=True)

            eval_commands = []
            for expected in topic_set['scores']:
                for metric, expected_value in expected.items():
                    expected_score = float(expected_value)
                    if args.dry_run:
                        print(f'    {metric:7}: {expected_score:.4f}')
                    elif args.skip_eval:
                        continue
                    elif os.path.exists(runfile):
                        score = float(run_eval_and_return_metric(metric, eval_key, definitions[metric], quote(runfile), display_command=False))
                        status = compare_reproduction_score(score, expected_score)
                        result_str = format_reproduction_status(status, expected_score)
                        print(f'    {metric:7}: {score:.4f} {result_str}')
                    else:
                        continue

                    if not args.skip_eval:
                        eval_commands.append(f'python -m pyserini.eval.trec_eval {definitions[metric]} {eval_key} {quote(runfile)}')

            if args.display_commands or args.dry_run:
                commands = format_command(cmd)
                if eval_commands:
                    commands += '\n\n' + '\n'.join(eval_commands)
                print(f'\n```bash\n{commands}\n```')
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
    if args.condition and args.condition not in get_condition_names(args.collection):
        parser.error(f'Unknown condition for {args.collection}: {args.condition}')

    if args.list_conditions:
        print('\n'.join(get_condition_names(args.collection)))
        sys.exit()

    if args.generate_report:
        if not args.output:
            parser.error('Must specify report filename with --output.')

        generate_report(args)
        sys.exit()

    if not args.all and not args.condition:
        parser.error('Must specify a specific condition using --condition or use --all to run all conditions.')

    run_conditions(args)
