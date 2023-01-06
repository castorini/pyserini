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

from tqdm import tqdm
from transformers import AutoTokenizer

from pyserini.analysis import JDefaultEnglishAnalyzer, JWhiteSpaceAnalyzer
from pyserini.output_writer import OutputFormat, get_output_writer
from pyserini.pyclass import autoclass
from pyserini.query_iterator import get_query_iterator, TopicsFormat
from pyserini.search import JDisjunctionMaxQueryGenerator
from . import LuceneImpactSearcher, LuceneSearcher
from .reranker import ClassifierType, PseudoRelevanceClassifierReranker


def set_bm25_parameters(searcher, index, k1=None, b=None):
    if k1 is not None or b is not None:
        if k1 is None or b is None:
            print('Must set *both* k1 and b for BM25!')
            exit()
        print(f'Setting BM25 parameters: k1={k1}, b={b}')
        searcher.set_bm25(k1, b)
    else:
        # Automatically set bm25 parameters based on known index...
        if index == 'msmarco-passage' or index == 'msmarco-passage-slim' or index == 'msmarco-v1-passage' or \
                index == 'msmarco-v1-passage-slim' or index == 'msmarco-v1-passage-full':
            # See https://github.com/castorini/anserini/blob/master/docs/regressions-msmarco-passage.md
            print('MS MARCO passage: setting k1=0.82, b=0.68')
            searcher.set_bm25(0.82, 0.68)
        elif index == 'msmarco-passage-expanded' or \
                index == 'msmarco-v1-passage-d2q-t5' or \
                index == 'msmarco-v1-passage-d2q-t5-docvectors':
            # See https://github.com/castorini/anserini/blob/master/docs/regressions-msmarco-passage-docTTTTTquery.md
            print('MS MARCO passage w/ doc2query-T5 expansion: setting k1=2.18, b=0.86')
            searcher.set_bm25(2.18, 0.86)
        elif index == 'msmarco-doc' or index == 'msmarco-doc-slim' or index == 'msmarco-v1-doc' or \
                index == 'msmarco-v1-doc-slim' or index == 'msmarco-v1-doc-full':
            # See https://github.com/castorini/anserini/blob/master/docs/regressions-msmarco-doc.md
            print('MS MARCO doc: setting k1=4.46, b=0.82')
            searcher.set_bm25(4.46, 0.82)
        elif index == 'msmarco-doc-per-passage' or index == 'msmarco-doc-per-passage-slim' or \
                index == 'msmarco-v1-doc-segmented' or index == 'msmarco-v1-doc-segmented-slim' or \
                index == 'msmarco-v1-doc-segmented-full':
            # See https://github.com/castorini/anserini/blob/master/docs/regressions-msmarco-doc-segmented.md
            print('MS MARCO doc, per passage: setting k1=2.16, b=0.61')
            searcher.set_bm25(2.16, 0.61)
        elif index == 'msmarco-doc-expanded-per-doc' or \
                index == 'msmarco-v1-doc-d2q-t5' or \
                index == 'msmarco-v1-doc-d2q-t5-docvectors':
            # See https://github.com/castorini/anserini/blob/master/docs/regressions-msmarco-doc-docTTTTTquery.md
            print('MS MARCO doc w/ doc2query-T5 (per doc) expansion: setting k1=4.68, b=0.87')
            searcher.set_bm25(4.68, 0.87)
        elif index == 'msmarco-doc-expanded-per-passage' or \
                index == 'msmarco-v1-doc-segmented-d2q-t5' or \
                index == 'msmarco-v1-doc-segmented-d2q-t5-docvectors':
            # See https://github.com/castorini/anserini/blob/master/docs/regressions-msmarco-doc-segmented-docTTTTTquery.md
            print('MS MARCO doc w/ doc2query-T5 (per passage) expansion: setting k1=2.56, b=0.59')
            searcher.set_bm25(2.56, 0.59)


def define_search_args(parser):
    parser.add_argument('--index', type=str, metavar='path to index or index name', required=True,
                        help="Path to Lucene index or name of prebuilt index.")

    parser.add_argument('--impact', action='store_true', help="Use Impact.")
    parser.add_argument('--encoder', type=str, default=None, help="encoder name")
    parser.add_argument('--min-idf', type=int, default=0, help="minimum idf")

    parser.add_argument('--bm25', action='store_true', default=True, help="Use BM25 (default).")
    parser.add_argument('--k1', type=float, help='BM25 k1 parameter.')
    parser.add_argument('--b', type=float, help='BM25 b parameter.')

    parser.add_argument('--rm3', action='store_true', help="Use RM3")
    parser.add_argument('--rocchio', action='store_true', help="Use Rocchio")
    parser.add_argument('--rocchio-use-negative', action='store_true', help="Use nonrelevant labels in Rocchio")
    parser.add_argument('--qld', action='store_true', help="Use QLD")

    parser.add_argument('--language', type=str, help='language code for BM25, e.g. zh for Chinese', default='en')
    parser.add_argument('--pretokenized', action='store_true', help="Boolean switch to accept pre-tokenized topics")

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

    parser.add_argument('--fields', metavar="key=value", nargs='+',
                        help='Fields to search with assigned float weights.')
    parser.add_argument('--dismax', action='store_true', default=False,
                        help='Use disjunction max queries when searching multiple fields.')
    parser.add_argument('--dismax.tiebreaker', dest='tiebreaker', type=float, default=0.0,
                        help='The tiebreaker weight to use in disjunction max queries.')

    parser.add_argument('--stopwords', type=str, help='Path to file with customstopwords.')


if __name__ == "__main__":
    JLuceneSearcher = autoclass('io.anserini.search.SimpleSearcher')
    parser = argparse.ArgumentParser(description='Search a Lucene index.')
    define_search_args(parser)
    parser.add_argument('--topics', type=str, metavar='topic_name', required=True,
                        help="Name of topics. Available: robust04, robust05, core17, core18.")
    parser.add_argument('--hits', type=int, metavar='num',
                        required=False, default=1000, help="Number of hits.")
    parser.add_argument('--topics-format', type=str, metavar='format', default=TopicsFormat.DEFAULT.value,
                        help=f"Format of topics. Available: {[x.value for x in list(TopicsFormat)]}")
    parser.add_argument('--output-format', type=str, metavar='format', default=OutputFormat.TREC.value,
                        help=f"Format of output. Available: {[x.value for x in list(OutputFormat)]}")
    parser.add_argument('--output', type=str, metavar='path',
                        help="Path to output file.")
    parser.add_argument('--max-passage',  action='store_true',
                        default=False, help="Select only max passage from document.")
    parser.add_argument('--max-passage-hits', type=int, metavar='num', required=False, default=100,
                        help="Final number of hits when selecting only max passage.")
    parser.add_argument('--max-passage-delimiter', type=str, metavar='str', required=False, default='#',
                        help="Delimiter between docid and passage id.")
    parser.add_argument('--batch-size', type=int, metavar='num', required=False,
                        default=1, help="Specify batch size to search the collection concurrently.")
    parser.add_argument('--threads', type=int, metavar='num', required=False,
                        default=1, help="Maximum number of threads to use.")
    parser.add_argument('--tokenizer', type=str, help='tokenizer used to preprocess topics')
    parser.add_argument('--remove-duplicates', action='store_true', default=False, help="Remove duplicate docs.")
    # For some test collections, a query is doc from the corpus (e.g., arguana in BEIR).
    # We want to remove the query from the results. This is equivalent to -removeQuery in Java.
    parser.add_argument('--remove-query', action='store_true', default=False, help="Remove query from results list.")

    args = parser.parse_args()

    query_iterator = get_query_iterator(args.topics, TopicsFormat(args.topics_format))
    topics = query_iterator.topics

    if not args.impact:
        if os.path.exists(args.index):
            # create searcher from index directory
            searcher = LuceneSearcher(args.index)
        else:
            # create searcher from prebuilt index name
            searcher = LuceneSearcher.from_prebuilt_index(args.index)
    elif args.impact:
        if os.path.exists(args.index):
            searcher = LuceneImpactSearcher(args.index, args.encoder, args.min_idf)
        else:
            searcher = LuceneImpactSearcher.from_prebuilt_index(args.index, args.encoder, args.min_idf)

    if args.language != 'en':
        searcher.set_language(args.language)

    if not searcher:
        exit()

    search_rankers = []

    if args.qld:
        search_rankers.append('qld')
        searcher.set_qld()
    elif args.bm25:
        search_rankers.append('bm25')
        set_bm25_parameters(searcher, args.index, args.k1, args.b)

    if args.rm3:
        search_rankers.append('rm3')
        searcher.set_rm3()
    
    if args.rocchio:
        search_rankers.append('rocchio')
        if args.rocchio_use_negative:
            searcher.set_rocchio(gamma=0.15, use_negative=True)
        else:
            searcher.set_rocchio()

    fields = dict()
    if args.fields:
        fields = dict([pair.split('=') for pair in args.fields])
        print(f'Searching over fields: {fields}')

    query_generator = None
    if args.dismax:
        query_generator = JDisjunctionMaxQueryGenerator(args.tiebreaker)
        print(f'Using dismax query generator with tiebreaker={args.tiebreaker}')
    
    if args.pretokenized:
        analyzer = JWhiteSpaceAnalyzer()
        searcher.set_analyzer(analyzer)
        if args.tokenizer is not None:
            raise ValueError(f"--tokenizer is not supported with when setting --pretokenized.")

    if args.tokenizer != None:
        analyzer = JWhiteSpaceAnalyzer()
        searcher.set_analyzer(analyzer)
        print(f'Using whitespace analyzer because of pretokenized topics')
        tokenizer = AutoTokenizer.from_pretrained(args.tokenizer)
        print(f'Using {args.tokenizer} to preprocess topics')

    if args.stopwords:
        analyzer = JDefaultEnglishAnalyzer.fromArguments('porter', False, args.stopwords)
        searcher.set_analyzer(analyzer)
        print(f'Using custom stopwords={args.stopwords}')

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

    output_writer = get_output_writer(output_path, OutputFormat(args.output_format), 'w',
                                      max_hits=args.hits, tag=tag, topics=topics,
                                      use_max_passage=args.max_passage,
                                      max_passage_delimiter=args.max_passage_delimiter,
                                      max_passage_hits=args.max_passage_hits)

    with output_writer:
        batch_topics = list()
        batch_topic_ids = list()
        for index, (topic_id, text) in enumerate(tqdm(query_iterator, total=len(topics.keys()))):
            if (args.tokenizer != None):
                toks = tokenizer.tokenize(text)
                text = ' '
                text = text.join(toks)
            if args.batch_size <= 1 and args.threads <= 1:
                if args.impact:
                    hits = searcher.search(text, args.hits, fields=fields)
                else:
                    hits = searcher.search(text, args.hits, query_generator=query_generator, fields=fields)
                results = [(topic_id, hits)]
            else:
                batch_topic_ids.append(str(topic_id))
                batch_topics.append(text)
                if (index + 1) % args.batch_size == 0 or \
                        index == len(topics.keys()) - 1:
                    if args.impact:
                        results = searcher.batch_search(
                            batch_topics, batch_topic_ids, args.hits, args.threads, fields=fields
                        )
                    else:
                        results = searcher.batch_search(
                            batch_topics, batch_topic_ids, args.hits, args.threads,
                            query_generator=query_generator, fields=fields
                        )
                    results = [(id_, results[id_]) for id_ in batch_topic_ids]
                    batch_topic_ids.clear()
                    batch_topics.clear()
                else:
                    continue

            for topic, hits in results:
                # do rerank
                if use_prcl and len(hits) > (args.r + args.n):
                    docids = [hit.docid.strip() for hit in hits]
                    scores = [hit.score for hit in hits]
                    scores, docids = ranker.rerank(docids, scores)
                    docid_score_map = dict(zip(docids, scores))
                    for hit in hits:
                        hit.score = docid_score_map[hit.docid.strip()]
                        
                if args.remove_duplicates:
                    seen_docids = set()
                    dedup_hits = []
                    for hit in hits:
                        if hit.docid.strip() in seen_docids:
                            continue
                        seen_docids.add(hit.docid.strip())
                        dedup_hits.append(hit)
                    hits = dedup_hits

                # For some test collections, a query is doc from the corpus (e.g., arguana in BEIR).
                # We want to remove the query from the results.
                if args.remove_query:
                    hits = [hit for hit in hits if hit.docid != topic]

                # write results
                output_writer.write(topic, hits)

            results.clear()
