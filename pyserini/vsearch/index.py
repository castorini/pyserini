#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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
import json
import os
import time

import nmslib
from scipy.sparse import csr_matrix

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=str, help='path to corpus with vectors', required=True)
    parser.add_argument('--hnsw-index', type=str, help='path to hnsw index', required=True)
    parser.add_argument('--M', type=int, help='M for hnsw', required=False, default=64)
    parser.add_argument('--ef', type=int, help='ef for hnsw', required=False, default=256)
    parser.add_argument('--threads', type=int, help='threads for hnsw', required=False, default=12)
    parser.add_argument('--dim', type=int, help='dimension of passage embeddings', required=False, default=768)
    parser.add_argument('--is-sparse', action='store_true', required=False)
    args = parser.parse_args()

    corpus = json.load(open(args.corpus, 'r'))
    if not os.path.exists(args.hnsw_index):
        os.mkdir(args.hnsw_index)

    with open(os.path.join(args.hnsw_index, 'sparse_index.bin'), 'w') as f:
        for d in corpus:
            docid = str(d['id'])
        f.write(f'{docid}\n')

    vectors = []
    if args.is_sparse:
        matrix_row, matrix_col, matrix_data = [], [], []
        for i, d in enumerate(corpus):
            matrix_row.extend([i] * len(d['vector'][0]))
            matrix_col.extend(d['vector'][0])
            matrix_data.extend(d['vector'][1])
        topic_vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(len(corpus), args.dim))
    else:
        for i, d in enumerate(corpus):
            vectors.append(d['vector'])

    M = args.M
    efC = args.ef
    num_threads = args.threads
    index_time_params = {'M': M, 'indexThreadQty': num_threads, 'efConstruction': efC, 'post': 0}
    if args.is_sparse:
        index = nmslib.init(method='hnsw', space='negdotprod_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
    else:
        index = nmslib.init(method='hnsw', space='negdotprod', data_type=nmslib.DataType.DENSE_VECTOR)
    index.addDataPointBatch(vectors)
    start = time.time()
    index.createIndex(index_time_params, print_progress=True)
    end = time.time()
    print('Index-time parameters', index_time_params)
    print('Indexing time = %f' % (end - start))
    index.saveIndex(os.path.join(args.hnsw_index, 'sparse_index.bin'), save_data=True)
