import math
import numpy as np
from typing import List
from scipy.sparse import csr_matrix
from pyserini.search import pysearch
from pyserini.index import pyutils


class TfidfVectorizer:
    def __init__(self, lucene_index_path: str, min_df: int = 1) -> None:
        self.min_df: int = min_df
        self.index_utils = pyutils.IndexReaderUtils(lucene_index_path)

        # get num_docs
        self.searcher = pysearch.SimpleSearcher(lucene_index_path)
        self.num_docs: int = self.searcher.num_docs

        # pre-processing
        self.vocabulary_ = set()
        self.idf_ = {}

        for term in self.index_utils.terms():
            self.idf_[term.term] = math.log(self.num_docs / term.df)
            if term.df > self.min_df:
                self.vocabulary_.add(term.term)

        self.term_to_index = {}
        for index, term in enumerate(self.vocabulary_):
            self.term_to_index[term] = index
        self.vocabulary_size = len(self.vocabulary_)
        print(f'Found {self.vocabulary_size} terms')

    def l2norm(self, a):
        norm_rows = np.sqrt(np.add.reduceat(a.data * a.data, a.indptr[:-1]))
        nnz_per_row = np.diff(a.indptr)
        a.data /= np.repeat(norm_rows, nnz_per_row)
        return a

    def get_vectors(self, doc_ids: List[str]):
        matrix_row, matrix_col, matrix_data = [], [], []

        for index, doc_id in enumerate(doc_ids):
            if index % 1000 == 0:
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

        vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(
            len(doc_ids), self.vocabulary_size))
        return self.l2norm(vectors)
