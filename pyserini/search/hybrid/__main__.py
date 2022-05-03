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
import json
import os
import sys

from tqdm import tqdm

from pyserini.search.faiss import FaissSearcher
from pyserini.query_iterator import get_query_iterator, TopicsFormat
from pyserini.output_writer import get_output_writer, OutputFormat
from pyserini.search.lucene import LuceneImpactSearcher, LuceneSearcher
from pyserini.search.hybrid import HybridSearcher

from pyserini.search.faiss.__main__ import define_dsearch_args, init_query_encoder
from pyserini.search.lucene.__main__ import define_search_args, set_bm25_parameters

# Fixes this error: "OMP: Error #15: Initializing libomp.a, but found libomp.dylib already initialized."
# https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'


def define_fusion_args(parser):
    parser.add_argument('--alpha', type=float, metavar='num', required=False, default=0.1,
                        help="alpha for hybrid search")
    parser.add_argument('--hits', type=int, required=False, default=1000, help='number of hits from dense and sparse')
    parser.add_argument('--normalization', action='store_true', required=False, help='hybrid score with normalization')
    parser.add_argument('--weight-on-dense', action='store_true', required=False, help='weight on dense part')


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
                            help="Name of topics. Available: msmarco-passage-dev-subset.")
    run_parser.add_argument('--hits', type=int, metavar='num', required=False, default=1000, help="Number of hits.")
    run_parser.add_argument('--topics-format', type=str, metavar='format', default=TopicsFormat.DEFAULT.value,
                            help=f"Format of topics. Available: {[x.value for x in list(TopicsFormat)]}")
    run_parser.add_argument('--output-format', type=str, metavar='format', default=OutputFormat.TREC.value,
                            help=f"Format of output. Available: {[x.value for x in list(OutputFormat)]}")
    run_parser.add_argument('--output', type=str, metavar='path', required=False, help="Path to output file.")
    run_parser.add_argument('--max-passage', action='store_true',
                            default=False, help="Select only max passage from document.")
    run_parser.add_argument('--max-passage-hits', type=int, metavar='num', required=False, default=100,
                            help="Final number of hits when selecting only max passage.")
    run_parser.add_argument('--max-passage-delimiter', type=str, metavar='str', required=False, default='#',
                            help="Delimiter between docid and passage id.")
    run_parser.add_argument('--batch-size', type=int, metavar='num', required=False,
                            default=1, help="Specify batch size to search the collection concurrently.")
    run_parser.add_argument('--threads', type=int, metavar='num', required=False,
                            default=1, help="Maximum number of threads to use.")

    args = parse_args(parser, commands)

    query_iterator = get_query_iterator(args.run.topics, TopicsFormat(args.run.topics_format))
    topics = query_iterator.topics

    query_encoder = init_query_encoder(args.dense.encoder,
                                       args.dense.encoder_class,
                                       args.dense.tokenizer,
                                       args.run.topics,
                                       args.dense.encoded_queries,
                                       args.dense.device,
                                       args.dense.query_prefix)

    if os.path.exists(args.dense.index):
        # create searcher from index directory
        dsearcher = FaissSearcher(args.dense.index, query_encoder)
    else:
        # create searcher from prebuilt index name
        dsearcher = FaissSearcher.from_prebuilt_index(args.dense.index, query_encoder)

    if not dsearcher:
        exit()

    if os.path.exists(args.sparse.index):
        # create searcher from index directory
        if args.sparse.impact:
            ssearcher = LuceneImpactSearcher(args.sparse.index, args.sparse.encoder, args.sparse.min_idf)
        else:
            ssearcher = LuceneSearcher(args.sparse.index)
    else:
        # create searcher from prebuilt index name
        if args.sparse.impact:
            ssearcher = LuceneImpactSearcher.from_prebuilt_index(args.sparse.index, args.sparse.encoder, args.sparse.min_idf)
        else:
            ssearcher = LuceneSearcher.from_prebuilt_index(args.sparse.index)

    if not ssearcher:
        exit()

    set_bm25_parameters(ssearcher, args.sparse.index, args.sparse.k1, args.sparse.b)

    if args.sparse.language != 'en':
        ssearcher.set_language(args.sparse.language)

    hsearcher = HybridSearcher(dsearcher, ssearcher)
    if not hsearcher:
        exit()

    # build output path
    output_path = args.run.output

    print(f'Running {args.run.topics} topics, saving to {output_path}...')
    tag = 'hybrid'

    output_writer = get_output_writer(output_path, OutputFormat(args.run.output_format), 'w',
                                      max_hits=args.run.hits, tag=tag, topics=topics,
                                      use_max_passage=args.run.max_passage,
                                      max_passage_delimiter=args.run.max_passage_delimiter,
                                      max_passage_hits=args.run.max_passage_hits)

    with output_writer:
        batch_topics = list()
        batch_topic_ids = list()
        for index, (topic_id, text) in enumerate(tqdm(query_iterator, total=len(topics.keys()))):
            if args.run.batch_size <= 1 and args.run.threads <= 1:
                hits = hsearcher.search(text, args.fusion.hits, args.run.hits, args.fusion.alpha, args.fusion.normalization, args.fusion.weight_on_dense)
                results = [(topic_id, hits)]
            else:
                batch_topic_ids.append(str(topic_id))
                batch_topics.append(text)
                if (index + 1) % args.run.batch_size == 0 or \
                        index == len(topics.keys()) - 1:
                    results = hsearcher.batch_search(
                        batch_topics, batch_topic_ids, args.fusion.hits, args.run.hits, args.run.threads,
                        args.fusion.alpha, args.fusion.normalization, args.fusion.weight_on_dense)
                    results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    batch_topic_ids.clear()
                    batch_topics.clear()
                else:
                    continue

            for topic, hits in results:
                output_writer.write(topic, hits)

            results.clear()
