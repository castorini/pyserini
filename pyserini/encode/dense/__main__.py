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
from pyserini.encode import JsonlEmbeddingWriter, FaissEmbeddingWriter, JsonlCollectionIterator
from pyserini.encode.dense import DprDocumentEncoder, TctColBertDocumentEncoder, \
    AnceDocumentEncoder, AutoDocumentEncoder


def init_encoder(encoder, device):
    if 'dpr' in encoder.lower():
        return DprDocumentEncoder(encoder, device=device)
    elif 'tct_colbert' in encoder.lower():
        return TctColBertDocumentEncoder(encoder, device=device)
    elif 'ance' in encoder.lower():
        return AnceDocumentEncoder(encoder, device=device)
    elif 'sentence-transformers' in encoder.lower():
        return AutoDocumentEncoder(encoder, device=device, pooling='mean', l2_norm=True)
    else:
        return AutoDocumentEncoder(encoder, device=device)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--corpus', type=str,
                        help='directory that contains corpus files to be encoded, in jsonl format.', required=True)
    parser.add_argument('--fields', help='fields that contents in jsonl has (in order)',
                        nargs='+', default=['text'], required=False)
    parser.add_argument('--encode-title', action='store_true')
    parser.add_argument('--batch', type=int, help='batch size', default=64)
    parser.add_argument('--shard-id', type=int, help='shard-id 0-based', default=0)
    parser.add_argument('--shard-num', type=int, help='number of shards', default=1)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cuda:0')
    parser.add_argument('--embeddings', type=str, help='directory to store encoded corpus', required=True)
    parser.add_argument('--to-faiss', action='store_true', default=False)
    args = parser.parse_args()

    encoder = init_encoder(args.encoder, device=args.device)
    if args.to_faiss:
        embedding_writer = FaissEmbeddingWriter(args.embeddings)
    else:
        embedding_writer = JsonlEmbeddingWriter(args.embeddings)
    collection_iterator = JsonlCollectionIterator(args.corpus, args.fields)

    with embedding_writer:
        for batch_info in collection_iterator(args.batch_size, args.shard_id, args.shard_num):
            if args.encode_title:
                embeddings = encoder.encode(texts=batch_info['text'], titles=batch_info['title'])
            else:
                embeddings = encoder.encode(texts=batch_info['text'])
            batch_info['vector'] = embeddings
            embedding_writer.write(batch_info, args.fields)
