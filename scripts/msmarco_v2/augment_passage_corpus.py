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
# https://github.com/jacklin64/pyserini/blob/msmarcov2/scripts/msmarco_v2/segment_docs.py

import argparse
import os
import sys
import gzip
import json
from tqdm import tqdm
import re
import glob
from multiprocessing import Pool, Manager


def read_doc_corpus(f_ins, docid_to_title, docid_to_headings, docid_to_url):
    for f_in in f_ins:
        print('read {}...'.format(f_in))
        with gzip.open(f_in, 'rt', encoding='utf8') as in_fh:
            for json_string in tqdm(in_fh):
                doc = json.loads(json_string)
                docid = doc['docid']
                headings = doc['headings']
                title = doc['title']
                url = doc['url']
                docid_to_title[docid] = title
                docid_to_headings[docid] = headings
                docid_to_url[docid] = url
                docid_to_pass_num[docid] = 0

def passage_corpus_to_tsv(f_ins, f_out):
    print('Output passages...')
    output = open(f_out, 'w')
    output_id = open(f_out.replace(".json", ".id"), 'w')

    max_len = 0
    total_len = 0
    counter = 0
    for f_in in f_ins:
        with gzip.open(f_in, 'rt', encoding='utf8') as in_fh:
            for json_string in tqdm(in_fh):
                input_dict = json.loads(json_string)
                docid = input_dict['docid']
                pid = input_dict['pid']
                passage = input_dict['passage']
                passage_len = len(input_dict['passage'])
                doc_url = docid_to_url[docid]
                doc_title = docid_to_title[docid]
                doc_headings = docid_to_headings[docid]
                docid_to_pass_num[docid]+=1

                total_len += passage_len
                if (passage_len > max_len):
                    max_len = passage_len
                counter+=1
                output_dict = input_dict
                output_dict['url'] = doc_url
                output_dict['title'] = doc_title
                output_dict['headings'] = doc_headings
                output.write(json.dumps(output_dict) + '\n')  
                output_id.write(pid+'\n')
    print('maximum passage length: {}'.format(max_len))
    print('average passage length: {}'.format(total_len/counter))
    output.close()
    output_id.close()
    print('Done!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Concatenate MS MARCO original docs with predicted queries')
    parser.add_argument('--original_psg_path', required=True, help='MS MARCO .tsv corpus file.')
    parser.add_argument('--original_doc_path', required=True, help='doc json file path.')
    parser.add_argument('--output_psg_path', required=True, help='Output file in the anserini jsonl format.')
    parser.add_argument('--num_workers', default=1, type=int)
    args = parser.parse_args()


    os.makedirs(args.output_psg_path, exist_ok=True)
    doc_files = glob.glob(os.path.join(args.original_doc_path, '*.gz'))
    psg_files = glob.glob(os.path.join(args.original_psg_path, '*.gz'))
    manager = Manager()

    docid_to_title = manager.dict()
    docid_to_headings = manager.dict()
    docid_to_url = manager.dict()
    docid_to_pass_num = manager.dict()
    num_files = len(doc_files)
    pool = Pool(args.num_workers)
    num_files_per_worker=num_files//args.num_workers
    for i in range(args.num_workers):
        if i==(args.num_workers-1):
            file_list = doc_files[i*num_files_per_worker:]
        else:
            file_list = doc_files[i*num_files_per_worker:((i+1)*num_files_per_worker)]
        pool.apply_async(read_doc_corpus ,(file_list, docid_to_title, docid_to_headings, docid_to_url))
    pool.close()
    pool.join() 
    print('Total document size: {}'.format(len(docid_to_title)))



    num_files = len(psg_files)
    pool = Pool(args.num_workers)
    num_files_per_worker=num_files//args.num_workers
    for i in range(args.num_workers):
        f_out = os.path.join(args.output_psg_path, 'psg' + str(i) + '.json')
        if i==(args.num_workers-1):
            file_list = psg_files[i*num_files_per_worker:]
        else:
            file_list = psg_files[i*num_files_per_worker:((i+1)*num_files_per_worker)]

        pool.apply_async(passage_corpus_to_tsv ,(file_list, f_out))

    pool.close()
    pool.join()

    print('Done!')


