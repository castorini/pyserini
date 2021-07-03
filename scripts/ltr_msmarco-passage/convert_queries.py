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

import sys

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')

import json
import argparse
from transformers import AutoTokenizer, AutoModel
import spacy
from convert_common import read_stopwords, SpacyTextParser, get_retokenized
from pyserini.analysis import Analyzer, get_lucene_analyzer
from tqdm import tqdm
import os
"""
add fields to query json with text(lemmatized), text_unlemm, contents(analyzer), raw, entity(NER), text_bert_tok(BERT token)
"""
sys.path.append('.')

parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc queries.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)
parser.add_argument('--min_query_token_qty', type=int, default=0,
                    metavar='min # of query tokens', help='ignore queries that have smaller # of tokens')

args = parser.parse_args()
print(args)
arg_vars = vars(args)

inpFile = open(args.input)
outFile = open(args.output, 'w')
minQueryTokQty = args.min_query_token_qty
if os.getcwd().endswith('ltr_msmarco-passage'):
    stopwords = read_stopwords('stopwords.txt', lower_case=True)
else:
    stopwords = read_stopwords('./scripts/ltr_msmarco-passage/stopwords.txt', lower_case=True)
print(stopwords)
nlp = SpacyTextParser('en_core_web_sm', stopwords, keep_only_alpha_num=True, lower_case=True)
analyzer = Analyzer(get_lucene_analyzer())
nlp_ent = spacy.load("en_core_web_sm")
bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

# Input file is a TSV file
ln = 0
for line in tqdm(inpFile):
    ln += 1
    line = line.strip()
    if not line:
        continue
    fields = line.split('\t')
    if len(fields) != 2:
        print('Misformated line %d ignoring:' % ln)
        print(line.replace('\t', '<field delimiter>'))
        continue

    did, query = fields

    query_lemmas, query_unlemm = nlp.proc_text(query)
    analyzed = analyzer.analyze(query)
    for token in analyzed:
        if ' ' in token:
            print(analyzed)

    query_toks = query_lemmas.split()

    doc = nlp_ent(query)
    entity = {}
    for i in range(len(doc.ents)):
        entity[doc.ents[i].text] = doc.ents[i].label_
    entity = json.dumps(entity)

    if len(query_toks) >= minQueryTokQty:
        doc = {"id": did,
               "text": query_lemmas,
               "text_unlemm": query_unlemm,
               "analyzed": ' '.join(analyzed),
               "entity": entity,
               "raw": query}

        doc["text_bert_tok"] = get_retokenized(bert_tokenizer, query.lower())

        docStr = json.dumps(doc) + '\n'
        outFile.write(docStr)

    if ln % 10000 == 0:
        print('Processed %d queries' % ln)

print('Processed %d queries' % ln)

inpFile.close()
outFile.close()