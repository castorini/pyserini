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
"""
This module provides Pyserini's hybrid searcher by Dense + Sparse
"""
from typing import List, Dict
from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher, QueryEncoder, DenseSearchResult

import numpy as np


class HybridSearcher:
    """Hybrid Searcher for dense + sparse

        Parameters
        ----------
        dense_searcher : SimpleDenseSearcher
        query_encoder : QueryEncoder
        sparse_searcher : SimpleSearcher
    """

    def __init__(self, dense_searcher, query_encoder, sparse_searcher):
        self.dense_searcher = dense_searcher
        self.query_encoder = query_encoder
        self.sparse_searcher = sparse_searcher

    def search(self, query: str, k: int = 10, alpha: float = 0.1) -> List[DenseSearchResult]:
        query_emb = self.query_encoder.encode(query)
        dense_hits = self.dense_searcher.search(query_emb, k)
        sparse_hits = self.sparse_searcher.search(query, k)
        return self._hybrid_results(dense_hits, sparse_hits, alpha)

    def batch_search(self, queries: List[str], q_ids: List[str], k: int = 10, threads: int = 1, alpha: float = 0.1) \
            -> Dict[str, List[DenseSearchResult]]:
        query_embs = np.array([self.query_encoder.encode(query) for query in queries])
        dense_result = self.dense_searcher.batch_search(query_embs, q_ids, k, threads)
        sparse_result = self.sparse_searcher.batch_search(queries, q_ids, k, threads)
        hybrid_result = {
            key: self._hybrid_results(dense_result[key], sparse_result[key], alpha)
            for key in dense_result
        }
        return hybrid_result

    @staticmethod
    def _hybrid_results(dense_results, sparse_results, alpha):
        dense_hits = {hit.docid: hit.score for hit in dense_results}
        sparse_hits = {hit.docid: hit.score for hit in sparse_results}
        hybrid_result = []
        for doc in set(dense_hits.keys()) | set(sparse_hits.keys()):
            if doc not in dense_hits:
                score = alpha * sparse_hits[doc] + min(dense_hits.values())
            elif doc not in sparse_hits:
                score = alpha * min(sparse_hits.values()) + dense_hits[doc]
            else:
                score = alpha * sparse_hits[doc] + dense_hits[doc]
            hybrid_result.append(DenseSearchResult(doc, score))
        return sorted(hybrid_result, key=lambda x: x.score, reverse=True)
