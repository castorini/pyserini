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
import ABC
import abstractmethod
from typing import List, Dict
import numpy as np
import torch
from transformers import AutoModelForMaskedLM, AutoTokenizer

from pyserini.encode import QueryEncoder, DocumentEncoder


class SpladeEncoder(ABC):
    @abstractmethod
    def encode(self, **kwargs) -> List[Dict[str, float]] | Dict[str, float]:
        """Encode a text or a list of texts into a list of token weight dictionaries."""
        pass

    def _output_to_weight_dicts(self, batch_aggregated_logits):
        to_return = []
        for aggregated_logits in batch_aggregated_logits:
            col = np.nonzero(aggregated_logits)[0]
            weights = aggregated_logits[col]
            d = {self.reverse_voc[k]: float(v) for k, v in zip(list(col), list(weights))}
            to_return.append(d)
        return to_return

    def _get_encoded_query_token_wight_dicts(self, tok_weights):
        to_return = []
        for _tok_weight in tok_weights:
            _weights = {}
            for token, weight in _tok_weight.items():
                weight_quanted = round(weight / self.weight_range * self.quant_range)
                _weights[token] = weight_quanted
            to_return.append(_weights)
        return to_return

class SpladeDocumentEncoder(DocumentEncoder, SpladeEncoder):
    def __init__(self, model_name_or_path, tokenizer_name=None, device='cuda:0', prefix=None, **kwargs):
        self.device = device
        self.model = AutoModelForMaskedLM.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name_or_path,
                                                       clean_up_tokenization_spaces=True)
        self.reverse_voc = {v: k for k, v in self.tokenizer.vocab.items()}
        self.weight_range = 5
        self.quant_range = 256
        self.prefix = prefix

    def encode(self, texts, titles=None, max_length=512, add_sep=False, **kwargs) -> List[Dict[str, float]]:
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

        input_ids = inputs['input_ids']
        input_attention = inputs['attention_mask']
        batch_logits = self.model(input_ids)['logits']
        batch_aggregated_logits, _ = torch.max(torch.log(1 + torch.relu(batch_logits))
                                               * input_attention.unsqueeze(-1), dim=1)
        batch_aggregated_logits = batch_aggregated_logits.cpu().detach().numpy()
        raw_weights = self._output_to_weight_dicts(batch_aggregated_logits)
        return self._get_encoded_query_token_wight_dicts(raw_weights)


class SpladeQueryEncoder(QueryEncoder, SpladeEncoder):
    def __init__(self, model_name_or_path, tokenizer_name=None, device='cpu'):
        self.device = device
        self.model = AutoModelForMaskedLM.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name_or_path,
                                                       clean_up_tokenization_spaces=True)
        self.reverse_voc = {v: k for k, v in self.tokenizer.vocab.items()}
        self.weight_range = 5
        self.quant_range = 256

    def encode(self, text, max_length=256, **kwargs) -> Dict[str, float]:
        inputs = self.tokenizer([text], max_length=max_length, padding='longest',
                                truncation=True, add_special_tokens=True,
                                return_tensors='pt').to(self.device)
        input_ids = inputs['input_ids']
        input_attention = inputs['attention_mask']
        batch_logits = self.model(input_ids)['logits']
        batch_aggregated_logits, _ = torch.max(torch.log(1 + torch.relu(batch_logits))
                                               * input_attention.unsqueeze(-1), dim=1)
        batch_aggregated_logits = batch_aggregated_logits.cpu().detach().numpy()
        raw_weights = self._output_to_weight_dicts(batch_aggregated_logits)
        return self._get_encoded_query_token_wight_dicts(raw_weights)[0]
