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

from pyserini.encode import QueryEncoder
from pyserini.prebuilt_index_info import TF_INDEX_INFO, IMPACT_INDEX_INFO, FAISS_INDEX_INFO, LUCENE_FLAT_INDEX_INFO, LUCENE_HNSW_INDEX_INFO
from pyserini.search.faiss import FaissSearcher, BinaryDenseFaissSearcher
from pyserini.search.lucene import LuceneSearcher, LuceneFlatDenseSearcher, LuceneHnswDenseSearcher


def check_lucene_sparse(index):
    for entry in index:
        print(f'# Validating "{entry}"...')
        LuceneSearcher.from_prebuilt_index(entry, verbose=True)
        print('\n')


def check_lucene_dense_hnsw(index):
    for entry in index:
        print(f'# Validating "{entry}"...')
        LuceneHnswDenseSearcher.from_prebuilt_index(entry, verbose=True)
        print('\n')


def check_lucene_dense_flat(index):
    for entry in index:
        print(f'# Validating "{entry}"...')
        LuceneFlatDenseSearcher.from_prebuilt_index(entry, verbose=True)
        print('\n')


def check_faiss(index):
    # dummy queries; there is no explicit validation...
    # we just try to initialize the index and make sure there are no exceptions
    dummy_queries = QueryEncoder.load_encoded_queries('tct_colbert-msmarco-passage-dev-subset')
    print('\n')
    for entry in index:
        print(f'# Validating "{entry}"...')
        if "bpr" in entry:
            BinaryDenseFaissSearcher.from_prebuilt_index(entry, dummy_queries)
        else:
            FaissSearcher.from_prebuilt_index(entry, dummy_queries)
        print('\n')


if __name__ == '__main__':
    check_lucene_sparse(TF_INDEX_INFO)
    check_lucene_sparse(IMPACT_INDEX_INFO)
    check_lucene_dense_flat(LUCENE_FLAT_INDEX_INFO)
    check_lucene_dense_hnsw(LUCENE_HNSW_INDEX_INFO)
    check_faiss(FAISS_INDEX_INFO)
