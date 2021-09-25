import numpy as np

from typing import List, Union, Dict

from ._dsearcher import PRFDenseSearchResult


class DenseVectorPrf:
    def __init__(self, topic_ids: Union[int, List[str]], emb_qs: np.ndarray,
                 prf_candidates: Union[List[PRFDenseSearchResult], Dict[str, List[PRFDenseSearchResult]]], **kwargs):
        self.topic_ids = topic_ids
        self.emb_qs = emb_qs
        self.prf_candidates = prf_candidates
        self.kwargs = kwargs

    def get_prf_q_emb(self) -> np.ndarray:
        pass


class DenseVectorAveragePrf(DenseVectorPrf):
    def get_prf_q_emb(self):
        """Perform Average PRF with Dense Vectors

        Parameters
        ----------
        Returns
        -------
        np.ndarray
            return new query embeddings
        """
        if isinstance(self.topic_ids, List):
            qids = list()
            new_emb_qs = list()
            for index, topic_id in enumerate(self.topic_ids):
                qids.append(topic_id)
                all_candidate_embs = [item.vectors for item in self.prf_candidates[topic_id]]
                new_emb_q = np.mean(np.vstack((self.emb_qs[index], all_candidate_embs)), axis=0)
                new_emb_qs.append(new_emb_q)
            new_emb_qs = np.array(new_emb_qs).astype('float32')
            return new_emb_qs
        else:
            all_candidate_embs = [item.vectors for item in self.prf_candidates]
            new_emb_qs = np.mean(np.vstack((self.emb_qs[0], all_candidate_embs)), axis=0)
            new_emb_qs = np.array([new_emb_qs]).astype('float32')
            return new_emb_qs


class DenseVectorRocchioPrf(DenseVectorPrf):
    def get_prf_q_emb(self):
        """Perform Rocchio PRF with Dense Vectors

        Parameters
        ----------
        Returns
        -------
        np.ndarray
            return new query embeddings
        """
        rocchio_alpha = self.kwargs.get('rocchio_alpha', 0.9)
        rocchio_beta = self.kwargs.get('rocchio_beta', 0.1)

        if isinstance(self.topic_ids, List):
            qids = list()
            new_emb_qs = list()
            for index, topic_id in enumerate(self.topic_ids):
                qids.append(topic_id)
                all_candidate_embs = [item.vectors for item in self.prf_candidates[topic_id]]
                weighted_mean_doc_embs = rocchio_beta * np.mean(all_candidate_embs, axis=0)
                weighted_query_embs = rocchio_alpha * self.emb_qs[index]
                new_emb_q = np.sum(np.vstack((weighted_query_embs, weighted_mean_doc_embs)), axis=0)
                new_emb_qs.append(new_emb_q)
            new_emb_qs = np.array(new_emb_qs).astype('float32')
            return new_emb_qs
        else:
            all_candidate_embs = [item.vectors for item in self.prf_candidates]
            weighted_mean_doc_embs = rocchio_beta * np.mean(all_candidate_embs, axis=0)
            weighted_query_embs = rocchio_alpha * self.emb_qs[0]
            new_emb_q = np.sum(np.vstack((weighted_query_embs, weighted_mean_doc_embs)), axis=0)
            new_emb_q = np.array([new_emb_q]).astype('float32')
            return new_emb_q
