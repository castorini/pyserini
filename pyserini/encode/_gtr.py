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

import torch
import torch.nn.functional as F
from transformers import T5EncoderModel, T5Tokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


class GtrDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0', pooling='mean'):
        self.device = device
        self.model = T5EncoderModel.from_pretrained(model_name)
        self.model.to(self.device)

        try:
            self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name or model_name)
        except:
            self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name or model_name, use_fast=False)

        self.has_model = True
        self.pooling = pooling

    def encode(self, texts, titles=None, max_length=512, add_sep=False, **kwargs):
        shared_tokenizer_kwargs = dict(
            max_length=max_length,
            truncation=True,
            padding=True,
            return_attention_mask=True,
            return_token_type_ids=False,
            return_tensors='pt',
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

        embeddings = self._mean_pooling(outputs[0], inputs['attention_mask']).detach().cpu()
        embeddings = F.normalize(embeddings, p=2, dim=1).numpy()

        return embeddings

class GtrQueryEncoder(QueryEncoder):

    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cuda:0',
                 pooling: str = 'mean', **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.model = T5EncoderModel.from_pretrained(encoder_dir)
            self.model.to(self.device)
            try:
                self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name or encoder_dir)
            except:
                self.tokenizer = T5Tokenizer.from_pretrained(tokenizer_name or encoder_dir, use_fast=False)
            self.has_model = True
            self.pooling = pooling
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        token_embeddings = model_output[0]  # First element of model_output contains all token embeddings
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        sum_embeddings = torch.sum(token_embeddings * input_mask_expanded, 1)
        sum_mask = torch.clamp(input_mask_expanded.sum(1), min=1e-9)
        return sum_embeddings / sum_mask

    def encode(self, query: str):
        if self.has_model:
            inputs = self.tokenizer(
                query,
                return_tensors='pt',
                truncation='only_first',
                padding='longest',
                return_token_type_ids=False,
            )

            inputs.to(self.device)
            outputs = self.model(**inputs)

            embeddings = self._mean_pooling(outputs, inputs['attention_mask']).detach().cpu()
            embeddings = F.normalize(embeddings, p=2, dim=1).numpy()
            return embeddings.flatten()