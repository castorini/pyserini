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

'''
Segment the documents and append their url, title, predicted queries to them. Then, they are saved into 
json which can be used for indexing.
'''

import argparse
import gzip
import json
import os
import spacy
from tqdm import tqdm
import re

def create_segments(doc_text, max_length, stride):
    doc_text = doc_text.strip()
    doc = nlp(doc_text[:10000])
    sentences = [str(sent).strip() for sent in doc.sents]
    segments = []
    
    for i in range(0, len(sentences), stride):
        segment = " ".join(sentences[i:i+max_length])
        segments.append(segment)
        if i + max_length >= len(sentences):
            break
    return segments

parser = argparse.ArgumentParser(
    description='Concatenate MS MARCO original docs with predicted queries')
parser.add_argument('--original_docs_path', required=True, help='MS MARCO .tsv corpus file.')
parser.add_argument('--doc_ids_path', required=True, help='File mapping segments to doc ids.')
parser.add_argument('--output_docs_path', required=True, help='Output file in the anserini jsonl format.')
parser.add_argument('--predictions_path', default=None, help='File containing predicted queries.')
parser.add_argument('--max_length', default=3)
parser.add_argument('--stride', default=1)
args = parser.parse_args()

os.makedirs(os.path.dirname(args.output_docs_path), exist_ok=True)

f_corpus = gzip.open(args.original_docs_path, mode='rt')
f_out = open(args.output_docs_path, 'w')
max_length = int(args.max_length)
stride = int(args.stride)
nlp = spacy.blank("en")
nlp.add_pipe("sentencizer")

print('Spliting documents...')
doc_id_ref = None
if args.predictions_path == None:
    doc_ids_queries = zip(open(args.doc_ids_path))
else:
    doc_ids_queries = zip(open(args.doc_ids_path),open(args.predictions_path))
for doc_id_query in tqdm(doc_ids_queries):
    doc_id = doc_id_query[0].strip()
    if doc_id != doc_id_ref:
        f_doc_id, doc_url, doc_title, doc_text = next(f_corpus).split('\t')
        while f_doc_id != doc_id:
            f_doc_id, doc_url, doc_title, doc_text = next(f_corpus).split('\t')
        segments = create_segments(doc_text, args.max_length, args.stride)
        seg_id = 0
    else:
        seg_id += 1
    doc_seg = f'{doc_id}#{seg_id}'
    if seg_id < len(segments):
        segment = segments[seg_id]
        if args.predictions_path == None:
            expanded_text = f'{doc_url} {doc_title} {segment}'
        else:
            predicted_queries_partial = doc_id_query[1]
            expanded_text = f'{doc_url} {doc_title} {segment} {predicted_queries_partial}'
        output_dict = {'id': doc_seg, 'contents': expanded_text}
        f_out.write(json.dumps(output_dict) + '\n')  
    doc_id_ref = doc_id  
    
f_corpus.close()
f_out.close()
print('Done!')