#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import argparse
import json
import os
import sys
import numpy as np
import faiss
import torch
from tqdm import tqdm

from transformers import BertTokenizer, BertModel

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')

def mean_pooling(last_hidden_state, attention_mask):
    token_embeddings = last_hidden_state
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
    sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
    sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
    return sum_embeddings / sum_mask


class TctColBertDocumentEncoder(torch.nn.Module):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        super().__init__()
        self.device = device
        self.model = BertModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, titles=None):
        texts = ['[CLS] [D] ' + text for text in texts]
        max_length = 512  # hardcode for now
        inputs = self.tokenizer(
            texts,
            max_length=max_length,
            padding="longest",
            truncation=True,
            add_special_tokens=False,
            return_tensors='pt'
        )
        inputs.to(self.device)
        outputs = self.model(**inputs)
        embeddings = mean_pooling(outputs["last_hidden_state"][:, 4:, :], inputs['attention_mask'][:, 4:])
        return embeddings.detach().cpu().numpy()



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--dimension', type=int, help='dimension of passage embeddings', required=False, default=768)
    parser.add_argument('--corpus', type=str,
                        help='collection file to be encoded (format: jsonl)', required=True)
    parser.add_argument('--index', type=str, help='directory to store brute force index of corpus', required=True)
    parser.add_argument('--batch', type=int, help='batch size', default=8)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cuda:0')
    args = parser.parse_args()

    # tokenizer = AutoTokenizer.from_pretrained(args.encoder)
    # model = AutoModel.from_pretrained(args.encoder)
    model = TctColBertDocumentEncoder(model_name=args.encoder, device=args.device)

    index = faiss.IndexFlatIP(args.dimension)

    if not os.path.exists(args.index):
        os.mkdir(args.index)

    texts = []
    with open(os.path.join(args.index, 'docid'), 'w') as id_file:
        file = os.path.join(args.corpus)
        print(f'Loading {file}')
        with open(file, 'r') as corpus:
            for idx, line in enumerate(tqdm(corpus.readlines())):
                info = json.loads(line)
                docid = info['id']
                text = info['contents']
                id_file.write(f'{docid}\n')
                # docs can have many \n ...
                fields = text.split('\n')
                title, text = fields[1], fields[2:]
                if len(text) > 1:
                    text = ' '.join(text)
                text = f"{title} {text}"
                texts.append(text.lower())

    for idx in tqdm(range(0, len(texts), args.batch)):
        text_batch = texts[idx: idx+args.batch]
        embeddings = model.encode(text_batch)
        index.add(np.array(embeddings))
    faiss.write_index(index, os.path.join(args.index, 'index'))
