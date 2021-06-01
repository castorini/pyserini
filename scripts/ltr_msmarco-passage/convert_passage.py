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

import multiprocessing
from joblib import Parallel, delayed
import sys
import json
import argparse
from transformers import AutoTokenizer, AutoModel
import spacy
import re
from convert_common import read_stopwords, SpacyTextParser, get_retokenized
from pyserini.analysis import Analyzer, get_lucene_analyzer
import time
import os
"""
add fields to jsonl with text(lemmatized), text_unlemm, contents(analyzer), raw, text_bert_tok(BERT token)
"""
sys.path.append('.')

parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc documents.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)
parser.add_argument('--max_doc_size', metavar='max doc size bytes',
                    help='the threshold for the document size, if a document is larger it is truncated',
                    type=int, default=16536 )
parser.add_argument('--proc_qty', metavar='# of processes', help='# of NLP processes to span',
                    type=int, default=multiprocessing.cpu_count() - 2)

args = parser.parse_args()
print(args)
arg_vars = vars(args)

inpFile = open(args.input)
outFile = open(args.output, 'w')
maxDocSize = args.max_doc_size


def batch_file(iterable, n=10000):
    batch = []
    for line in iterable:
        batch.append(line)
        if len(batch) == n:
            yield batch
            batch = []
    if len(batch)>0:
        yield batch
        batch = []
    return

def batch_process(batch):
    if(os.getcwd().endswith('ltr_msmarco-passage')):
        stopwords = read_stopwords('stopwords.txt', lower_case=True)
    else:
        stopwords = read_stopwords('./scripts/ltr_msmarco-passage/stopwords.txt', lower_case=True)
    nlp = SpacyTextParser('en_core_web_sm', stopwords, keep_only_alpha_num=True, lower_case=True)
    analyzer = Analyzer(get_lucene_analyzer())
    #nlp_ent = spacy.load("en_core_web_sm")
    bert_tokenizer =AutoTokenizer.from_pretrained("bert-base-uncased")

    def process(line):
        if not line:
            return None

        line = line[:maxDocSize]  # cut documents that are too long!
        fields = line.split('\t')
        if len(fields) != 2:
            return None

        pid, body = fields

        text, text_unlemm = nlp.proc_text(body)


        #doc = nlp_ent(body)
        #entity = {}
        #for i in range(len(doc.ents)):
            #entity[doc.ents[i].text] = doc.ents[i].label_
        #entity = json.dumps(entity)

        analyzed = analyzer.analyze(body)
        for token in analyzed:
            assert ' ' not in token
        contents = ' '.join(analyzed)

        doc = {"id": pid,
               "text": text,
               "text_unlemm": text_unlemm,
               'contents': contents,
               "raw": body}
        doc["text_bert_tok"] = get_retokenized(bert_tokenizer, body.lower())
        return doc
    res = []
    start = time.time()
    for line in batch:
        res.append(process(line))
        if len(res) % 1000 == 0:
            end = time.time()
            print(f'finish {len(res)} using {end-start}')
            start = end
    return res


if __name__ == '__main__':
    proc_qty = args.proc_qty
    print(f'Spanning {proc_qty} processes')
    pool = Parallel(n_jobs=proc_qty, verbose=10)
    ln = 0
    for batch_json in pool([delayed(batch_process)(batch) for batch in batch_file(inpFile)]):
        for docJson in batch_json:
            ln = ln + 1
            if docJson is not None:
                outFile.write(json.dumps(docJson) + '\n')
            else:
                print('Ignoring misformatted line %d' % ln)

            if ln % 100 == 0:
                print('Processed %d passages' % ln)

    print('Processed %d passages' % ln)

    inpFile.close()
    outFile.close()
