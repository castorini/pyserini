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
import tensorflow.compat.v1 as tf
from tqdm import tqdm

from pyserini.util import download_prebuilt_index, download_encoded_queries, get_indexes_info


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

    def __init__(self, index_dir: str):
        self.index, self.docids = self.load_index(index_dir)
        self.dimension = self.index.d
        self.num_docs = self.index.ntotal
        assert self.num_docs == len(self.docids)

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
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
        return cls(index_dir)

    @staticmethod
    def list_prebuilt_indexes():
        """Display information about available prebuilt indexes."""
        get_indexes_info()

    def search(self, emb_q: np.array, k: int = 10, threads: int = 1) -> List[DenseSearchResult]:
        """Search the collection.

        Parameters
        ----------
        emb_q : np.array
            query embedding
        k : int
            Number of hits to return.
        threads : int
            Maximum number of threads to use for intra-query search.
        Returns
        -------
        List[DenseSearchResult]
            List of search results.
        """
        assert len(emb_q) == self.dimension
        emb_q = emb_q.reshape((1, len(emb_q)))
        faiss.omp_set_num_threads(threads)
        distances, indexes = self.index.search(emb_q, k)
        distances = distances.flat
        indexes = indexes.flat
        return [DenseSearchResult(self.docids[idx], score)
                for score, idx in zip(distances, indexes) if idx != -1]

    def batch_search(self, q_embs: np.array, q_ids: List[str], k: int = 10, threads: int = 1)\
            -> Dict[str, List[DenseSearchResult]]:
        """

        Parameters
        ----------
        q_embs : np.array
            np.array of query embeddings
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


class QueryEncoder:
    def __init__(self, encoder_dir: str):
        self.embedding, self.text2idx = self.load_encoder(encoder_dir)

    def encode(self, query: str):
        return self.embedding[self.text2idx[query]]

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
        return cls(query_dir)

    def load_encoder(self, encoder_dir: str):
        q_path = os.path.join(encoder_dir, 'queries')
        emb_path = os.path.join(encoder_dir, 'query_embs')
        return self.load_embedding_from_tfds(emb_path), self.load_queries(q_path)

    @staticmethod
    def load_queries(queries_path: str):
        text2idx = {}
        with open(queries_path, 'r') as f:
            for idx, line in tqdm(enumerate(f)):
                qid, text = line.rstrip().split('\t')
                text = text.strip()
                text2idx[text] = idx
        return text2idx

    @staticmethod
    def load_embedding_from_tfds(srcfile):

        def _parse_function(example_proto):
            features = {'doc_emb': tf.FixedLenFeature([], tf.string),
                        'docid': tf.FixedLenFeature([], tf.int64)}
            parsed_features = tf.parse_single_example(example_proto, features)
            corpus = tf.decode_raw(parsed_features['doc_emb'], tf.float32)
            doc_id = tf.cast(parsed_features['docid'], tf.int32)
            return corpus, doc_id

        with tf.Session() as sess:
            docids = []
            corpus_embs = []

            dataset = tf.data.TFRecordDataset(srcfile)
            dataset = dataset.map(_parse_function)
            iterator = dataset.make_one_shot_iterator()
            next_data = iterator.get_next()
            while True:
                try:
                    corpus_emb, docid = sess.run(next_data)
                    corpus_embs.append(np.array(corpus_emb).astype(np.float32))
                    docids.append(str(docid))
                except tf.errors.OutOfRangeError:
                    break
        return np.array(corpus_embs).astype(np.float32)
