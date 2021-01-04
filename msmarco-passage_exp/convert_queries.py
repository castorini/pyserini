#!/usr/bin/env python
# Convert MSMARCO queries
import sys
import json
import argparse
from transformers import AutoTokenizer, AutoModel
import spacy
from convert_common import readStopWords, SpacyTextParser, getRetokenized
from pyserini.analysis import Analyzer, get_lucene_analyzer
from tqdm import tqdm

sys.path.append('.')

parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc queries.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)
parser.add_argument('--min_query_token_qty', type=int, default=0,
                    metavar='min # of query tokens', help='ignore queries that have smaller # of tokens')
parser.add_argument('--bert_tokenize', action='store_true', help='Apply the BERT tokenizer and store result in a separate field')

args = parser.parse_args()
print(args)
arg_vars = vars(args)

inpFile = open(args.input)
outFile = open(args.output, 'w')
minQueryTokQty = args.min_query_token_qty

stopWords = readStopWords('stopwords.txt', lowerCase=True)
print(stopWords)
nlp = SpacyTextParser('en_core_web_sm', stopWords, keepOnlyAlphaNum=True, lowerCase=True)
analyzer = Analyzer(get_lucene_analyzer())
nlp_ent = spacy.load("en_core_web_sm")

if 'bert_tokenize' in arg_vars:
    print('BERT-tokenizing input into the field: ' + 'text_bert_tok')
    bertTokenizer =AutoTokenizer.from_pretrained("bert-base-uncased")

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

    query_lemmas, query_unlemm = nlp.procText(query)
    analyzed = analyzer.analyze(query)
    for token in analyzed:
        if ' ' in token:
            print(analyzed)

    query_toks = query_lemmas.split()

    doc = nlp_ent(query)
    entity = '{'
    for i in range(len(doc.ents)):
        if (i != 0):
            entity += ','
        entity += '"' + doc.ents[i].label_ + '"' + ':' + '"' + doc.ents[i].text + '"'
    entity += '}'

    if len(query_toks) >= minQueryTokQty:
        doc = {"id": did,
               "text": query_lemmas,
               "text_unlemm": query_unlemm,
               "analyzed": ' '.join(analyzed),
               "entity": entity,
               "raw": query}

        doc["text_bert_tok"] = getRetokenized(bertTokenizer, query.lower())

        docStr = json.dumps(doc) + '\n'
        outFile.write(docStr)

    if ln % 10000 == 0:
        print('Processed %d queries' % ln)

print('Processed %d queries' % ln)

inpFile.close()
outFile.close()
