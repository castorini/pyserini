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

import sklearn
import numpy as np
from transformers import AutoModel, AutoTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


class AutoDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0', pooling='cls', l2_norm=False):
        self.device = device
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name)
        self.has_model = True
        self.pooling = pooling
        self.l2_norm = l2_norm

    def encode(self, texts, titles=None, **kwargs):
        if titles:
            texts = [f'{title} {text}' for title, text in zip(titles, texts)]
        inputs = self.tokenizer(
            texts,
            max_length=512,
            padding='longest',
            truncation=True,
            add_special_tokens=True,
            return_tensors='pt'
        )
        inputs.to(self.device)
        outputs = self.model(**inputs)
        if self.pooling == "mean":
            embeddings = self._mean_pooling(outputs[0], inputs['attention_mask']).detach().cpu().numpy()
        else:
            embeddings = outputs[0][:, 0, :].detach().cpu().numpy()
        if self.l2_norm:
            sklearn.preprocessing.normalize(embeddings, axis=1)
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
            padding='longest',
            truncation=True,
            add_special_tokens=True,
            return_tensors='pt'
        )
        inputs.to(self.device)
        outputs = self.model(**inputs)[0].detach().cpu().numpy()
        if self.pooling == "mean":
            embeddings = np.average(outputs, axis=-2)
        else:
            embeddings = outputs[:, 0, :]
        if self.l2_norm:
            embeddings = sklearn.preprocessing.normalize(outputs, norm='l2')
        return embeddings.flatten()
