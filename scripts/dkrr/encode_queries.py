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
import os

import pandas as pd
from tqdm import tqdm

from pyserini.encode.query import DkrrDprQueryEncoder
from pyserini.query_iterator import DefaultQueryIterator

ENCODER = 'castorini/dkrr-dpr-nq-retriever'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=str, help='path to topics file or topics name', required=True)
    parser.add_argument('--output', type=str, help='path to store query embeddings', required=True)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    args = parser.parse_args()

    encoder = DkrrDprQueryEncoder(encoder_dir=ENCODER, device=args.device)

    embeddings = {'id': [], 'text': [], 'embedding': []}
    for qid, text in tqdm(DefaultQueryIterator.from_topics(args.topics)):
        embeddings['id'].append(qid)
        embeddings['text'].append(text)
        embeddings['embedding'].append(encoder.encode(text))

    embeddings = pd.DataFrame(embeddings)
    output_dir = os.path.dirname(args.output)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    embeddings.to_pickle(args.output)
