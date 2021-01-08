import argparse

import numpy as np
import pandas as pd
from tqdm import tqdm
from transformers import BertModel, BertTokenizer


def encode_query(text, tokenizer, model, device='cpu'):
    max_length = 36  # hardcode for now
    inputs = tokenizer(
        '[CLS] [Q] ' + text + " [MASK]" * max_length,
        max_length=max_length,
        truncation=True,
        add_special_tokens=False,
        return_tensors="pt"
    )
    inputs.to(device)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.detach().cpu().numpy()
    return np.average(embeddings[:, 4:, :], axis=-2).flatten()


def encode_passage(text, tokenizer, model, device='cpu'):
    max_length = 154  # hardcode for now
    inputs = tokenizer(
        '[CLS] [D] ' + text,
        max_length=max_length,
        truncation=True,
        add_special_tokens=False,
        return_tensors="pt"
    )
    inputs.to(device)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.detach().cpu().numpy()
    return np.mean(embeddings[:, 4:, :], axis=-2).flatten()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--encoder", type=str, help='encoder name or path', required=True)
    parser.add_argument("--input", type=str, help='doc file to get encoded.', required=True)
    parser.add_argument("--type", type=str, help='doc type, [passage, query]', required=True)
    parser.add_argument("--output", type=str, help='path to store embeddings', required=True)
    parser.add_argument("--store-text", action="store_true")
    parser.add_argument("--device", type=str, help='device cpu or cuda [cuda:0, cuda:1...]', required=True)
    args = parser.parse_args()

    tokenizer = BertTokenizer.from_pretrained(args.encoder)
    model = BertModel.from_pretrained(args.encoder)
    model.to(args.device)
    embeddings = {'id': [], 'embedding': []}
    if args.store_text:
        embeddings['text'] = []
    for line in tqdm(open(args.input, 'r').readlines()):
        id_, text = line.rstrip().split('\t')
        id_ = id_.strip()
        text = text.strip()
        if args.store_text:
            embeddings['text'].append(text)
        embeddings['id'].append(id_)
        if args.type == 'passage':
            embeddings['embedding'].append(encode_passage(text, tokenizer, model, args.device))
        elif args.type == 'query':
            embeddings['embedding'].append(encode_query(text, tokenizer, model, args.device))
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(args.output)
