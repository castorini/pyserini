#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

from transformers import BertTokenizer, T5Tokenizer
import argparse
import json

def main(args):
    if (args.tokenizer == 'bert'):
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
    else:
        tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
    with open(args.input_json, encoding='utf-8') as f:
        out_f = open(args.output_json,'w')
        for i, line in enumerate(f):
            fdict = json.loads(line)
            contents = fdict['contents']
            tok = tokenizer.tokenize(contents)
            fdict['contents']=tok
            out_f.write(json.dumps(fdict) + '\n')
            if (i%10000==0):
                print(f'Converted {i:,} docs, writing into file {args.output_json}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_json", type=str, help='Input Json file', required=True)
    parser.add_argument("--output_json", type=str, help='Output Json file', required=True)
    parser.add_argument("--tokenizer", type=str, help='bert/t5', required=True)

    args = parser.parse_args()

    main(parser.parse_args())