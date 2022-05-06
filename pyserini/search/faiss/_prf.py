import numpy as np
from typing import List, Dict
from pyserini.search.faiss import PRFDenseSearchResult, AnceQueryEncoder
from pyserini.search.lucene import LuceneSearcher
import json


class DenseVectorPrf:
    def __init__(self):
        pass

    def get_prf_q_emb(self, **kwargs):
        pass

    def get_batch_prf_q_emb(self, **kwargs):
        pass


class DenseVectorAveragePrf(DenseVectorPrf):

    def get_prf_q_emb(self, emb_qs: np.ndarray = None, prf_candidates: List[PRFDenseSearchResult] = None):
        """Perform Average PRF with Dense Vectors

        Parameters
        ----------
        emb_qs : np.ndarray
            Query embedding
        prf_candidates : List[PRFDenseSearchResult]
            List of PRFDenseSearchResult, contains document embeddings.

        Returns
        -------
        np.ndarray
            return new query embeddings
        """
        all_candidate_embs = [item.vectors for item in prf_candidates]
        new_emb_qs = np.mean(np.vstack((emb_qs, all_candidate_embs)), axis=0)
        return new_emb_qs

    def get_batch_prf_q_emb(self, topic_ids: List[str] = None, emb_qs: np.ndarray = None,
                            prf_candidates: Dict[str, List[PRFDenseSearchResult]] = None):
        """Perform Average PRF with Dense Vectors

        Parameters
        ----------
        topic_ids : List[str]
            List of topic ids.
        emb_qs : np.ndarray
            Query embeddings
        prf_candidates : List[PRFDenseSearchResult]
            List of PRFDenseSearchResult, contains document embeddings.

        Returns
        -------
        np.ndarray
            return new query embeddings
        """

        qids = list()
        new_emb_qs = list()
        for index, topic_id in enumerate(topic_ids):
            qids.append(topic_id)
            new_emb_qs.append(self.get_prf_q_emb(emb_qs[index], prf_candidates[topic_id]))
        new_emb_qs = np.array(new_emb_qs).astype('float32')
        return new_emb_qs


class DenseVectorRocchioPrf(DenseVectorPrf):
    def __init__(self, alpha: float, beta: float, gamma: float, topk: int, bottomk: int):
        """
        Parameters
        ----------
        alpha : float
            Rocchio parameter, controls the weight assigned to the original query embedding.
        beta : float
            Rocchio parameter, controls the weight assigned to the positive document embeddings.
        gamma : float
            Rocchio parameter, controls the weight assigned to the negative document embeddings.
        topk : int
            Rocchio parameter, set topk documents as positive document feedbacks.
        bottomk : int
            Rocchio parameter, set bottomk documents as negative document feedbacks.
        """
        DenseVectorPrf.__init__(self)
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.topk = topk
        self.bottomk = bottomk

    def get_prf_q_emb(self, emb_qs: np.ndarray = None, prf_candidates: List[PRFDenseSearchResult] = None):
        """Perform Rocchio PRF with Dense Vectors

        Parameters
        ----------
        emb_qs : np.ndarray
            query embedding
        prf_candidates : List[PRFDenseSearchResult]
            List of PRFDenseSearchResult, contains document embeddings.

        Returns
        -------
        np.ndarray
            return new query embeddings
        """

        all_candidate_embs = [item.vectors for item in prf_candidates]
        weighted_query_embs = self.alpha * emb_qs
        weighted_mean_pos_doc_embs = self.beta * np.mean(all_candidate_embs[:self.topk], axis=0)
        new_emb_q = weighted_query_embs + weighted_mean_pos_doc_embs
        if self.bottomk > 0:
            weighted_mean_neg_doc_embs = self.gamma * np.mean(all_candidate_embs[-self.bottomk:], axis=0)
            new_emb_q -= weighted_mean_neg_doc_embs
        return new_emb_q

    def get_batch_prf_q_emb(self, topic_ids: List[str] = None, emb_qs: np.ndarray = None,
                            prf_candidates: Dict[str, List[PRFDenseSearchResult]] = None):
        """Perform Rocchio PRF with Dense Vectors

        Parameters
        ----------
        topic_ids : List[str]
            List of topic ids.
        emb_qs : np.ndarray
            Query embeddings
        prf_candidates : List[PRFDenseSearchResult]
            List of PRFDenseSearchResult, contains document embeddings.

        Returns
        -------
        np.ndarray
            return new query embeddings
        """
        qids = list()
        new_emb_qs = list()
        for index, topic_id in enumerate(topic_ids):
            qids.append(topic_id)
            new_emb_qs.append(self.get_prf_q_emb(emb_qs[index], prf_candidates[topic_id]))
        new_emb_qs = np.array(new_emb_qs).astype('float32')
        return new_emb_qs


class DenseVectorAncePrf(DenseVectorPrf):
    def __init__(self, encoder: AnceQueryEncoder, sparse_searcher: LuceneSearcher):
        """
        Parameters
        ----------
        encoder : AnceQueryEncoder
            The new ANCE query encoder for ANCE-PRF.
        sparse_searcher : LuceneSearcher
            The sparse searcher using lucene index, for retrieving doc contents.
        """
        DenseVectorPrf.__init__(self)
        self.encoder = encoder
        self.sparse_searcher = sparse_searcher

    def get_prf_q_emb(self, query: str = None, prf_candidates: List[PRFDenseSearchResult] = None):
        """Perform single ANCE-PRF with Dense Vectors

        Parameters
        ----------
        query : str
            query text
        prf_candidates : List[PRFDenseSearchResult]
            List of PRFDenseSearchResult, contains document embeddings.

        Returns
        -------
        np.ndarray
            return new query embeddings
        """
        passage_texts = [query]
        for item in prf_candidates:
            raw_text = json.loads(self.sparse_searcher.doc(item.docid).raw())
            passage_texts.append(raw_text['contents'])
        full_text = f'{self.encoder.tokenizer.cls_token}{self.encoder.tokenizer.sep_token.join(passage_texts)}{self.encoder.tokenizer.sep_token}'
        emb_q = self.encoder.prf_encode(full_text)
        emb_q = emb_q.reshape((1, len(emb_q)))
        return emb_q

    def get_batch_prf_q_emb(self, topics: List[str], topic_ids: List[str],
                            prf_candidates: Dict[str, List[PRFDenseSearchResult]]) -> np.ndarray:
        """Perform batch ANCE-PRF with Dense Vectors

        Parameters
        ----------
        topics : List[str]
            List of query texts.
        topic_ids: List[str]
            List of topic ids.
        prf_candidates : List[PRFDenseSearchResult]
            List of PRFDenseSearchResult, contains document embeddings.

        Returns
        -------
        np.ndarray
            return new query embeddings
        """
        prf_passage_texts = list()
        for index, query in enumerate(topics):
            passage_texts = [query]
            prf_candidate = prf_candidates[topic_ids[index]]
            for item in prf_candidate:
                raw_text = json.loads(self.sparse_searcher.doc(item.docid).raw())
                passage_texts.append(raw_text['contents'])
            full_text = f'{self.encoder.tokenizer.cls_token}{self.encoder.tokenizer.sep_token.join(passage_texts)}{self.encoder.tokenizer.sep_token}'
            prf_passage_texts.append(full_text)
        emb_q = self.encoder.prf_batch_encode(prf_passage_texts)
        return emb_q
