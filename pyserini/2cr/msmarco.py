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



def get_topic_set_key(collection, topic_key):
    """Return the report/runfile key, preserving full topic names for V2.1."""
    if collection.startswith('msmarco-v2.1-'):
        return topic_key

    v1 = collection.startswith('msmarco-v1-')
    if v1 and topic_key.startswith('msmarco'):
        return 'dev'
    if not v1:
        for split in ('dev', 'dev2'):
            if topic_key.endswith((split, f'{split}-unicoil', f'{split}-unicoil-noexp')):
                return split

    # Collapse encoder variants such as dl19-passage-unicoil to the TREC year.
    years = ('dl19', 'dl20') if v1 else ('dl21', 'dl22', 'dl23')
    return next((year for year in years if topic_key.startswith(year)), '')


def get_run_command(collection, condition, topic_set, directory=''):
    topic_key = topic_set['topic_key']
    runfile = os.path.join(directory, f'run.{collection}.{condition["name"]}.{get_topic_set_key(collection, topic_key)}.txt')
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


def _get_display_num(num: float) -> str:
    return f'{num:.4f}' if num != 0 else '-'


REPORT_TOPICS = {
    'msmarco-v1-passage': ('dl19', 'dl20', 'dev'),
    'msmarco-v1-doc': ('dl19', 'dl20', 'dev'),
    'msmarco-v2-passage': ('dl21', 'dl22', 'dl23'),
    'msmarco-v2-doc': ('dl21', 'dl22', 'dl23'),
    'msmarco-v2.1-doc': ('dl21-doc', 'dl22-doc', 'dl23-doc'),
    'msmarco-v2.1-doc-segmented': ('rag24.test', 'rag25.test'),
}


def generate_report(args):
    """Render all MS MARCO reproduction matrices with shared rows and command tabs."""
    v21 = args.collection.startswith('msmarco-v2.1-')
    v1 = args.collection.startswith('msmarco-v1-')
    config = yaml.safe_load(read_file(f'{args.collection}.yaml'))
    conditions = {condition['name']: condition for condition in config['conditions']}

    def topic_label(topic_set):
        key = topic_set['eval_key']
        if key.startswith('dl'):
            return f'TREC 20{key[2:4]}'
        if key.startswith('rag'):
            year = key[3:5]
            split = 'dev' if 'dev' in key else 'test'
            judgments = 'Umbrela' if 'umbrela' in key else 'NIST'
            return f'RAG 20{year} {split} ({judgments})'
        return get_topic_set_key(args.collection, topic_set['topic_key'])

    def report_metrics(topic_set):
        scores = {metric: score for group in topic_set['scores'] for metric, score in group.items()}
        if args.collection == 'msmarco-v2.1-doc-segmented':
            metric = 'nDCG@20' if topic_set['topic_key'].startswith('rag24') else 'nDCG@30'
            return {metric: scores[metric], 'R@100': scores['R@100']}
        if args.collection == 'msmarco-v2.1-doc' and 'MAP@100' in scores:
            return {metric: scores[metric] for metric in ('MAP@100', 'nDCG@10', 'R@1K')}
        return scores

    def topic_id(topic):
        return (topic['topic_key'], topic['eval_key'])

    # Use the union so missing evaluations retain their columns and unavailable tabs.
    all_topics = {topic_id(t): t for c in config['conditions'] for t in c['topics']}
    # Keep every evaluation for each selected topic (e.g., Umbrela and NIST).
    topic_sets = [topic for key in REPORT_TOPICS[args.collection]
                  for topic in all_topics.values()
                  if get_topic_set_key(args.collection, topic['topic_key']) == key]

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
        condition_topics = {topic_id(t): t for t in condition['topics']}
        for tab_num, reference in enumerate(topic_sets, 1):
            topic_set = condition_topics.get(topic_id(reference))
            available = topic_set is not None
            topic_set = topic_set or reference
            runfile, command = get_run_command(args.collection, condition, topic_set)
            definitions = topic_set['metric_definitions']
            eval_commands = []
            for metric, score in report_metrics(topic_set).items():
                value = (f'{score:.4f}' if v21 else _get_display_num(score)) if available else '-'
                cells.append(f'<td>{value}</td>')
                eval_commands.append(f'python -m pyserini.eval.trec_eval {definitions[metric]} {topic_set["eval_key"]} {runfile}')
            if not v1 or tab_num < len(topic_sets):
                cells.append('<td></td>')
            if not v21:
                available = available and next(iter(report_metrics(topic_set).values())) != 0
            tab_id = f'row{row_num}-tab{tab_num}'
            active = ' active' if tab_num == 1 else ''
            tabs.append(f'<li class="nav-item" role="presentation"><a class="nav-link{active}" id="{tab_id}-header" data-mdb-toggle="tab" href="#{tab_id}" role="tab" aria-controls="{tab_id}" aria-selected="{str(tab_num == 1).lower()}" style="text-transform:none">{escape(topic_label(topic_set))}</a></li>')
            panel = command_template.substitute(
                tab_id=tab_id, active=' show active' if tab_num == 1 else '',
                topics=escape(topic_set['topic_key']), qrels=escape(topic_set['eval_key']),
                command=escape(format_command(command)),
                eval_commands=escape('\n'.join(eval_commands)))
            if not available:
                panel = f'<div class="tab-pane fade{" show active" if tab_num == 1 else ""}" id="{tab_id}" role="tabpanel" aria-labelledby="{tab_id}-header">Not available.</div>'
            commands.append(panel)
        rows.append(row_template.substitute(
            row_num=row_num, row_label=row_num if v21 else condition.get('display-row', ''),
            row_style=' style="min-width: 75px"' if v1 else '',
            display_width=410 if v1 else 400,
            name=escape(name), display=condition['display-html'],
            cells=''.join(cells), colspan=len(cells) + 2,
            tabs='\n'.join(tabs), commands='\n'.join(commands)))

    suffix = args.collection.removeprefix('msmarco-')
    title = 'Pyserini: MS MARCO ' + {
        'v1-passage': 'V1 Passage', 'v1-doc': 'V1 Doc',
        'v2-passage': 'V2 Passage', 'v2-doc': 'V2 Doc',
        'v2.1-doc': 'V2.1 Doc', 'v2.1-doc-segmented': 'V2.1 Segmented Doc',
    }[suffix]
    template = 'msmarco_html_' + suffix.replace('v2.1', 'v21').replace('-', '_') + '.template'
    with open(args.output, 'w') as out:
        out.write(Template(read_file(template)).substitute(
            title=title, collection=args.collection.removeprefix('msmarco-'),
            corpus=args.collection, headers=headers, rows='\n'.join(rows),
            example_condition=models[args.collection][0]))


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
                definitions = topic_set['metric_definitions']

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
    if args.condition and args.condition not in get_condition_names(args.collection):
        parser.error(f'Unknown condition for {args.collection}: {args.condition}')

    if args.list_conditions:
        print('\n'.join(get_condition_names(args.collection)))
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
