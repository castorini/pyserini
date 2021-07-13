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

from transformers import AutoTokenizer

from pyserini.encode import QueryEncoder


class TokFreqQueryEncoder(QueryEncoder):
    def __init__(self, model_name_or_path=None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name_or_path) if model_name_or_path else None

    def encode(self, text, **kwargs):
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
