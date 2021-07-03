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

import faiss
import shutil


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--bf-index', type=str, help='path to brute force index', required=True)
    parser.add_argument('--hnsw-index', type=str, help='path to hnsw index', required=True)
    parser.add_argument('--dimension', type=int, help='dimension of passage embeddings', required=False, default=768)
    args = parser.parse_args()

    if not os.path.exists(args.hnsw_index):
        os.mkdir(args.hnsw_index)
    shutil.copy(os.path.join(args.bf_index, 'docid'), os.path.join(args.hnsw_index, 'docid'))

    bf_index = faiss.read_index(os.path.join(args.bf_index, 'index'))
    hnsw_index = faiss.IndexHNSWFlat(args.dimension, 256, faiss.METRIC_INNER_PRODUCT)
    hnsw_index.hnsw.efConstruction = 256  # hardcode for now
    hnsw_index.hnsw.efSearch = 256  # hardcode for now
    vectors = bf_index.reconstruct_n(0, bf_index.ntotal)
    print(vectors)
    print('Indexing')
    hnsw_index.add(vectors)
    faiss.write_index(hnsw_index, os.path.join(args.hnsw_index, 'index'))
