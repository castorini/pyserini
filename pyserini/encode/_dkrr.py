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
from transformers import (BertModel, BertTokenizerFast)

from pyserini.encode import QueryEncoder


class DkrrDprQueryEncoder(QueryEncoder):
    def __init__(self, encoder_dir: str = None, encoded_query_dir: str = None, device: str = 'cpu',
                 prefix: str = "question:", **kwargs):
        super().__init__(encoded_query_dir)
        self.device = device
        self.model = BertModel.from_pretrained(encoder_dir)
        self.model.to(self.device)
        self.tokenizer = BertTokenizerFast.from_pretrained('bert-base-uncased',
                                                           clean_up_tokenization_spaces=True)
        self.has_model = True
        self.prefix = prefix

    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        model_output = model_output[0].masked_fill(attention_mask[:, :, None] == 0, 0.)
        model_output = torch.sum(model_output, dim=1) / torch.clamp(torch.sum(attention_mask, dim=1), min=1e-9)[:, None]
        return model_output.flatten()

    def encode(self, query: str):
        if self.has_model:
            if self.prefix:
                query = f'{self.prefix} {query}'
            inputs = self.tokenizer(query, return_tensors='pt', max_length=40, padding="max_length")
            inputs.to(self.device)
            outputs = self.model(input_ids=inputs["input_ids"],
                                 attention_mask=inputs["attention_mask"])
            embeddings = self._mean_pooling(outputs, inputs['attention_mask']).detach().cpu().numpy()
            return embeddings.flatten()
        else:
            return super().encode(query)
