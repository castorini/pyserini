import argparse
import pickle
from tqdm import tqdm
import os
import sys
import os
import pandas as pd

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')
from pyserini.encode._aggretriever import AggretrieverQueryEncoder


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, help='model name or path', required=True)
    parser.add_argument('--query', type=str,
                        help='query file to be encoded (format: tsv)', required=True)
    parser.add_argument('--output', type=str, help='dir to store query embeddings', required=True)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cuda:0')
    args = parser.parse_args()

    model = AggretrieverQueryEncoder(model_name=args.model_name, device=args.device)

    embeddings = {'id': [], 'text': [], 'embedding': []}
    with open(args.query, 'r') as fin:
        for line in tqdm(fin): 
            qid, text = line.strip().split('\t')
            qid = str(qid)
            embeddings['id'].append(qid)
            embeddings['text'].append(text)
            embeddings['embedding'].append(model.encode(text))
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(os.path.join(args.output, 'embedding.pkl'))