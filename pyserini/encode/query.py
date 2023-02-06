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

from tqdm import tqdm
import numpy as np
import pandas as pd
from pyserini.query_iterator import DefaultQueryIterator
from pyserini.encode import DprQueryEncoder, TctColBertQueryEncoder, AnceQueryEncoder, AutoQueryEncoder
from pyserini.encode import UniCoilQueryEncoder, SpladeQueryEncoder


def init_encoder(encoder, device):
    if 'dpr' in encoder.lower():
        return DprQueryEncoder(encoder, device=device)
    elif 'tct' in encoder.lower():
        return TctColBertQueryEncoder(encoder, device=device)
    elif 'ance' in encoder.lower():
        return AnceQueryEncoder(encoder, device=device, tokenizer_name='roberta-base')
    elif 'sentence-transformers' in encoder.lower():
        return AutoQueryEncoder(encoder, device=device, pooling='mean', l2_norm=True)
    elif 'unicoil' in encoder.lower():
        return UniCoilQueryEncoder(encoder, device=device)
    elif 'splade' in encoder.lower():
        return SpladeQueryEncoder(encoder, device=device)
    else:
        return AutoQueryEncoder(encoder, device=device)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=str,
                        help='path to topics file in tsv format or self-contained topics name', required=True)
    parser.add_argument('--encoder', type=str, help='encoder model name or path', required=True)
    parser.add_argument('--weight-range', type=int, help='range of weights for sparse embedding', required=False)
    parser.add_argument('--quant-range', type=int, help='range of quantization for sparse embedding', required=False)
    parser.add_argument('--output', type=str, help='path to stored encoded queries', required=True)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]',
                        default='cpu', required=False)
    args = parser.parse_args()

    encoder = init_encoder(args.encoder, device=args.device)
    query_iterator = DefaultQueryIterator.from_topics(args.topics)

    is_sparse = False
    query_ids = []
    query_texts = []
    query_embeddings = []
    for topic_id, text in tqdm(query_iterator):
        embedding = encoder.encode(text)
        if isinstance(embedding, dict):
            is_sparse = True
            pseudo_str = []
            for tok, weight in embedding.items():
                weight_quanted = int(np.round(weight/args.weight_range*args.quant_range))
                pseudo_str += [tok] * weight_quanted
            pseudo_str = " ".join(pseudo_str)
            embedding = pseudo_str
        query_ids.append(topic_id)
        query_texts.append(text)
        query_embeddings.append(embedding)
    if is_sparse:
        with open(args.output, 'w') as f:
            for i in range(len(query_ids)):
                f.write(f"{query_ids[i]}\t{query_embeddings[i]}\n")
    else:
        embeddings = {'id': query_ids, 'text': query_texts, 'embedding': query_embeddings}
        embeddings = pd.DataFrame(embeddings)
        embeddings.to_pickle(args.output)
