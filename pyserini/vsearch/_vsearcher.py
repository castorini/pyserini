import os
from dataclasses import dataclass
from typing import Dict, List

import nmslib


@dataclass
class SearchResult:
    docid: str
    score: float


class SimpleVectorSearcher:
    """Simple Searcher for vector representation
    """

    def __init__(self, index_dir: str, ef_search: int = 1000, is_sparse=False):
        self.is_sparse = is_sparse
        self.index, self.docids = self._load_index(index_dir, self.is_sparse)
        self.index.setQueryTimeParams({'efSearch': ef_search})

    def search(self, query, k: int = 10) -> List[SearchResult]:
        """Search the collection.

        Parameters
        ----------
        query : query vector
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use for intra-query search.
        Returns
        -------
        List[SearchResult]
            List of search results.
        """
        indexes, scores = self.index.knnQueryBatch(query, k=k, num_threads=1)[0]
        return [SearchResult(self.docids[idx], -score)
                for score, idx in zip(scores, indexes) if idx != -1]

    def batch_search(self, queries, q_ids: List[str], k: int = 10, threads: int = 1) \
            -> Dict[str, List[SearchResult]]:
        """

        Parameters
        ----------
        queries : List[str]
            List of query texts
        q_ids : List[str]
            List of corresponding query ids.
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use.

        Returns
        -------
        Dict[str, List[SearchResult]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        I, D = zip(*self.index.knnQueryBatch(queries, k=k, num_threads=threads))
        return {key: [SearchResult(self.docids[idx], -score)
                      for score, idx in zip(distances, indexes) if idx != -1]
                for key, distances, indexes in zip(q_ids, D, I)}

    def _load_index(self, index_dir: str, is_sparse: bool):
        print(is_sparse)
        if is_sparse:
            index = nmslib.init(method='hnsw', space='negdotprod_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
            print("AAA")
        else:
            index = nmslib.init(method='hnsw', space='negdotprod', data_type=nmslib.DataType.DENSE_VECTOR)
        index_path = os.path.join(index_dir, 'sparse_index.bin')
        docid_path = os.path.join(index_dir, 'docid')
        index.loadIndex(index_path, load_data=True)
        docids = self._load_docids(docid_path)
        return index, docids

    @staticmethod
    def _load_docids(docid_path: str) -> List[str]:
        docids = [line.rstrip() for line in open(docid_path, 'r').readlines()]
        return docids
