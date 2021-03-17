import json
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
    dense_result = json.load(open(args.dense))
    sparse_result = json.load(open(args.sparse))
    hybrid_result = {}

    for key in tqdm(list(dense_result.keys())):
        question = dense_result[key]['question']
        answers = dense_result[key]['answers']
        sparse_contexts = sparse_result[key]['contexts']
        dense_contexts = dense_result[key]['contexts']
        dense_hits = {hit['docid']: float(hit['score']) for hit in dense_contexts}
        sparse_hits = {hit['docid']: float(hit['score']) for hit in sparse_contexts}
        hybrid_scores = {}
        dense_scores = {}
        spares_scores = {}
        min_dense_score = min(dense_hits.values())
        min_sparse_score = min(sparse_hits.values())
        for doc in set(dense_hits.keys()) | set(sparse_hits.keys()):
            if doc not in dense_hits:
                score = alpha * sparse_hits[doc] + min_dense_score
                spares_scores[doc] = sparse_hits[doc]
                dense_scores[doc] = -1
            elif doc not in sparse_hits:
                score = alpha * min_sparse_score + dense_hits[doc]
                spares_scores[doc] = -1
                dense_scores[doc] = dense_hits[doc]
            else:
                score = alpha * sparse_hits[doc] + dense_hits[doc]
                spares_scores[doc] = sparse_hits[doc]
                dense_scores[doc] = dense_hits[doc]
            hybrid_scores[doc] = score
        total_ids = []
        total_context = []
        for sctx, dctx in zip(sparse_contexts, dense_contexts):
            if sctx['docid'] not in total_ids:
                total_ids.append(sctx['docid'])
                sctx['score'] = hybrid_scores[sctx['docid']]
                sctx['sparse_score'] = spares_scores[sctx['docid']]
                sctx['dense_score'] = dense_scores[sctx['docid']]
                total_context.append(sctx)
            if dctx['docid'] not in total_ids:
                total_ids.append(dctx['docid'])
                dctx['score'] = hybrid_scores[dctx['docid']]
                dctx['sparse_score'] = spares_scores[dctx['docid']]
                dctx['dense_score'] = dense_scores[dctx['docid']]
                total_context.append(dctx)
        total_context = sorted(total_context, key=lambda x: x['score'], reverse=True)
        hybrid_result[key] = {'question': question, 'answers': answers, 'contexts': total_context}
    json.dump(hybrid_result, open(args.output, 'w'), indent=4)
