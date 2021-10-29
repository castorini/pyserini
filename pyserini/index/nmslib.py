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
import copy
import json
import os
import shutil
import time

import faiss
import nmslib
from scipy.sparse import csr_matrix

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='path to embeddings directory', required=True)
    parser.add_argument('--output', type=str, help='path to output index dir', required=True)
    parser.add_argument('--M', type=int, default=256, required=False)
    parser.add_argument('--efC', type=int, default=256, required=False)
    parser.add_argument('--threads', type=int, default=12, required=False)
    args = parser.parse_args()

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    is_sparse = False

    if 'index' in os.listdir(args.input):
        shutil.copy(os.path.join(args.input, 'docid'), os.path.join(args.output, 'docid'))
        bf_index = faiss.read_index(os.path.join(args.input, 'index'))
        vectors = bf_index.reconstruct_n(0, bf_index.ntotal)
    else:
        vectors = []
        for filename in os.listdir(args.input):
            path = os.path.join(args.input, filename)
            with open(path) as f_in, open(os.path.join(args.output, 'docid'), 'w') as f_out:
                for line in f_in:
                    info = json.loads(line)
                    docid = info['id']
                    vector = info['vector']
                    f_out.write(f'{docid}\n')
                    vectors.append(vector)

    tokens = set()
    if isinstance(vectors[0], dict):
        is_sparse = True
        for vec in vectors:
            for key in vec:
                tokens.add(key)
    token2id = {}
    with open(os.path.join(args.output, 'tokens'), 'w') as f:
        for idx, tok in enumerate(tokens):
            token2id[tok] = idx
            f.write(f'{tok}\n')

    if is_sparse:
        matrix_row, matrix_col, matrix_data = [], [], []
        for i, vec in enumerate(vectors):
            weight_dict = vec
            tokens = weight_dict.keys()
            col = [token2id[tok] for tok in tokens]
            data = weight_dict.values()
            matrix_row.extend([i] * len(weight_dict))
            matrix_col.extend(col)
            matrix_data.extend(data)
        vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(len(vectors), len(token2id)))

    M = args.M
    efC = args.efC
    num_threads = args.threads
    index_time_params = {'M': M, 'indexThreadQty': num_threads, 'efConstruction': efC, 'post': 0}
    if is_sparse:
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
    index.saveIndex(os.path.join(args.output, 'index.bin'), save_data=True)

    metadata = copy.deepcopy(index_time_params)
    metadata['index-time'] = index_time
    metadata['type'] = 'sparse' if is_sparse else 'dense'
    json.dump(metadata, open(os.path.join(args.output, 'meta'), 'w'), indent=4)
