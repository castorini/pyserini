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
from torch import Tensor
from transformers import AutoTokenizer, AutoModel

from pyserini.encode import DocumentEncoder, QueryEncoder

def last_token_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    left_padding = (attention_mask[:, -1].sum() == attention_mask.shape[0])
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths]

class Qwen3DocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0', l2_norm=True, prefix=None, **kwargs):
        self.device = device
        self.l2_norm = l2_norm
        self.prefix = prefix or ''
        self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or model_name, padding_side='left',
                                                       trust_remote_code=True, clean_up_tokenization_spaces=True)
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        self.model.to(self.device).eval()

    def encode(self, texts, titles=None, **kwargs):
        max_length = 16384
        if isinstance(texts, str):
            texts = [texts]
        if titles is not None:
            texts = [f"{t} {d}" if t else d for t, d in zip(titles, texts)]
        texts = [f"{self.prefix}{t}" for t in texts]

        batch_dict = self.tokenizer(texts, padding=True, truncation=True, max_length=max_length, return_tensors="pt")
        batch_dict = {k: v.to(self.device) for k, v in batch_dict.items()}

        with torch.no_grad():
            outputs = self.model(**batch_dict)
            embeddings = last_token_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
            if self.l2_norm:
                embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.cpu().numpy()

class Qwen3QueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir, tokenizer_name=None, encoded_query_dir=None,
                 device='cuda:0', l2_norm=True, prefix=None, **kwargs):
        super().__init__(encoded_query_dir)
        self.prefix = prefix or ''
        if encoder_dir:
            self.device = device
            self.l2_norm = l2_norm
            self.tokenizer = AutoTokenizer.from_pretrained(tokenizer_name or encoder_dir, padding_side='left',
                                                           trust_remote_code=True, clean_up_tokenization_spaces=True)
            self.model = AutoModel.from_pretrained(encoder_dir, trust_remote_code=True)
            self.model.to(self.device).eval()
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one.')

    def encode(self, query: str, **kwargs):
        if self.has_model:
            max_length = 16384
            text = f"{self.prefix}{query}" if self.prefix else query
            batch_dict = self.tokenizer([text], padding=True, truncation=True, max_length=max_length, return_tensors="pt")
            batch_dict = {k: v.to(self.device) for k, v in batch_dict.items()}

            with torch.no_grad():
                outputs = self.model(**batch_dict)
                embeddings = last_token_pool(outputs.last_hidden_state, batch_dict['attention_mask'])
                if self.l2_norm:
                    embeddings = F.normalize(embeddings, p=2, dim=1)
            return embeddings.cpu().numpy().flatten()
        else:
            return super().encode(query)
