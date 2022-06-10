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

# The models: the rows of the results table will be ordered this way.
models = {
    'msmarco-v1-passage':
    ['bm25-default',
     'bm25-rm3-default',
     '',
     'bm25-d2q-t5-default',
     'bm25-rm3-d2q-t5-default',
     '',
     'unicoil-noexp',
     'unicoil-noexp-otf',
     'unicoil',
     'unicoil-otf',
     '',
     'bm25-tuned',
     'bm25-rm3-tuned',
     '',
     'bm25-d2q-t5-tuned',
     'bm25-rm3-d2q-t5-tuned',
     '',
     'ance',
     'ance-otf',
     '',
     'distilbert-kd',
     'distilbert-kd-otf',
     '',
     'distilbert-kd-tasb',
     'distilbert-kd-tasb-otf',
     '',
     'tct_colbert-v2-hnp',
     'tct_colbert-v2-hnp-otf'],
    'msmarco-v1-doc':
    ['bm25-doc-default',
     'bm25-doc-segmented-default',
     'bm25-rm3-doc-default',
     'bm25-rm3-doc-segmented-default',
     '',
     'bm25-d2q-t5-doc-default',
     'bm25-d2q-t5-doc-segmented-default',
     'bm25-rm3-d2q-t5-doc-default',
     'bm25-rm3-d2q-t5-doc-segmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'bm25-doc-tuned',
     'bm25-doc-segmented-tuned',
     'bm25-rm3-doc-tuned',
     'bm25-rm3-doc-segmented-tuned',
     '',
     'bm25-d2q-t5-doc-tuned',
     'bm25-d2q-t5-doc-segmented-tuned',
     'bm25-rm3-d2q-t5-doc-tuned',
     'bm25-rm3-d2q-t5-doc-segmented-tuned',
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
     'bm25-rm3-d2q-t5-default',
     'bm25-rm3-d2q-t5-augmented-default',
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
     'bm25-rm3-d2q-t5-doc-default',
     'bm25-rm3-d2q-t5-doc-segmented-default',
     '',
     'unicoil-noexp',
     'unicoil',
     '',
     'unicoil-noexp-otf',
     'unicoil-otf'
     ]
}

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