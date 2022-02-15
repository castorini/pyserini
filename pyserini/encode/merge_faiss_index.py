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

import os
import glob
import argparse

import faiss
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument('--dimension', type=int, help='dimension of passage embeddings', required=False, default=768)
parser.add_argument('--input', type=str, help='wildcard directory to input indexes', required=True)
parser.add_argument('--output', type=str, help='directory to output full indexes', required=True)
args = parser.parse_args()
os.makedirs(args.output, exist_ok=True)

# merge index
new_index = faiss.IndexFlatIP(args.dimension)
docid_files = []
for index_dir in tqdm(sorted(glob.glob(args.input)), desc="Merging Faiss Index"):
    index = faiss.read_index(os.path.join(index_dir, 'index'))
    docid_files.append(os.path.join(index_dir, 'docid'))
    vectors = index.reconstruct_n(0, index.ntotal)
    new_index.add(vectors)

faiss.write_index(new_index, os.path.join(args.output, 'index'))

# merge docid
with open(os.path.join(args.output, 'docid'), 'w') as wfd:
    for f in docid_files:
        with open(f, 'r') as f1:
            for line in f1:
                wfd.write(line)
