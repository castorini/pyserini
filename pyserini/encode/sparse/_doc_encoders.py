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
from torch.cuda.amp import autocast
from transformers import BertTokenizer

from pyserini.encode import UniCoilEncoder, DocumentEncoder


class UniCoilDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.model = UniCoilEncoder.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, titles=None, expands=None, fp16=False):
        if titles:
            texts = [f'{title} {text}' for title, text in zip(titles, texts)]
        max_length = 512  # hardcode for now
        if expands:
            input_ids = self._tokenize_with_injects(texts, expands)
        else:
            input_ids = self.tokenizer(texts, max_length=max_length, padding='longest',
                                       truncation=True, add_special_tokens=True,
                                       return_tensors='pt').to(self.device)["input_ids"]
        if fp16:
            with autocast():
                with torch.no_grad():
                    batch_weights = self.model(input_ids).cpu().detach().numpy()
        else:
            batch_weights = self.model(input_ids).cpu().detach().numpy()
        batch_token_ids = input_ids.cpu().detach().numpy()
        return self._output_to_weight_dicts(batch_token_ids, batch_weights)

    def _output_to_weight_dicts(self, batch_token_ids, batch_weights):
        to_return = []
        for i in range(len(batch_token_ids)):
            weights = batch_weights[i].flatten()
            tokens = self.tokenizer.convert_ids_to_tokens(batch_token_ids[i])
            tok_weights = {}
            for j in range(len(tokens)):
                tok = str(tokens[j])
                weight = float(weights[j])
                if tok == '[CLS]':
                    continue
                if tok == '[PAD]':
                    break
                if tok not in tok_weights:
                    tok_weights[tok] = weight
                elif weight > tok_weights[tok]:
                    tok_weights[tok] = weight
            to_return.append(tok_weights)
        return to_return

    def _tokenize_with_injects(self, texts, expands):
        tokenized = []
        max_len = 0
        for text, expand in zip(texts, expands):
            text_ids = self.tokenizer.encode(text, add_special_tokens=False, max_length=400, truncation=True)
            expand_ids = self.tokenizer.encode(expand, add_special_tokens=False, max_length=100, truncation=True)
            injects = set()
            for tok_id in expand_ids:
                if tok_id not in text_ids:
                    injects.add(tok_id)
            all_tok_ids = [101] + text_ids + [102] + list(injects) + [102]  # 101: CLS, 102: SEP
            tokenized.append(all_tok_ids)
            cur_len = len(all_tok_ids)
            if cur_len > max_len:
                max_len = cur_len
        for i in range(len(tokenized)):
            tokenized[i] += [0] * (max_len - len(tokenized[i]))
        return torch.tensor(tokenized, device=self.device)
