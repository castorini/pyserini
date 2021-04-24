import argparse
import json
import sys

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')

from pyserini.search import SimpleSearcher


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qrels', type=str, help='qrels file', required=True)
    parser.add_argument('--index', type=str, help='index location', required=True)
    args = parser.parse_args()

    searcher = SimpleSearcher(args.index)
    with open(args.qrels, 'r') as reader:
        for line in reader.readlines():
            arr = line.split('\t')
            doc = json.loads(searcher.doc(arr[2]).raw())['contents']
            print(f'{arr[2]}\t{doc}')
