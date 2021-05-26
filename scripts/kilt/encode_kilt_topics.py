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

from pyserini.dsearch import DprQueryEncoder
from pyserini.query_iterator import get_query_iterator, TopicsFormat

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Compute embeddings for KILT topics')
    parser.add_argument('--topics', required=True)
    parser.add_argument('--output', default="embedding.pkl", help="Name and path to output file.")
    parser.add_argument('--encoder', metavar='path to query encoder checkpoint or encoder name',
                        required=True,
                        help="Path to query encoder pytorch checkpoint or hgf encoder model name")
    parser.add_argument('--tokenizer', metavar='name or path',
                        required=True,
                        help="Path to a hgf tokenizer name or path")
    parser.add_argument('--device', metavar='device to run query encoder', required=False, default='cpu',
                        help="Device to run query encoder, cpu or [cuda:0, cuda:1, ...]")
    args = parser.parse_args()

    query_iterator = get_query_iterator(args.topics, TopicsFormat.KILT)
    query_encoder = DprQueryEncoder(encoder_dir=args.encoder, tokenizer_name=args.tokenizer, device=args.device)

    texts = []
    embeddings = []
    for i, (topic_id, text) in enumerate(tqdm(query_iterator)):
        texts.append(text)
        embeddings.append(query_encoder.encode(text))

    df = pd.DataFrame({
        'text': texts,
        'embedding': embeddings
    })

    df.to_pickle(args.output)
