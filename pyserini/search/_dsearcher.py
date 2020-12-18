from typing import List, Optional
import faiss
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm


@dataclass
class DenseSearchResult:
    docid: str
    score: float
    raw: Optional[str]


@dataclass
class Document:
    docid: str
    raw: Optional[str]


class SimpleDenseSearcher:
    """Simple Searcher for dense representation

    Parameters
    ----------
    index_path : str
        Path to faiss index directory.
    """

    def __init__(self, index_path: str, doc_path: str):
        self.index = faiss.read_index(index_path)
        self.dimension = self.index.d
        self.num_docs = self.index.ntotal
        self.idx2id, self.docs = self.load_corpus(doc_path)

    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str, corpus_name: str = None):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        corpus_name : str
            corpus name
        prebuilt_index_name : str
            Prebuilt index name.

        Returns
        -------
        SimpleDenseSearcher
            Searcher built from the prebuilt faiss index.
        """
        return cls(prebuilt_index_name, corpus_name)

    def search(self, emb_q: np.array, k: int = 10) -> List[DenseSearchResult]:
        """Search the collection.

        Parameters
        ----------
        emb_q : np.array
            Query string
        k : int
            Number of hits to return.
        Returns
        -------
        List[DenseSearchResult]
            List of search results.
        """
        assert len(emb_q) == self.dimension
        emb_q = emb_q.reshape((1, len(emb_q)))
        distances, indexes = self.index.search(emb_q, k)
        distances = distances.flat
        indexes = indexes.flat
        if self.idx2id is None:
            return [DenseSearchResult(str(idx), score, None) for score, idx in zip(distances, indexes)]
        else:
            return [
                DenseSearchResult(self.idx2id[idx], score, self.docs[self.idx2id[idx]])
                for score, idx in zip(distances, indexes)
            ]

    def doc(self, docid: str):
        """

        Parameters
        ----------
        docid : str
            doc id

        Returns
        -------
        Document
            document object that contains the raw text
        """
        if self.docs is None:
            return None
        try:
            return Document(docid, self.docs[docid])
        except KeyError:
            print(f'Doc {docid} does not exits')
            return None

    @staticmethod
    def load_corpus(corpus_path: str):
        if corpus_path is None:
            print('Warning, no doc text and ids provided.')
            return None, None
        corpus = {}
        idx2id = {}
        with open(corpus_path, 'r') as f:
            for idx, line in tqdm(enumerate(f)):
                doc_id, doc = line.rstrip().split('\t')
                corpus[doc_id] = doc
                idx2id[idx] = doc_id
        return idx2id, corpus
