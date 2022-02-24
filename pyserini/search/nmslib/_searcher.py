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
import json
import os
from dataclasses import dataclass
from typing import Dict, List

import nmslib
import numpy as np
from scipy.sparse import csr_matrix, vstack


@dataclass
class SearchResult:
    docid: str
    score: float


class NmslibSearcher:
    """Simple Searcher for vector representation
    """

    def __init__(self, index_dir: str, ef_search: int = 1000, is_sparse=False):
        self.is_sparse = is_sparse
        self.index, self.docids, self.token2id, self.metadata = self._load_index(index_dir, self.is_sparse)
        self.index.setQueryTimeParams({'efSearch': ef_search})
        self.dimension = len(self.token2id) if self.is_sparse else None

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
        if self.is_sparse:
            query = self._token_dict_to_sparse_vector(query)
        else:
            query = np.array([query])
        indexes, scores = self.index.knnQueryBatch(query, k=k, num_threads=1)[0]
        return [SearchResult(self.docids[idx], -score)
                for score, idx in zip(scores, indexes) if idx != -1]

    def batch_search(self, queries, q_ids: List[str], k: int = 10, threads: int = 1) \
            -> Dict[str, List[SearchResult]]:
        """

        Parameters
        ----------
        queries : vectors
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
        if self.is_sparse:
            queries = [self._token_dict_to_sparse_vector(query) for query in queries]
            queries = vstack(queries)
        else:
            queries = np.array(queries)
        I, D = zip(*self.index.knnQueryBatch(queries, k=k, num_threads=threads))
        return {key: [SearchResult(self.docids[idx], -score)
                      for score, idx in zip(distances, indexes) if idx != -1]
                for key, distances, indexes in zip(q_ids, D, I)}

    def _load_index(self, index_dir: str, is_sparse: bool):
        if is_sparse:
            index = nmslib.init(method='hnsw', space='negdotprod_sparse', data_type=nmslib.DataType.SPARSE_VECTOR)
        else:
            index = nmslib.init(method='hnsw', space='negdotprod', data_type=nmslib.DataType.DENSE_VECTOR)
        index_path = os.path.join(index_dir, 'index.bin')
        docid_path = os.path.join(index_dir, 'docid')
        tokens_path = os.path.join(index_dir, 'tokens')
        metadata_path = os.path.join(index_dir, 'meta')
        index.loadIndex(index_path, load_data=True)
        docids = self._load_docids(docid_path)
        token2id = self._load_tokens(tokens_path)
        metadata = self._load_metadata(metadata_path)
        return index, docids, token2id, metadata

    def _token_dict_to_sparse_vector(self, token_dict):
        matrix_row, matrix_col, matrix_data = [], [], []
        tokens = token_dict.keys()
        col = []
        data = []
        for tok in tokens:
            if tok in self.token2id:
                col.append(self.token2id[tok])
                data.append(token_dict[tok])
        matrix_row.extend([0] * len(col))
        matrix_col.extend(col)
        matrix_data.extend(data)
        vector = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(1, self.dimension))
        return vector

    @staticmethod
    def _load_docids(docid_path: str) -> List[str]:
        docids = [line.rstrip() for line in open(docid_path, 'r').readlines()]
        return docids

    @staticmethod
    def _load_tokens(tokens_path: str):
        if not os.path.exists(tokens_path):
            return None
        tokens = [line.rstrip() for line in open(tokens_path, 'r').readlines()]
        return dict(zip(tokens, range(len(tokens))))

    @staticmethod
    def _load_metadata(metadata_path):
        if not os.path.exists(metadata_path):
            return None
        meta = json.load(open(metadata_path))
        return meta
