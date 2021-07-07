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

import json
from transformers import AutoTokenizer, BertTokenizer

from pyserini.encode import UniCoilEncoder, QueryEncoder


class PseudoQueryEncoder(QueryEncoder):
    def __init__(self, model_name_or_path):
        self.vectors = self._load_from_jsonl(model_name_or_path)

    @staticmethod
    def _load_from_jsonl(path):
        vectors = {}
        with open(path) as f:
            for line in f:
                info = json.loads(line)
                text = info['contents'].strip()
                vec = info['vector']
                vectors[text] = vec
        return vectors

    def encode(self, text):
        return self.vectors[text.strip()]


class TokFreqQueryEncoder(QueryEncoder):
    def __init__(self, model_name_or_path):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)

    def encode(self, text):
        vector = {}
        if self.tokenizer is not None:
            tok_list = self.tokenizer.tokenize(text)
        else:
            tok_list = text.strip().split()
        for tok in tok_list:
            if tok not in vector:
                vector[tok] = 1
            else:
                vector[tok] += 1
        return vector


class UniCoilQueryEncoder(QueryEncoder):
    def __init__(self, model_name_or_path, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.model = UniCoilEncoder.from_pretrained(model_name_or_path)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name_or_path)

    def encode(self, text):
        max_length = 128  # hardcode for now
        input_ids = self.tokenizer([text], max_length=max_length, padding='longest',
                                   truncation=True, add_special_tokens=True,
                                   return_tensors='pt').to(self.device)["input_ids"]
        batch_weights = self.model(input_ids).cpu().detach().numpy()
        batch_token_ids = input_ids.cpu().detach().numpy()
        return self._output_to_weight_dicts(batch_token_ids, batch_weights)[0]

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
