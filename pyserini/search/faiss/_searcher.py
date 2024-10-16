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
This module provides Pyserini's dense search interface to FAISS index.
The main entry point is the ``FaissSearcher`` class.
"""

import os
from dataclasses import dataclass
from typing import Dict, List, Union, Optional, Tuple

import faiss
import numpy as np
from transformers.file_utils import requires_backends

from pyserini.encode import QueryEncoder, AutoQueryEncoder
from pyserini.encode import AnceQueryEncoder, BprQueryEncoder, DprQueryEncoder, TctColBertQueryEncoder
from pyserini.index import Document
from pyserini.search.lucene import LuceneSearcher
from pyserini.util import download_prebuilt_index, get_dense_indexes_info, get_sparse_index
from ._prf import PrfDenseSearchResult


@dataclass
class DenseSearchResult:
    docid: str
    score: float


class FaissSearcher:
    """Simple Searcher for dense representation

    Parameters
    ----------
    index_dir : str
        Path to faiss index directory.
    """

    def __init__(self, index_dir: str, query_encoder: Union[QueryEncoder, str],
                 prebuilt_index_name: Optional[str] = None):
        requires_backends(self, "faiss")
        if not isinstance(query_encoder, str):
            self.query_encoder = query_encoder
        else:
            self.query_encoder = self._init_encoder_from_str(query_encoder)
        self.index, self.docids = self.load_index(index_dir)
        self.dimension = self.index.d
        self.num_docs = self.index.ntotal

        assert self.docids is None or self.num_docs == len(self.docids)
        if prebuilt_index_name:
            sparse_index = get_sparse_index(prebuilt_index_name)
            self.ssearcher = LuceneSearcher.from_prebuilt_index(sparse_index)

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str, query_encoder: QueryEncoder):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        query_encoder: QueryEncoder
            the query encoder, which has `encode` method that convert query text to embedding
        prebuilt_index_name : str
            Prebuilt index name.

        Returns
        -------
        FaissSearcher
            Searcher built from the prebuilt faiss index.
        """
        print(f'Attempting to initialize pre-built index {prebuilt_index_name}.')
        # see integrations/papers/test_sigir2021.py - preserve working commands published in papers
        if prebuilt_index_name == 'msmarco-passage-tct_colbert-hnsw':
            prebuilt_index_name = 'msmarco-v1-passage.tct_colbert.hnsw'
        # see integrations/papers/test_ecir2023.py - preserve working commands published in papers
        elif prebuilt_index_name == 'wikipedia-dpr-dkrr-nq':
            prebuilt_index_name = 'wikipedia-dpr-100w.dkrr-nq'

        try:
            index_dir = download_prebuilt_index(prebuilt_index_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {prebuilt_index_name}...')
        return cls(index_dir, query_encoder, prebuilt_index_name)

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        get_dense_indexes_info()

    def search(self, query: Union[str, np.ndarray], k: int = 10, threads: int = 1, remove_dups: bool = False, return_vector: bool = False) \
            -> Union[List[DenseSearchResult], Tuple[np.ndarray, List[PrfDenseSearchResult]]]:
        """Search the collection.

        Parameters
        ----------
        query : Union[str, np.ndarray]
            query text or query embeddings
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use for intra-query search.
        remove_dups : bool
            Remove duplicate docids when writing final run output.    
        return_vector : bool
            Return the results with vectors
        Returns
        -------
        Union[List[DenseSearchResult], Tuple[np.ndarray, List[PRFDenseSearchResult]]]
            Either returns a list of search results.
            Or returns the query vector with the list of PRF dense search results with vectors.
        """
        if isinstance(query, str):
            emb_q = self.query_encoder.encode(query)
            assert len(emb_q) == self.dimension
            emb_q = emb_q.reshape((1, len(emb_q)))
        else:
            emb_q = query
        faiss.omp_set_num_threads(threads)
        if return_vector:
            distances, indexes, vectors = self.index.search_and_reconstruct(emb_q, k)
            vectors = vectors[0]
            distances = distances.flat
            indexes = indexes.flat
            return emb_q, [PrfDenseSearchResult(self.docids[idx], score, vector)
                           for score, idx, vector in zip(distances, indexes, vectors) if idx != -1]
        else:
            distances, indexes = self.index.search(emb_q, k)
            distances = distances.flat
            indexes = indexes.flat
            if remove_dups:
                unique_docs = set()
                results = list()
                for score, idx in zip(distances, indexes):
                    if idx not in unique_docs:
                        unique_docs.add(idx)
                        results.append(DenseSearchResult(self.docids[idx],score))
                return results
            return [DenseSearchResult(self.docids[idx], score)
                    for score, idx in zip(distances, indexes) if idx != -1]

    def batch_search(self, queries: Union[List[str], np.ndarray], q_ids: List[str], k: int = 10,
                     threads: int = 1, return_vector: bool = False) \
            -> Union[Dict[str, List[DenseSearchResult]], Tuple[np.ndarray, Dict[str, List[PrfDenseSearchResult]]]]:
        """

        Parameters
        ----------
        queries : Union[List[str], np.ndarray]
            List of query texts or list of query embeddings
        q_ids : List[str]
            List of corresponding query ids.
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use.
        return_vector : bool
            Return the results with vectors

        Returns
        -------
        Union[Dict[str, List[DenseSearchResult]], Tuple[np.ndarray, Dict[str, List[PRFDenseSearchResult]]]]
            Either returns a dictionary holding the search results, with the query ids as keys and the
            corresponding lists of search results as the values.
            Or returns a tuple with ndarray of query vectors and a dictionary of PRF Dense Search Results with vectors
        """
        if isinstance(queries, np.ndarray):
            q_embs = queries
        else:
            q_embs = np.array([self.query_encoder.encode(q) for q in queries])
            n, m = q_embs.shape
            assert m == self.dimension
        faiss.omp_set_num_threads(threads)
        if return_vector:
            D, I, V = self.index.search_and_reconstruct(q_embs, k)
            return q_embs, {key: [PrfDenseSearchResult(self.docids[idx], score, vector)
                                  for score, idx, vector in zip(distances, indexes, vectors) if idx != -1]
                            for key, distances, indexes, vectors in zip(q_ids, D, I, V)}
        else:
            D, I = self.index.search(q_embs, k)
            return {key: [DenseSearchResult(self.docids[idx], score)
                          for score, idx in zip(distances, indexes) if idx != -1]
                    for key, distances, indexes in zip(q_ids, D, I)}

    def load_index(self, index_dir: str):
        index_path = os.path.join(index_dir, 'index')
        docid_path = os.path.join(index_dir, 'docid')
        index = faiss.read_index(index_path)
        docids = self.load_docids(docid_path)
        return index, docids

    def doc(self, docid: Union[str, int]) -> Optional[Document]:
        """Return the :class:`Document` corresponding to ``docid``. Since dense indexes don't store documents
        but sparse indexes do, route over to corresponding sparse index (according to prebuilt_index_info.py)
        and use its doc API 

        Parameters
        ----------
        docid : Union[str, int]
            Overloaded ``docid``: either an external collection ``docid`` (``str``) or an internal Lucene ``docid``
            (``int``).

        Returns
        -------
        Document
            :class:`Document` corresponding to the ``docid``.
        """
        return self.ssearcher.doc(docid) if self.ssearcher else None

    @staticmethod
    def _init_encoder_from_str(encoder):
        encoder_lower = encoder.lower()
        if 'dpr' in encoder_lower:
            return DprQueryEncoder(encoder_dir=encoder)
        elif 'tct_colbert' in encoder_lower:
            return TctColBertQueryEncoder(encoder_dir=encoder)
        elif 'ance' in encoder_lower:
            return AnceQueryEncoder(encoder_dir=encoder)
        elif 'sentence' in encoder_lower:
            return AutoQueryEncoder(encoder_dir=encoder, pooling='mean', l2_norm=True)
        else:
            return AutoQueryEncoder(encoder_dir=encoder)

    @staticmethod
    def load_docids(docid_path: str) -> List[str]:
        id_f = open(docid_path, 'r')
        docids = [line.rstrip() for line in id_f.readlines()]
        id_f.close()
        return docids
    
    def set_hnsw_ef_search(self, ef_search: int):
        self.index.hnsw.efSearch = ef_search


class BinaryDenseFaissSearcher(FaissSearcher):
    """Simple Searcher for binary-dense representation

    Parameters
    ----------
    index_dir : str
        Path to faiss index directory.
    """

    def __init__(self, index_dir: str, query_encoder: Union[QueryEncoder, str],
                 prebuilt_index_name: Optional[str] = None):
        super().__init__(index_dir, query_encoder, prebuilt_index_name)

    def search(self, query: str, k: int = 10, binary_k: int = 100, rerank: bool = True, threads: int = 1) \
            -> List[DenseSearchResult]:
        """Search the collection.

        Parameters
        ----------
        query : str
            query text
        k : int
            Number of hits to return at second stage.
        binary_k : int
            Number of hits to return at first stage.
        rerank: bool
            Whether to use dense repr to rerank the binary ranking results.
        threads : int
            Maximum number of threads to use for intra-query search.
        Returns
        -------
        List[DenseSearchResult]
            List of search results.
        """
        ret = self.query_encoder.encode(query)
        dense_emb_q = ret['dense']
        sparse_emb_q = ret['sparse']
        assert len(dense_emb_q) == self.dimension
        assert len(sparse_emb_q) == self.dimension

        dense_emb_q = dense_emb_q.reshape((1, len(dense_emb_q)))
        sparse_emb_q = sparse_emb_q.reshape((1, len(sparse_emb_q)))
        faiss.omp_set_num_threads(threads)
        distances, indexes = self.binary_dense_search(k, binary_k, rerank, dense_emb_q, sparse_emb_q)
        distances = distances.flat
        indexes = indexes.flat
        return [DenseSearchResult(str(idx), score)
                for score, idx in zip(distances, indexes) if idx != -1]

    def batch_search(self, queries: List[str], q_ids: List[str], k: int = 10, binary_k: int = 100,
                     rerank: bool = True, threads: int = 1) -> Dict[str, List[DenseSearchResult]]:
        """

        Parameters
        ----------
        queries : List[str]
            List of query texts
        q_ids : List[str]
            List of corresponding query ids.
        k : int
            Number of hits to return.
        binary_k : int
            Number of hits to return at first stage.
        rerank: bool
            Whether to use dense repr to rerank the binary ranking results.
        threads : int
            Maximum number of threads to use.

        Returns
        -------
        Dict[str, List[DenseSearchResult]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        dense_q_embs = []
        sparse_q_embs = []
        for q in queries:
            ret = self.query_encoder.encode(q)
            dense_q_embs.append(ret['dense'])
            sparse_q_embs.append(ret['sparse'])
        dense_q_embs = np.array(dense_q_embs)
        sparse_q_embs = np.array(sparse_q_embs)
        n, m = dense_q_embs.shape
        assert m == self.dimension
        faiss.omp_set_num_threads(threads)
        D, I = self.binary_dense_search(k, binary_k, rerank, dense_q_embs, sparse_q_embs)
        return {key: [DenseSearchResult(str(idx), score)
                      for score, idx in zip(distances, indexes) if idx != -1]
                for key, distances, indexes in zip(q_ids, D, I)}

    def binary_dense_search(self, k, binary_k, rerank, dense_emb_q, sparse_emb_q):
        num_queries = dense_emb_q.shape[0]
        sparse_emb_q = np.packbits(np.where(sparse_emb_q > 0, 1, 0)).reshape(num_queries, -1)

        if not rerank:
            distances, indexes = self.index.search(sparse_emb_q, k)
        else:
            raw_index = self.index.index
            _, indexes = raw_index.search(sparse_emb_q, binary_k)
            sparse_emb_p = np.vstack(
                [np.unpackbits(raw_index.reconstruct(int(id_))) for id_ in indexes.reshape(-1)]
            )
            sparse_emb_p = sparse_emb_p.reshape(
                dense_emb_q.shape[0], binary_k, dense_emb_q.shape[1]
            )
            sparse_emb_p = sparse_emb_p.astype(np.float32)
            sparse_emb_p = sparse_emb_p * 2 - 1
            distances = np.einsum("ijk,ik->ij", sparse_emb_p, dense_emb_q)
            sorted_indices = np.argsort(-distances, axis=1)

            indexes = indexes[np.arange(num_queries)[:, None], sorted_indices]
            indexes = np.array([self.index.id_map.at(int(id_)) for id_ in indexes.reshape(-1)], dtype=np.int32)
            indexes = indexes.reshape(num_queries, -1)[:, :k]
            distances = distances[np.arange(num_queries)[:, None], sorted_indices][:, :k]
        return distances, indexes

    def load_index(self, index_dir: str):
        index_path = os.path.join(index_dir, 'index')
        index = faiss.read_index_binary(index_path)
        return index, None

    @staticmethod
    def _init_encoder_from_str(encoder):
        encoder = encoder.lower()
        if 'bpr' in encoder:
            return BprQueryEncoder(encoder_dir=encoder)
        else:
            raise NotImplementedError
