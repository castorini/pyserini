import argparse
import json
import os

from scipy.sparse import csr_matrix
from tqdm import tqdm
import numpy as np
from multiprocessing import Pool, Manager


def token_dict_to_sparse_vector(token_dict, token2id):
    matrix_row, matrix_col, matrix_data = [], [], []
    tokens = token_dict.keys()
    col = []
    data = []
    for tok in tokens:
        if tok in token2id:
            col.append(token2id[tok])
            data.append(token_dict[tok])
    matrix_row.extend([0] * len(col))
    matrix_col.extend(col)
    matrix_data.extend(data)
    vector = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(1, len(token2id)))
    return vector


parser = argparse.ArgumentParser()
parser.add_argument('--corpus', type=str, help='path to corpus with vectors', required=True)
parser.add_argument('--topics', type=str, help='path to topics with vectors', required=True)
parser.add_argument('--tokens', type=str, help='path to token list', required=True)
parser.add_argument('--run', type=str, help='path to run file', required=True)
parser.add_argument('--threads', type=int, help='threads for hnsw', required=False, default=12)

args = parser.parse_args()

token2id = {}
with open(args.tokens) as tok_f:
    for idx, line in enumerate(tok_f):
        tok = line.rstrip()
        token2id[tok] = idx

corpus = []
for file in sorted(os.listdir(args.corpus)):
    file = os.path.join(args.corpus, file)
    if file.endswith('json') or file.endswith('jsonl'):
        print(f'Loading {file}')
        with open(file, 'r') as f:
            for idx, line in enumerate(tqdm(f.readlines())):
                info = json.loads(line)
                corpus.append(info)

ids = []
vectors = []
matrix_row, matrix_col, matrix_data = [], [], []
for i, d in enumerate(tqdm(corpus)):
    weight_dict = d['vector']
    tokens = weight_dict.keys()
    col = [token2id[tok] for tok in tokens]
    data = weight_dict.values()
    matrix_row.extend([i] * len(weight_dict))
    matrix_col.extend(col)
    matrix_data.extend(data)
    ids.append(d['id'])
vectors = csr_matrix((matrix_data, (matrix_row, matrix_col)), shape=(len(corpus), len(token2id)))

topic_ids = []
topic_vectors = []
with open(args.topics) as topic_f:
    for line in topic_f:
        info = json.loads(line)
        topic_ids.append(info['id'])
        topic_vectors.append(token_dict_to_sparse_vector(info['vector'], token2id))

vectors_T = vectors.T

manager = Manager()
results = manager.dict()


def run_search(idx):
    global results
    qid = topic_ids[idx]
    t_vec = topic_vectors[idx]
    scores = np.array(t_vec.dot(vectors_T).todense())[0]
    top_idx = sorted(range(len(scores)), key=lambda x: scores[x], reverse=True)[:1000]
    result = [(ids[x], scores[x]) for x in top_idx]
    results[qid] = result


with Pool(args.threads) as p:
    for _ in tqdm(p.imap_unordered(run_search, list(range(len(topic_ids)))), total=len(topic_ids)):
        pass

with open(args.run, 'w') as f:
    for qid in results:
        for idx, item in enumerate(results[qid]):
            did = item[0]
            score = item[1]
            f.write(f'{qid} Q0 {did} {idx+1} {score} bf\n')
