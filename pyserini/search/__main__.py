import re
import argparse

from pyserini.search.pysearch import get_topics,SimpleSearcher

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create a input schema')
    parser.add_argument('-index', metavar='path', required=True,
                        help='the path to workspace')
    parser.add_argument('-topics', metavar='path', required=True,
                        help='path to topics')
    parser.add_argument('-output', metavar='path', required=True,
                        help='path to the output file')
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
        with open(args.topics, 'r') as content_file:
            content = content_file.read()
        topics_lst = re.findall(r'(?<=<top>)(.+?)(?=<desc>)', content, flags=re.S)
        topics_lst = [i.strip() for i in topics_lst]
        target_file = open(args.output, 'w')
        for topic in topics_lst:
            number_search = topic.split("<title>")
            number = number_search[0].strip().split(" ")[-1]
            search = number_search[1].strip()
            hits = searcher.search(search, 1000)
            for i in range(0, len(hits)):
                target_file.write(f'{number} Q0 {hits[i].docid.strip()} {i + 1} {hits[i].score:.6f} Anserini\n')
        target_file.close()