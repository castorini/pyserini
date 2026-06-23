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

from pyserini.encode import BprQueryEncoder
from pyserini.query_iterator import DefaultQueryIterator


def parse_topics(topics):
    for topic_id, text in DefaultQueryIterator.from_topics(topics):
        yield topic_id, text


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', default='castorini/bpr-nq-question-encoder', required=False)
    parser.add_argument('--topics', type=str, help='path to topics file or self-contained topics name', required=True)
    parser.add_argument('--output', type=str, help='path to store query embeddings', required=True)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    parser.add_argument('--batch-size', type=int, help='query encoding batch size', default=256, required=False)
    args = parser.parse_args()

    model = BprQueryEncoder(encoder_dir=args.encoder, device=args.device)

    embeddings = {'id': [], 'text': [], 'dense_embedding': [], 'sparse_embedding': []}
    queries = list(parse_topics(args.topics))

    for qid, question in tqdm(queries):
        embeddings['id'].append(qid)
        embeddings['text'].append(question)
        ret = model.encode(question)
        embeddings['dense_embedding'].append(ret['dense'])
        embeddings['sparse_embedding'].append(ret['sparse'])

    embeddings = pd.DataFrame(embeddings)
    output_dir = os.path.dirname(args.output)

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    embeddings.to_pickle(args.output)
