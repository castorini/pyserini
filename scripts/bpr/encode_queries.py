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

import argparse
import csv
import json

import pandas as pd
from tqdm import tqdm
import sys

# We're going to explicitly use a local installation of Pyserini.
sys.path.insert(0, './')
sys.path.insert(0, '../pyserini/')

from pyserini.dsearch import BprQueryEncoder

def parse_qa_csv_file(location):
    with open(location) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            question = row[0]
            answers = eval(row[1])
            yield question, answers


def parse_qa_json_file(location):
    with open(location) as file:
        for line in file:
            qa = json.loads(line)
            question = qa['question']
            answers = qa['answer']
            yield question, answers


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path',
                        default='facebook/dpr-question_encoder-multiset-base', required=False)
    parser.add_argument('--input', type=str, help='qas file, json file by default', required=True)
    parser.add_argument('--format', type=str, help='qas file format', default='json', required=False)
    parser.add_argument('--output', type=str, help='path to store query embeddings', required=True)
    args = parser.parse_args()

    model = BprQueryEncoder(args.encoder)
    tokenizer = model.tokenizer
    
    embeddings = {'id': [], 'text': [], 'dense_embedding': [], 'sparse_embedding': []}
    qa_parser = None
    if args.format == 'csv':
        qa_parser = parse_qa_csv_file
    elif args.format == 'json':
        qa_parser = parse_qa_json_file
    if qa_parser is None:
        print(f'No QA parser defined for file format: {args.format}, or format not match')
    for qid, (question, answers) in enumerate(tqdm(list(qa_parser(args.input)))):
        embeddings['id'].append(qid)
        embeddings['text'].append(question)
        ret = model.encode(question)
        embeddings['dense_embedding'].append(ret['dense'])
        embeddings['sparse_embedding'].append(ret['sparse'])
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(args.output)
