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
import sys

from tqdm import tqdm

from pyserini.dsearch import SimpleDenseSearcher
from pyserini.query_iterator import QUERY_IDS, query_iterator
from pyserini.search import SimpleSearcher, get_topics
from pyserini.hsearch import HybridSearcher

from pyserini.dsearch.__main__ import define_dsearch_args, init_query_encoder
from pyserini.search.__main__ import define_search_args, write_result, write_result_max_passage

# Fixes this error: "OMP: Error #15: Initializing libomp.a, but found libomp.dylib already initialized."
# https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def define_fusion_args(parser):
    parser.add_argument('--alpha', type=float, metavar='num', required=False, default=0.1,
                        help="alpha for hybrid search")


def parse_args(parser, commands):
    # Divide argv by commands
    split_argv = [[]]
    for c in sys.argv[1:]:
        if c in commands.choices:
            split_argv.append([c])
        else:
            split_argv[-1].append(c)
    # Initialize namespace
    args = argparse.Namespace()
    for c in commands.choices:
        setattr(args, c, None)
    # Parse each command
    parser.parse_args(split_argv[0], namespace=args)  # Without command
    for argv in split_argv[1:]:  # Commands
        n = argparse.Namespace()
        setattr(args, argv[0], n)
        parser.parse_args(argv, namespace=n)
    return args


def set_bm25_parameters(searcher, index, k1=None, b=None):
    if k1 is not None or b is not None:
        if k1 is None or b is None:
            print('Must set *both* k1 and b for BM25!')
            exit()
        print(f'Setting BM25 parameters: k1={k1}, b={b}')
        searcher.set_bm25(k1, b)
    else:
        pass  # placeholder, the parameters for hybrid search need re-tune


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Conduct a hybrid search on dense+sparse indexes.')

    commands = parser.add_subparsers(title='sub-commands')

    dense_parser = commands.add_parser('dense')
    define_dsearch_args(dense_parser)

    sparse_parser = commands.add_parser('sparse')
    define_search_args(sparse_parser)

    fusion_parser = commands.add_parser('fusion')
    define_fusion_args(fusion_parser)

    run_parser = commands.add_parser('run')
    run_parser.add_argument('--topics', type=str, metavar='topic_name', required=False,
                            help="Name of topics. Available: msmarco_passage_dev_subset.")
    run_parser.add_argument('--hits', type=int, metavar='num', required=False, default=1000, help="Number of hits.")
    run_parser.add_argument('--msmarco', action='store_true', default=False, help="Output in MS MARCO format.")
    run_parser.add_argument('--output', type=str, metavar='path', required=False, help="Path to output file.")
    run_parser.add_argument('--max-passage', action='store_true',
                            default=False, help="Select only max passage from document.")
    run_parser.add_argument('--max-passage-hits', type=int, metavar='num', required=False, default=100,
                            help="Final number of hits when selecting only max passage.")
    run_parser.add_argument('--max-passage-delimiter', type=str, metavar='str', required=False, default='#',
                            help="Delimiter between docid and passage id.")

    args = parse_args(parser, commands)

    if os.path.exists(args.run.topics) and args.run.topics.endswith('.json'):
        topics = json.load(open(args.run.topics))
    else:
        topics = get_topics(args.run.topics)
    # invalid topics name
    if topics == {}:
        print(f'Topic {args.run.topics} Not Found')
        exit()

    query_encoder = init_query_encoder(args.dense.encoder, args.run.topics, args.dense.device)
    if not query_encoder:
        print(f'No encoded queries for topic {args.run.topics}')
        exit()

    if os.path.exists(args.dense.index):
        # create searcher from index directory
        dsearcher = SimpleDenseSearcher(args.dense.index, query_encoder)
    else:
        # create searcher from prebuilt index name
        dsearcher = SimpleDenseSearcher.from_prebuilt_index(args.dense.index, query_encoder)

    if not dsearcher:
        exit()

    if os.path.exists(args.sparse.index):
        # create searcher from index directory
        ssearcher = SimpleSearcher(args.sparse.index)
    else:
        # create searcher from prebuilt index name
        ssearcher = SimpleSearcher.from_prebuilt_index(args.sparse.index)

    if not ssearcher:
        exit()

    set_bm25_parameters(ssearcher, args.sparse.index, args.sparse.k1, args.sparse.b)

    hsearcher = HybridSearcher(dsearcher, ssearcher)
    if not hsearcher:
        exit()

    # build output path
    output_path = args.run.output

    print(f'Running {args.run.topics} topics, saving to {output_path}...')
    tag = 'hybrid'

    order = None
    if args.run.topics in QUERY_IDS:
        print(f'Using pre-defined topic order for {args.run.topics}')
        order = QUERY_IDS[args.run.topics]

    with open(output_path, 'w') as target_file:
        batch_topics = list()
        batch_topic_ids = list()
        for index, (topic_id, text) in enumerate(tqdm(list(query_iterator(topics, order)))):
            if args.dense.batch_size <= 1 and args.dense.threads <= 1:
                hits = hsearcher.search(text, args.run.hits, args.fusion.alpha)
                results = [(topic_id, hits)]
            else:
                batch_topic_ids.append(str(topic_id))
                batch_topics.append(text)
                if (index + 1) % args.dense.batch_size == 0 or \
                        index == len(topics.keys()) - 1:
                    results = hsearcher.batch_search(
                        batch_topics, batch_topic_ids, args.run.hits, args.dense.threads, args.fusion.alpha)
                    results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    batch_topic_ids.clear()
                    batch_topics.clear()
                else:
                    continue

            for result in results:
                if args.run.max_passage:
                    write_result_max_passage(target_file, result, args.run.max_passage_delimiter,
                                             args.run.max_passage_hits, args.run.msmarco, tag)
                else:
                    write_result(target_file, result, args.run.hits, args.run.msmarco, tag)
            results.clear()
