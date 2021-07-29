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
import shutil
import time
import copy

import nmslib
from scipy.sparse import csr_matrix
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=str, help='path to corpus with vectors', required=True)
    parser.add_argument('--hnsw-index', type=str, help='path to hnsw index', required=True)
    parser.add_argument('--M', type=int, help='M for hnsw', required=False, default=64)
    parser.add_argument('--ef', type=int, help='ef for hnsw', required=False, default=256)
    parser.add_argument('--threads', type=int, help='threads for hnsw', required=False, default=12)
    parser.add_argument('--is-sparse', action='store_true', required=False)
    parser.add_argument('--tokens', type=str, help='path to token list', required=False)
    args = parser.parse_args()

    if not os.path.exists(args.hnsw_index):
        os.mkdir(args.hnsw_index)

    token2id = {}
    if args.is_sparse:
        with open(args.tokens) as tok_f:
            for idx, line in enumerate(tok_f):
                tok = line.rstrip()
                token2id[tok] = idx

        shutil.copy(args.tokens, os.path.join(args.hnsw_index, 'tokens'))

    corpus = []
    for file in sorted(os.listdir(args.corpus)):
        file = os.path.join(args.corpus, file)
        if file.endswith('json') or file.endswith('jsonl'):
            print(f'Loading {file}')
            with open(file, 'r') as f:
                for idx, line in enumerate(tqdm(f.readlines())):
                    info = json.loads(line)
                    corpus.append(info)

    with open(os.path.join(args.hnsw_index, 'docid'), 'w') as f:
        for d in corpus:
            docid = str(d['id'])
            f.write(f'{docid}\n')

    vectors = []
    if args.is_sparse:
        matrix_row, matrix_col, matrix_data = [], [], []
        for i, d in enumerate(tqdm(corpus)):
            weight_dict = d['vector']
            tokens = weight_dict.keys()
            col = [token2id[tok] for tok in tokens]
            data = weight_dict.values()
            matrix_row.extend([i] * len(weight_dict))
            matrix_col.extend(col)
            matrix_data.extend(data)
        vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(len(corpus), len(token2id)))
    else:
        for i, d in enumerate(tqdm(corpus)):
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
    index_time = end - start
    print('Index-time parameters', index_time_params)
    print('Indexing time = %f' % index_time)
    index.saveIndex(os.path.join(args.hnsw_index, 'index.bin'), save_data=True)

    metadata = copy.deepcopy(index_time_params)
    metadata['index-time'] = index_time
    json.dump(metadata, open(os.path.join(args.hnsw_index, 'meta'), 'w'), indent=4)
