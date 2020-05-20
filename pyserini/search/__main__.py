import re
import argparse

from pyserini.search.pysearch import get_topics,SimpleSearcher

parser = argparse.ArgumentParser(description='Create a input schema')
parser.add_argument('-index', metavar='path', required=True,
                        help='the path to workspace')
parser.add_argument('-topics', metavar='topicsname', required=True,
                        help='topicsname')
parser.add_argument('-output', metavar='path', required=True,
                        help='path to the output file')
parser.add_argument('-rm3',  action='store_true',
                        help='take rm3 ranker')
parser.add_argument('-qld',  action='store_true',
                        help='take qld ranker')
args = parser.parse_args()
searcher = SimpleSearcher(args.index)
topics_dic = get_topics(args.topics)
if topics_dic != {}:
    target_file = open(args.output, 'w')
    for key, value in sorted(topics_dic.items()):
        search = value.get('title')
        hits = searcher.search(search, 1000)
        for i in range(0, len(hits)):
            target_file.write(f'{key} Q0 {hits[i].docid.strip()} {i + 1} {hits[i].score:.6f} Anserini\n')
    target_file.close()
else:
   print('Topic Not Found')