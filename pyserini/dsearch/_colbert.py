from typing import List
from pyserini.dsearch import DenseSearchResult, QueryEncoder

class ColBertSearcher:
    def __init__(self, index_path: str, query_encoder: QueryEncoder):
        print('ColbertSearcher', index_path, query_encoder)

    def search(self, query: str, k: int = 10) -> List[DenseSearchResult]:
        print('ColBertSearcher query:', query)
        raise NotImplementedError
