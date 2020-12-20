from typing import List, Optional
import faiss
from dataclasses import dataclass
import numpy as np
from tqdm import tqdm
import tensorflow.compat.v1 as tf


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
            return [DenseSearchResult(str(idx), score, None) for score, idx in zip(distances, indexes) if idx != -1]
        else:
            return [
                DenseSearchResult(self.idx2id[idx], score, self.docs[self.idx2id[idx]])
                for score, idx in zip(distances, indexes) if idx != -1
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


class QueryEncoder:
    def __init__(self, embedding_path, queries_path):
        self.embedding = self.load_embedding_from_tfds(embedding_path)
        self.text2idx = self.load_queries(queries_path)

    @classmethod
    def from_pre_encoded(cls, prebuilt_embedding, queries_name):
        return cls(prebuilt_embedding, queries_name)

    def encode(self, query: str):
        return self.embedding[self.text2idx[query]]

    @staticmethod
    def load_queries(queries_path: str):
        text2idx = {}
        with open(queries_path, 'r') as f:
            for idx, line in tqdm(enumerate(f)):
                qid, text = line.rstrip().split('\t')
                text2idx[text] = idx
        return text2idx

    @staticmethod
    def load_embedding_from_tfds(srcfile):

        def _parse_function(example_proto):
            features = {'doc_emb': tf.FixedLenFeature([], tf.string),
                        'docid': tf.FixedLenFeature([], tf.int64)}
            parsed_features = tf.parse_single_example(example_proto, features)
            corpus = tf.decode_raw(parsed_features['doc_emb'], tf.float32)
            docid = tf.cast(parsed_features['docid'], tf.int32)
            return corpus, docid

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
