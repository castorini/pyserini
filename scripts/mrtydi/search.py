import logging
from argparse import ArgumentParser

from transformers import AutoTokenizer

from pyserini.search import SimpleSearcher
from pyserini.analysis import JWhiteSpaceAnalyzer


# logger = logging.getLogger(__name__)
logger = logging.getLogger(os.path.basename(__file__))
logger.setLevel(logging.INFO)


def main(args):
    query = args.query
    index = args.index
    if args.do_tokenize:
        tokenizer = AutoTokenizer.from_pretrained('bert-multilingual-base-uncased')
        query = " ".join(tokenizer.tokenize(query))

    logger.info(f'searching for: {query}')
    searcher = SimpleSearcher(index)
    searcher.set_analyzer(JWhiteSpaceAnalyzer())
    hits = searcher.search(query, 1000)

    for i in range(len(hits)):
        doc = hits[i]
        print(f'{i+1:2} {hits[i].docid:4} {hits[i].score:.5f}')


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--query', '-q', type=str, required=True, help="The query to search in the index")
    parser.add_argument('--index', '-i', type=str, required=True, help="Path to the anserini index directory")
    parser.add_argument('--do-tokenize', '-t', action='store_false', help="Whether to perform mbert tokenization on the query")
    
    args = parser.parse_args()
    main(args)
