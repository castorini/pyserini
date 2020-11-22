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
from pyserini.search import get_topics, SimpleSearcher
from pyserini.search.reranker import ClassifierType, PseudoRelevanceClassifierReranker
from tqdm import tqdm

parser = argparse.ArgumentParser(description='Search a Lucene index.')
parser.add_argument('--index', type=str, metavar='path to index or index name', required=True, help="Path to Lucene index or prebuilt index's name.")
parser.add_argument('--topics', type=str, metavar='topic_name', required=True,
                    help="Name of topics. Available: robust04, robust05, core17, core18.")
parser.add_argument('--msmarco',  action='store_true', default=False, help="Output in MS MARCO format.")
parser.add_argument('--output', type=str, metavar='path', help="Path to output file.")
parser.add_argument('--bm25',  action='store_true', default=True, help="Use BM25 (default).")
parser.add_argument('--rm3',  action='store_true', help="Use RM3")
parser.add_argument('--qld',  action='store_true', help="Use QLD")
parser.add_argument('--prcl',  type=ClassifierType, nargs='+', default=[],
                    help='Specify the classifier PseudoRelevanceClassifierReranker uses.')
parser.add_argument('--prcl.vectorizer',  dest='vectorizer', type=str,
                    help='Type of vectorizer. Available: TfidfVectorizer, BM25Vectorizer.')
parser.add_argument('--prcl.r',  dest='r', type=int, default=10,
                    help='Number of positive labels in pseudo relevance feedback.')
parser.add_argument('--prcl.n', dest='n', type=int, default=100,
                    help='Number of negative labels in pseudo relevance feedback.')
parser.add_argument('--prcl.alpha', dest='alpha', type=float, default=0.5,
                    help='Alpha value for interpolation in pseudo relevance feedback.')
args = parser.parse_args()

topics = get_topics(args.topics)

if os.path.exists(args.index):
    # create searcher from index directory
    searcher = SimpleSearcher(args.index)
else:
    # create searcher from prebuilt index name
    searcher = SimpleSearcher.from_prebuilt_index(args.index)
if searcher == None:
    exit()

search_rankers = []

if args.qld:
    search_rankers.append('qld')
    searcher.set_qld()
else:
    search_rankers.append('bm25')
    if args.msmarco:
        # setting k1=0.82 and b=0.68 for ms-marco passage
        # tuned parameters from grid search of parameter values
        # link to BM25 tuning: https://github.com/castorini/anserini/blob/master/docs/experiments-msmarco-passage.md#bm25-tuning
        searcher.set_bm25(0.82, 0.68)

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

with open(output_path, 'w') as target_file:
    for index, topic in enumerate(tqdm(sorted(topics.keys()))):
        search = topics[topic].get('title')
        hits = searcher.search(search, 1000)
        doc_ids = [hit.docid.strip() for hit in hits]
        scores = [hit.score for hit in hits]

        if use_prcl and len(hits) > (args.r + args.n):
            scores, doc_ids = ranker.rerank(doc_ids, scores)

        if args.msmarco:
            for i, doc_id in enumerate(doc_ids):
                target_file.write('{}\t{}\t{}\n'.format(topic, doc_id, i + 1))
        else:
            tag = output_path[:-4] if args.output is None else 'Anserini'
            for i, (doc_id, score) in enumerate(zip(doc_ids, scores)):
                target_file.write(f'{topic} Q0 {doc_id} {i + 1} {score:.6f} {tag}\n')
