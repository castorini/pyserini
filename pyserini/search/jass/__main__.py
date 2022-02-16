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
import os
import errno

from tqdm import tqdm

from pyserini.output_writer import OutputFormat, get_output_writer
from pyserini.query_iterator import get_query_iterator, TopicsFormat
from pyserini.search.jass import JASSv2Searcher




def define_search_args(parser):
    parser.add_argument('--index', type=str, default='/home/pradeesh', metavar='path to index or index name', required=False,
                        help="Path to pyJass index")
    parser.add_argument('--rho', type=int, help='rho parameter.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Search a pyJass index.')
    define_search_args(parser)
    parser.add_argument('--topics', type=str, default='/home/pradeesh/query/sample_queries.tsv',metavar='topic_name', required=False,
                        help="Name of topics. Available: robust04, robust05, core17, core18.")
    parser.add_argument('--hits', type=int, metavar='num',
                        required=False, default=1000, help="Number of hits.")
    parser.add_argument('--topics-format', type=str, metavar='format', default=TopicsFormat.DEFAULT.value,
                        help=f"Format of topics. Available: {[x.value for x in list(TopicsFormat)]}")
    parser.add_argument('--output-format', type=str, metavar='format', default=OutputFormat.TREC.value,
                        help=f"Format of output. Available: {[x.value for x in list(OutputFormat)]}")
    parser.add_argument('--output', type=str, metavar='path',
                        help="Path to output file.")
    parser.add_argument('--batch-size', type=int, metavar='num', required=False,
                        default=1, help="Specify batch size to search the collection concurrently.")
    parser.add_argument('--threads', type=int, metavar='num', required=False,
                        default=1, help="Maximum number of threads to use.")
    args = parser.parse_args()

    query_iterator = get_query_iterator(args.topics, TopicsFormat(args.topics_format))
    topics = query_iterator.topics

    if os.path.exists(args.index):
        # create searcher from index directory
        print(args.index)
        searcher = JASSv2Searcher('/home/pradeesh',2)
    else:
        # TODO: handle pre_build index if it's not found but we will throw file not found
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), args.index) 

    if not searcher:
        exit()

    fields = dict()
    if args.fields:
        fields = dict([pair.split('=') for pair in args.fields])
        print(f'Searching over fields: {fields}')


    # build output path
    output_path = args.output
    if output_path is None:
        tokens = ['run', args.topics, '+'.join(['rho',args.rho]), 'txt'] # we use the rho output
        output_path = '.'.join(tokens)

    print(f'Running {args.topics} topics, saving to {output_path}...')
    tag = output_path[:-4] if args.output is None else 'pyJass'

    output_writer = get_output_writer(output_path, OutputFormat(args.output_format), 'w',
                                      max_hits=args.hits, tag=tag, topics=topics)

    with output_writer:
        batch_topics = list()
        batch_topic_ids = list()
        for index, (topic_id, text) in enumerate(tqdm(query_iterator, total=len(topics.keys()))):
            if args.batch_size <= 1 and args.threads <= 1:
                hits = searcher.search(text, args.hits, fields=fields)
                results = [(topic_id, hits)]
            else:
                batch_topic_ids.append(str(topic_id))
                batch_topics.append(text)
                if (index + 1) % args.batch_size == 0 or \
                    index == len(topics.keys()) - 1:
                    results = searcher.batch_search(
                        batch_topics, batch_topic_ids, args.hits, args.threads, fields=fields
                    )
                    results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    batch_topic_ids.clear()
                    batch_topics.clear()
                else:
                    continue

            for topic, hits in results:
                # write results
                output_writer.write(topic, hits)

            results.clear()
