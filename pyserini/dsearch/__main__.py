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
import os

import json
from tqdm import tqdm

from pyserini.dsearch import SimpleDenseSearcher, TCTColBERTQueryEncoder, QueryEncoder, DPRQueryEncoder
from pyserini.query_iterator import QUERY_IDS, query_iterator
from pyserini.search import get_topics
from pyserini.search.__main__ import write_result, write_result_max_passage

# Fixes this error: "OMP: Error #15: Initializing libomp.a, but found libomp.dylib already initialized."
# https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def define_dsearch_args(parser):
    parser.add_argument('--index', type=str, metavar='path to index or index name', required=True,
                        help="Path to Faiss index or name of prebuilt index.")
    parser.add_argument('--encoder', type=str, metavar='path to query encoder checkpoint or encoder name',
                        required=False,
                        help="Path to query encoder pytorch checkpoint or hgf encoder model name")
    parser.add_argument('--device', type=str, metavar='device to run query encoder', required=False, default='cpu',
                        help="Device to run query encoder, cpu or [cuda:0, cuda:1, ...]")
    parser.add_argument('--batch-size', type=int, metavar='num', required=False, default=1,
                        help="search batch of queries in parallel")
    parser.add_argument('--threads', type=int, metavar='num', required=False, default=1,
                        help="maximum threads to use during search")


def init_query_encoder(encoder, topics_name, device):
    encoded_queries = {
        'msmarco_passage_dev_subset': 'msmarco-passage-dev-subset-tct_colbert',
        'nq_dev_dpr': 'nq-dev-dpr',
        'nq_test_dpr': 'nq-test-dpr',
    }
    if encoder:
        if 'dpr' in encoder:
            return DPRQueryEncoder(encoder_dir=encoder, device=device)
        elif 'tct_colbert' in encoder:
            return TCTColBERTQueryEncoder(encoder_dir=encoder, device=device)
    if topics_name in encoded_queries:
        return QueryEncoder.load_encoded_queries(encoded_queries[topics_name])
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Search a Faiss index.')
    parser.add_argument('--topics', type=str, metavar='topic_name', required=True,
                        help="Name of topics. Available: msmarco_passage_dev_subset.")
    parser.add_argument('--hits', type=int, metavar='num', required=False, default=1000, help="Number of hits.")
    parser.add_argument('--msmarco', action='store_true', default=False, help="Output in MS MARCO format.")
    parser.add_argument('--output', type=str, metavar='path', required=True, help="Path to output file.")
    parser.add_argument('--max-passage',  action='store_true',
                        default=False, help="Select only max passage from document.")
    parser.add_argument('--max-passage-hits', type=int, metavar='num', required=False, default=100,
                        help="Final number of hits when selecting only max passage.")
    parser.add_argument('--max-passage-delimiter', type=str, metavar='str', required=False, default='#',
                        help="Delimiter between docid and passage id.")
    define_dsearch_args(parser)
    args = parser.parse_args()

    if os.path.exists(args.topics) and args.topics.endswith('.json'):
        topics = json.load(open(args.topics))
    else:
        topics = get_topics(args.topics)

    # invalid topics name
    if topics == {}:
        print(f'Topic {args.topics} Not Found')
        exit()

    query_encoder = init_query_encoder(args.encoder, args.topics, args.device)
    if not query_encoder:
        print(f'No encoded queries for topic {args.topics}')
        exit()

    if os.path.exists(args.index):
        # create searcher from index directory
        searcher = SimpleDenseSearcher(args.index, query_encoder)
    else:
        # create searcher from prebuilt index name
        searcher = SimpleDenseSearcher.from_prebuilt_index(args.index, query_encoder)

    if not searcher:
        exit()

    # build output path
    output_path = args.output

    print(f'Running {args.topics} topics, saving to {output_path}...')
    tag = 'Faiss'

    order = None
    if args.topics in QUERY_IDS:
        print(f'Using pre-defined topic order for {args.topics}')
        order = QUERY_IDS[args.topics]

    with open(output_path, 'w') as target_file:
        batch_topics = list()
        batch_topic_ids = list()
        for index, (topic_id, text) in enumerate(tqdm(list(query_iterator(topics, order)))):
            if args.batch_size <= 1 and args.threads <= 1:
                hits = searcher.search(text, args.hits)
                results = [(topic_id, hits)]
            else:
                batch_topic_ids.append(str(topic_id))
                batch_topics.append(text)
                if (index + 1) % args.batch_size == 0 or \
                        index == len(topics.keys()) - 1:
                    results = searcher.batch_search(
                        batch_topics, batch_topic_ids, args.hits, args.threads)
                    results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    batch_topic_ids.clear()
                    batch_topics.clear()
                else:
                    continue

            for result in results:
                if args.max_passage:
                    write_result_max_passage(target_file, result, args.max_passage_delimiter,
                                             args.max_passage_hits, args.msmarco, tag)
                else:
                    write_result(target_file, result, args.hits, args.msmarco, tag)
            results.clear()
