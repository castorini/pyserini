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
import gzip
import os
import time

from pyserini.index.lucene import LuceneIndexer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Index MS MARCO Passage corpus.')
    parser.add_argument('--input', required=True, help='Path to MS MARCO Passage corpus.')
    parser.add_argument('--index', required=True, help='Path to index.')
    args = parser.parse_args()

    start = time.time()

    print(f'input: {args.input}')
    print(f'index: {args.index}')

    indexer = LuceneIndexer(args.index)
    cnt = 0
    for file in os.listdir(args.input):
        if not file.endswith('gz'):
            continue
        with gzip.open(os.path.join(args.input, file), 'r') as f:
            for line in f:
                indexer.add(line.decode())
                cnt += 1
                if cnt % 100000 == 0:
                    print(f'{cnt} docs indexed')

    indexer.close()
    end = time.time()
    print(f'Total {cnt} docs indexed in {end - start:.0f}s')
