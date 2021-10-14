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

from typing import Optional

import torch
import torch.nn as nn
from transformers import BertTokenizer, BertTokenizerFast
from transformers import BertModel, BertPreTrainedModel
from pyserini.encode import DocumentEncoder, QueryEncoder
from pyserini.encode import RepresentationWriter

# Hacky: Import ColBertIndexer beyond top level module `pyserini.encode`
import os
import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f'{script_path}/../index')
from colbert import ColBertIndexer


class ColBERT(BertPreTrainedModel):
    def __init__(self, config, dim=128):
        super().__init__(config)
        self.dim = dim
        self.bert = BertModel(config, add_pooling_layer=False)
        self.linear = nn.Linear(config.hidden_size, dim, bias=False)
        self.init_weights()

    def forward(self, Q, D):
        return self.score(self.query(Q), self.doc(D))

    def query(self, inputs):
        Q = self.bert(**inputs)[0] # last-layer hidden state
        # Q: (B, Lq, H) -> (B, Lq, dim)
        Q = self.linear(Q)
        # return: (B, Lq, dim) normalized
        return torch.nn.functional.normalize(Q, p=2, dim=2)

    def doc(self, inputs):
        D = self.bert(**inputs)[0]
        D = self.linear(D)
        return torch.nn.functional.normalize(D, p=2, dim=2)

    def score(self, Q, D):
        # (B, Lq, dim) x (B, dim, Ld) -> (B, Lq, Ld)
        cmp_matrix = Q @ D.permute(0, 2, 1)
        best_match = cmp_matrix.max(2).values # best match per query
        scores = best_match.sum(1) # sum score over each query
        return scores


class ColBertEncoder(DocumentEncoder):
    def __init__(self, model: str, prepend_tok: str,
        tokenizer: Optional[str]=None, device: Optional[str]='cuda:0'):
        # determine encoder prepend token
        prepend_tokens = ['[D]', '[Q]']
        assert prepend_tok in prepend_tokens
        self.prepend_tok = prepend_tok

        # load model
        self.model = ColBERT.from_pretrained(model,
            tie_word_embeddings=True
        )

        # load tokenizer and add ColBERT special tokens
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer or model)
        self.tokenizer.add_special_tokens({
            'additional_special_tokens': prepend_tokens
        })
        self.model.resize_token_embeddings(len(self.tokenizer))

        # specify device
        self.device = device
        self.model.to(self.device)

    def encode(self, texts, titles=None, fp16=False,
               sep='\n', debug=False, **kwargs):
        # preprocess input fields
        prepend_contents = []
        for b, text in enumerate(texts):
            title = titles[b] if titles is not None else None
            content = text if title is None else f'{title}{sep}{text}'
            # prepend ColBERT special tokens
            content = f'{self.prepend_tok} {content}'
            prepend_contents.append(content)

        # tokenize
        enc_tokens = self.tokenizer(prepend_contents,
            padding=True, truncation=True, return_tensors="pt")
        enc_tokens.to(self.device)

        if debug:
            for b, ids in enumerate(enc_tokens['input_ids']):
                print(f'--- ColBertEncoder Batch#{b} ---')
                print(self.tokenizer.decode(ids))

        # actual encoding
        if self.prepend_tok == '[D]':
            return self.model.doc(enc_tokens)
        else:
            return self.model.query(enc_tokens)


class ColbertRepresentationWriter(RepresentationWriter):
    def __init__(self, output_path):
        self.indexer = ColBertIndexer(output_path)

    def __enter__(self):
        print('Enter')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit')

    def write(self, batch_info, fields=None):
        print(batch_info['id'])
        print(batch_info['vector'].shape) # [B, seqlen, dim]
