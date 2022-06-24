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
