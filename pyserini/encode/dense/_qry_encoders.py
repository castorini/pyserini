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
import sklearn
from transformers import (AutoModel, AutoTokenizer, BertModel, BertTokenizer, BertTokenizerFast,
                          DPRQuestionEncoder, DPRQuestionEncoderTokenizer, RobertaTokenizer)
from pyserini.encode import AnceEncoder, QueryEncoder


class TctColBertQueryEncoder(QueryEncoder):

    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu'):
        self.device = device
        self.model = BertModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, query: str):
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


class DprQueryEncoder(QueryEncoder):

    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu'):
        self.device = device
        self.model = DPRQuestionEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, query: str):
        input_ids = self.tokenizer(query, return_tensors='pt')
        input_ids.to(self.device)
        embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu().numpy()
        return embeddings.flatten()


class BprQueryEncoder(QueryEncoder):

    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu'):
        self.device = device
        self.model = DPRQuestionEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, query: str):
        input_ids = self.tokenizer(query, return_tensors='pt')
        input_ids.to(self.device)
        embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu()
        dense_embeddings = embeddings.numpy()
        return dense_embeddings.flatten()


class DkrrDprQueryEncoder(QueryEncoder):

    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu', prefix: str = "question:"):
        self.device = device
        self.model = BertModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizerFast.from_pretrained(tokenizer_name or model_name)
        self.prefix = prefix

    def encode(self, query: str):
        if self.prefix:
            query = f'{self.prefix} {query}'
        inputs = self.tokenizer(query, return_tensors='pt', max_length=40, padding="longest")
        inputs.to(self.device)
        embeddings = self.model(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"]
        )[0].detach().cpu()
        return np.average(embeddings, axis=-2).flatten()


class AnceQueryEncoder(QueryEncoder):

    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu'):
        self.device = device
        self.model = AnceEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = RobertaTokenizer.from_pretrained(tokenizer_name or tokenizer_name)

    def encode(self, query: str):
        inputs = self.tokenizer(
            [query],
            max_length=64,
            padding='longest',
            truncation=True,
            add_special_tokens=True,
            return_tensors='pt'
        )
        inputs.to(self.device)
        embeddings = self.model(inputs["input_ids"]).detach().cpu().numpy()
        return embeddings.flatten()


class AutoQueryEncoder(QueryEncoder):

    def __init__(self, model_name: str, tokenizer_name: str = None, device: str = 'cpu',
                 pooling: str = 'cls', l2_norm: bool = False):
        self.device = device
        self.model = AutoModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name)
        self.has_model = True
        self.pooling = pooling
        self.l2_norm = l2_norm

    def encode(self, query: str):
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
