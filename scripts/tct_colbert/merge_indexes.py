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
parser.add_argument('--segment-num', type=int, help='number of passage segments, use -1 for MaxP', default=1)
parser.add_argument('--shard-num', type=int, help='number of shards', default=1)
args = parser.parse_args()

new_index = faiss.IndexFlatIP(args.dimension)
docid_list = []
for i in range(args.shard_num):
    index = os.path.join(args.prefix + f"{i:02d}", 'index')
    docid = os.path.join(args.prefix + f"{i:02d}", 'docid')
    print(f"reading ... {index}")
    line_idx = []
    with open(docid, 'r') as f:
        for idx, line in enumerate(f):
            doc_id, psg_id = line.strip().split("#")
            if args.segment_num == -1:
                line_idx.append(idx)
                docid_list.append(doc_id + "#" + psg_id)

            elif int(psg_id) < args.segment_num:
                line_idx.append(idx)
                docid_list.append(doc_id + "#" + psg_id)

    index = faiss.read_index(index)
    vectors = index.reconstruct_n(0, index.ntotal)
    new_index.add(vectors[line_idx]) # filter segments

if args.segment_num == -1:
    postfix = 'maxp'
elif args.segment_num == 1:
    postfix = 'firstp'
else:
    postfix = f'seg{args.segment_num}'

if not os.path.exists(args.prefix + f'full-{postfix}'):
    os.mkdir(args.prefix + f'full-{postfix}')


print(f"number of docs: {len(docid_list)}")
print(f"number of vecs: {new_index.ntotal}")
assert len(docid_list) == new_index.ntotal
faiss.write_index(new_index, os.path.join(args.prefix + f'full-{postfix}', 'index'))

with open(os.path.join(args.prefix + f'full-{postfix}', 'docid'), 'w') as wfd:
    for docid in docid_list:
        wfd.write(docid + '\n')
