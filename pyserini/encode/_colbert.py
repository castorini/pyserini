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
from transformers import BertModel, BertTokenizer, BertTokenizerFast
from pyserini.encode import DocumentEncoder, QueryEncoder
from pyserini.encode import RepresentationWriter

# Hacky: Import ColBertIndexer beyond top level module `pyserini.encode`
import os
import sys
script_path = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, f'{script_path}/../index')
from colbert import ColBertIndexer


class ColBertDocumentEncoder(DocumentEncoder):
    def __init__(self, model_name: str, tokenizer_name=None, device='cuda:0'):
        self.device = device
        self.model = BertModel.from_pretrained(model_name)
        self.model.to(self.device)
        self.tokenizer = BertTokenizer.from_pretrained(tokenizer_name or model_name)

    def encode(self, texts, titles=None, fp16=False, **kwargs):
        return None #embeddings.detach().cpu().numpy()


class ColBertQueryEncoder(QueryEncoder):
    pass


class ColbertRepresentationWriter(RepresentationWriter):
    def __enter__(self):
        print('Enter')

    def __exit__(self, exc_type, exc_val, exc_tb):
        print('Exit')

    def write(self, batch_info, fields=None):
        print('Write')
