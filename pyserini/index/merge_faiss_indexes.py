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

import faiss
import os


parser = argparse.ArgumentParser()
parser.add_argument('--dimension', type=int, help='dimension of passage embeddings', required=False, default=768)
parser.add_argument('--prefix', type=str, help='directory to store brute force index of corpus', required=True)
parser.add_argument('--shard-num', type=int, help='number of shards', default=1)
args = parser.parse_args()

new_index = faiss.IndexFlatIP(args.dimension)
docid_files = []
for i in range(args.shard_num):
    index = faiss.read_index(os.path.join(args.prefix + str(i), 'index'))
    docid_files.append(os.path.join(args.prefix + str(i), 'docid'))
    vectors = index.reconstruct_n(0, index.ntotal)
    new_index.add(vectors)

if not os.path.exists(args.prefix + 'full'):
    os.mkdir(args.prefix + 'full')

faiss.write_index(new_index, os.path.join(args.prefix + 'full', 'index'))

with open(os.path.join(args.prefix + 'full', 'docid'), 'w') as wfd:
    for f in docid_files:
        with open(f, 'r') as f1:
            for line in f1:
                wfd.write(line)
