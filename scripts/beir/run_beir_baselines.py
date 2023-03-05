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

import os


beir_keys = {
    'trec-covid': 'TREC-COVID',
    'bioasq': 'BioASQ',
    'nfcorpus': 'NFCorpus',
    'nq': 'NQ',
    'hotpotqa': 'HotpotQA',
    'fiqa': 'FiQA-2018',
    'signal1m': 'Signal-1M',
    'trec-news': 'TREC-NEWS',
    'robust04': 'Robust04',
    'arguana': 'ArguAna',
    'webis-touche2020': 'Webis-Touche2020',
    'cqadupstack-android': 'CQADupStack-android',
    'cqadupstack-english': 'CQADupStack-english',
    'cqadupstack-gaming': 'CQADupStack-gaming',
    'cqadupstack-gis': 'CQADupStack-gis',
    'cqadupstack-mathematica': 'CQADupStack-mathematica',
    'cqadupstack-physics': 'CQADupStack-physics',
    'cqadupstack-programmers': 'CQADupStack-programmers',
    'cqadupstack-stats': 'CQADupStack-stats',
    'cqadupstack-tex': 'CQADupStack-tex',
    'cqadupstack-unix': 'CQADupStack-unix',
    'cqadupstack-webmasters': 'CQADupStack-webmasters',
    'cqadupstack-wordpress': 'CQADupStack-wordpress',
    'quora': 'Quora',
    'dbpedia-entity': 'DBPedia',
    'scidocs': 'SCIDOCS',
    'fever': 'FEVER',
    'climate-fever': 'Climate-FEVER',
    'scifact': 'SciFact'
}

commitid = '1842ee'
date = '20220501'


# Runs on "flat" index
for key in beir_keys:
    cmd = f'python -m pyserini.search.lucene \
              --index beir-v1.0.0-{key}-flat \
              --topics beir-v1.0.0-{key}-test \
              --output runs/run.beir-v1.0.0-{key}-flat.trec \
              --output-format trec \
              --batch 36 --threads 12 \
              --remove-query --hits 1000'
    os.system(cmd)
    cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 beir-v1.0.0-{key}-test runs/run.beir-v1.0.0-{key}-flat.trec'
    os.system(cmd)

# Runs on "multifield" index
for key in beir_keys:
    cmd = f'python -m pyserini.search.lucene \
              --index beir-v1.0.0-{key}-multifield \
              --topics beir-v1.0.0-{key}-test \
              --output runs/run.beir-v1.0.0-{key}-multifield.trec \
              --output-format trec \
              --batch 36 --threads 12 \
              --fields contents=1.0 title=1.0 \
              --remove-query --hits 1000'
    os.system(cmd)
    cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 beir-v1.0.0-{key}-test runs/run.beir-v1.0.0-{key}-multifield.trec'
    os.system(cmd)

# Runs on SPLADE-distill CoCodenser-medium index
for key in beir_keys:
    cmd = f'python -m pyserini.search.lucene \
              --index beir-v1.0.0-{key}-splade_distil_cocodenser_medium \
              --topics beir-v1.0.0-{key}-test-splade_distil_cocodenser_medium \
              --output runs/run.beir-v1.0.0-{key}-splade_distil_cocodenser_medium.trec \
              --output-format trec \
              --batch 36 --threads 12 \
              --remove-query --impact --hits 1000'
    os.system(cmd)
    cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 beir-v1.0.0-{key}-test runs/run.beir-v1.0.0-{key}-splade_distil_cocodenser_medium.trec'
    os.system(cmd)

# Runs on Contriever index
for key in beir_keys:
    cmd = f'python -m pyserini.search.faiss \
              --encoder-class contriever --encoder facebook/contriever \
              --index beir-v1.0.0-{key}.contriever \
              --topics beir-v1.0.0-{key}-test \
              --output runs/run.beir.contriever.{key}.txt \
              --batch 128 --threads 16 \
              --remove-query --hits 1000'
    os.system(cmd)
    cmd = f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100,1000 beir-v1.0.0-{key}-test runs/run.beir.contriever.{key}.txt'
    os.system(cmd)
