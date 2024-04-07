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

from pyserini.index.lucene import IndexReader
from pyserini.util import compute_md5

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

commitid = 'a66f86f'
date = '20231124'
type = 'splade-pp-ed'

for key in beir_keys:
    index_reader = IndexReader(f'indexes/lucene-inverted.beir-v1.0.0-{key}.{type}.{date}.{commitid}')
    stats = index_reader.stats()
    md5 = compute_md5(f'indexes/lucene-inverted.beir-v1.0.0-{key}.{type}.{date}.{commitid}.tar.gz')
    size = os.path.getsize(f'indexes/lucene-inverted.beir-v1.0.0-{key}.{type}.{date}.{commitid}.tar.gz')
    print(f'    "beir-v1.0.0-{key}.{type}": {{')
    print(f'        "description": "Lucene impact index of BEIR (v1.0.0): {beir_keys[key]} encoded by SPLADE++ (CoCondenser-EnsembleDistil)",')
    print(f'        "filename": "lucene-inverted.beir-v1.0.0-{key}.{type}.{date}.{commitid}.tar.gz",')
    #print(f'        "readme": "lucene-inverted.beir-v1.0.0-{key}.{type}.{date}.{commitid}.README.md",')
    print(f'        "urls": [')
    print(f'            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/lucene/lucene-inverted.beir-v1.0.0-{key}.{type}.{date}.{commitid}.tar.gz"')
    print(f'        ],')
    print(f'        "md5": "{md5}",')
    print(f'        "size compressed (bytes)": {size},')
    print(f'        "total_terms": {stats["total_terms"]},')
    print(f'        "documents": {stats["documents"]},')
    print(f'        "unique_terms": {stats["unique_terms"]},')
    print(f'        "downloaded": False')
    print(f'    }},')
