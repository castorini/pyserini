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
from transformers import BertModel, BertTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


class TctColBertDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.model = BertModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, titles=None, **kwargs):
        if titles is not None:
            texts = [f'[CLS] [D] {title} {text}' for title, text in zip(titles, texts)]
        else:
            texts = ['[CLS] [D] ' + text for text in texts]
        max_length = 154  # hardcode for now
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
        embeddings = self._mean_pooling(outputs["last_hidden_state"][:, 4:, :], inputs['attention_mask'][:, 4:])
        return embeddings.detach().cpu().numpy()


class TctColBertQueryEncoder(QueryEncoder):
    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu'):
        self.device = device
        self.model = BertModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, query: str, **kwargs):
        max_length = 36  # hardcode for now
        inputs = self.tokenizer(
            '[CLS] [Q] ' + query + '[MASK]' * max_length,
            max_length=max_length,
            truncation=True,
            add_special_tokens=False,
            return_tensors='pt'
        )
        inputs.to(self.device)
        outputs = self.model(**inputs)
        embeddings = outputs.last_hidden_state.detach().cpu().numpy()
        return np.average(embeddings[:, 4:, :], axis=-2).flatten()
