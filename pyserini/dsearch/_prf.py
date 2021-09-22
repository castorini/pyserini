import numpy as np

from typing import List, Union, Dict

from ._dsearcher import PRFDenseSearchResult


def average_prf(topic_ids: Union[int, List[str]], emb_qs: np.ndarray,
                prf_candidates: Union[List[PRFDenseSearchResult], Dict[str, List[PRFDenseSearchResult]]]):
    """Perform Average PRF

        Parameters
        ----------
        topic_ids : Union[int, List[str]]
            single topic id or list of topic id depends on batch
        emb_qs : np.ndarray
            query embeddings
        prf_candidates : Union[List[PRFDenseSearchResult], Dict[str, List[PRFDenseSearchResult]]]
            the PRF candidate passage vectors for each query
        Returns
        -------
        np.ndarray
            return new query embeddings
        """
    if isinstance(topic_ids, List):
        qids = list()
        new_emb_qs = list()
        for index, topic_id in enumerate(topic_ids):
            qids.append(topic_id)
            all_candidate_embs = [item.vectors for item in prf_candidates[topic_id]]
            new_emb_q = np.mean(np.vstack((emb_qs[index], all_candidate_embs)), axis=0)
            new_emb_qs.append(new_emb_q)
        new_emb_qs = np.array(new_emb_qs).astype('float32')
        return new_emb_qs
    else:
        if len(prf_candidates) == 0:
            new_emb_qs = emb_qs[0]
        else:
            all_candidate_embs = [item.vectors for item in prf_candidates]
            new_emb_qs = np.mean(np.vstack((emb_qs[0], all_candidate_embs)), axis=0)
        new_emb_qs = np.array([new_emb_qs]).astype('float32')
        return new_emb_qs


def rocchio_prf(topic_ids: Union[int, List[str]], emb_qs: np.ndarray,
                prf_candidates: Union[List[PRFDenseSearchResult], Dict[str, List[PRFDenseSearchResult]]],
                rocchio_alpha: float, rocchio_beta: float):
    """Perform Average PRF

        Parameters
        ----------
        topic_ids : Union[int, List[str]]
            single topic id or list of topic id depends on batch
        emb_qs : np.ndarray
            query embeddings
        prf_candidates : Union[List[PRFDenseSearchResult], Dict[str, List[PRFDenseSearchResult]]]
            the PRF candidate passage vectors for each query
        rocchio_alpha : float
            alpha parameter in Rocchio
        rocchio_beta : float
            beta parameter in Rocchio
        Returns
        -------
        np.ndarray
            return new query embeddings
        """
    if isinstance(topic_ids, List):
        qids = list()
        new_emb_qs = list()
        for index, topic_id in enumerate(topic_ids):
            qids.append(topic_id)
            all_candidate_embs = [item.vectors for item in prf_candidates[topic_id]]
            weighted_mean_doc_embs = rocchio_beta * np.mean(all_candidate_embs, axis=0)
            weighted_query_embs = rocchio_alpha * emb_qs[index]
            new_emb_q = np.sum(np.vstack((weighted_query_embs, weighted_mean_doc_embs)), axis=0)
            new_emb_qs.append(new_emb_q)
        new_emb_qs = np.array(new_emb_qs).astype('float32')
        return new_emb_qs
    else:
        if len(prf_candidates) == 0:
            new_emb_q = emb_qs[0]
        else:
            all_candidate_embs = [item.vectors for item in prf_candidates]
            weighted_mean_doc_embs = rocchio_beta * np.mean(all_candidate_embs, axis=0)
            weighted_query_embs = rocchio_alpha * emb_qs[0]
            new_emb_q = np.sum(np.vstack((weighted_query_embs, weighted_mean_doc_embs)), axis=0)
        new_emb_q = np.array([new_emb_q]).astype('float32')
        return new_emb_q
