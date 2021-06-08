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
import json
import os

from transformers import BertTokenizer, T5Tokenizer


def write_to_file(tokenizer, input, output):
    with open(input, encoding='utf-8') as f:
        out_f = open(output, 'w')
        for i, line in enumerate(f):
            fdict = json.loads(line)
            contents = fdict['contents']
            tok = tokenizer.tokenize(contents)
            tokcont = ' '
            fdict['contents'] = tokcont.join(tok)
            out_f.write(json.dumps(fdict) + '\n')
            if i % 10000 == 0:
                print(f'Converted {i:,} docs, writing into file {output}')
        out_f.close()


def main(args):
    if ('bert' in args.tokenizer):
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    else:
        tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
    if (os.path.isdir(args.input)):
        for i, inf in enumerate(sorted(os.listdir(args.input))):
            if not os.path.isdir(args.output):
                os.mkdir(args.output)
            outf = os.path.join(args.output, 'docs{:02d}.json'.format(i))
            write_to_file(tokenizer,os.path.join(args.input, inf), outf)
    else:
        write_to_file(tokenizer,args.input, args.output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, help='Input file/dir', required=True)
    parser.add_argument("--output", type=str, help='Output file/dir', required=True)
    parser.add_argument("--tokenizer", type=str, help='full name of tokenizer', default='bert-base-uncased')

    args = parser.parse_args()

    main(parser.parse_args())