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

import argparse

import pandas as pd

from tqdm import tqdm
from pyserini.query_iterator import get_query_iterator, TopicsFormat
from transformers import BertModel,  BertTokenizerFast
import torch

class DkrrDprQueryEncoder():

    def __init__(self, encoder: str = None, device: str = 'cpu', prefix: str = "question:"):
        self.device = device
        self.model = BertModel.from_pretrained(encoder)
        self.model.to(self.device)
        self.tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")
        self.prefix = prefix

    @staticmethod
    def _mean_pooling(model_output, attention_mask):
        model_output = model_output[0].masked_fill(1 - attention_mask[:, :, None], 0.)
        model_output = torch.sum(model_output, dim=1) / torch.clamp(torch.sum(attention_mask, dim=1), min=1e-9)[:, None]
        return model_output.flatten()

    def encode(self, query: str):
        if self.prefix:
            query = f'{self.prefix} {query}'
        inputs = self.tokenizer(query, return_tensors='pt', max_length=40, padding="max_length")
        inputs.to(self.device)
        outputs = self.model(input_ids=inputs["input_ids"],
                            attention_mask=inputs["attention_mask"])
        embeddings = self._mean_pooling(outputs, inputs['attention_mask']).detach().cpu().numpy()
        return embeddings.flatten()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=str, metavar='topic_name', required=True,
                        help="Name of topics.")
    parser.add_argument('--encoder', type=str, help='encoder name or path',
                        default='facebook/dpr-question_encoder-multiset-base', required=False)
    parser.add_argument('--output', type=str, help='path to store query embeddings', required=True)
    parser.add_argument('--device', type=str,
                        help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    args = parser.parse_args()

    query_iterator = get_query_iterator(args.topics, TopicsFormat(TopicsFormat.DEFAULT.value))
    topics = query_iterator.topics
    
    encoder = DkrrDprQueryEncoder(args.encoder, args.device)

    embeddings = {'id': [], 'text': [], 'embedding': []}
    for index, (topic_id, text) in enumerate(tqdm(query_iterator, total=len(topics.keys()))):
        embeddings['id'].append(topic_id)
        embeddings['text'].append(text)
        embeddings['embedding'].append(encoder.encode(text))
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(args.output)
