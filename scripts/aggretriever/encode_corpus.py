import argparse
import pickle
import numpy as np
from tqdm import tqdm
import faiss
import json
import sys
import os

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')
from pyserini.encode._aggretriever import AggretrieverDocumentEncoder

DATA_ITEM = {'msmarco-passage': {'id':'id', 'contents': ['contents']}, 
             'beir': {'id':'_id', 'contents': ['title', 'text']}}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, help='model name or path', required=True)
    parser.add_argument('--corpus_domain', required=False, default='msmarco-passage')
    parser.add_argument('--dimension', type=int, help='dimension of passage embeddings', required=False, default=768)
    parser.add_argument('--corpus', type=str,
                        help='collection file to be encoded (format: jsonl)', required=True)
    parser.add_argument('--index', type=str, help='directory to store brute force index of corpus', required=True)
    parser.add_argument('--batch', type=int, help='batch size', default=8)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cuda:0')
    args = parser.parse_args()

    model = AggretrieverDocumentEncoder(model_name=args.model_name, device=args.device)

    if not os.path.exists(args.index):
        os.mkdir(args.index)

    data_item = DATA_ITEM[args.corpus_domain]
    index = faiss.IndexFlatIP(args.dimension)
    texts = []
    with open(os.path.join(args.index, 'docid'), 'w') as id_file:
        file = os.path.join(args.corpus)
        print(f'Loading {file}')
        with open(file, 'r') as corpus:
            for idx, line in enumerate(tqdm(corpus.readlines())):
                info = json.loads(line)
                docid = info[data_item['id']]
                text = []
                for key in data_item['contents']:
                    text.extend(info[key].strip().split('\t'))
                text = ' '.join(text)
                id_file.write(f'{docid}\n')
                texts.append(text.lower())

    for idx in tqdm(range(0, len(texts), args.batch)):
        text_batch = texts[idx: idx+args.batch]
        embeddings = model.encode(text_batch)
        index.add(np.array(embeddings))
    faiss.write_index(index, os.path.join(args.index, 'index'))