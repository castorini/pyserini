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
if torch.cuda.is_available():
    from torch.cuda.amp import autocast
from transformers import BertModel, BertTokenizer, BertTokenizerFast

from pyserini.encode import DocumentEncoder, QueryEncoder
from onnxruntime import ExecutionMode, SessionOptions, InferenceSession


class TctColBertDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name: str, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.onnx = False
        if model_name.endswith('onnx'):
            options = SessionOptions()
            self.session = InferenceSession(model_name, options)
            self.onnx = True
            self.tokenizer = BertTokenizerFast.from_pretrained(tokenizer_name or model_name[:-5])
        else:
            self.model = BertModel.from_pretrained(model_name)
            self.model.to(self.device)
            self.tokenizer = BertTokenizerFast.from_pretrained(tokenizer_name or model_name)

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
            if fp16:
                with autocast():
                    with torch.no_grad():
                        outputs = self.model(**inputs)
            else:
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
