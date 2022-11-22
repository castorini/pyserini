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

import numpy as np
import pandas as pd

from transformers import (AutoModel, AutoTokenizer, BertModel, BertTokenizer, BertTokenizerFast,
                          DPRQuestionEncoder, DPRQuestionEncoderTokenizer, RobertaTokenizer)
from transformers.file_utils import is_faiss_available, requires_backends

from pyserini.util import (download_encoded_queries, download_prebuilt_index,
                           get_dense_indexes_info, get_sparse_index)
from pyserini.search.lucene import LuceneSearcher
from pyserini.index import Document

from ._model import AnceEncoder
import torch

from ...encode import PcaEncoder

if is_faiss_available():
    import faiss


class QueryEncoder:
    def __init__(self, encoded_query_dir: str = None):
        self.has_model = False
        self.has_encoded_query = False
        if encoded_query_dir:
            self.embedding = self._load_embeddings(encoded_query_dir)
            self.has_encoded_query = True

    def encode(self, query: str):
        return self.embedding[query]

    @classmethod
    def load_encoded_queries(cls, encoded_query_name: str):
        """Build a query encoder from a pre-encoded query; download the encoded queries if necessary.

        Parameters
        ----------
        encoded_query_name : str
            pre encoded query name.

        Returns
        -------
        QueryEncoder
            Encoder built from the pre encoded queries.
        """
        print(f'Attempting to initialize pre-encoded queries {encoded_query_name}.')
        try:
            query_dir = download_encoded_queries(encoded_query_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {encoded_query_name}...')
        return cls(encoded_query_dir=query_dir)

    @staticmethod
    def _load_embeddings(encoded_query_dir):
        df = pd.read_pickle(os.path.join(encoded_query_dir, 'embedding.pkl'))
        return dict(zip(df['text'].tolist(), df['embedding'].tolist()))


class TctColBertQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cpu', **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.model = BertModel.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or encoder_dir)
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            max_length = 36  # hardcode for now
            inputs = self.tokenizer(
                '[CLS] [Q] ' + query + '[MASK]' * max_length,
                max_length=max_length,
                truncation=True,
                add_special_tokens=False,
                return_tensors='pt'
            )
            inputs.to(self.device)
            outputs = self.model(**inputs)
            embeddings = outputs.last_hidden_state.detach().cpu().numpy()
            return np.average(embeddings[:, 4:, :], axis=-2).flatten()
        else:
            return super().encode(query)


class DprQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cpu', **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.model = DPRQuestionEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(tokenizer_name or encoder_dir)
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            input_ids = self.tokenizer(query, return_tensors='pt')
            input_ids.to(self.device)
            embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)


class BprQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cpu', **kwargs):
        self.has_model = False
        self.has_encoded_query = False
        if encoded_query_dir:
            self.embedding = self._load_embeddings(encoded_query_dir)
            self.has_encoded_query = True

        if encoder_dir:
            self.device = device
            self.model = DPRQuestionEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(tokenizer_name or encoder_dir)
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            input_ids = self.tokenizer(query, return_tensors='pt')
            input_ids.to(self.device)
            embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu()
            dense_embeddings = embeddings.numpy()
            sparse_embeddings = self.convert_to_binary_code(embeddings).numpy()
            return {'dense': dense_embeddings.flatten(), 'sparse': sparse_embeddings.flatten()}
        else:
            return super().encode(query)

    def convert_to_binary_code(self, input_repr: torch.Tensor):
        return input_repr.new_ones(input_repr.size()).masked_fill_(input_repr < 0, -1.0)

    @staticmethod
    def _load_embeddings(encoded_query_dir):
        df = pd.read_pickle(os.path.join(encoded_query_dir, 'embedding.pkl'))
        ret = {}
        for text, dense, sparse in zip(df['text'].tolist(), df['dense_embedding'].tolist(),
                                       df['sparse_embedding'].tolist()):
            ret[text] = {'dense': dense, 'sparse': sparse}
        return ret


class DkrrDprQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, encoded_query_dir: str = None, device: str = 'cpu',
                 prefix: str = "question:", **kwargs):
        super().__init__(encoded_query_dir)
        self.device = device
        self.model = BertModel.from_pretrained(encoder_dir)
        self.model.to(self.device)
        self.tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
        self.has_model = True
        self.prefix = prefix

    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        model_output = model_output[0].masked_fill(1 - attention_mask[:, :, None], 0.)
        model_output = torch.sum(model_output, dim=1) / torch.clamp(torch.sum(attention_mask, dim=1), min=1e-9)[:, None]
        return model_output.flatten()

    def encode(self, query: str):
        if self.has_model:
            if self.prefix:
                query = f'{self.prefix} {query}'
            inputs = self.tokenizer(query, return_tensors='pt', max_length=40, padding="max_length")
            inputs.to(self.device)
            outputs = self.model(input_ids=inputs["input_ids"],
                                 attention_mask=inputs["attention_mask"])
            embeddings = self._mean_pooling(outputs, inputs['attention_mask']).detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)


class AnceQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cpu', **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.model = AnceEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = RobertaTokenizer.from_pretrained(tokenizer_name or encoder_dir)
            self.has_model = True
            self.tokenizer.do_lower_case = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            inputs = self.tokenizer(
                [query],
                max_length=64,
                padding='longest',
                truncation=True,
                add_special_tokens=True,
                return_tensors='pt'
            )
            inputs.to(self.device)
            embeddings = self.model(inputs["input_ids"]).detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)

    def prf_encode(self, query: str):
        if self.has_model:
            inputs = self.tokenizer(
                [query],
                max_length=512,
                padding='longest',
                truncation=True,
                add_special_tokens=False,
                return_tensors='pt'
            )
            inputs.to(self.device)
            embeddings = self.model(inputs["input_ids"]).detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)

    def prf_batch_encode(self, query: List[str]):
        inputs = self.tokenizer(
            query,
            max_length=512,
            padding='longest',
            truncation=True,
            add_special_tokens=False,
            return_tensors='pt'
        )
        inputs.to(self.device)
        embeddings = self.model(inputs["input_ids"]).detach().cpu().numpy()
        return embeddings


class AutoQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cpu',
                 pooling: str = 'cls', l2_norm: bool = False, **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.model = AutoModel.from_pretrained(encoder_dir)
            self.model.to(self.device)
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or encoder_dir)
            except:
                self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or encoder_dir, use_fast=False)
            self.has_model = True
            self.pooling = pooling
            self.l2_norm = l2_norm
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def encode(self, query: str):
        if self.has_model:
            inputs = self.tokenizer(
                query,
                add_special_tokens=True,
                return_tensors='pt',
                truncation='only_first',
                padding='longest',
                return_token_type_ids=False,
            )

            inputs.to(self.device)
            outputs = self.model(**inputs)
            if self.pooling == "mean":
                embeddings = self._mean_pooling(outputs, inputs['attention_mask']).detach().cpu().numpy()
            else:
                embeddings = outputs[0][:, 0, :].detach().cpu().numpy()
            if self.l2_norm:
                faiss.normalize_L2(embeddings)
            return embeddings.flatten()
        else:
            return super().encode(query)


@dataclass
class DenseSearchResult:
    docid: str
    score: float


@dataclass
class PRFDenseSearchResult:
    docid: str
    score: float
    vectors: [float]


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
        if isinstance(query_encoder, QueryEncoder) or isinstance(query_encoder, PcaEncoder):
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

    def search(self, query: Union[str, np.ndarray], k: int = 10, threads: int = 1, return_vector: bool = False) \
            -> Union[List[DenseSearchResult], Tuple[np.ndarray, List[PRFDenseSearchResult]]]:
        """Search the collection.

        Parameters
        ----------
        query : Union[str, np.ndarray]
            query text or query embeddings
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use for intra-query search.
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
            return emb_q, [PRFDenseSearchResult(self.docids[idx], score, vector)
                           for score, idx, vector in zip(distances, indexes, vectors) if idx != -1]
        else:
            distances, indexes = self.index.search(emb_q, k)
            distances = distances.flat
            indexes = indexes.flat
            return [DenseSearchResult(self.docids[idx], score)
                    for score, idx in zip(distances, indexes) if idx != -1]

    def batch_search(self, queries: Union[List[str], np.ndarray], q_ids: List[str], k: int = 10,
                     threads: int = 1, return_vector: bool = False) \
            -> Union[Dict[str, List[DenseSearchResult]], Tuple[np.ndarray, Dict[str, List[PRFDenseSearchResult]]]]:
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
            return q_embs, {key: [PRFDenseSearchResult(self.docids[idx], score, vector)
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


class BinaryDenseSearcher(FaissSearcher):
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
            indexes = np.array([self.index.id_map.at(int(id_)) for id_ in indexes.reshape(-1)], dtype=np.int)
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
