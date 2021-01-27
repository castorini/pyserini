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
from typing import Tuple, List, TextIO

from pyserini.pyclass import autoclass
from pyserini.search import get_topics, SimpleSearcher, JSimpleSearcherResult
from pyserini.search.reranker import ClassifierType, PseudoRelevanceClassifierReranker
from pyserini.query_iterator import QUERY_IDS, query_iterator
from tqdm import tqdm


def write_result(target_file: TextIO, result: Tuple[str, List[JSimpleSearcherResult]],
                 hits_num: int, msmarco: bool, tag: str):
    topic, hits = result
    docids = [hit.docid.strip() for hit in hits]
    scores = [hit.score for hit in hits]

    if msmarco:
        for i, docid in enumerate(docids):
            if i >= hits_num:
                break
            target_file.write(f'{topic}\t{docid}\t{i + 1}\n')
    else:
        for i, (docid, score) in enumerate(zip(docids, scores)):
            if i >= hits_num:
                break
            target_file.write(
                f'{topic} Q0 {docid} {i + 1} {score:.6f} {tag}\n')


def write_result_max_passage(target_file: TextIO, result: Tuple[str, List[JSimpleSearcherResult]],
                             max_passage_delimiter: str, max_passage_hits: int,
                             msmarco: bool, tag: str):
    topic, hits = result
    unique_docs = set()
    rank = 1
    for hit in hits:
        docid, _ = hit.docid.split(max_passage_delimiter)
        if docid in unique_docs:
            continue

        if msmarco:
            target_file.write(f'{topic}\t{docid}\t{rank}\n')
        else:
            target_file.write(
                f'{topic} Q0 {docid} {rank} {hit.score:.6f} {tag}\n')
        rank = rank + 1
        unique_docs.add(docid)
        if rank > max_passage_hits:
            break


def set_bm25_parameters(searcher, index, k1=None, b=None):
    if k1 is not None or b is not None:
        if k1 is None or b is None:
            print('Must set *both* k1 and b for BM25!')
            exit()
        print(f'Setting BM25 parameters: k1={k1}, b={b}')
        searcher.set_bm25(k1, b)
    else:
        # Automatically set bm25 parameters based on known index:
        if index == 'msmarco-passage' or index == 'msmarco-passage-slim':
            print('MS MARCO passage: setting k1=0.82, b=0.68')
            searcher.set_bm25(0.82, 0.68)
        elif index == 'msmarco-passage-expanded':
            print('MS MARCO passage w/ doc2query-T5 expansion: setting k1=2.18, b=0.86')
            searcher.set_bm25(2.18, 0.86)
        elif index == 'msmarco-doc' or index == 'msmarco-doc-slim':
            print('MS MARCO doc: setting k1=4.46, b=0.82')
            searcher.set_bm25(4.46, 0.82)
        elif index == 'msmarco-doc-per-passage' or index == 'msmarco-doc-per-passage-slim':
            print('MS MARCO doc, per passage: setting k1=2.16, b=0.61')
            searcher.set_bm25(2.16, 0.61)
        elif index == 'msmarco-doc-expanded-per-doc':
            print('MS MARCO doc w/ doc2query-T5 (per doc) expansion: setting k1=4.68, b=0.87')
            searcher.set_bm25(4.68, 0.87)
        elif index == 'msmarco-doc-expanded-per-passage':
            print('MS MARCO doc w/ doc2query-T5 (per passage) expansion: setting k1=2.56, b=0.59')
            searcher.set_bm25(2.56, 0.59)


def define_search_args(parser):
    parser.add_argument('--index', type=str, metavar='path to index or index name', required=True,
                        help="Path to Lucene index or name of prebuilt index.")
    parser.add_argument('--batch-size', type=int, metavar='num', required=False,
                        default=1, help="Specify batch size to search the collection concurrently.")
    parser.add_argument('--threads', type=int, metavar='num', required=False,
                        default=1, help="Maximum number of threads to use.")
    parser.add_argument('--bm25', action='store_true', default=True, help="Use BM25 (default).")
    parser.add_argument('--k1', type=float, help='BM25 k1 parameter.')
    parser.add_argument('--b', type=float, help='BM25 b parameter.')

    parser.add_argument('--rm3', action='store_true', help="Use RM3")
    parser.add_argument('--qld', action='store_true', help="Use QLD")

    parser.add_argument('--prcl', type=ClassifierType, nargs='+', default=[],
                        help='Specify the classifier PseudoRelevanceClassifierReranker uses.')
    parser.add_argument('--prcl.vectorizer', dest='vectorizer', type=str,
                        help='Type of vectorizer. Available: TfidfVectorizer, BM25Vectorizer.')
    parser.add_argument('--prcl.r', dest='r', type=int, default=10,
                        help='Number of positive labels in pseudo relevance feedback.')
    parser.add_argument('--prcl.n', dest='n', type=int, default=100,
                        help='Number of negative labels in pseudo relevance feedback.')
    parser.add_argument('--prcl.alpha', dest='alpha', type=float, default=0.5,
                        help='Alpha value for interpolation in pseudo relevance feedback.')


if __name__ == "__main__":
    JSimpleSearcher = autoclass('io.anserini.search.SimpleSearcher')
    parser = argparse.ArgumentParser(description='Search a Lucene index.')
    define_search_args(parser)
    parser.add_argument('--topics', type=str, metavar='topic_name', required=True,
                        help="Name of topics. Available: robust04, robust05, core17, core18.")
    parser.add_argument('--hits', type=int, metavar='num',
                        required=False, default=1000, help="Number of hits.")
    parser.add_argument('--msmarco',  action='store_true',
                        default=False, help="Output in MS MARCO format.")
    parser.add_argument('--output', type=str, metavar='path',
                        help="Path to output file.")
    parser.add_argument('--max-passage',  action='store_true',
                        default=False, help="Select only max passage from document.")
    parser.add_argument('--max-passage-hits', type=int, metavar='num', required=False, default=100,
                        help="Final number of hits when selecting only max passage.")
    parser.add_argument('--max-passage-delimiter', type=str, metavar='str', required=False, default='#',
                        help="Delimiter between docid and passage id.")
    args = parser.parse_args()

    topics = get_topics(args.topics)

    if os.path.exists(args.index):
        # create searcher from index directory
        searcher = SimpleSearcher(args.index)
    else:
        # create searcher from prebuilt index name
        searcher = SimpleSearcher.from_prebuilt_index(args.index)

    if not searcher:
        exit()

    search_rankers = []

    if args.qld:
        search_rankers.append('qld')
        searcher.set_qld()
    else:
        search_rankers.append('bm25')
        set_bm25_parameters(searcher, args.index, args.k1, args.b)

    if args.rm3:
        search_rankers.append('rm3')
        searcher.set_rm3()

    # invalid topics name
    if topics == {}:
        print(f'Topic {args.topics} Not Found')
        exit()

    # get re-ranker
    use_prcl = args.prcl and len(args.prcl) > 0 and args.alpha > 0
    if use_prcl is True:
        ranker = PseudoRelevanceClassifierReranker(
            searcher.index_dir, args.vectorizer, args.prcl, r=args.r, n=args.n, alpha=args.alpha)

    # build output path
    output_path = args.output
    if output_path is None:
        if use_prcl is True:
            clf_rankers = []
            for t in args.prcl:
                if t == ClassifierType.LR:
                    clf_rankers.append('lr')
                elif t == ClassifierType.SVM:
                    clf_rankers.append('svm')

            r_str = f'prcl.r_{args.r}'
            n_str = f'prcl.n_{args.n}'
            a_str = f'prcl.alpha_{args.alpha}'
            clf_str = 'prcl_' + '+'.join(clf_rankers)
            tokens1 = ['run', args.topics, '+'.join(search_rankers)]
            tokens2 = [args.vectorizer, clf_str, r_str, n_str, a_str]
            output_path = '.'.join(tokens1) + '-' + '-'.join(tokens2) + ".txt"
        else:
            tokens = ['run', args.topics, '+'.join(search_rankers), 'txt']
            output_path = '.'.join(tokens)

    print(f'Running {args.topics} topics, saving to {output_path}...')
    tag = output_path[:-4] if args.output is None else 'Anserini'

    order = None
    if args.topics in QUERY_IDS:
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
                # do rerank
                if use_prcl and len(hits) > (args.r + args.n):
                    hits = result[1]
                    docids = [hit.docid.strip() for hit in hits]
                    scores = [hit.score for hit in hits]
                    scores, docids = ranker.rerank(docids, scores)
                    docid_score_map = dict(zip(docids, scores))
                    for hit in hits:
                        hit.score = docid_score_map[hit.docid.strip()]

                # write results
                if args.max_passage:
                    write_result_max_passage(target_file, result, args.max_passage_delimiter,
                                             args.max_passage_hits, args.msmarco, tag)
                else:
                    write_result(target_file, result, args.hits, args.msmarco, tag)
            results.clear()
