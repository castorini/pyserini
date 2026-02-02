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
from transformers import AutoModel, AutoTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder


def last_token_pool(last_hidden_states: Tensor, attention_mask: Tensor) -> Tensor:
    left_padding = attention_mask[:, -1].sum() == attention_mask.shape[0]
    if left_padding:
        return last_hidden_states[:, -1]
    else:
        sequence_lengths = attention_mask.sum(dim=1) - 1
        batch_size = last_hidden_states.shape[0]
        return last_hidden_states[
            torch.arange(batch_size, device=last_hidden_states.device), sequence_lengths
        ]


class Qwen3DocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, device='cuda:0', **kwargs):
        self.device = device
        self.l2_norm = kwargs.get('l2_norm', False)
        self.prefix = kwargs.get('prefix', '')
        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name, padding_side='left', trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(model_name, trust_remote_code=True)
        self.model.to(device=self.device).eval()

    def encode(self, texts, **kwargs):
        max_length = kwargs.get('max_length', 8192)
        # For document encoders, fp16 is passed at encode time.
        self.dtype = torch.bfloat16 if kwargs.get('fp16', False) else torch.float32
        self.model.to(device=self.device, dtype=self.dtype).eval()
        if isinstance(texts, str):
            texts = [texts]
        texts = [f"{self.prefix}{t}" for t in texts]
        batch_dict = self.tokenizer(
            texts,
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        batch_dict = {k: v.to(device=self.device) for k, v in batch_dict.items()}

        with torch.no_grad():
            with torch.autocast(device_type=self.device, dtype=self.dtype):
                outputs = self.model(**batch_dict)
            embeddings = last_token_pool(
                outputs.last_hidden_state, batch_dict['attention_mask']
            )
            if self.l2_norm:
                embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.cpu().float().numpy()


class Qwen3QueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir, device='cuda:0', **kwargs):
        self.prefix = kwargs.get('prefix', '')
        self.device = device
        self.l2_norm = kwargs.get('l2_norm', False)
        # For query encoders, fp16 is passed at initialization time.
        self.dtype = torch.bfloat16 if kwargs.get('fp16', False) else torch.float32
        self.tokenizer = AutoTokenizer.from_pretrained(
            encoder_dir, padding_side='left', trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            encoder_dir, trust_remote_code=True, torch_dtype=self.dtype
        )
        self.model.to(device=self.device, dtype=self.dtype).eval()

    def encode(self, query: str, **kwargs):
        max_length = kwargs.get('max_length', 8192)
        text = f"{self.prefix}{query}" if self.prefix else query
        batch_dict = self.tokenizer(
            [text],
            padding=True,
            truncation=True,
            max_length=max_length,
            return_tensors="pt",
        )
        batch_dict = {k: v.to(device=self.device) for k, v in batch_dict.items()}
        with torch.no_grad():
            with torch.autocast(device_type=self.device, dtype=self.dtype):
                outputs = self.model(**batch_dict)
            embeddings = last_token_pool(
                outputs.last_hidden_state, batch_dict['attention_mask']
            )
            if self.l2_norm:
                embeddings = F.normalize(embeddings, p=2, dim=1)
        return embeddings.cpu().float().numpy().flatten()
