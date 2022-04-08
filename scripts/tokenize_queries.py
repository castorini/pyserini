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

'''Convert MSMARCO queries'''

import argparse
from transformers import AutoTokenizer
from tqdm import tqdm
from ltr_msmarco.convert_common import get_retokenized


parser = argparse.ArgumentParser(description='Convert queries in tsv format with tokenization')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)

args = parser.parse_args()
print(args)
arg_vars = vars(args)

bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

with open(args.input) as inFile:
    with open(args.output, 'w') as outFile:
        # Input file is a TSV file
        line_num = 0
        for line in tqdm(inFile):
            line_num += 1
            line = line.strip()
            if not line:
                continue
            fields = line.split('\t')
            if len(fields) != 2:
                print(f"Misformated line {line_num} ignoring:")
                print(line.replace('\t', '<field delimiter>'))
                continue

            did, query = fields

            doc = {"id": did,
                "contents": get_retokenized(bert_tokenizer, query.lower())}
            docStr = f"{doc['id']}\t{doc['contents']}\n"
            outFile.write(docStr)

            if line_num % 10000 == 0:
                print(f"Processed {line_num} queries")

        print(f"Processed {line_num} queries")
