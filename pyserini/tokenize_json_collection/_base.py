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
import os

class JsonTokenizerWriter():
    def __init__(self, tok_name):
        if('bert' in tok_name):
            self.tokenizer = tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        else:
            self.tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')

    def write_to_file(self, inputf, outputf):
        with open(inputf, encoding='utf-8') as f:
            out_f = open(outputf,'w')
            for i, line in enumerate(f):
                fdict = json.loads(line)
                contents = fdict['contents']
                tok = self.tokenizer.tokenize(contents)
                fdict['contents'] = tok
                out_f.write(json.dumps(fdict) + '\n')
                if i%10000 == 0:
                    print(f'Converted {i:,} docs, writing into file {outputf}')
            out_f.close()

    def write_to_dir(self, inputDir, outputDir):
        if not os.path.isdir(outputDir):
            os.mkdir(outputDir)
        for i, inf in enumerate(os.listdir(inputDir)):
            outf = os.path.join(outputDir, 'docs{:02d}.json'.format(i))
            self.write_to_file(os.path.join(inputDir,inf),outf)
