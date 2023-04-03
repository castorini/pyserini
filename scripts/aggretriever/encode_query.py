import argparse
import pickle
import numpy as np
from tqdm import tqdm
import faiss
import os
import json
from pyserini.encode._aggretriever import AggretrieverQueryEncoder

DATA_ITEM = {'msmarco-passage': {'id':'id', 'contents': ['contents']}, 
             'beir': {'id':'_id', 'contents': ['text']}}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, help='model name or path', required=True)
    parser.add_argument('--corpus_domain', required=False, default='msmarco-passage')
    parser.add_argument('--dimension', type=int, help='dimension of passage embeddings', required=False, default=768)
    parser.add_argument('--query', type=str,
                        help='collection file to be encoded (format: jsonl)', required=True)
    parser.add_argument('--index', type=str, help='directory to store brute force index of corpus', required=False)
    parser.add_argument('--batch', type=int, help='batch size', default=8)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cuda:0')
    args = parser.parse_args()

    model = AggretrieverDocumentEncoder(model_name=args.model_name, device=args.device)
    data_item = DATA_ITEM[args.corpus_domain]
    index = faiss.IndexFlatIP(args.dimension)

    # if not os.path.exists(args.index):
    #     os.mkdir(args.index)

    texts = []
    lookup_indices = []
    file = os.path.join(args.query)
    print(f'Loading {file}')
    with open(file, 'r') as corpus:
        for idx, line in enumerate(tqdm(corpus.readlines())):
            info = json.loads(line)
            lookup_indices.append(info[data_item['id']])
            text = []

            for key in data_item['contents']:
                text.extend(info[key].strip().split('\t'))
            text = ' '.join(text)
            texts.append(text.lower())

    value_encoded, index_encoded = None, None
    value_encoded = np.zeros((len(texts), 768), dtype=np.float16)
    for idx in tqdm(range(0, len(texts), args.batch)):
        text_batch = texts[idx: idx+args.batch]
        value_encoded[idx: idx+args.batch, :] = model.encode(text_batch)

    with open('/store2/scratch/s269lin/Aggretriever/results/experiments/msmarco/coCondenser-Concatenator/encoding640/queries/queries.nfcorpus.test.pt', 'wb') as f:
        pickle.dump([value_encoded, index_encoded, lookup_indices], f, protocol=4)

    # texts = []
    # with open(os.path.join(args.index, 'docid'), 'w') as id_file:
    #     file = os.path.join(args.corpus)
    #     print(f'Loading {file}')
    #     with open(file, 'r') as corpus:
    #         for idx, line in enumerate(tqdm(corpus.readlines())):
    #             info = json.loads(line)
    #             docid = info['id']
    #             text = info['contents']
    #             id_file.write(f'{docid}\n')
    #             # docs can have many \n ...
    #             fields = text.split('\n')
    #             title, text = fields[1], fields[2:]
    #             if len(text) > 1:
    #                 text = ' '.join(text)
    #             text = f"{title} {text}"
    #             texts.append(text.lower())

    # for idx in tqdm(range(0, len(texts), args.batch)):
    #     text_batch = texts[idx: idx+args.batch]
    #     embeddings = model.encode(text_batch)
    #     index.add(np.array(embeddings))
    # faiss.write_index(index, os.path.join(args.index, 'index'))