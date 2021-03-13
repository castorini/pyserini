import argparse
import pandas as pd
from tqdm import tqdm
import sys

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')

from pyserini.dsearch import AnceQueryEncoder

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--input', type=str, help='query file to be encoded.', required=True)
    parser.add_argument('--output', type=str, help='path to store query embeddings', required=True)
    parser.add_argument('--device', type=str,
                        help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    args = parser.parse_args()

    encoder = AnceQueryEncoder(args.encoder, device=args.device)
    embeddings = {'id': [], 'text': [], 'embedding': []}
    for line in tqdm(open(args.input, 'r').readlines()):
        qid, text = line.rstrip().split('\t')
        qid = qid.strip()
        text = text.strip()
        embeddings['id'].append(qid)
        embeddings['text'].append(text)
        embeddings['embedding'].append(encoder.encode(text))
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(args.output)
