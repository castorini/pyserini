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

import os

import pandas as pd
import torch
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer

from pyserini.encode import QueryEncoder


class BprQueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir: str = None, tokenizer_name: str = None,
                 encoded_query_dir: str = None, device: str = 'cpu', **kwargs):
        self.has_model = False
        self.has_encoded_query = False

        if encoded_query_dir:
            self.embedding = self._load_embeddings(encoded_query_dir)
            self.has_encoded_query = True

        if encoder_dir:
            self.device = device
            self.model = DPRQuestionEncoder.from_pretrained(encoder_dir)
            self.model.to(self.device)
            self.tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(tokenizer_name or encoder_dir,
                                                                         clean_up_tokenization_spaces=True)
            self.has_model = True

        if (not self.has_model) and (not self.has_encoded_query):
            raise Exception('Neither query encoder model nor encoded queries provided. Please provide at least one')

    def encode(self, query: str):
        if self.has_model:
            input_ids = self.tokenizer(query, return_tensors='pt')
            input_ids.to(self.device)
            embeddings = self.model(input_ids["input_ids"]).pooler_output.detach().cpu()
            dense_embeddings = embeddings.numpy()
            sparse_embeddings = self.convert_to_binary_code(embeddings).numpy()
            return {'dense': dense_embeddings.flatten(), 'sparse': sparse_embeddings.flatten()}
        else:
            return super().encode(query)

    def convert_to_binary_code(self, input_repr: torch.Tensor):
        return input_repr.new_ones(input_repr.size()).masked_fill_(input_repr < 0, -1.0)

    @staticmethod
    def _load_embeddings(encoded_query_dir):
        df = pd.read_pickle(os.path.join(encoded_query_dir, 'embedding.pkl'))
        ret = {}
        for text, dense, sparse in zip(df['text'].tolist(), df['dense_embedding'].tolist(),
                                       df['sparse_embedding'].tolist()):
            ret[text] = {'dense': dense, 'sparse': sparse}
        return ret
