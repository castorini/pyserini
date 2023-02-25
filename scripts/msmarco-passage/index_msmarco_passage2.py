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
import json
import os
import time

from pyserini.index.lucene import LuceneIndexer, JacksonObjectMapper


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Index MS MARCO Passage corpus.')
    parser.add_argument('--input', required=True, type=str, help='Path to MS MARCO Passage corpus.')
    parser.add_argument('--index', required=True, type=str, help='Path to index.')
    parser.add_argument('--threads', required=True, type=int, help='Number of threads.')
    parser.add_argument('--batch-size', required=True, type=int, help='Batch size.')
    parser.add_argument('--raw',  action='store_true', default=False, help="Directly index raw documents.")
    parser.add_argument('--dict',  action='store_true', default=False, help="Parse and index Python dictionaries.")
    args = parser.parse_args()

    mapper = JacksonObjectMapper()
    start = time.time()

    print(f'input: {args.input}')
    print(f'index: {args.index}')
    print(f'threads: {args.threads}')
    print(f'batch size: {args.batch_size}')
    print(f'index raw? {args.raw}')

    batch = []
    indexer = LuceneIndexer(args.index, threads=args.threads)
    cnt = 0
    batch_cnt = 0
    for file in os.listdir(args.input):
        if not file.endswith('gz'):
            continue
        with gzip.open(os.path.join(args.input, file), 'r') as f:
            for line in f:
                if args.raw:
                    batch.append(line.decode())
                elif args.dict:
                    obj = json.loads(line.decode())
                    batch.append({'id': obj['id'], 'contents': obj['contents']})
                else:
                    obj = json.loads(line.decode())
                    batch.append(mapper.createObjectNode().put('id', obj['id']).put('contents', obj['contents']))
                cnt += 1

                if len(batch) == args.batch_size:
                    if args.raw:
                        indexer.add_batch_raw(batch)
                    elif args.dict:
                        indexer.add_batch_dict(batch)
                    else:
                        indexer.add_batch_json(batch)
                    batch = []
                    batch_cnt += 1

                if cnt % 100000 == 0:
                    cur = time.time()
                    print(f'{cnt} docs indexed, {batch_cnt} batches, {cnt/(cur - start):.0f} docs/s')

    # Remember to add the final batch.
    if args.raw:
        indexer.add_batch_raw(batch)
    elif args.dict:
        indexer.add_batch_dict(batch)
    else:
        indexer.add_batch_json(batch)

    indexer.close()
    end = time.time()
    print(f'Total {cnt} docs indexed in {end - start:.0f}s, {cnt/(cur - start):.0f} docs/s')
