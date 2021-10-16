import argparse
from typing import List
from pyserini.dsearch import DenseSearchResult, QueryEncoder
from pyserini.encode import ColBertEncoder


class ColBertSearcher:
    def __init__(self, index_path: str, query_encoder: QueryEncoder):
        print('ColbertSearcher', index_path, query_encoder)

    def search(self, query: str, k: int = 10) -> List[DenseSearchResult]:
        print('ColBertSearcher query:', query)
        raise NotImplementedError


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='ColBertSearcher Test.')
    parser.add_argument('--device', type=str, required=False, default='cpu',
        help='device to run query encoder and searcher.')
    parser.add_argument('--query', type=str, required=True,
        help="Test query in string.")
    parser.add_argument('--encoder', type=str, required=True,
        help="Path or name for ColBert query encoder.")
    parser.add_argument('--tokenizer', type=str, required=True,
        help="Path or name for ColBert query tokenizer.")
    parser.add_argument('--index', type=str, required=True,
        help="Path to ColBert index directory.")
    parser.add_argument('--topk', type=int, required=False, default=10,
        help="limit the number of maximum top-k results.")
    args = parser.parse_args()

    encoder = ColBertEncoder(args.encoder, '[Q]',
        device=args.device, tokenizer=args.tokenizer)

    searcher = ColBertSearcher(args.index, encoder)

    results = searcher.search(args.query, k=args.topk)
    print(results)
