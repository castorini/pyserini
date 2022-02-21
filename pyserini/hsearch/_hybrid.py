#
# Pyserini: Reproducible IR research with sparse and dense representations
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
from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher, DenseSearchResult


class HybridSearcher:
    """Hybrid Searcher for dense + sparse

        Parameters
        ----------
        dense_searcher : FaissSearcher
        sparse_searcher : LuceneSearcher
    """

    def __init__(self, dense_searcher, sparse_searcher):
        self.dense_searcher = dense_searcher
        self.sparse_searcher = sparse_searcher

    def search(self, query: str, k0: int = 10, k: int = 10, alpha: float = 0.1, normalization: bool = False, weight_on_dense: bool = False) -> List[DenseSearchResult]:
        dense_hits = self.dense_searcher.search(query, k0)
        sparse_hits = self.sparse_searcher.search(query, k0)
        return self._hybrid_results(dense_hits, sparse_hits, alpha, k, normalization, weight_on_dense)

    def batch_search(self, queries: List[str], q_ids: List[str], k0: int = 10, k: int = 10, threads: int = 1,
            alpha: float = 0.1, normalization: bool = False, weight_on_dense: bool = False) \
            -> Dict[str, List[DenseSearchResult]]:
        dense_result = self.dense_searcher.batch_search(queries, q_ids, k0, threads)
        sparse_result = self.sparse_searcher.batch_search(queries, q_ids, k0, threads)
        hybrid_result = {
            key: self._hybrid_results(dense_result[key], sparse_result[key], alpha, k, normalization, weight_on_dense)
            for key in dense_result
        }
        return hybrid_result

    @staticmethod
    def _hybrid_results(dense_results, sparse_results, alpha, k, normalization=False, weight_on_dense=False):
        dense_hits = {hit.docid: hit.score for hit in dense_results}
        sparse_hits = {hit.docid: hit.score for hit in sparse_results}
        hybrid_result = []
        min_dense_score = min(dense_hits.values()) if len(dense_hits) > 0 else 0
        max_dense_score = max(dense_hits.values()) if len(dense_hits) > 0 else 1
        min_sparse_score = min(sparse_hits.values()) if len(sparse_hits) > 0 else 0
        max_sparse_score = max(sparse_hits.values()) if len(sparse_hits) > 0 else 1
        for doc in set(dense_hits.keys()) | set(sparse_hits.keys()):
            if doc not in dense_hits:
                sparse_score = sparse_hits[doc]
                dense_score = min_dense_score
            elif doc not in sparse_hits:
                sparse_score = min_sparse_score
                dense_score = dense_hits[doc]
            else:
                sparse_score = sparse_hits[doc]
                dense_score = dense_hits[doc]
            if normalization:
                sparse_score = (sparse_score - (min_sparse_score + max_sparse_score) / 2) \
                               / (max_sparse_score - min_sparse_score)
                dense_score = (dense_score - (min_dense_score + max_dense_score) / 2) \
                              / (max_dense_score - min_dense_score)
            score = alpha * sparse_score + dense_score if not weight_on_dense else sparse_score + alpha * dense_score
            hybrid_result.append(DenseSearchResult(doc, score))
        return sorted(hybrid_result, key=lambda x: x.score, reverse=True)[:k]
