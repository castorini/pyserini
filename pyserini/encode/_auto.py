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

import numpy as np
from sklearn.preprocessing import normalize
from transformers import AutoModel, AutoTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


class AutoDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0', pooling='cls', l2_norm=False):
        self.device = device
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name)
        except:
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name, use_fast=False)
        self.has_model = True
        self.pooling = pooling
        self.l2_norm = l2_norm

    def encode(self, texts, titles=None, max_length=256, add_sep=False, **kwargs):
        shared_tokenizer_kwargs = dict(
            max_length=max_length,
            truncation=True,
            padding='longest',
            return_attention_mask=True,
            return_token_type_ids=False,
            return_tensors='pt',
            add_special_tokens=True,
        )
        input_kwargs = {}
        if not add_sep:
            input_kwargs["text"] = [f'{title} {text}' for title, text in zip(titles, texts)] if titles is not None else texts
        else:
            if titles is not None:
                input_kwargs["text"] = titles
                input_kwargs["text_pair"] = texts
            else:
                input_kwargs["text"] = texts

        inputs = self.tokenizer(**input_kwargs, **shared_tokenizer_kwargs)
        inputs.to(self.device)
        outputs = self.model(**inputs)
        if self.pooling == "mean":
            embeddings = self._mean_pooling(outputs[0], inputs['attention_mask']).detach().cpu().numpy()
        else:
            embeddings = outputs[0][:, 0, :].detach().cpu().numpy()
        if self.l2_norm:
            normalize(embeddings, axis=1)
        return embeddings


class AutoQueryEncoder(QueryEncoder):
    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu',
                 pooling: str = 'cls', l2_norm: bool = False, prefix=None):
        self.device = device
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name)
        self.pooling = pooling
        self.l2_norm = l2_norm
        self.prefix = prefix

    def encode(self, query: str, **kwargs):
        if self.prefix:
            query = f'{self.prefix} {query}'
        inputs = self.tokenizer(
            query,
            add_special_tokens=True,
            return_tensors='pt',
            truncation='only_first',
            padding='longest',
            return_token_type_ids=False,
        )
        inputs.to(self.device)
        outputs = self.model(**inputs)[0].detach().cpu().numpy()
        if self.pooling == "mean":
            embeddings = np.average(outputs, axis=-2)
        else:
            embeddings = outputs[:, 0, :]
        if self.l2_norm:
            embeddings = normalize(outputs, norm='l2')
        return embeddings.flatten()
