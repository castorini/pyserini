import numpy as np

from typing import List, Union

from ._dsearcher import PRFDenseSearchResult


def average_prf(topic_ids: Union[int, List[int]], emb_qs: List[List[float]], prf_candidates: List[PRFDenseSearchResult]):
    if isinstance(topic_ids, List):
        pass
    else:
        if len(prf_candidates) == 0:
            new_emb_q = emb_qs[0]
        else:
            all_candidate_embs = [item.vectors for item in prf_candidates]
            new_emb_q = np.mean(np.vstack((emb_qs[0], all_candidate_embs)), axis=0)
        new_emb_q = np.array([new_emb_q]).astype('float32')
        return new_emb_q


def rocchio_prf(topic_ids: Union[int, List[int]], emb_qs, prf_candidates, rocchio_alpha, rocchio_beta):
    if isinstance(topic_ids, List):
        pass
    else:
        if len(prf_candidates) == 0:
            new_emb_q = emb_qs[0]
        else:
            all_candidate_embs = [item.vectors for item in prf_candidates]
            mean_doc_embs = [float(v) * float(rocchio_beta) for v in np.mean(all_candidate_embs, axis=0)]
            weighted_query_embs = [float(q) * float(rocchio_alpha) for q in emb_qs[0]]
            new_emb_q = np.sum(np.vstack((weighted_query_embs, mean_doc_embs)), axis=0)
        new_emb_q = np.array([new_emb_q]).astype('float32')
        return new_emb_q
