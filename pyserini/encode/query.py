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
import inspect
import os
from itertools import islice

import numpy as np
import pandas as pd
from tqdm import tqdm

from pyserini.encode import (
    MMEB_IMPORT_ERROR,
    AnceQueryEncoder,
    ArcticQueryEncoder,
    AutoQueryEncoder,
    BprQueryEncoder,
    CosDprQueryEncoder,
    DprQueryEncoder,
    DseQueryEncoder,
    MMEBQueryEncoder,
    OpenAiQueryEncoder,
    SpladeQueryEncoder,
    TctColBertQueryEncoder,
    UniCoilQueryEncoder,
)
from pyserini.query_iterator import DefaultQueryIterator


def init_encoder(encoder, device, pooling, l2_norm, prefix, bpr):
    if bpr:
        return BprQueryEncoder(encoder, device=device)
    elif 'dpr' in encoder.lower():
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
    elif 'openai-api' in encoder.lower():
        return OpenAiQueryEncoder(encoder, device=device)
    elif 'cosdpr' in encoder.lower():
        return CosDprQueryEncoder(encoder, device=device)
    elif 'arctic' in encoder.lower():
        return ArcticQueryEncoder(encoder, device=device)
    elif 'dse' in encoder.lower():
        return DseQueryEncoder(encoder_dir=encoder, device=device, pooling=pooling, l2_norm=l2_norm)
    elif 'mmeb' in encoder.lower():
        if MMEBQueryEncoder is None:
            raise ValueError(f"MMEB's query encoder class is not available. Have you installed the vlm2vec-for-pyserini package? Detailed stack trace:\n {MMEB_IMPORT_ERROR}")
        return MMEBQueryEncoder(encoder_dir=encoder, device=device, pooling=pooling, l2_norm=l2_norm)
    else:
        return AutoQueryEncoder(encoder, device=device, pooling=pooling, l2_norm=l2_norm, prefix=prefix)


def encode_query(encoder, text, max_length):
    signature = inspect.signature(encoder.encode)
    if 'max_length' in signature.parameters:
        return encoder.encode(text, max_length=max_length)
    return encoder.encode(text)


def create_output_dir(output):
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--topics', type=str, help='path to topics file in tsv format or self-contained topics name', required=True)
    parser.add_argument('--encoder', type=str, help='encoder model name or path', required=True)
    parser.add_argument('--weight-range', type=int, help='range of weights for sparse embedding', required=False)
    parser.add_argument('--quant-range', type=int, help='range of quantization for sparse embedding', required=False)
    parser.add_argument('--output', type=str, help='path to stored encoded queries', required=True)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    parser.add_argument('--max-length', type=int, help='max length', default=256, required=False)
    parser.add_argument('--max-queries', type=int, help='maximum number of queries to encode', default=None, required=False)
    parser.add_argument('--pooling', type=str, help='pooling strategy', default='cls', choices=['cls', 'mean'], required=False)
    parser.add_argument('--l2-norm', action='store_true', help='whether to normalize embedding', default=False, required=False)
    parser.add_argument('--prefix', type=str, help='prefix query input', default=None, required=False)
    parser.add_argument('--bpr', action='store_true', help='encode BPR dense and binary query representations', default=False, required=False)
    args = parser.parse_args()

    if args.max_queries is not None and args.max_queries < 0:
        raise ValueError('--max-queries must be non-negative')

    encoder = init_encoder(args.encoder, device=args.device, pooling=args.pooling, l2_norm=args.l2_norm, prefix=args.prefix, bpr=args.bpr)
    query_iterator = DefaultQueryIterator.from_topics(args.topics)
    if args.max_queries is not None:
        query_iterator = islice(query_iterator, args.max_queries)

    is_sparse = False
    query_ids = []
    query_texts = []
    query_embeddings = []
    dense_embeddings = []
    sparse_embeddings = []
    for topic_id, text in tqdm(query_iterator):
        embedding = encode_query(encoder, text, args.max_length)
        if args.bpr:
            query_ids.append(topic_id)
            query_texts.append(text)
            dense_embeddings.append(embedding['dense'])
            sparse_embeddings.append(embedding['sparse'])
            continue
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

    create_output_dir(args.output)

    if is_sparse:
        with open(args.output, 'w') as f:
            for i in range(len(query_ids)):
                f.write(f"{query_ids[i]}\t{query_embeddings[i]}\n")
    elif args.bpr:
        embeddings = {
            'id': query_ids,
            'text': query_texts,
            'dense_embedding': dense_embeddings,
            'sparse_embedding': sparse_embeddings,
        }
        embeddings = pd.DataFrame(embeddings)
        embeddings.to_pickle(args.output)
    else:
        embeddings = {'id': query_ids, 'text': query_texts, 'embedding': query_embeddings}
        embeddings = pd.DataFrame(embeddings)
        embeddings.to_pickle(args.output)
