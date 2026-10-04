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

"""Encoders for NVIDIA Nemotron embedding models, e.g. nvidia/Nemotron-3-Embed-8B-BF16.

The model card specifies the contract this implements:

  * asymmetric prefixes, ``query: `` for queries and ``passage: `` for documents, and the prefix
    tokens are part of the pooled representation (``1_Pooling/config.json`` sets
    ``include_prompt: true``);
  * mean pooling over the unpadded tokens of ``last_hidden_state``;
  * L2 normalisation, so dot product and cosine similarity coincide -- which is what lets a flat
    inner-product Faiss index reproduce the model card's scores;
  * left padding, since the checkpoint is a decoder and the card's examples tokenise that way;
  * bfloat16 weights with FlashAttention-2 where available, falling back to SDPA.

The defaults here are the card's values, so a caller that passes no prefixes or pooling flags still
gets the intended behaviour.
"""

import torch
import torch.nn.functional as F
from torch import Tensor
from transformers import AutoModel, AutoTokenizer

from pyserini.encode import DocumentEncoder, QueryEncoder

DEFAULT_QUERY_PREFIX = 'query: '
DEFAULT_DOCUMENT_PREFIX = 'passage: '
DEFAULT_MAX_LENGTH = 32768


def mean_pool(last_hidden_state: Tensor, attention_mask: Tensor) -> Tensor:
    """Average the hidden states of the real tokens, ignoring padding.

    Written to match the model card's ``average_pool`` exactly, including the zero-fill before the
    sum, so padded positions cannot contribute even if the backbone emits non-zero states there.
    """
    masked = last_hidden_state.masked_fill(~attention_mask[..., None].bool(), 0.0)
    return masked.sum(dim=1) / attention_mask.sum(dim=1)[..., None]


def _load(model_name, dtype, attn_implementation):
    """Load the backbone, degrading to SDPA when FlashAttention-2 is unavailable.

    The card's snippets default to flash_attention_2 because the NVIDIA container ships flash-attn;
    a plain pip environment usually does not, and the resulting ImportError is unhelpful this deep
    in an indexing run.
    """
    try:
        return AutoModel.from_pretrained(model_name, dtype=dtype,
                                         attn_implementation=attn_implementation)
    except (ImportError, ValueError):
        if attn_implementation == 'sdpa':
            raise
        return AutoModel.from_pretrained(model_name, dtype=dtype, attn_implementation='sdpa')


def _tokenizer(model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name, padding_side='left')
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


class NemotronDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, device='cuda:0', **kwargs):
        self.device = device
        self.prefix = kwargs.get('prefix')
        if self.prefix is None:
            self.prefix = DEFAULT_DOCUMENT_PREFIX
        # the card states the embeddings are L2-normalised; normalising is part of the model's
        # contract rather than an option, so it is on unless a caller explicitly disables it
        self.l2_norm = kwargs.get('l2_norm', True)
        self.max_length = kwargs.get('max_length', DEFAULT_MAX_LENGTH)
        self.dtype = torch.bfloat16 if kwargs.get('fp16', True) else torch.float32
        self.tokenizer = _tokenizer(model_name)
        self.model = _load(model_name, self.dtype, kwargs.get('attn_implementation', 'flash_attention_2'))
        self.model.to(self.device).eval()

    def encode(self, texts, titles=None, max_length=None, **kwargs):
        if isinstance(texts, str):
            texts = [texts]
        if titles is not None:
            texts = [f'{title} {text}' for title, text in zip(titles, texts)]
        texts = [f'{self.prefix}{text}' for text in texts]
        inputs = self.tokenizer(texts, max_length=max_length or self.max_length, truncation=True,
                                padding=True, return_tensors='pt')
        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
        with torch.inference_mode():
            outputs = self.model(**inputs)
            embeddings = mean_pool(outputs.last_hidden_state, inputs['attention_mask'])
            if self.l2_norm:
                embeddings = F.normalize(embeddings, p=2, dim=-1)
        return embeddings.detach().cpu().to(torch.float32).numpy()


class NemotronQueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir=None, device='cpu', **kwargs):
        self.device = device
        self.prefix = kwargs.get('prefix')
        if self.prefix is None:
            self.prefix = DEFAULT_QUERY_PREFIX
        self.l2_norm = kwargs.get('l2_norm', True)
        self.max_length = kwargs.get('max_length', DEFAULT_MAX_LENGTH)
        self.dtype = torch.bfloat16 if kwargs.get('fp16', True) else torch.float32
        self.tokenizer = _tokenizer(encoder_dir)
        self.model = _load(encoder_dir, self.dtype, kwargs.get('attn_implementation', 'flash_attention_2'))
        self.model.to(self.device).eval()

    def encode(self, query: str, **kwargs):
        inputs = self.tokenizer([f'{self.prefix}{query}'], max_length=self.max_length,
                                truncation=True, padding=True, return_tensors='pt')
        inputs = {name: tensor.to(self.device) for name, tensor in inputs.items()}
        with torch.inference_mode():
            outputs = self.model(**inputs)
            embeddings = mean_pool(outputs.last_hidden_state, inputs['attention_mask'])
            if self.l2_norm:
                embeddings = F.normalize(embeddings, p=2, dim=-1)
        return embeddings.detach().cpu().to(torch.float32).numpy().flatten()
