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

import json
import os
import argparse
import shutil
import numpy as np

import faiss
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='path to embeddings directory', required=True)
    parser.add_argument('--output', type=str, help='path to output index dir', required=True)
    parser.add_argument('--dim', type=int, default=768, required=False)
    parser.add_argument('--hnsw', action="store_true", required=False)
    parser.add_argument('--M', type=int, default=256, required=False)
    parser.add_argument('--efC', type=int, default=256, required=False)
    parser.add_argument('--pq', action="store_true", required=False)
    parser.add_argument('--pq-m', type=int, default=192, required=False)
    parser.add_argument('--pq-nbits', type=int, default=8, required=False)
    parser.add_argument('--threads', type=int, default=12, required=False)
    args = parser.parse_args()

    faiss.omp_set_num_threads(args.threads)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    if 'index' in os.listdir(args.input):
        shutil.copy(os.path.join(args.input, 'docid'), os.path.join(args.output, 'docid'))
        bf_index = faiss.read_index(os.path.join(args.input, 'index'))
        vectors = bf_index.reconstruct_n(0, bf_index.ntotal)
    else:
        vectors = []
        with open(os.path.join(args.output, 'docid'), 'w') as f_out:
            for filename in tqdm(os.listdir(args.input)):
                path = os.path.join(args.input, filename)
                with open(path) as f_in:
                    for line in f_in:
                        info = json.loads(line)
                        docid = info['id']
                        vector = info['vector']
                        f_out.write(f'{docid}\n')
                        vectors.append(vector)
    vectors = np.array(vectors, dtype='float32')
    print(vectors.shape)

    if args.hnsw and args.pq:
        index = faiss.IndexHNSWPQ(args.dim, args.pq_m, args.M)
        index.hnsw.efConstruction = args.efC
        index.metric_type = faiss.METRIC_INNER_PRODUCT
    elif args.hnsw:
        index = faiss.IndexHNSWFlat(args.dim, args.M, faiss.METRIC_INNER_PRODUCT)
        index.hnsw.efConstruction = args.efC
    elif args.pq:
        index = faiss.IndexPQ(args.dim, args.pq_m, args.pq_nbits, faiss.METRIC_INNER_PRODUCT)
    else:
        index = faiss.IndexFlatIP(args.dim)
    index.verbose = True

    if args.pq:
        index.train(vectors)

    index.add(vectors)
    print(index.ntotal)
    faiss.write_index(index, os.path.join(args.output, 'index'))
