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
This module provides Pyserini's dense search interface to FAISS index.
The main entry point is the ``SimpleDenseSearcher`` class.
"""
import os
from dataclasses import dataclass
from typing import Dict, List

import faiss
import numpy as np
import pandas as pd
from transformers import BertModel, BertTokenizer, DPRQuestionEncoder, DPRQuestionEncoderTokenizer

from pyserini.util import (download_encoded_queries, download_prebuilt_index,
                           get_indexes_info)


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


class TCTColBERTQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, encoded_query_dir: str = None, device: str = 'cpu'):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.model = BertModel.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = BertTokenizer.from_pretrained(encoder_dir)
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


class DPRQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, encoded_query_dir: str = None, device: str = 'cpu'):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.model = DPRQuestionEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(encoder_dir)
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


@dataclass
class DenseSearchResult:
    docid: str
    score: float


class SimpleDenseSearcher:
    """Simple Searcher for dense representation

    Parameters
    ----------
    index_dir : str
        Path to faiss index directory.
    """

    def __init__(self, index_dir: str, query_encoder: QueryEncoder):
        self.query_encoder = query_encoder
        self.index, self.docids = self.load_index(index_dir)
        self.dimension = self.index.d
        self.num_docs = self.index.ntotal
        assert self.num_docs == len(self.docids)

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
        SimpleDenseSearcher
            Searcher built from the prebuilt faiss index.
        """
        print(f'Attempting to initialize pre-built index {prebuilt_index_name}.')
        try:
            index_dir = download_prebuilt_index(prebuilt_index_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {prebuilt_index_name}...')
        return cls(index_dir, query_encoder)

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        get_indexes_info()

    def search(self, query: str, k: int = 10, threads: int = 1) -> List[DenseSearchResult]:
        """Search the collection.

        Parameters
        ----------
        query : str
            query text
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use for intra-query search.
        Returns
        -------
        List[DenseSearchResult]
            List of search results.
        """
        emb_q = self.query_encoder.encode(query)
        assert len(emb_q) == self.dimension
        emb_q = emb_q.reshape((1, len(emb_q)))
        faiss.omp_set_num_threads(threads)
        distances, indexes = self.index.search(emb_q, k)
        distances = distances.flat
        indexes = indexes.flat
        return [DenseSearchResult(self.docids[idx], score)
                for score, idx in zip(distances, indexes) if idx != -1]

    def batch_search(self, queries: List[str], q_ids: List[str], k: int = 10, threads: int = 1) \
            -> Dict[str, List[DenseSearchResult]]:
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
        Dict[str, List[DenseSearchResult]]
            Dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        q_embs = np.array([self.query_encoder.encode(q) for q in queries])
        n, m = q_embs.shape
        assert m == self.dimension
        faiss.omp_set_num_threads(threads)
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

    @staticmethod
    def load_docids(docid_path: str) -> List[str]:
        docids = [line.rstrip() for line in open(docid_path, 'r').readlines()]
        return docids
