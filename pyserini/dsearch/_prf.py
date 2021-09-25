import numpy as np
from typing import List, Union, Dict
from pyserini.dsearch import PRFDenseSearchResult


class DenseVectorPrf:
    # def __init__(self, topic_ids: Union[int, List[str]], emb_qs: np.ndarray,
    #              prf_candidates: Union[List[PRFDenseSearchResult], Dict[str, List[PRFDenseSearchResult]]], **kwargs):
    #     self.topic_ids = topic_ids
    #     self.emb_qs = emb_qs
    #     self.prf_candidates = prf_candidates
    #     self.kwargs = kwargs
    def __init__(self):
        pass

    def get_prf_q_emb(self, emb_qs: np.ndarray, prf_candidates: List[PRFDenseSearchResult]) -> np.ndarray:
        pass

    def get_batch_prf_q_emb(self, topic_ids: List[str], emb_qs: np.ndarray,
                            prf_candidates: Dict[str, List[PRFDenseSearchResult]]) -> np.ndarray:
        pass


class DenseVectorAveragePrf(DenseVectorPrf):

    def get_prf_q_emb(self, emb_qs: np.ndarray, prf_candidates: List[PRFDenseSearchResult]):
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

    def get_batch_prf_q_emb(self, topic_ids: List[str], emb_qs: np.ndarray, prf_candidates: Dict[str, List[PRFDenseSearchResult]]):
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
        self.alpha = alpha
        self.beta = beta

    def get_prf_q_emb(self, emb_qs: np.ndarray, prf_candidates: List[PRFDenseSearchResult]):
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

    def get_batch_prf_q_emb(self, topic_ids: List[str], emb_qs: np.ndarray, prf_candidates: Dict[str, List[PRFDenseSearchResult]]):
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
