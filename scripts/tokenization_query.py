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

"""Convert MSMARCO queries"""

import argparse
import multiprocessing
from transformers import AutoTokenizer
from tqdm import tqdm
from scripts.ltr_msmarco.convert_common import get_retokenized
"""
add fields to query json with contents((BERT token)                                  
"""


parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc documents.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)
parser.add_argument('--proc_qty', metavar='# of processes', help='# of NLP processes to span',
                    type=int, default=multiprocessing.cpu_count() - 2)


args = parser.parse_args()
print(args)
arg_vars = vars(args)

inpFile = open(args.input)
outFile = open(args.output, 'w')
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Input file is a TSV file
line_num = 0
for line in tqdm(inpFile):
    line_num += 1
    line = line.strip()
    if not line:
        continue
    fields = line.split('\t')
    if len(fields) != 2:
        print('Misformated line %d ignoring:' % line_num)
        print(line.replace('\t', '<field delimiter>'))
        continue

    did, query = fields

    doc = {"id": did,
          "contents": get_retokenized(bert_tokenizer, query.lower())}
    docStr = doc['id']+'\t'+doc['contents']+'\n'
    outFile.write(docStr)

    if line_num % 10000 == 0:
        print('Processed %d queries' % line_num)

print('Processed %d queries' % line_num)

inpFile.close()
outFile.close()