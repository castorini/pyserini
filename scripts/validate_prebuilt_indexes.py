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

import sys

# Use Pyserini in this repo (as opposed to pip install)
sys.path.insert(0, './')

from pyserini.index import IndexReader
from pyserini.dsearch import SimpleDenseSearcher, QueryEncoder, BinaryDenseSearcher 
from pyserini.prebuilt_index_info import TF_INDEX_INFO, IMPACT_INDEX_INFO, FAISS_INDEX_INFO


def check_sparse(index):
    for entry in index:
        print(f'# Validating "{entry}"...')
        IndexReader.validate_prebuilt_index(entry)
        print('\n')


def check_dense(index):
    # dummy queries; there is no explicit validation...
    # we just try to initialize the and make sure there are no exceptions
    dummy_queries = QueryEncoder.load_encoded_queries('tct_colbert-msmarco-passage-dev-subset')
    print('\n')
    for entry in index:
        print(f'# Validating "{entry}"...')
        if "bpr" in entry:
            BinaryDenseSearcher.from_prebuilt_index(entry, dummy_queries)
        else:
            SimpleDenseSearcher.from_prebuilt_index(entry, dummy_queries)
        print('\n')


if __name__ == '__main__':
    check_sparse(TF_INDEX_INFO)
    check_sparse(IMPACT_INDEX_INFO)
    check_dense(FAISS_INDEX_INFO)
