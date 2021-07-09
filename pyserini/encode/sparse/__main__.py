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
from pyserini.encode import JsonlCollectionIterator, JsonlEmbeddingWriter
from pyserini.encode.sparse import UniCoilDocumentEncoder


def init_encoder(encoder, device):
    if 'unicoil' in encoder.lower():
        return UniCoilDocumentEncoder(encoder, device=device)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--corpus', type=str,
                        help='directory that contains corpus files to be encoded, in jsonl format.', required=True)
    parser.add_argument('--fields', help='fields that contents in jsonl has (in order)',
                        nargs='+', default=['text'], required=False)
    parser.add_argument('--embeddings', type=str, help='directory to store encoded corpus', required=True)
    parser.add_argument('--batch-size', type=int, help='batch size', default=16)
    parser.add_argument('--shard-id', type=int, help='shard-id 0-based', default=0)
    parser.add_argument('--shard-num', type=int, help='number of shards', default=1)
    parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]', default='cuda:0')
    parser.add_argument('--encode-title', action='store_true', required=False)
    parser.add_argument('--encode-expand', action='store_true', required=False)
    parser.add_argument('--fp16', action='store_true', required=False)
    args = parser.parse_args()

    encoder = init_encoder(args.encoder, device=args.device)
    collection_iterator = JsonlCollectionIterator(args.corpus, args.fields)
    embedding_writer = JsonlEmbeddingWriter(args.embeddings)

    with embedding_writer:
        for batch_info in collection_iterator(args.batch_size, args.shard_id, args.shard_num):
            kwargs = {
                'texts': batch_info['text'],
                'titles': batch_info['title'] if args.encode_title else None,
                'expands': batch_info['expand'] if args.encode_expand else None
            }
            embeddings = encoder.encode(**kwargs, fp16=args.fp16)
            batch_info['vector'] = embeddings
            embedding_writer.write(batch_info, args.fields)
