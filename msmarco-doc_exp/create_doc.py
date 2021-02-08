'''
Segment the documents and append their url, title, predicted queries to them. Then, they are saved into
json which can be used for indexing.
'''

import argparse
import gzip
import json
import os
import spacy
import time
from joblib import Parallel, delayed
import multiprocessing

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

def batch_process(batch, p_max_length, p_stride):
    nlp = spacy.blank("en")
    nlp.add_pipe(nlp.create_pipe("sentencizer"))
    
    def create_segments(doc_text, max_length, stride):
        doc_text = doc_text.strip()
        doc = nlp(doc_text[:10000])
        sentences = [sent.string.strip() for sent in doc.sents]
        segments = []

        for i in range(0, len(sentences), stride):
            segment = " ".join(sentences[i:i + max_length])
            segments.append(segment)
            if i + max_length >= len(sentences):
                break
        return segments

    res = []
    start = time.time()
    for line in batch:
        seg_id = 0
        doc_id, doc_url, doc_title, doc_text = line.split('\t')
        for seg in create_segments(doc_text, p_max_length, p_stride):
            doc_seg = f'{doc_id}#{seg_id}'
            res.append(json.dumps({'id':doc_seg,'contents':seg}))
            seg_id += 1
    end = time.time()
    print(f'finish {len(res)} using {end-start}')
    return res


parser = argparse.ArgumentParser(
    description='Concatenate MS MARCO original docs with predicted queries')
parser.add_argument('--original_docs_path', required=True, help='MS MARCO .tsv corpus file.')
parser.add_argument('--output_docs_path', required=True, help='Output file in the anserini jsonl format.')
parser.add_argument('--max_length', default=10)
parser.add_argument('--stride', default=5)
parser.add_argument('--proc_qty', metavar='# of processes', help='# of NLP processes to span',
                    type=int, default=multiprocessing.cpu_count()//2)
args = parser.parse_args()

os.makedirs(os.path.dirname(args.output_docs_path), exist_ok=True)

f_corpus = open(args.original_docs_path)
f_out = open(args.output_docs_path, 'w')
a_max_length = args.max_length
a_stride = args.stride

print('Spliting documents...')

proc_qty = args.proc_qty
print(f'Spanning {proc_qty} processes')
pool = Parallel(n_jobs=proc_qty, verbose=10)
ln = 0
for big_batch in batch_file(f_corpus, 20000*proc_qty):
    for batch_json in pool(delayed(batch_process)(batch, a_max_length, a_stride) for batch in batch_file(big_batch)):
        for docJson in batch_json:
            ln = ln + 1
            if docJson is not None:
                f_out.write(docJson + '\n')
            else:
                print('Ignoring misformatted line %d' % ln)

print('Processed %d passages' % ln)

f_corpus.close()
f_out.close()
print('Done!')
