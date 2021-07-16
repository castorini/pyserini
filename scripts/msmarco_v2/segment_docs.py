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
# Starting point for writing this script
# https://github.com/castorini/docTTTTTquery/blob/master/convert_msmarco_passages_doc_to_anserini.py
import argparse
import os
import sys
import gzip
import json
import spacy #Currently using spacy 2.3.5
from tqdm import tqdm
import re
import glob
from multiprocessing import Pool

def create_segments(doc_text, max_length, stride):
    doc_text = doc_text.strip()
    doc = nlp(doc_text[:10000])
    sentences = [sent.string.strip() for sent in doc.sents]
    segments = []
    
    for i in range(0, len(sentences), stride):
        segment = " ".join(sentences[i:i+max_length])
        segments.append(segment)
        if i + max_length >= len(sentences):
            break
    return segments

def split_document(f_ins, f_out): 
    print('Spliting documents...')
    output = open(f_out, 'w')
    output_id = open(f_out.replace(".json", ".id"), 'w')
    for f_in in f_ins:
        with gzip.open(f_in, 'rt', encoding='utf8') as in_fh:
            for json_string in tqdm(in_fh):
                doc = json.loads(json_string)
                f_doc_id = doc['docid']
                doc_url = doc['url']
                doc_title = doc['title']
                doc_headings = doc['headings']
                doc_text = doc['body']

                segments = create_segments(doc_text, args.max_length, args.stride)

                for seg_id, segment in enumerate(segments):
                    # expanded_text = f'{doc_url}\n{doc_headings}\n{doc_title}\n{segment}'
                    doc_seg = f'{f_doc_id}#{seg_id}'
                    output_dict = {'docid': doc_seg, 'url': doc_url, 'title': doc_title, 'headings': doc_headings, 'segment': segment}
                    output.write(json.dumps(output_dict) + '\n')  
                    output_id.write(doc_seg+'\n')

    output.close()
    output_id.close()
    print('Done!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Segment MS MARCO V2 original docs into passages')
    parser.add_argument('--input', required=True, help='MS MARCO V2 corpus path.')
    parser.add_argument('--output', required=True, help='output file path with json format.')
    parser.add_argument('--max_length', default=10, help='maximum sentence length per passage')
    parser.add_argument('--stride', default=5, help='the distance between each beginning sentence of passage in a document')
    parser.add_argument('--num_workers', default=1, type=int)
    args = parser.parse_args()


    os.makedirs(os.path.dirname(args.output_docs_path), exist_ok=True)


    max_length = args.max_length
    stride = args.stride
    nlp = spacy.blank("en")
    nlp.add_pipe(nlp.create_pipe("sentencizer"))

    files = glob.glob(os.path.join(args.original_docs_path, '*.gz'))
    num_files = len(files)
    pool = Pool(args.num_workers)
    num_files_per_worker=num_files//args.num_workers
    for i in range(args.num_workers):
        f_out = os.path.join(args.output_docs_path, 'doc' + str(i) + '.json')
        if i==(args.num_workers-1):
            file_list = files[i*num_files_per_worker:]
        else:
            file_list = files[i*num_files_per_worker:((i+1)*num_files_per_worker)]

        pool.apply_async(split_document ,(file_list, f_out))

    pool.close()
    pool.join()

    print('Done!')


