import argparse
from tqdm import tqdm

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Externally hybrid results')
    parser.add_argument('--dense', required=True, help='dense retrieval result')
    parser.add_argument('--sparse', required=True, help='sparse retrieval result')
    parser.add_argument('--alpha', type=float, required=True, help='hybrid alpha')
    parser.add_argument('--output', required=True, help='hybrid result')
    args = parser.parse_args()

    alpha = args.alpha
    dense_result = {}
    with open(args.dense) as f:
        for line in f:
            qid, _, docid, rank, score, _ = line.rstrip().split()
            score = float(score)
            if qid in dense_result:
                dense_result[qid][docid] = score
            else:
                dense_result[qid] = {docid: score}
    sparse_result = {}
    with open(args.sparse) as f:
        for line in f:
            qid, _, docid, rank, score, _ = line.rstrip().split()
            score = float(score)
            if qid in sparse_result:
                sparse_result[qid][docid] = score
            else:
                sparse_result[qid] = {docid: score}

    hybrid_result = {}

    output_f = open(args.output, 'w')
    for key in tqdm(list(dense_result.keys())):
        dense_hits = {docid: float(dense_result[key][docid]) for docid in dense_result[key]}
        sparse_hits = {docid: float(sparse_result[key][docid]) for docid in sparse_result[key]}
        hybrid_scores = []
        min_dense_score = min(dense_hits.values())
        min_sparse_score = min(sparse_hits.values())
        for doc in set(dense_hits.keys()) | set(sparse_hits.keys()):
            if doc not in dense_hits:
                score = alpha * sparse_hits[doc] + min_dense_score
            elif doc not in sparse_hits:
                score = alpha * min_sparse_score + dense_hits[doc]
            else:
                score = alpha * sparse_hits[doc] + dense_hits[doc]
            hybrid_scores.append((doc, score))
        hybrid_scores = sorted(hybrid_scores, key=lambda x: x[1], reverse=True)
        for idx, item in enumerate(hybrid_scores):
            output_f.write(f'{key} Q0 {item[0]} {idx+1} {item[1]} hybrid\n')
    output_f.close()
