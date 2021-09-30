import numpy as np
from typing import List, Dict
from pyserini.dsearch import PRFDenseSearchResult, AnceQueryEncoder
from pyserini.search import SimpleSearcher


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
        new_emb_qs = np.mean(np.vstack((emb_qs[0], all_candidate_embs)), axis=0)
        new_emb_qs = np.array([new_emb_qs]).astype('float32')
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
            all_candidate_embs = [item.vectors for item in prf_candidates[topic_id]]
            new_emb_q = np.mean(np.vstack((emb_qs[index], all_candidate_embs)), axis=0)
            new_emb_qs.append(new_emb_q)
        new_emb_qs = np.array(new_emb_qs).astype('float32')
        return new_emb_qs


class DenseVectorRocchioPrf(DenseVectorPrf):
    def __init__(self, alpha: float, beta: float):
        """
        Parameters
        ----------
        alpha : float
            Rocchio parameter, controls the weight assigned to the original query embedding.
        beta : float
            Rocchio parameter, controls the weight assigned to the document embeddings.
        """
        DenseVectorPrf.__init__(self)
        self.alpha = alpha
        self.beta = beta

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
        weighted_mean_doc_embs = self.beta * np.mean(all_candidate_embs, axis=0)
        weighted_query_embs = self.alpha * emb_qs[0]
        new_emb_q = np.sum(np.vstack((weighted_query_embs, weighted_mean_doc_embs)), axis=0)
        new_emb_q = np.array([new_emb_q]).astype('float32')
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
            all_candidate_embs = [item.vectors for item in prf_candidates[topic_id]]
            weighted_mean_doc_embs = self.beta * np.mean(all_candidate_embs, axis=0)
            weighted_query_embs = self.alpha * emb_qs[index]
            new_emb_q = np.sum(np.vstack((weighted_query_embs, weighted_mean_doc_embs)), axis=0)
            new_emb_qs.append(new_emb_q)
        new_emb_qs = np.array(new_emb_qs).astype('float32')
        return new_emb_qs


class DenseVectorAncePrf(DenseVectorPrf):
    def __init__(self, encoder: AnceQueryEncoder, sparse_searcher: SimpleSearcher):
        DenseVectorPrf.__init__(self)
        self.encoder = encoder
        self.sparse_searcher = sparse_searcher

    def get_prf_q_emb(self, query: str = None, prf_candidates: List[PRFDenseSearchResult] = None):
        passage_texts = [query]
        for item in prf_candidates:
            passage_texts.append(self.sparse_searcher.doc(item.docid).raw())
        full_text = f'{self.encoder.tokenizer.cls_token}{self.encoder.tokenizer.sep_token.join(passage_texts)}{self.encoder.tokenizer.sep_token}'
        emb_q = self.encoder.prf_encode(full_text)
        emb_q = emb_q.reshape((1, len(emb_q)))
        return emb_q

    def get_batch_prf_q_emb(self, topics: List[str], topic_ids: List[str],
                            prf_candidates: Dict[str, List[PRFDenseSearchResult]]) -> np.ndarray:
        prf_passage_texts = list()
        for index, query in enumerate(topics):
            passage_texts = [query]
            prf_candidate = prf_candidates[topic_ids[index]]
            for item in prf_candidate:
                passage_texts.append(self.sparse_searcher.doc(item.docid).raw())
            full_text = f'{self.encoder.tokenizer.cls_token}{self.encoder.tokenizer.sep_token.join(passage_texts)}{self.encoder.tokenizer.sep_token}'
            prf_passage_texts.append(full_text)
        emb_q = self.encoder.prf_batch_encode(prf_passage_texts)
        return emb_q
