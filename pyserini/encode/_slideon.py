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

from typing import Dict, List

import numpy as np
import torch
from transformers import AutoModel, AutoTokenizer

from ._base import DocumentEncoder, QueryEncoder


class _SlideOnEncoder:
    """Shared loading, task-aware preprocessing, and Lucene impact conversion."""

    def _init_model(self, model_name_or_path, tokenizer_name, device, task):
        self.scale = np.float32(100)
        self.max_active_dims = 64 if task == 'query' else 512
        self.device = device
        self.task = task
        self.model = AutoModel.from_pretrained(
            model_name_or_path, trust_remote_code=True,
            dtype=torch.float32, attn_implementation='eager',
        ).to(self.device).eval()
        self.tokenizer = AutoTokenizer.from_pretrained(
            tokenizer_name or model_name_or_path, trust_remote_code=True,
        )
        # Match the official SlideOn adapter's padding-token selection for batches.
        if self.tokenizer.mask_token_id is not None:
            self.tokenizer.pad_token_id = self.tokenizer.mask_token_id
        elif self.tokenizer.eos_token_id is not None:
            self.tokenizer.pad_token_id = self.tokenizer.eos_token_id
        self.prefix = self.model.config.inference['prompts'][task]
        self.max_length = self.model.config.inference[task + '_length']
        self.prefix_token = self.model.config.tokenizer_settings.get(task + '_prefix', '')

    @torch.inference_mode()
    def _encode(self, texts, max_length=None) -> List[Dict[str, int]]:
        max_length = self.max_length if max_length is None else max_length
        if not texts:
            return []
        inputs = dict(self.tokenizer(
            [(self.prefix + text).strip() for text in texts],
            max_length=max_length - bool(self.prefix_token), truncation=True, padding=True,
            add_special_tokens=True, return_attention_mask=True,
            return_tensors='pt',
        ))
        # A configured prefix token is distinct from the textual query/document prompt.
        if self.prefix_token:
            prefix_id = self.tokenizer.convert_tokens_to_ids(self.prefix_token)
            for name, value in inputs.items():
                fill = prefix_id if name == 'input_ids' else (1 if name == 'attention_mask' else 0)
                marker = torch.full((value.shape[0], 1), fill, dtype=value.dtype, device=value.device)
                inputs[name] = torch.cat((value[:, :1], marker, value[:, 1:]), dim=1)
        inputs = {key: value.to(self.device) for key, value in inputs.items()
                  if key in ('input_ids', 'attention_mask', 'token_type_ids')}
        # Delegate pruning, including its position before final FP16 rounding, to SlideOn.
        output = self.model(**inputs, task=self.task, max_active_dims=self.max_active_dims)
        weights = output['sentence_embedding'].float().cpu().numpy()
        return [self._quantize_weights(vector) for vector in weights]

    def _quantize_weights(self, weights) -> Dict[str, int]:
        weights = np.asarray(weights, dtype=np.float32)
        if weights.ndim != 1 or not np.isfinite(weights).all() or np.any(weights < 0):
            raise ValueError('Expected a one-dimensional vector of finite nonnegative weights')
        indices = np.flatnonzero(weights > 0)
        with np.errstate(over='ignore'):
            impacts = np.rint(weights[indices] * self.scale)
        if not np.isfinite(impacts).all() or np.any(impacts >= np.float32(2**31)):
            raise ValueError('Quantized weight exceeds the Java int range')
        return {str(int(index)): int(impact) for index, impact in zip(indices, impacts) if impact > 0}


class SlideOnQueryEncoder(QueryEncoder, _SlideOnEncoder):
    """Encode query text as latent-ID-to-impact weights using q64 and scale 100.

    Loading executes the checkpoint's custom code via ``trust_remote_code=True``.
    """

    def __init__(self, model_name_or_path, tokenizer_name=None, device='cpu'):
        self._init_model(model_name_or_path, tokenizer_name, device, 'query')

    def encode(self, text, max_length=None, **kwargs) -> Dict[str, int]:
        if not isinstance(text, str):
            raise TypeError('SlideOn accepts text strings only')
        return self._encode([text], max_length=max_length)[0]


class SlideOnDocumentEncoder(DocumentEncoder, _SlideOnEncoder):
    """Encode documents as latent-ID-to-impact weights using d512 and scale 100.

    Returns one dictionary per document. Loading executes the checkpoint's custom
    code via ``trust_remote_code=True``.
    """

    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        self._init_model(model_name, tokenizer_name, device, 'document')

    def encode(self, texts, max_length=None, **kwargs) -> List[Dict[str, int]]:
        texts = [texts] if isinstance(texts, str) else list(texts)
        if not all(isinstance(text, str) for text in texts):
            raise TypeError('SlideOn accepts text strings only')
        return self._encode(texts, max_length=max_length)
