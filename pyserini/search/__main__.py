import re
import argparse
from pyserini.search.pysearch import get_topics, SimpleSearcher
from pyserini.search.reranker import ClassifierType, PseudoRelevanceClassifierReranker


parser = argparse.ArgumentParser(description='Create a input schema')
parser.add_argument('-index', metavar='path', required=True,
                    help='the path to workspace')
parser.add_argument('-topics', metavar='topicsname', required=True,
                    help='topicsname')
parser.add_argument('-output', metavar='path', required=True,
                    help='path to the output file')
parser.add_argument('-rm3',  action='store_true',
                    help='use rm3 ranker')
parser.add_argument('-qld',  action='store_true',
                    help='use qld ranker')
parser.add_argument('-prf',  type=ClassifierType, nargs='+',
                    help='use pseudo relevance feedback ranker')
parser.add_argument('-r',  type=int, default=10,
                    help='number of positive labels in pseudo relevance feedback')
parser.add_argument('-n',  type=int, default=100,
                    help='number of negative labels in pseudo relevance feedback')
parser.add_argument('-alpha',  type=float, default=0.5,
                    help='alpha value for interpolation in pseudo relevance feedback')
args = parser.parse_args()

searcher = SimpleSearcher(args.index)
topics_dic = get_topics(args.topics)
if args.rm3:
    searcher.set_rm3()
if args.qld:
    searcher.set_qld()

if topics_dic == {}:
    print('Topic Not Found')
    exit()

with open(args.output, 'w') as target_file:
    for index, topic in enumerate(sorted(topics_dic.keys())):
        print(f'Topic {topic}: {index + 1}/{len(topics_dic)}')
        search = topics_dic[topic].get('title')
        hits = searcher.search(search, 1000)
        doc_ids = [hit.docid.strip() for hit in hits]
        scores = [hit.score for hit in hits]

        if args.prf and len(args.prf) > 0 and args.alpha > 0 and len(hits) > (args.r + args.n):
            ranker = PseudoRelevanceClassifierReranker(
                args.index, args.prf, r=args.r, n=args.n, alpha=args.alpha)
            scores, doc_ids = ranker.rerank(doc_ids, scores)

        tag = f'{args.prf}-A{args.alpha}' if args.prf else 'Anserini'
        for i, (doc_id, score) in enumerate(zip(doc_ids, scores)):
            target_file.write(
                f'{topic} Q0 {doc_id} {i + 1} {score:.6f} {tag}\n')
