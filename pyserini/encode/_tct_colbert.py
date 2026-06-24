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

from transformers import BertModel
from transformers.utils import logging as transformers_logging

from pyserini.encode._base import DocumentEncoder, QueryEncoder, load_bert_tokenizer


def _load_bert_backbone(model_name):
    # TCT-ColBERT checkpoints include BERT pretraining heads, but these encoders
    # only use the BERT backbone. Suppress the expected Transformers load report
    # for those extra cls.* weights while preserving diagnostics for real issues.
    verbosity = transformers_logging.get_verbosity()
    transformers_logging.set_verbosity_error()
    try:
        model, loading_info = BertModel.from_pretrained(model_name, output_loading_info=True)
    finally:
        transformers_logging.set_verbosity(verbosity)

    has_only_bert_pretraining_head_unexpected_keys = all(
        key.startswith('cls.predictions.') or key.startswith('cls.seq_relationship.')
        for key in loading_info['unexpected_keys']
    )
    if (
        loading_info['missing_keys']
        or loading_info['mismatched_keys']
        or loading_info['error_msgs']
        or not has_only_bert_pretraining_head_unexpected_keys
    ):
        transformers_logging.get_logger(__name__).warning(
            'BertModel load from %s had non-benign loading info: %s', model_name, loading_info
        )

    return model


class TctColBertDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name: str, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.onnx = False
        if model_name.endswith('onnx'):
            from onnxruntime import InferenceSession, SessionOptions

            options = SessionOptions()
            self.session = InferenceSession(model_name, options)
            self.onnx = True
            self.tokenizer = load_bert_tokenizer(
                tokenizer_name or model_name[:-5],
                clean_up_tokenization_spaces=True
            )
        else:
            self.model = _load_bert_backbone(model_name)
            self.model.to(self.device)
            self.tokenizer = load_bert_tokenizer(
                tokenizer_name or model_name,
                clean_up_tokenization_spaces=True
            )

    def encode(self, texts, titles=None, fp16=False,  max_length=512, **kwargs):
        if titles is not None:
            texts = [f'[CLS] [D] {title} {text}' for title, text in zip(titles, texts)]
        else:
            texts = ['[CLS] [D] ' + text for text in texts]
        inputs = self.tokenizer(
            texts,
            max_length=max_length,
            padding="longest",
            truncation=True,
            add_special_tokens=False,
            return_tensors='pt'
        )
        if self.onnx:
            inputs_onnx = {name: np.atleast_2d(value) for name, value in inputs.items()}
            inputs.to(self.device)
            outputs, _ = self.session.run(None, inputs_onnx)
            outputs = torch.from_numpy(outputs).to(self.device)
            embeddings = self._mean_pooling(outputs[:, 4:, :], inputs['attention_mask'][:, 4:])
        else:
            inputs.to(self.device)
            with torch.no_grad():
                if fp16 and str(self.device).startswith('cuda'):
                    with torch.amp.autocast('cuda'):
                        outputs = self.model(**inputs)
                else:
                    outputs = self.model(**inputs)
            embeddings = self._mean_pooling(outputs["last_hidden_state"][:, 4:, :], inputs['attention_mask'][:, 4:])
        return embeddings.detach().cpu().numpy()


class TctColBertQueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_queries_dir: str = None, device: str = 'cpu', **kwargs):
        super().__init__(encoded_queries_dir)
        if encoder_dir:
            self.device = device
            self.model = _load_bert_backbone(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = load_bert_tokenizer(
                tokenizer_name or encoder_dir,
                clean_up_tokenization_spaces=True
            )
            self.has_model = True
        if (not self.has_model) and (not self.has_encoded_queries):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one.')

    def encode(self, query: str):
        if self.has_model:
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
        else:
            return super().encode(query)
