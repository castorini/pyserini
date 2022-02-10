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

import os
import string
import torch
import torch.nn as nn
import contextlib
from transformers import BertModel, BertPreTrainedModel, BertTokenizer
from transformers import AutoTokenizer, PretrainedConfig
from transformers import DistilBertModel, DistilBertPreTrainedModel
from pyserini.encode import DocumentEncoder, QueryEncoder
from pyserini.encode import RepresentationWriter
from pyserini.index import ColBertIndexer


class ColBertConfig(PretrainedConfig):
    model_type = "colbert"

    def __init__(self, code_dim=128, **kwargs):
        self.code_dim = code_dim
        super().__init__(**kwargs)


class ColBERT(BertPreTrainedModel):

    def __init__(self, config):
        super().__init__(config)
        self.dim = 128
        self.bert = BertModel(config, add_pooling_layer=True)
        self.linear = nn.Linear(config.hidden_size, self.dim, bias=False)
        self.skiplist = dict()
        self.init_weights()

    def use_puct_mask(self, tokenizer):
        encode = lambda x: tokenizer.encode(x, add_special_tokens=False)[0]
        self.skiplist = {w: True
                for symbol in string.punctuation
                for w in [symbol, encode(symbol)]}

    def punct_mask(self, input_ids):
        PAD_CODE = 0
        mask = [
            [(x not in self.skiplist) and (x != PAD_CODE) for x in d]
            for d in input_ids.cpu().tolist()
        ]
        return mask

    def forward(self, Q, D):
        q_reps, _ = self.query(Q)
        d_reps, d_lens = self.doc(D)
        d_mask = D['attention_mask'].unsqueeze(-1)
        return self.score(q_reps, d_reps, d_mask)

    def query(self, inputs):
        Q = self.bert(**inputs)[0] # last-layer hidden state
        # Q: (B, Lq, H) -> (B, Lq, dim)
        Q = self.linear(Q)
        # return: (B, Lq, dim) normalized
        lengths = inputs['attention_mask'].sum(1).cpu().numpy()
        return torch.nn.functional.normalize(Q, p=2, dim=2), lengths

    def doc(self, inputs):
        D = self.bert(**inputs)[0]
        D = self.linear(D)
        # apply mask
        if self.skiplist:
            ids = inputs['input_ids']
            mask = torch.tensor(self.punct_mask(ids), device=ids.device)
            D = D * mask.unsqueeze(2).float()
        lengths = inputs['attention_mask'].sum(1).cpu().numpy()
        return torch.nn.functional.normalize(D, p=2, dim=2), lengths

    def score(self, Q, D, mask):
        # (B, Ld, dim) x (B, dim, Lq) -> (B, Ld, Lq)
        cmp_matrix = D @ Q.permute(0, 2, 1)
        cmp_matrix = cmp_matrix * mask # [B, Ld, Lq]
        best_match = cmp_matrix.max(1).values # best match per query
        scores = best_match.sum(-1) # sum score over each query
        return scores, cmp_matrix


class ColBERT_distil(DistilBertPreTrainedModel):
    config_class = ColBertConfig

    def __init__(self, config):
        super().__init__(config)
        self.distilbert = DistilBertModel(config)
        self.pooler = nn.Linear(config.hidden_size, config.code_dim)
        self.skiplist = dict()
        self.init_weights()

    def use_puct_mask(self, tokenizer):
        encode = lambda x: tokenizer.encode(x, add_special_tokens=False)[0]
        self.skiplist = {w: True
                for symbol in string.punctuation
                for w in [symbol, encode(symbol)]}

    def punct_mask(self, input_ids):
        PAD_CODE = 0
        mask = [
            [(x not in self.skiplist) and (x != PAD_CODE) for x in d]
            for d in input_ids.cpu().tolist()
        ]
        return mask

    def score(self, q_reps, p_reps, p_mask):
        cmp_matrix = torch.einsum('imk,ink->imn', [q_reps, p_reps])
        cmp_matrix = cmp_matrix.permute(0, 2, 1) # [B, Ld, Lq]
        score = cmp_matrix * p_mask
        score = score.max(dim=1).values.sum(dim=-1)
        return score, cmp_matrix

    def forward(self, qry, psg):
        q_reps, _ = self.query(qry)
        d_reps, d_lens = self.doc(psg)
        d_mask = psg['attention_mask'].unsqueeze(-1)
        return self.score(q_reps, d_reps, d_mask)

    def query(self, qry):
        qry_out = self.distilbert(**qry, return_dict=True)
        q_hidden = qry_out.last_hidden_state
        q_reps = self.pooler(q_hidden) # excluding [CLS]
        # apply mask
        if self.skiplist:
            q_ids = qry['input_ids']
            q_mask = torch.tensor(self.punct_mask(q_ids), device=q_ids.device)
            q_reps = q_reps * q_mask.unsqueeze(2).float()
        # normalize after masking
        q_reps = torch.nn.functional.normalize(q_reps, dim=2, p=2)
        lengths = qry['attention_mask'].sum(1).cpu().numpy()
        return q_reps, lengths

    def doc(self, psg):
        psg_out = self.distilbert(**psg, return_dict=True)
        p_hidden = psg_out.last_hidden_state
        p_reps = self.pooler(p_hidden) # excluding [CLS]
        # apply mask
        if self.skiplist:
            p_ids = psg['input_ids']
            p_mask = torch.tensor(self.punct_mask(p_ids), device=p_ids.device)
            p_reps = p_reps * p_mask.unsqueeze(2).float()
        # normalize after masking
        p_reps = torch.nn.functional.normalize(p_reps, dim=2, p=2)
        lengths = psg['attention_mask'].sum(1).cpu().numpy()
        return p_reps, lengths


class ColBertEncoder(DocumentEncoder):
    def __init__(self, model: str, prepend_tok: str,
        maxlen: Optional[int] = None, tokenizer: Optional[str] = None,
        device: Optional[str] = 'cuda:0', query_augment: bool = False):
        # determine encoder prepend token
        prepend_tokens = ['[Q]', '[D]']
        assert prepend_tok in prepend_tokens
        self.actual_prepend_tokens = ['[unused0]', '[unused1]'] # for compatibility of original Colbert ckpt
        prepend_map = dict(list(zip(prepend_tokens, self.actual_prepend_tokens)))
        self.actual_prepend_tok = prepend_map[prepend_tok]
        self.query_augment = (query_augment and prepend_tok == '[Q]')

        # load model
        if 'distil' in model:
            print('Using distil ColBERT:', model, tokenizer)
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer)
            self.model = ColBERT_distil.from_pretrained(model)
            self.dim = self.model.config.code_dim
            self.maxlen = {'[Q]': 32, '[D]': 128}[prepend_tok]
            self.prepend = False
        else:
            print('Using vanilla ColBERT:', model, tokenizer)
            self.model = ColBERT.from_pretrained(model,
                tie_word_embeddings=True
            )
            self.dim = 128
            self.maxlen = {'[Q]': 32, '[D]': 128}[prepend_tok]
            self.prepend = True
            # load tokenizer and add special tokens
            self.tokenizer = BertTokenizer.from_pretrained(tokenizer or model)
            self.tokenizer.add_special_tokens({
                'additional_special_tokens': self.actual_prepend_tokens
            })
            self.model.resize_token_embeddings(len(self.tokenizer))
            # mask punctuations
            self.model.use_puct_mask(self.tokenizer)

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
            # prepend special tokens
            content = f'{self.actual_prepend_tok} {content}' if self.prepend else content
            prepend_contents.append(content)

        # tokenize
        enc_tokens = self.tokenizer(prepend_contents, max_length=self.maxlen,
            padding='max_length' if self.query_augment else 'longest',
            truncation=True, return_tensors="pt")

        # query augmentation
        if self.query_augment:
            ids, mask = enc_tokens['input_ids'], enc_tokens['attention_mask']
            ids[ids == 0]   = 103
            #mask[mask == 0] = 1 # following original colbert, no mask change

        enc_tokens.to(self.device)

        if debug:
            for b, ids in enumerate(enc_tokens['input_ids']):
                print(f'--- ColBertEncoder Batch#{b} ---')
                print(self.tokenizer.decode(ids))

        # actual encoding
        if fp16:
            amp_ctx = torch.cuda.amp.autocast()
        else:
            amp_ctx = contextlib.nullcontext()

        with torch.no_grad():
            with amp_ctx:
                if self.actual_prepend_tok == self.actual_prepend_tokens[0]:
                    embs, lengths = self.model.query(enc_tokens)
                else:
                    embs, lengths = self.model.doc(enc_tokens)
                return embs, lengths


class ColbertRepresentationWriter(RepresentationWriter):
    def __init__(self, output_path, encoder):
        self.output_path = output_path
        self.dim = encoder.dim

    def __enter__(self):
        os.makedirs(self.output_path, exist_ok=True)
        self.indexer = ColBertIndexer(self.output_path, dim=self.dim)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.indexer.close()

    def write(self, batch_info, fields=None):
        vectors, lengths = batch_info['vector'] # [B, seqlen, dim], [length..]
        doc_ids = batch_info['id']
        self.indexer.write(vectors, doc_ids, lengths)
