# -*- coding: utf-8 -*-
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

import argparse
import re
from tqdm import tqdm
from pyserini.search.pysearch import get_topics, SimpleSearcher
from pyserini.search.reranker import ClassifierType, PseudoRelevanceClassifierReranker

parser = argparse.ArgumentParser(description='Create a input schema')
parser.add_argument('-index', type=str, metavar='path to index',
                    required=True, help='the path to lucene index')
parser.add_argument('-topics', type=str, metavar='topic_name', required=True,
                    help='topics name e.g. robust04, robust05, core17 & core18')
parser.add_argument('-output', type=str, metavar='path',
                    help='path to the output file')
parser.add_argument('-bm25',  action='store_true', default=True,
                    help='use bm25 ranker by default')
parser.add_argument('-rm3',  action='store_true', help='use rm3 ranker')
parser.add_argument('-qld',  action='store_true', help='use qld ranker')
parser.add_argument('-prcl',  type=ClassifierType, nargs='+', default=[],
                    help='specify the classifier PseudoRelevanceClassifierReranker uses')
parser.add_argument('-prcl.r',  dest='r', type=int, default=10,
                    help='number of positive labels in pseudo relevance feedback')
parser.add_argument('-prcl.n', dest='n', type=int, default=100,
                    help='number of negative labels in pseudo relevance feedback')
parser.add_argument('-prcl.alpha', dest='alpha', type=float, default=0.5,
                    help='alpha value for interpolation in pseudo relevance feedback')
args = parser.parse_args()

searcher = SimpleSearcher(args.index)
topics = get_topics(args.topics)
search_rankers = ['bm25']
if args.rm3:
    search_rankers.append('rm3')
    searcher.set_rm3()
if args.qld:
    search_rankers.append('qld')
    searcher.set_qld()

# invalid topics name
if topics == {}:
    print(f'Topic {args.topics} Not Found')
    exit()

# get re-ranker
use_prcl = args.prcl and len(args.prcl) > 0 and args.alpha > 0
if use_prcl is True:
    ranker = PseudoRelevanceClassifierReranker(
        args.index, args.prcl, r=args.r, n=args.n, alpha=args.alpha)

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

        tokens = [args.topics, '+'.join(clf_rankers), f'A{args.alpha}', '+'.join(search_rankers)]
        output_path = '_'.join(tokens) + ".txt"
    else:
        tokens = [args.topics, '+'.join(search_rankers)]
        output_path = '_'.join(tokens) + ".txt"

print('Output ->', output_path)

with open(output_path, 'w') as target_file:
    for index, topic in enumerate(tqdm(sorted(topics.keys()))):
        search = topics[topic].get('title')
        hits = searcher.search(search, 1000)
        doc_ids = [hit.docid.strip() for hit in hits]
        scores = [hit.score for hit in hits]

        if use_prcl and len(hits) > (args.r + args.n):
            scores, doc_ids = ranker.rerank(doc_ids, scores)

        tag = output_path[:-4] if args.output is None else 'Anserini'
        for i, (doc_id, score) in enumerate(zip(doc_ids, scores)):
            target_file.write(f'{topic} Q0 {doc_id} {i + 1} {score:.6f} {tag}\n')
