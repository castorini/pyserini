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
import sys

from tqdm import tqdm

from pyserini.dsearch import TCTColBERTQueryEncoder, SimpleDenseSearcher
from pyserini.search import SimpleSearcher, get_topics
from pyserini.hsearch import HybridSearcher

from pyserini.dsearch.__main__ import define_dsearch_args
from pyserini.search.__main__ import define_search_args

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

    args = parse_args(parser, commands)

    topics = get_topics(args.run.topics)

    if args.dense.encoded_queries:
        if os.path.exists(args.dense.encoded_queries):
            # create query encoder from query embedding directory
            query_encoder = TCTColBERTQueryEncoder(args.dense.encoded_queries)
        else:
            # create query encoder from pre encoded query name
            query_encoder = TCTColBERTQueryEncoder.load_encoded_queries(args.dense.encoded_queries)
    else:
        query_encoder = TCTColBERTQueryEncoder(encoder_dir=args.dense.encoder, device=args.dense.device)

    if not query_encoder:
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

    hsearcher = HybridSearcher(dsearcher, ssearcher)
    if not hsearcher:
        exit()

    # invalid topics name
    if topics == {}:
        print(f'Topic {args.run.topics} Not Found')
        exit()

    # build output path
    output_path = args.run.output

    print(f'Running {args.run.topics} topics, saving to {output_path}...')
    tag = 'hybrid'

    if args.dense.batch > 1:
        with open(output_path, 'w') as target_file:
            topic_keys = sorted(topics.keys())
            for i in tqdm(range(0, len(topic_keys), args.dense.batch)):
                topic_key_batch = topic_keys[i: i + args.dense.batch]
                topic_batch = [topics[topic].get('title').strip() for topic in topic_key_batch]
                hits = hsearcher.batch_search(topic_batch,
                                              list(map(str, topic_key_batch)),
                                              k=args.run.hits, threads=args.dense.threads, alpha=args.fusion.alpha)
                for topic in hits:
                    for idx, hit in enumerate(hits[str(topic)]):
                        if args.run.msmarco:
                            if idx < args.run.hits:
                                target_file.write(f'{topic}\t{hit.docid}\t{idx + 1}\n')
                        else:
                            if idx < args.run.hits:
                                target_file.write(f'{topic} Q0 {hit.docid} {idx + 1} {hit.score:.6f} {tag}\n')
        exit()

    with open(output_path, 'w') as target_file:
        for topic in tqdm(sorted(topics.keys())):
            search = topics[topic].get('title').strip()
            hits = hsearcher.search(search, k=args.run.hits, alpha=args.fusion.alpha)
            docids = [hit.docid.strip() for hit in hits]
            scores = [hit.score for hit in hits]

            if args.run.msmarco:
                for i, docid in enumerate(docids):
                    if i < args.run.hits:
                        target_file.write(f'{topic}\t{docid}\t{i + 1}\n')
            else:
                for i, (docid, score) in enumerate(zip(docids, scores)):
                    if i < args.run.hits:
                        target_file.write(f'{topic} Q0 {docid} {i + 1} {score:.6f} {tag}\n')
