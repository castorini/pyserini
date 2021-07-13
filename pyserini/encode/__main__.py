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
import sys

from pyserini.encode import JsonlRepresentationWriter, FaissRepresentationWriter, JsonlCollectionIterator
from pyserini.encode import DprDocumentEncoder, TctColBertDocumentEncoder, AnceDocumentEncoder, AutoDocumentEncoder
from pyserini.encode import UniCoilDocumentEncoder


def init_encoder(encoder, device):
    if 'dpr' in encoder.lower():
        return DprDocumentEncoder(encoder, device=device)
    elif 'tct_colbert' in encoder.lower():
        return TctColBertDocumentEncoder(encoder, device=device)
    elif 'ance' in encoder.lower():
        return AnceDocumentEncoder(encoder, device=device)
    elif 'sentence-transformers' in encoder.lower():
        return AutoDocumentEncoder(encoder, device=device, pooling='mean', l2_norm=True)
    elif 'unicoil' in encoder.lower():
        return UniCoilDocumentEncoder(encoder, device=device)
    else:
        return AutoDocumentEncoder(encoder, device=device)


def parse_args(parser, commands):
    # Divide argv by commands
    split_argv = [[]]
    for c in sys.argv[1:]:
        if c in commands.choices:
            split_argv.append([c])
        else:
            split_argv[-1].append(c)
    # Initialize namespace
    args = argparse.Namespace()
    for c in commands.choices:
        setattr(args, c, None)
    # Parse each command
    parser.parse_args(split_argv[0], namespace=args)  # Without command
    for argv in split_argv[1:]:  # Commands
        n = argparse.Namespace()
        setattr(args, argv[0], n)
        parser.parse_args(argv, namespace=n)
    return args


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(title='sub-commands')
    input_parser = commands.add_parser('input')
    input_parser.add_argument('--corpus', type=str,
                              help='directory that contains corpus files to be encoded, in jsonl format.',
                              required=True)
    input_parser.add_argument('--fields', help='fields that contents in jsonl has (in order)',
                              nargs='+', default=['text'], required=False)
    input_parser.add_argument('--shard-id', type=int, help='shard-id 0-based', default=0, required=False)
    input_parser.add_argument('--shard-num', type=int, help='number of shards', default=1, required=False)

    output_parser = commands.add_parser('output')
    output_parser.add_argument('--embeddings', type=str, help='directory to store encoded corpus', required=True)
    output_parser.add_argument('--to-faiss', action='store_true', default=False)

    encoder_parser = commands.add_parser('encoder')
    encoder_parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    encoder_parser.add_argument('--fields', help='fields to encode', nargs='+', default=['text'], required=False)
    encoder_parser.add_argument('--batch-size', type=int, help='batch size', default=64, required=False)
    encoder_parser.add_argument('--device', type=str, help='device cpu or cuda [cuda:0, cuda:1...]',
                                default='cuda:0', required=False)
    encoder_parser.add_argument('--fp16', action='store_true', default=False)

    args = parse_args(parser, commands)

    encoder = init_encoder(args.encoder.encoder, device=args.encoder.device)
    if args.output.to_faiss:
        embedding_writer = FaissRepresentationWriter(args.output.embeddings)
    else:
        embedding_writer = JsonlRepresentationWriter(args.output.embeddings)
    collection_iterator = JsonlCollectionIterator(args.input.corpus, args.input.fields)

    with embedding_writer:
        for batch_info in collection_iterator(args.encoder.batch_size, args.input.shard_id, args.input.shard_num):
            kwargs = {
                'texts': batch_info['text'],
                'titles': batch_info['title'] if 'title' in args.encoder.fields else None,
                'expands': batch_info['expand'] if 'expand' in args.encoder.fields else None,
                'fp16': args.encoder.fp16}
            embeddings = encoder.encode(**kwargs)
            batch_info['vector'] = embeddings
            embedding_writer.write(batch_info, args.input.fields)
