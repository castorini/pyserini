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
import time
from tqdm import tqdm

from ._searcher import NmslibSearcher
from pyserini.output_writer import get_output_writer, OutputFormat, tie_breaker

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a nmslib index.')
    parser.add_argument('--index', type=str, metavar='path to index or index name', required=True,
                        help="Path to nmslib index.")
    parser.add_argument('--topics', type=str, required=True, help="path to topics")
    parser.add_argument('--hits', type=int, metavar='num', required=False, default=1000, help="Number of hits.")
    parser.add_argument('--output-format', type=str, metavar='format', default=OutputFormat.TREC.value,
                        help=f"Format of output. Available: {[x.value for x in list(OutputFormat)]}")
    parser.add_argument('--output', type=str, metavar='path', required=True, help="Path to output file.")
    parser.add_argument('--ef', type=int, required=False, default=256, help="hnsw ef_search")
    parser.add_argument('--threads', type=int, metavar='num', required=False, default=1,
                        help="maximum threads to use during search")
    parser.add_argument('--batch-size', type=int, metavar='num', required=False, default=1,
                        help="search batch of queries in parallel")
    parser.add_argument('--is-sparse', action='store_true', required=False)
    args = parser.parse_args()

    searcher = NmslibSearcher(args.index, ef_search=args.ef, is_sparse=args.is_sparse)

    topic_ids = []
    topic_vectors = []
    with open(args.topics) as topic_f:
        for line in topic_f:
            info = json.loads(line)
            topic_ids.append(info['id'])
            topic_vectors.append(info['vector'])

    if not searcher:
        exit()

    # build output path
    output_path = args.output

    print(f'Running {args.topics} topics, saving to {output_path}...')
    tag = 'HNSW'

    # support trec and msmarco format only for now
    output_writer = get_output_writer(output_path, OutputFormat(args.output_format), max_hits=args.hits, tag=tag)

    search_time = 0
    with output_writer:
        batch_topic_vectors = list()
        batch_topic_ids = list()
        for index, (topic_id, vec) in enumerate(tqdm(zip(topic_ids, topic_vectors))):
            if args.batch_size <= 1 and args.threads <= 1:
                start = time.time()
                hits = searcher.search(vec, args.hits)
                search_time += time.time() - start
                results = [(topic_id, hits)]
            else:
                batch_topic_ids.append(str(topic_id))
                batch_topic_vectors.append(vec)
                if (index + 1) % args.batch_size == 0 or \
                        index == len(topic_ids) - 1:
                    start = time.time()
                    results = searcher.batch_search(
                            batch_topic_vectors, batch_topic_ids, args.hits, args.threads)
                    search_time += time.time() - start
                    results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    batch_topic_ids.clear()
                    batch_topic_vectors.clear()
                else:
                    continue

            for topic, hits in results:
                output_writer.write(topic, tie_breaker(hits))

            results.clear()

    print(f'Search {len(topic_ids)} topics in {search_time} seconds')
