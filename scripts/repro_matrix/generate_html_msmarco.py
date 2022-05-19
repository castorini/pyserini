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
import yaml

from collections import defaultdict
from scripts.repro_matrix.utils import run_eval_and_return_metric
from string import Template

# The models: the rows of the results table will be ordered this way.
models = {
    'msmarco-v1-passage':
    ['bm25-tuned',
     'bm25-rm3-tuned',
     '',
     'bm25-d2q-t5-tuned',
     '',
     'bm25-default',
     'bm25-rm3-default',
     '',
     'bm25-d2q-t5-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf',
     '',
     'tct_colbert-v2-hnp',
     'tct_colbert-v2-hnp-otf'],
    'msmarco-v1-doc':
    ['bm25-doc-tuned',
     'bm25-doc-segmented-tuned',
     'bm25-rm3-doc-tuned',
     'bm25-rm3-doc-segmented-tuned',
     '',
     'bm25-d2q-t5-doc-tuned',
     'bm25-d2q-t5-doc-segmented-tuned',
     '',
     'bm25-doc-default',
     'bm25-doc-segmented-default',
     'bm25-rm3-doc-default',
     'bm25-rm3-doc-segmented-default',
     '',
     'bm25-d2q-t5-doc-default',
     'bm25-d2q-t5-doc-segmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'],
    'msmarco-v2-passage':
    ['bm25-default',
     'bm25-augmented-default',
     'bm25-rm3-default',
     'bm25-rm3-augmented-default',
     '',
     'bm25-d2q-t5-default',
     'bm25-d2q-t5-augmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'],
    'msmarco-v2-doc':
    ['bm25-doc-default',
     'bm25-doc-segmented-default',
     'bm25-rm3-doc-default',
     'bm25-rm3-doc-segmented-default',
     '',
     'bm25-d2q-t5-doc-default',
     'bm25-d2q-t5-doc-segmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'
     ]
}

fail_str = '\033[91m[FAIL]\033[0m'
ok_str = '[OK] '

trec_eval_metric_definitions = {
    'msmarco-v1-passage': {
        'msmarco-passage-dev-subset': {
            'MRR@10': '-c -M 10 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'dl19-passage': {
            'MAP': '-c -l 2 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -l 2 -m recall.1000'
        },
        'dl20-passage': {
            'MAP': '-c -l 2 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -l 2 -m recall.1000'
        }
    },
    'msmarco-v1-doc': {
        'msmarco-doc-dev': {
            'MRR@10': '-c -M 100 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'dl19-doc': {
            'MAP': '-c -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -m recall.1000'
        },
        'dl20-doc': {
            'MAP': '-c -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'R@1K': '-c -m recall.1000'
        }
    },
    'msmarco-v2-passage': {
        'msmarco-v2-passage-dev': {
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'msmarco-v2-passage-dev2': {
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'dl21-passage': {
            'MAP@100': '-c -l 2 -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'MRR@100': '-c -l 2 -M 100 -m recip_rank',
            'R@100': '-c -l 2 -m recall.100',
            'R@1K': '-c -l 2 -m recall.1000'
        }
    },
    'msmarco-v2-doc': {
        'msmarco-v2-doc-dev': {
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'msmarco-v2-doc-dev2': {
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@1K': '-c -m recall.1000'
        },
        'dl21-doc': {
            'MAP@100': '-c -M 100 -m map',
            'nDCG@10': '-c -m ndcg_cut.10',
            'MRR@100': '-c -M 100 -m recip_rank',
            'R@100': '-c -m recall.100',
            'R@1K': '-c -m recall.1000'
        }
    }
}

table = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: 0.0)))
commands = defaultdict(lambda: defaultdict(lambda: ''))

table_keys = {}


def find_table_topic_set_key_v1(topic_key):
    # E.g., we want to map variants like 'dl19-passage-unicoil' and 'dl19-passage' both into 'dl19'
    key = ''
    if topic_key.startswith('dl19'):
        key = 'dl19'
    elif topic_key.startswith('dl20'):
        key = 'dl20'
    elif topic_key.startswith('msmarco'):
        key = 'msmarco'

    return key


def find_table_topic_set_key_v2(topic_key):
    key = ''
    if topic_key.endswith('dev') or topic_key.endswith('dev-unicoil') or topic_key.endswith('dev-unicoil-noexp'):
        key = 'dev'
    elif topic_key.endswith('dev2') or topic_key.endswith('dev2-unicoil') or topic_key.endswith('dev2-unicoil-noexp'):
        key = 'dev2'
    elif topic_key.startswith('dl21'):
        key = 'dl21'

    return key


html_template = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <meta http-equiv="x-ua-compatible" content="ie=edge" />
    <title>Material Design for Bootstrap</title>
    <!-- Font Awesome -->
    <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.11.2/css/all.css" />
    <!-- Google Fonts Roboto -->
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" />
    <!-- MDB -->
   <link href="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.0.0/mdb.min.css" rel="stylesheet" />

    <style>
tr.hide-table-padding td {
  padding: 0;
}

.expand-button {
	position: relative;
}

.accordion-toggle .expand-button:after
{
  position: absolute;
  left:.75rem;
  top: 50%;
  transform: translate(0, -50%);
  content: '-';
}
.accordion-toggle.collapsed .expand-button:after
{
  content: '+';
}
    </style>
</head>
<body>

<div class="container my-4">

<div class="table-responsive">
  <table class="table">
    <thead>
      <tr>
        <th></th>
        <th></th>
        <th colspan="6"><b>TREC 2021</b></th>
        <th colspan="3"><b>dev</b></th>
        <th colspan="3"><b>dev2</b></th>
      </tr>
      <tr>
        <th scope="col"></th>
        <th scope="col"></th>
        <th scope="col"><br/>MAP@100</th>
        <th scope="col">nDCG@10</th>
        <th scope="col">MRR@100</th>
        <th scope="col">R@100</th>
        <th scope="col">R@1K</th>
        <th scope="col"></th>
        <th scope="col">MRR@100</th>
        <th scope="col">R@1K</th>
        <th scope="col"></th>
        <th scope="col">MRR@100</th>
        <th scope="col">R@1K</th>
      </tr>
    </thead>
    <tbody>

$rows

    </tbody>
  </table>
</div>

      </div>



    <script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.4.0/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/js/bootstrap.min.js"></script>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/mdb-ui-kit/4.0.0/mdb.min.js"></script>

</body>
</html>
'''

row_template_v2 = '''
<!-- Condition: ${condition_name} -->
<tr class="accordion-toggle collapsed" id="row${row_cnt}" data-toggle="collapse" data-parent="#row${row_cnt}" href="#collapse${row_cnt}">
<td class="expand-button"></td>
<td>${condition_name}</td>
<td>$s1</td>
<td>$s2</td>
<td>$s3</td>
<td>$s4</td>
<td>$s5</td>
<td></td>
<td>$s6</td>
<td>$s7</td>
<td></td>
<td>$s8</td>
<td>$s9</td>
</tr>
<tr class="hide-table-padding">
<td></td>
<td></td>
<td colspan="11">
<div id="collapse${row_cnt}" class="collapse in p-3">

<!-- Tabs navs -->
<ul class="nav nav-tabs mb-3" id="row${row_cnt}-tabs" role="tablist">
  <li class="nav-item" role="presentation">
    <a class="nav-link active" id="row${row_cnt}-tab1-header" data-mdb-toggle="tab" href="#row${row_cnt}-tab1" role="tab" aria-controls="row${row_cnt}-tab1" aria-selected="true">TREC 2021</a>
  </li>
  <li class="nav-item" role="presentation">
    <a class="nav-link" id="row${row_cnt}-tab2-header" data-mdb-toggle="tab" href="#row${row_cnt}-tab2" role="tab" aria-controls="row${row_cnt}-tab2" aria-selected="false">dev</a>
  </li>
  <li class="nav-item" role="presentation">
    <a class="nav-link" id="row${row_cnt}-tab3-header" data-mdb-toggle="tab" href="#row${row_cnt}-tab3" role="tab" aria-controls="row${row_cnt}-tab3" aria-selected="false">dev2</a>
  </li>
</ul>
<!-- Tabs navs -->

<!-- Tabs content -->
<div class="tab-content" id="row${row_cnt}-content">
  <div class="tab-pane fade show active" id="row${row_cnt}-tab1" role="tabpanel" aria-labelledby="row${row_cnt}-tab1">
Command to generate run on TREC 2021:

  <blockquote>
<pre><code>
$cmd1
</code></pre>
  </blockquote>
  </div>
  <div class="tab-pane fade" id="row${row_cnt}-tab2" role="tabpanel" aria-labelledby="row${row_cnt}-tab2">
    Command to generate run on dev:
  <blockquote>
<pre><code>
$cmd2
</code></pre>
  </blockquote>
  </div>
  <div class="tab-pane fade" id="row${row_cnt}-tab3" role="tabpanel" aria-labelledby="row${row_cnt}-tab3">
    Command to generate run on dev2:
  <blockquote>
<pre><code>
$cmd3
</code></pre>
  </blockquote>

  </div>
</div>
<!-- Tabs content -->

</div></td>
</tr>
'''


def format_command(raw):
    return raw.replace('--topics', '\\\n  --topics')\
        .replace('--index', '\\\n  --index')\
        .replace('--output', '\\\n  --output')\
        .replace('.txt', '.txt \\\n ')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generate regression matrix for MS MARCO V1 passage corpus.')
    parser.add_argument('--collection', type=str, help='Collection = {v1-passage, v1-doc, v2-passage, v2-doc}.', required=True)
    args = parser.parse_args()

    if args.collection == 'v1-passage':
        collection = 'msmarco-v1-passage'
        yaml_file = 'pyserini/resources/msmarco-v1-passage.yaml'
    elif args.collection == 'v1-doc':
        collection = 'msmarco-v1-doc'
        yaml_file = 'pyserini/resources/msmarco-v1-doc.yaml'
    elif args.collection == 'v2-passage':
        collection = 'msmarco-v2-passage'
        yaml_file = 'pyserini/resources/msmarco-v2-passage.yaml'
    elif args.collection == 'v2-doc':
        collection = 'msmarco-v2-doc'
        yaml_file = 'pyserini/resources/msmarco-v2-doc.yaml'
    else:
        raise ValueError(f'Unknown corpus: {args.collection}')

    with open(yaml_file) as f:
        yaml_data = yaml.safe_load(f)
        for condition in yaml_data['conditions']:
            name = condition['name']
            display = condition['display']
            cmd_template = condition['command']

            for topic_set in condition['topics']:
                topic_key = topic_set['topic_key']
                eval_key = topic_set['eval_key']

                runfile = f'run.{collection}.{topic_key}.{name}.txt'
                cmd = cmd_template.replace('_R_', f'runs/{runfile}').replace('_T_', topic_key)
                commands[name][find_table_topic_set_key_v2(topic_key)] = cmd

                for expected in topic_set['scores']:
                    for metric in expected:
                        table_keys[name] = display
                        if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
                            table[name][find_table_topic_set_key_v1(topic_key)][metric] = expected[metric]
                        else:
                            table[name][find_table_topic_set_key_v2(topic_key)][metric] = expected[metric]

    if collection == 'msmarco-v1-passage' or collection == 'msmarco-v1-doc':
        print(' ' * 64 + 'TREC 2019' + ' ' * 16 + 'TREC 2020' + ' ' * 12 + 'MS MARCO dev')
        print(' ' * 57 + 'MAP    nDCG@10    R@1K       MAP nDCG@10    R@1K    MRR@10    R@1K')
        print(' ' * 57 + '-' * 22 + '    ' + '-' * 22 + '    ' + '-' * 14)
        for name in models[collection]:
            if not name:
                print('')
                continue
            print(f'{table_keys[name]:55}' +
                  f'{table[name]["dl19"]["MAP"]:8.4f}{table[name]["dl19"]["nDCG@10"]:8.4f}{table[name]["dl19"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["dl20"]["MAP"]:8.4f}{table[name]["dl20"]["nDCG@10"]:8.4f}{table[name]["dl20"]["R@1K"]:8.4f}  ' +
                  f'{table[name]["msmarco"]["MRR@10"]:8.4f}{table[name]["msmarco"]["R@1K"]:8.4f}')
    else:
        row_cnt = 1

        html_rows = []
        for name in models[collection]:
            if not name:
                continue
            # print(row_cnt)
            # print(f'{table_keys[name]:55}' +
            #       f'{table[name]["dl21"]["MAP@100"]:8.4f}{table[name]["dl21"]["nDCG@10"]:8.4f}' +
            #       f'{table[name]["dl21"]["MRR@100"]:8.4f}{table[name]["dl21"]["R@100"]:8.4f}{table[name]["dl21"]["R@1K"]:8.4f}  ' +
            #       f'{table[name]["dev"]["MRR@100"]:8.4f}{table[name]["dev"]["R@1K"]:8.4f}  ' +
            #       f'{table[name]["dev2"]["MRR@100"]:8.4f}{table[name]["dev2"]["R@1K"]:8.4f}\n\n')
            # print(f'{commands[name]["dl21"]}')
            # print(f'{commands[name]["dev"]}')
            # print(f'{commands[name]["dev2"]}\n')

            s = Template(row_template_v2)
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
                             cmd3=format_command(commands[name]['dev2'])
                             )
            #print(s)
            html_rows.append(s)
            row_cnt += 1

        all_rows = '\n'.join(html_rows)
        print(Template(html_template).substitute(rows=all_rows))
        #print(all_rows)
