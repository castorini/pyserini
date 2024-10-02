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
import math
import os
import sys
import time
from collections import defaultdict
from datetime import datetime
from string import Template

import yaml

from ._base import run_eval_and_return_metric, ok_str, okish_str, fail_str

dense_threads = 16
dense_batch_size = 512
sparse_threads = 16
sparse_batch_size = 128

metrics = ['nDCG@10', 'R@100', 'R@1000']

trec_eval_metric_definitions = {
    'nDCG@10': '-c -m ndcg_cut.10',
    'R@100': '-c -m recall.100',
    'R@1000': '-c -m recall.1000'
}

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

models = ['bm25-flat', 
          'bm25-multifield', 
          'splade-pp-ed', 
          'contriever', 
          'contriever-msmarco', 
          'bge-base-en-v1.5.faiss',
          'bge-base-en-v1.5.lucene-flat',
          'bge-base-en-v1.5.lucene-hnsw',
          'cohere-embed-english-v3.0']


def format_run_command(raw):
    return raw.replace('--topics', '\\\n  --topics') \
        .replace('--threads', '\\\n  --threads') \
        .replace('--index', '\\\n  --index') \
        .replace('--encoder-class', '\\\n  --encoder-class') \
        .replace('--encoded-queries', '\\\n  --encoded-queries') \
        .replace('--output ', '\\\n  --output ') \
        .replace('--output-format trec ', '\\\n  --output-format trec ') \
        .replace('--hits ', '\\\n  --hits ') \
        .replace('--query-prefix', '\\\n  --query-prefix')


def format_eval_command(raw):
    return raw.replace('-c ', '\\\n  -c ') \
        .replace('run.', '\\\n  run.')


def read_file(f):
    fin = open(importlib.resources.files("pyserini.2cr")/f, 'r')
    text = fin.read()
    fin.close()

    return text


def list_conditions():
    with open(importlib.resources.files("pyserini.2cr")/'beir.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            print(condition['name'])


def list_datasets():
    for dataset in beir_keys:
        print(dataset)


def generate_report(args):
    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
    commands = defaultdict(lambda: defaultdict(lambda: ''))
    eval_commands = defaultdict(lambda: defaultdict(lambda: ''))
    cqa_commands = defaultdict(lambda: '')
    cqa_eval_commands = defaultdict(lambda: '')

    html_template = read_file('beir_html.template')
    row_template = read_file('beir_html_row.template')

    with open(importlib.resources.files("pyserini.2cr")/'beir.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            cmd_template = condition['command']

            for datasets in condition['datasets']:
                dataset = datasets['dataset']
                query_prefix = '""'
                if name == 'bge-base-en-v1.5.faiss' and dataset not in ['quora', 'arguana']:
                    query_prefix = '"Represent this sentence for searching relevant passages:"'
                runfile = os.path.join(args.directory, f'run.beir.{name}.{dataset}.txt')
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile,
                                                        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                                        dense_threads=dense_threads, dense_batch_size=dense_batch_size, query_prefix=query_prefix)
                commands[dataset][name] = format_run_command(cmd)

                if dataset.startswith('cqadupstack-'):
                    cqa_commands[name] += commands[dataset][name] + '\n\n'

                for expected in datasets['scores']:
                    for metric in expected:
                        eval_cmd = f'python -m pyserini.eval.trec_eval ' + \
                                   f'{trec_eval_metric_definitions[metric]} beir-v1.0.0-{dataset}-test {runfile}'
                        eval_commands[dataset][name] += format_eval_command(eval_cmd) + '\n\n'
                        
                        if dataset.startswith('cqadupstack-'):
                            cqa_eval_commands[name] += eval_commands[dataset][name]
                        
                        table[dataset][name][metric] = expected[metric]

        row_cnt = 1
        main_rows = []
        cqa_rows = []
        cqa_row_flag = False
        cqadupstack_sums = defaultdict(lambda: defaultdict(float))
        
        for dataset in beir_keys:
            s = Template(row_template)
            s = s.substitute(row_cnt=row_cnt,
                             dataset=dataset.split('-')[1] if dataset.startswith('cqadupstack-') else dataset,
                             s1=f'{table[dataset]["bm25-flat"]["nDCG@10"]:8.3f}',
                             s2=f'{table[dataset]["bm25-flat"]["R@100"]:8.3f}',
                             s3=f'{table[dataset]["bm25-multifield"]["nDCG@10"]:8.3f}',
                             s4=f'{table[dataset]["bm25-multifield"]["R@100"]:8.3f}',
                             s5=f'{table[dataset]["splade-pp-ed"]["nDCG@10"]:8.3f}',
                             s6=f'{table[dataset]["splade-pp-ed"]["R@100"]:8.3f}',
                             s7=f'{table[dataset]["contriever-msmarco"]["nDCG@10"]:8.3f}',
                             s8=f'{table[dataset]["contriever-msmarco"]["R@100"]:8.3f}',
                             s9=f'{table[dataset]["bge-base-en-v1.5.faiss"]["nDCG@10"]:8.3f}',
                             s10=f'{table[dataset]["bge-base-en-v1.5.faiss"]["R@100"]:8.3f}',
                             s11=f'{table[dataset]["cohere-embed-english-v3.0"]["nDCG@10"]:8.3f}',
                             s12=f'{table[dataset]["cohere-embed-english-v3.0"]["R@100"]:8.3f}',
                             cmd1=commands[dataset]["bm25-flat"],
                             cmd2=commands[dataset]["bm25-multifield"],
                             cmd3=commands[dataset]["splade-pp-ed"],
                             cmd4=commands[dataset]["contriever-msmarco"],
                             cmd5=commands[dataset]["bge-base-en-v1.5.faiss"],
                             cmd6=commands[dataset]["cohere-embed-english-v3.0"],
                             eval_cmd1=eval_commands[dataset]["bm25-flat"].rstrip(),
                             eval_cmd2=eval_commands[dataset]["bm25-multifield"].rstrip(),
                             eval_cmd3=eval_commands[dataset]["splade-pp-ed"].rstrip(),
                             eval_cmd4=eval_commands[dataset]["contriever-msmarco"].rstrip(),
                             eval_cmd5=eval_commands[dataset]["bge-base-en-v1.5.faiss"].rstrip(),
                             eval_cmd6=eval_commands[dataset]["cohere-embed-english-v3.0"].rstrip())
            row_cnt += 1
            if dataset.startswith('cqadupstack-'):
                cqa_rows.append(s)
                if cqa_row_flag is False:
                    cqa_row_flag = True

                for model in models:
                    for metric in metrics:
                        cqadupstack_sums[model][metric] += table[dataset][model][metric]
            else:
                if cqa_row_flag:
                    cqa_row_flag = False
                    cqa_row = Template(row_template)
                    cqa_row = cqa_row.substitute(row_cnt=row_cnt,
                             dataset='cqadupstack (average)',
                             s1=f'{cqadupstack_sums["bm25-flat"]["nDCG@10"]/12:8.3f}',
                             s2=f'{cqadupstack_sums["bm25-flat"]["R@100"]/12:8.3f}',
                             s3=f'{cqadupstack_sums["bm25-multifield"]["nDCG@10"]/12:8.3f}',
                             s4=f'{cqadupstack_sums["bm25-multifield"]["R@100"]/12:8.3f}',
                             s5=f'{cqadupstack_sums["splade-pp-ed"]["nDCG@10"]/12:8.3f}',
                             s6=f'{cqadupstack_sums["splade-pp-ed"]["R@100"]/12:8.3f}',
                             s7=f'{cqadupstack_sums["contriever-msmarco"]["nDCG@10"]/12:8.3f}',
                             s8=f'{cqadupstack_sums["contriever-msmarco"]["R@100"]/12:8.3f}',
                             s9=f'{cqadupstack_sums["bge-base-en-v1.5.faiss"]["nDCG@10"]/12:8.3f}',
                             s10=f'{cqadupstack_sums["bge-base-en-v1.5.faiss"]["R@100"]/12:8.3f}',
                             s11=f'{cqadupstack_sums["cohere-embed-english-v3.0"]["nDCG@10"]/12:8.3f}',
                             s12=f'{cqadupstack_sums["cohere-embed-english-v3.0"]["R@100"]/12:8.3f}',
                             cmd1=cqa_commands["bm25-flat"],
                             cmd2=cqa_commands["bm25-multifield"],
                             cmd3=cqa_commands["splade-pp-ed"],
                             cmd4=cqa_commands["contriever-msmarco"],
                             cmd5=cqa_commands["bge-base-en-v1.5.faiss"],
                             cmd6=cqa_commands["cohere-embed-english-v3.0"],
                             eval_cmd1=cqa_eval_commands["bm25-flat"].rstrip(),
                             eval_cmd2=cqa_eval_commands["bm25-multifield"].rstrip(),
                             eval_cmd3=cqa_eval_commands["splade-pp-ed"].rstrip(),
                             eval_cmd4=cqa_eval_commands["contriever-msmarco"].rstrip(),
                             eval_cmd5=cqa_eval_commands["bge-base-en-v1.5.faiss"].rstrip(),
                             eval_cmd6=cqa_eval_commands["cohere-embed-english-v3.0"].rstrip())
                    main_rows.append(cqa_row)
                    row_cnt += 1
                main_rows.append(s)
            
        main_rows = '\n'.join(main_rows)
        cqa_rows = '\n'.join(cqa_rows)
        with open(args.output, 'w') as out:
            out.write(Template(html_template).substitute(title='Pyserini BEIR Regressions', main_rows=main_rows, cqa_rows=cqa_rows))


def run_conditions(args):
    start = time.time()

    table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))

    with open(importlib.resources.files("pyserini.2cr")/'beir.yaml') as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            cmd_template = condition['command']

            if args.all or args.condition == name:
                print(f'condition {name}:')
            else:
                continue

            for datasets in condition['datasets']:
                dataset = datasets['dataset']
                query_prefix = '""'
                if name == 'bge-base-en-v1.5.faiss' and dataset not in ['quora', 'arguana']:
                    query_prefix = '"Represent this sentence for searching relevant passages:"'
                if args.all:
                    pass
                elif args.condition != name:
                    continue
                elif args.dataset and args.dataset != dataset:
                    continue

                print(f'  - dataset: {dataset}')

                runfile = os.path.join(args.directory, f'run.beir.{name}.{dataset}.txt')
                cmd = Template(cmd_template).substitute(dataset=dataset, output=runfile,
                                                        sparse_threads=sparse_threads, sparse_batch_size=sparse_batch_size,
                                                        dense_threads=dense_threads, dense_batch_size=dense_batch_size, query_prefix=query_prefix)
                
                if args.display_commands:
                    print(f'\n```bash\n{format_run_command(cmd)}\n```\n')

                if not os.path.exists(runfile):
                    if not args.dry_run:
                        os.system(cmd)

                for expected in datasets['scores']:
                    for metric in expected:
                        if not args.skip_eval and not args.dry_run:
                            if not os.path.exists(runfile):
                                continue

                            score = float(run_eval_and_return_metric(metric, f'beir-v1.0.0-{dataset}-test',
                                                                     trec_eval_metric_definitions[metric], runfile))
                            if math.isclose(score, float(expected[metric])):
                                result = ok_str
                            # If results are within 0.0005, just call it "OKish".
                            elif abs(score - float(expected[metric])) <= 0.0005:
                                result = okish_str + f' expected {expected[metric]:.4f}'
                            else:
                                result = fail_str + f' expected {expected[metric]:.4f}'
                            print(f'      {metric:7}: {score:.4f} {result}')

                            table[dataset][name][metric] = score
                        else:
                            table[dataset][name][metric] = expected[metric]
                    print('')

            print('')

    top_level_sums = defaultdict(lambda: defaultdict(float))
    cqadupstack_sums = defaultdict(lambda: defaultdict(float))
    cqa_scores = defaultdict(lambda: defaultdict(float))
    final_scores = defaultdict(lambda: defaultdict(float))

    # Compute the running sums to compute the final mean scores
    for key in beir_keys:
        for model in models:
            for metric in metrics:
                if key.startswith('cqa'):
                    # The running sum for cqa needs to be kept separately.
                    cqadupstack_sums[model][metric] += table[key][model][metric]
                else:
                    top_level_sums[model][metric] += table[key][model][metric]

    # Compute the final mean
    for model in models:
        for metric in metrics:
            # Compute mean over cqa sub-collections first
            cqa_score = cqadupstack_sums[model][metric] / 12
            cqa_scores[model][metric] = cqa_score
            # Roll cqa scores into final overall mean
            final_score = (top_level_sums[model][metric] + cqa_score) / 18
            final_scores[model][metric] = final_score

    cqa_output_flag = False

    print(' ' * 30 + 'BM25-flat' + ' ' * 10 + 'BM25-mf' + ' ' * 13 + 'SPLADE' + ' ' * 11 + 'Contriever' + ' ' * 5 + 'Contriever-msmarco' +
          ' ' * 6 + 'BGE.Faiss' + ' ' * 7 + 'BGE.Lucene-flat' + ' ' * 4 + 'BGE.Lucene-HNSW' + ' ' * 8 + 'Cohere')
    print(' ' * 28 + 'nDCG    R@100      ' * 9)
    print(' ' * 28 + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13)
    for dataset in beir_keys:
        # The first encounter of 'cqa', print out the average.
        if dataset.startswith('cqa') and not cqa_output_flag:
            print('cqa' + ' ' * 22 + f'{cqa_scores["bm25-flat"]["nDCG@10"]:8.3f}{cqa_scores["bm25-flat"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["bm25-multifield"]["nDCG@10"]:8.3f}{cqa_scores["bm25-multifield"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["splade-pp-ed"]["nDCG@10"]:8.3f}{cqa_scores["splade-pp-ed"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["contriever"]["nDCG@10"]:8.3f}{cqa_scores["contriever"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["contriever-msmarco"]["nDCG@10"]:8.3f}{cqa_scores["contriever-msmarco"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["bge-base-en-v1.5.faiss"]["nDCG@10"]:8.3f}{cqa_scores["bge-base-en-v1.5.faiss"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["bge-base-en-v1.5.lucene-flat"]["nDCG@10"]:8.3f}{cqa_scores["bge-base-en-v1.5.lucene-flat"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["bge-base-en-v1.5.lucene-hnsw"]["nDCG@10"]:8.3f}{cqa_scores["bge-base-en-v1.5.lucene-hnsw"]["R@100"]:8.3f}   ' +
                  f'{cqa_scores["cohere-embed-english-v3.0"]["nDCG@10"]:8.3f}{cqa_scores["cohere-embed-english-v3.0"]["R@100"]:8.3f}')
            cqa_output_flag = True
            continue

        # Skip all other cqa sub-collections.
        if dataset.startswith('cqa'):
            continue

        print(f'{dataset:25}' +
              f'{table[dataset]["bm25-flat"]["nDCG@10"]:8.3f}{table[dataset]["bm25-flat"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bm25-multifield"]["nDCG@10"]:8.3f}{table[dataset]["bm25-multifield"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["splade-pp-ed"]["nDCG@10"]:8.3f}{table[dataset]["splade-pp-ed"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["contriever"]["nDCG@10"]:8.3f}{table[dataset]["contriever"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["contriever-msmarco"]["nDCG@10"]:8.3f}{table[dataset]["contriever-msmarco"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bge-base-en-v1.5.faiss"]["nDCG@10"]:8.3f}{table[dataset]["bge-base-en-v1.5.faiss"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bge-base-en-v1.5.lucene-flat"]["nDCG@10"]:8.3f}{table[dataset]["bge-base-en-v1.5.lucene-flat"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bge-base-en-v1.5.lucene-hnsw"]["nDCG@10"]:8.3f}{table[dataset]["bge-base-en-v1.5.lucene-hnsw"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["cohere-embed-english-v3.0"]["nDCG@10"]:8.3f}{table[dataset]["cohere-embed-english-v3.0"]["R@100"]:8.3f}')
    print(' ' * 28 + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13)
    print('avg' + ' ' * 22 + f'{final_scores["bm25-flat"]["nDCG@10"]:8.3f}{final_scores["bm25-flat"]["R@100"]:8.3f}   ' +
          f'{final_scores["bm25-multifield"]["nDCG@10"]:8.3f}{final_scores["bm25-multifield"]["R@100"]:8.3f}   ' +
          f'{final_scores["splade-pp-ed"]["nDCG@10"]:8.3f}{final_scores["splade-pp-ed"]["R@100"]:8.3f}   ' +
          f'{final_scores["contriever"]["nDCG@10"]:8.3f}{final_scores["contriever"]["R@100"]:8.3f}   ' +
          f'{final_scores["contriever-msmarco"]["nDCG@10"]:8.3f}{final_scores["contriever-msmarco"]["R@100"]:8.3f}   ' +
          f'{final_scores["bge-base-en-v1.5.faiss"]["nDCG@10"]:8.3f}{final_scores["bge-base-en-v1.5.faiss"]["R@100"]:8.3f}   ' +
          f'{final_scores["bge-base-en-v1.5.lucene-flat"]["nDCG@10"]:8.3f}{final_scores["bge-base-en-v1.5.lucene-flat"]["R@100"]:8.3f}   ' +
          f'{final_scores["bge-base-en-v1.5.lucene-hnsw"]["nDCG@10"]:8.3f}{final_scores["bge-base-en-v1.5.lucene-hnsw"]["R@100"]:8.3f}   ' +
          f'{final_scores["cohere-embed-english-v3.0"]["nDCG@10"]:8.3f}{final_scores["cohere-embed-english-v3.0"]["R@100"]:8.3f}')

    print('\n')
    # Separately print out all the cqa sub-collections.
    for dataset in beir_keys:
        if not dataset.startswith('cqa'):
            continue

        print(f'{dataset:25}' +
              f'{table[dataset]["bm25-flat"]["nDCG@10"]:8.3f}{table[dataset]["bm25-flat"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bm25-multifield"]["nDCG@10"]:8.3f}{table[dataset]["bm25-multifield"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["splade-pp-ed"]["nDCG@10"]:8.3f}{table[dataset]["splade-pp-ed"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["contriever"]["nDCG@10"]:8.3f}{table[dataset]["contriever"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["contriever-msmarco"]["nDCG@10"]:8.3f}{table[dataset]["contriever-msmarco"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bge-base-en-v1.5.faiss"]["nDCG@10"]:8.3f}{table[dataset]["bge-base-en-v1.5.faiss"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bge-base-en-v1.5.lucene-flat"]["nDCG@10"]:8.3f}{table[dataset]["bge-base-en-v1.5.lucene-flat"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["bge-base-en-v1.5.lucene-hnsw"]["nDCG@10"]:8.3f}{table[dataset]["bge-base-en-v1.5.lucene-hnsw"]["R@100"]:8.3f}   ' +
              f'{table[dataset]["cohere-embed-english-v3.0"]["nDCG@10"]:8.3f}{table[dataset]["cohere-embed-english-v3.0"]["R@100"]:8.3f}')
    print(' ' * 28 + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13 + '      ' + '-' * 13)
    print('avg' + ' ' * 22 + f'{cqa_scores["bm25-flat"]["nDCG@10"]:8.3f}{cqa_scores["bm25-flat"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["bm25-multifield"]["nDCG@10"]:8.3f}{cqa_scores["bm25-multifield"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["splade-pp-ed"]["nDCG@10"]:8.3f}{cqa_scores["splade-pp-ed"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["contriever"]["nDCG@10"]:8.3f}{cqa_scores["contriever"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["contriever-msmarco"]["nDCG@10"]:8.3f}{cqa_scores["contriever-msmarco"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["bge-base-en-v1.5.faiss"]["nDCG@10"]:8.3f}{cqa_scores["bge-base-en-v1.5.faiss"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["bge-base-en-v1.5.lucene-flat"]["nDCG@10"]:8.3f}{cqa_scores["bge-base-en-v1.5.lucene-flat"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["bge-base-en-v1.5.lucene-hnsw"]["nDCG@10"]:8.3f}{cqa_scores["bge-base-en-v1.5.lucene-hnsw"]["R@100"]:8.3f}   ' +
          f'{cqa_scores["cohere-embed-english-v3.0"]["nDCG@10"]:8.3f}{cqa_scores["cohere-embed-english-v3.0"]["R@100"]:8.3f}')

    end = time.time()

    start_str = datetime.utcfromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    end_str = datetime.utcfromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')

    print('\n')
    print(f'Start time: {start_str}')
    print(f'End time: {end_str}')
    print(f'Total elapsed time: {end - start:.0f}s ~{(end - start)/3600:.1f}hr')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for BeIR corpora.')
    # To list all conditions/datasets
    parser.add_argument('--list-conditions', action='store_true', default=False, help='List available conditions.')
    parser.add_argument('--list-datasets', action='store_true', default=False, help='List available datasets.')
    # For generating reports
    parser.add_argument('--generate-report', action='store_true', default=False, help='Generate report.')
    parser.add_argument('--output', type=str, help='File to store report.', required=False)
    # For actually running the experimental conditions
    parser.add_argument('--all', action='store_true', default=False, help='Run all conditions.')
    parser.add_argument('--condition', type=str, help='Condition to run.', required=False)
    parser.add_argument('--dataset', type=str, help='Dataset to run.', required=False)
    parser.add_argument('--directory', type=str, help='Base directory.', default='', required=False)
    parser.add_argument('--dry-run', action='store_true', default=False, help='Print out commands but do not execute.')
    parser.add_argument('--skip-eval', action='store_true', default=False, help='Skip running trec_eval.')
    parser.add_argument('--display-commands', action='store_true', default=False, help='Display command.')
    args = parser.parse_args()

    if args.list_conditions:
        list_conditions()
        sys.exit()
    
    if args.list_datasets:
        list_datasets()
        sys.exit()

    if args.generate_report:
        if not args.output:
            print(f'Must specify report filename with --output.')
            sys.exit()

        generate_report(args)
        sys.exit()

    if args.condition and args.condition not in models:
        print(f'Invalid condition: {args.condition}')
        sys.exit()

    if not args.all and not args.condition:
        print(f'Must specify a specific condition using --condition or use --all to run all conditions.')
        sys.exit()
        
    if args.all and (args.condition or args.dataset):
        print('Specifying --all will run all conditions and datasets')
        sys.exit()

    run_conditions(args)
