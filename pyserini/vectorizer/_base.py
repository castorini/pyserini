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

import math
from typing import List

from scipy.sparse import csr_matrix
from sklearn.preprocessing import normalize

from pyserini import index, search


class Vectorizer:
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

    def __init__(self, lucene_index_path: str, min_df: int = 1, verbose: bool = False):
        self.min_df: int = min_df
        self.verbose: bool = verbose
        self.index_reader = index.IndexReader(lucene_index_path)
        self.searcher = search.SimpleSearcher(lucene_index_path)
        self.num_docs: int = self.searcher.num_docs

        # build vocabulary
        self.vocabulary_ = set()
        for term in self.index_reader.terms():
            if term.df > self.min_df:
                self.vocabulary_.add(term.term)

        # build term to index mapping
        self.term_to_index = {}
        for i, term in enumerate(self.vocabulary_):
            self.term_to_index[term] = i
        self.vocabulary_size = len(self.vocabulary_)

        if self.verbose:
            print(f'Found {self.vocabulary_size} terms with min_df={self.min_df}')


class TfidfVectorizer(Vectorizer):
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

    def __init__(self, lucene_index_path: str, min_df: int = 1, verbose: bool = False):
        super().__init__(lucene_index_path, min_df, verbose)

        self.idf_ = {}
        for term in self.index_reader.terms():
            self.idf_[term.term] = math.log(self.num_docs / term.df)

    def get_vectors(self, docids: List[str]):
        """Get the tf-idf vectors given a list of docids

        Parameters
        ----------
        docids : List[str]
            The piece of text to analyze.

        Returns
        -------
        csr_matrix
            L2 normalized sparse matrix representation of tf-idf vectors
        """
        matrix_row, matrix_col, matrix_data = [], [], []
        num_docs = len(docids)

        for index, doc_id in enumerate(docids):
            if index % 1000 == 0 and num_docs > 1000 and self.verbose:
                print(f'Vectorizing: {index}/{len(docids)}')

            # Term Frequency
            tf = self.index_reader.get_document_vector(doc_id)
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
        return normalize(vectors, norm='l2')


class BM25Vectorizer(Vectorizer):
    """Wrapper class for BM25 vectorizer implemented on top of Pyserini.

    Parameters
    ----------
    lucene_index_path : str
        Path to lucene index folder
    min_df : int
        Minimum acceptable document frequency
    verbose : bool
        Whether to print out debugging information
    """

    def __init__(self, lucene_index_path: str, min_df: int = 1, verbose: bool = False):
        super().__init__(lucene_index_path, min_df, verbose)

    def get_vectors(self, docids: List[str]):
        """Get the BM25 vectors given a list of docids

        Parameters
        ----------
        docids : List[str]
            The piece of text to analyze.

        Returns
        -------
        csr_matrix
            L2 normalized sparse matrix representation of BM25 vectors
        """
        matrix_row, matrix_col, matrix_data = [], [], []
        num_docs = len(docids)

        for index, doc_id in enumerate(docids):
            if index % 1000 == 0 and num_docs > 1000 and self.verbose:
                print(f'Vectorizing: {index}/{len(docids)}')

            # Term Frequency
            tf = self.index_reader.get_document_vector(doc_id)
            if tf is None:
                continue

            # Filter out in-eligible terms
            tf = {t: tf[t] for t in tf if t in self.term_to_index}

            # Convert from dict to sparse matrix
            for term in tf:
                bm25_weight = self.index_reader.compute_bm25_term_weight(doc_id, term, analyzer=None)
                matrix_row.append(index)
                matrix_col.append(self.term_to_index[term])
                matrix_data.append(bm25_weight)

        vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(num_docs, self.vocabulary_size))
        return normalize(vectors, norm='l2')
