# -*- coding: utf-8 -*-
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

import math
import numpy as np
from typing import List
from scipy.sparse import csr_matrix
from pyserini.search import pysearch
from pyserini.index import pyutils


class VectorizerBase:
    """Base class for vectorizer implemented on top of Pyserini.

    Parameters
    ----------
    lucene_index_path : str
        Path to lucene index folder
    min_df : int
        Minimum acceptable document frequency
    verbose : bool
        Whether to print out debugging information
    """

    def __init__(self, lucene_index_path: str, min_df: int = 1, verbose: bool = False) -> None:
        self.min_df: int = min_df
        self.verbose: bool = verbose
        self.index_utils = pyutils.IndexReaderUtils(lucene_index_path)
        self.searcher = pysearch.SimpleSearcher(lucene_index_path)
        self.num_docs: int = self.searcher.num_docs

        # build vocabulary
        self.vocabulary_ = set()
        self.idf_ = {}
        for term in self.index_utils.terms():
            self.idf_[term.term] = math.log(self.num_docs / term.df)
            if term.df > self.min_df:
                self.vocabulary_.add(term.term)

        # build term to index mapping
        self.term_to_index = {}
        for index, term in enumerate(self.vocabulary_):
            self.term_to_index[term] = index
        self.vocabulary_size = len(self.vocabulary_)

        if self.verbose:
            print(f'Found {self.vocabulary_size} terms')

    def _l2normalize(self, a):
        norm_rows = np.sqrt(np.add.reduceat(a.data * a.data, a.indptr[:-1]))
        nnz_per_row = np.diff(a.indptr)
        a.data /= np.repeat(norm_rows, nnz_per_row)
        return a


class TfidfVectorizer(VectorizerBase):
    """Wrapper class for tf-idf vectorizer implemented on top of Pyserini.

    Parameters
    ----------
    lucene_index_path : str
        Path to lucene index folder
    min_df : int
        Minimum acceptable document frequency
    verbose : bool
        Whether to print out debugging information
    """

    def __init__(self, lucene_index_path: str, min_df: int = 1, verbose: bool = False) -> None:
        super().__init__(lucene_index_path, verbose, min_df)

    def get_vectors(self, doc_ids: List[str]):
        """Get the tf-idf vectors given a list of doc_ids

        Parameters
        ----------
        doc_ids : List[str]
            The piece of text to analyze.

        Returns
        -------
        csr_matrix
            L2 normalized sparse matrix representation of tf-idf vectors
        """
        matrix_row, matrix_col, matrix_data = [], [], []
        num_docs = len(doc_ids)

        for index, doc_id in enumerate(doc_ids):
            if index % 1000 == 0 and num_docs > 1000 and self.verbose:
                print(f'Vectorizing: {index}/{len(doc_ids)}')

            # Term Frequency
            tf = self.index_utils.get_document_vector(doc_id)
            if tf is None:
                continue

            # Filter out in-eligible terms
            tf = {t: tf[t] for t in tf if t in self.term_to_index}

            # Convert from dict to sparse matrix
            for term in tf:
                tfidf = tf[term] * self.idf_[term]
                matrix_row.append(index)
                matrix_col.append(self.term_to_index[term])
                matrix_data.append(tfidf)

        vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(num_docs, self.vocabulary_size))
        return self._l2normalize(vectors)


class BM25Vectorizer(VectorizerBase):
    """Wrapper class for bm25 vectorizer implemented on top of Pyserini.

    Parameters
    ----------
    lucene_index_path : str
        Path to lucene index folder
    min_df : int
        Minimum acceptable document frequency
    verbose : bool
        Whether to print out debugging information
    """

    def __init__(self, lucene_index_path: str, min_df: int = 1, verbose: bool = False) -> None:
        super().__init__(lucene_index_path, verbose, min_df)

    def get_vectors(self, doc_ids: List[str]):
        """Get the bm25 vectors given a list of doc_ids

        Parameters
        ----------
        doc_ids : List[str]
            The piece of text to analyze.

        Returns
        -------
        csr_matrix
            L2 normalized sparse matrix representation of bm25 vectors
        """
        matrix_row, matrix_col, matrix_data = [], [], []
        num_docs = len(doc_ids)

        for index, doc_id in enumerate(doc_ids):
            if index % 1000 == 0 and num_docs > 1000 and self.verbose:
                print(f'Vectorizing: {index}/{len(doc_ids)}')

            tf = self.index_utils.get_document_vector(doc_id)
            tf = {term: self.index_utils.compute_bm25_term_weight(doc_id, term, analyzer=None) for term in tf.keys()}

            # Convert from dict to sparse matrix
            for term in tf:
                matrix_row.append(index)
                matrix_col.append(self.term_to_index[term])
                matrix_data.append(tf[term])

        vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(num_docs, self.vocabulary_size))
        return self._l2normalize(vectors)
