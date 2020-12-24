#!/usr/bin/env python
# Convert MSMARCO queries
import multiprocessing
import sys
import json
import argparse
from transformers import AutoTokenizer, AutoModel
import spacy
import re
from convert_common import readStopWords, SpacyTextParser, getRetokenized
from pyserini.analysis import Analyzer, get_lucene_analyzer

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
                    type=int, default=multiprocessing.cpu_count() - 1)
parser.add_argument('--bert_tokenize', action='store_true', help='Apply the BERT tokenizer and store result in a separate field')

args = parser.parse_args()
print(args)
arg_vars = vars(args)

inpFile = open(args.input)
outFile = open(args.output, 'w')
maxDocSize = args.max_doc_size

stopWords = readStopWords('stopwords.txt', lowerCase=True)
print(stopWords)
nlp = SpacyTextParser('en_core_web_sm', stopWords, keepOnlyAlphaNum=True, lowerCase=True)
analyzer = Analyzer(get_lucene_analyzer())

if 'bert_tokenize' in arg_vars:
    print('BERT-tokenizing input into the field: ' + 'text_bert_tok')
    bertTokenizer =AutoTokenizer.from_pretrained("bert-base-uncased")

class PassParseWorker:
    def __call__(self, line):

        if not line:
            return None

        line = line[:maxDocSize]  # cut documents that are too long!
        fields = line.split('\t')
        if len(fields) != 2:
            return None

        pid, body = fields

        text, text_unlemm = nlp.procText(body)

        doc = {"id": pid,
               "text": text,
               "text_unlemm": text_unlemm,
               "raw": body}
        doc["text_bert_tok"] = getRetokenized(bertTokenizer, body.lower())
        return doc


proc_qty = args.proc_qty
print(f'Spanning {proc_qty} processes')
pool = multiprocessing.Pool(processes=proc_qty)
ln = 0
for docJson in pool.imap(PassParseWorker(), inpFile, 500):
    ln = ln + 1
    if docJson is not None:
        analyzed = analyzer.analyze(docJson["raw"])
        for token in analyzed:
            if ' ' in token:
                print(analyzed)
        docJson['contents'] = ' '.join(analyzed)
        outFile.write(json.dumps(docJson) + '\n')
    else:
        print('Ignoring misformatted line %d' % ln)

    if ln % 10000 == 0:
        print('Processed %d passages' % ln)

print('Processed %d passages' % ln)

inpFile.close()
outFile.close()

