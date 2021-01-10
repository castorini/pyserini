import argparse

import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import BertModel, BertTokenizer


def encode_query(text, tokenizer, model, device='cpu'):
    max_length = 36  # hardcode for now
    inputs = tokenizer(
        '[CLS] [Q] ' + text + ' [MASK]' * max_length,
        max_length=max_length,
        truncation=True,
        add_special_tokens=False,
        return_tensors='pt'
    )
    inputs.to(device)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.detach().cpu().numpy()
    return np.average(embeddings[:, 4:, :], axis=-2).flatten()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--input', type=str, help='query file to be encoded.', required=True)
    parser.add_argument('--output', type=str, help='path to store query embeddings', required=True)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', required=True)
    args = parser.parse_args()

    tokenizer = BertTokenizer.from_pretrained(args.encoder)
    model = BertModel.from_pretrained(args.encoder)
    model.to(args.device)
    embeddings = {'id': [], 'text': [], 'embedding': []}
    for line in tqdm(open(args.input, 'r').readlines()):
        qid, text = line.rstrip().split('\t')
        qid = qid.strip()
        text = text.strip()
        embeddings['id'].append(qid)
        embeddings['text'].append(text)
        embeddings['embedding'].append(encode_query(text, tokenizer, model, args.device))
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(args.output)
