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
import torch
from contextlib import nullcontext
from sklearn.preprocessing import normalize
from transformers import AutoModel, AutoTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


class AutoDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0', pooling='cls', l2_norm=False, prefix=None, fp16=False, padding_side='right'):
        self.device = device
        self.fp16 = fp16
        torch_dtype = torch.float16 if fp16 else torch.float32
        self.model = AutoModel.from_pretrained(model_name, torch_dtype=torch_dtype if device.startswith('cuda') else None)
        self.model.to(self.device)
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name,
                                                           clean_up_tokenization_spaces=True)
        except:
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name,
                                                           use_fast=False,
                                                           clean_up_tokenization_spaces=True)
        if self.tokenizer.pad_token_id is None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.tokenizer.padding_side = padding_side
        self.has_model = True
        self.pooling = pooling
        self.l2_norm = l2_norm
        self.prefix = prefix

    def encode(self, texts, titles=None, max_length=256, add_sep=False, **kwargs):
        if self.prefix is not None:
            texts = [f'{self.prefix} {text}' for text in texts]
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
        autocast_context = torch.amp.autocast('cuda') if self.fp16 and self.device.startswith('cuda') else nullcontext()
        with autocast_context:
            with torch.no_grad():
                outputs = self.model(**inputs)
        if self.pooling == "mean":
            embeddings = self._mean_pooling(outputs[0], inputs['attention_mask']).detach().cpu().numpy()
        elif self.pooling == "eos":
            attention_mask = inputs['attention_mask']
            last_hidden_state = outputs[0]
            left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
            if left_padding:
                embeddings = last_hidden_state[:, -1].detach().cpu().numpy()
            else:
                sequence_lengths = attention_mask.sum(dim=1) - 1
                batch_size = last_hidden_state.shape[0]
                embeddings = last_hidden_state[torch.arange(batch_size, device=last_hidden_state.device), sequence_lengths].detach().cpu().numpy()
        else:
            embeddings = outputs[0][:, 0, :].detach().cpu().numpy()
        if self.l2_norm:
            embeddings = normalize(embeddings, axis=1, norm='l2')
        return embeddings


class AutoQueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cpu',
                 pooling: str = 'cls', l2_norm: bool = False, prefix=None, fp16=False, padding_side='right', **kwargs):
        super().__init__(encoded_query_dir)
        if encoder_dir:
            self.device = device
            self.fp16 = fp16
            torch_dtype = torch.float16 if fp16 else torch.float32
            self.model = AutoModel.from_pretrained(encoder_dir, torch_dtype=torch_dtype if device.startswith('cuda') else None)
            self.model.to(self.device)
            try:
                self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or encoder_dir,
                                                               clean_up_tokenization_spaces=True)
            except:
                self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or encoder_dir,
                                                               use_fast=False,
                                                               clean_up_tokenization_spaces=True)
            if self.tokenizer.pad_token_id is None:
                self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
            self.tokenizer.padding_side = padding_side
            self.has_model = True
            self.pooling = pooling
            self.l2_norm = l2_norm
            self.prefix = prefix
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str, max_length=None):
        if self.has_model:
            if self.prefix:
                query = f'{self.prefix} {query}'
            tokenizer_kwargs = dict(
                add_special_tokens=True,
                return_tensors='pt',
                truncation='only_first',
                padding='longest',
                return_token_type_ids=False,
                return_attention_mask=True,
            )
            if max_length is not None:
                tokenizer_kwargs['max_length'] = max_length
            inputs = self.tokenizer(query, **tokenizer_kwargs)
            inputs.to(self.device)
            autocast_context = torch.amp.autocast('cuda') if self.fp16 and self.device.startswith('cuda') else nullcontext()
            with autocast_context:
                with torch.no_grad():
                    model_outputs = self.model(**inputs)
            last_hidden_state = model_outputs[0]
            if self.pooling == "mean":
                outputs = last_hidden_state.detach().cpu().numpy()
                embeddings = np.average(outputs, axis=-2)
            elif self.pooling == "eos":
                attention_mask = inputs['attention_mask']
                left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
                if left_padding:
                    embeddings = last_hidden_state[:, -1].detach().cpu().numpy()
                else:
                    sequence_lengths = attention_mask.sum(dim=1) - 1
                    batch_size = last_hidden_state.shape[0]
                    embeddings = last_hidden_state[torch.arange(batch_size, device=last_hidden_state.device), sequence_lengths].detach().cpu().numpy()
            else:
                outputs = last_hidden_state.detach().cpu().numpy()
                embeddings = outputs[:, 0, :]
            if self.l2_norm:
                embeddings = normalize(embeddings, norm='l2')
            return embeddings.flatten()
        else:
            return super().encode(query)
