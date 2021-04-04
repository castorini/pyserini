import argparse
import pandas as pd
from tqdm import tqdm
import sys
import os

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')

from pyserini.dsearch import AnceQueryEncoder, AutoQueryEncoder, TctColBertQueryEncoder, DprQueryEncoder
from pyserini.search import get_topics

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--topics', type=str, help='topic name', required=True)
    parser.add_argument('--output', type=str, help='dir to store query embeddings', required=True)
    parser.add_argument('--device', type=str,
                        help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    args = parser.parse_args()
    device = args.device
    topics = get_topics(args.topics)

    if not os.path.exists(args.output):
        os.mkdir(args.output)

    if 'dpr' in args.encoder:
        encoder = DprQueryEncoder(encoder_dir=args.encoder, device=device)
    elif 'tct_colbert' in args.encoder:
        encoder = TctColBertQueryEncoder(encoder_dir=args.encoder, device=device)
    elif 'ance' in args.encoder:
        encoder = AnceQueryEncoder(encoder_dir=args.encoder, device=device)
    elif 'sentence' in args.encoder:
        encoder = AutoQueryEncoder(encoder_dir=args.encoder, device=device, pooling='mean', l2_norm=True)
    else:
        encoder = AutoQueryEncoder(encoder_dir=args.encoder, device=device)

    embeddings = {'id': [], 'text': [], 'embedding': []}
    for key in tqdm(topics):
        qid = str(key)
        text = topics[key]['title'].strip()
        embeddings['id'].append(qid)
        embeddings['text'].append(text)
        embeddings['embedding'].append(encoder.encode(text))
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(os.path.join(args.output, 'embedding.pkl'))
