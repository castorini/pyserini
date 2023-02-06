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
import json
import os
from tqdm import tqdm

from pyserini.search import get_topics, get_topics_with_reader
from pyserini.search.lucene import LuceneSearcher
from pyserini.eval.evaluate_dpr_retrieval import has_answers, SimpleTokenizer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert an TREC run to DPR retrieval result json.')
    parser.add_argument('--topics', help='topic name')
    parser.add_argument('--topics-file', help='path to a topics file')
    parser.add_argument('--topics-reader', help='anserini TopicReader class')
    parser.add_argument('--index', required=True, help='Anserini Index that contains raw')
    parser.add_argument('--input', required=True, help='Input TREC run file.')
    parser.add_argument('--store-raw', action='store_true', help='Store raw text of passage')
    parser.add_argument('--regex', action='store_true', default=False, help="regex match")
    parser.add_argument('--combine-title-text', action='store_true', help="Make context the concatenation of title and text.")
    parser.add_argument('--output', required=True, help='Output DPR Retrieval json file.')
    args = parser.parse_args()

    if args.topics_file:
        qas = get_topics_with_reader(args.topics_reader, args.topics_file)
    elif args.topics:
        qas = get_topics(args.topics)
    else:
        print("No topics file or topics name was provided")

    if os.path.exists(args.index):
        searcher = LuceneSearcher(args.index)
    else:
        searcher = LuceneSearcher.from_prebuilt_index(args.index)
    if not searcher:
        exit()

    retrieval = {}
    tokenizer = SimpleTokenizer()
    with open(args.input) as f_in:
        for line in tqdm(f_in.readlines()):
            question_id, _, doc_id, _, score, _ = line.strip().split()
            question_id = int(question_id)
            question = qas[question_id]['title']
            answers = qas[question_id]['answers']
            if answers[0] == '"':
                answers = answers[1:-1].replace('""', '"')
            answers = eval(answers)
            if args.combine_title_text:
                passage = json.loads(searcher.doc(doc_id).raw())
                ctx = passage['title'] + "\n" + passage['text']
            else:
                ctx = json.loads(searcher.doc(doc_id).raw())['contents']
            if question_id not in retrieval:
                retrieval[question_id] = {'question': question, 'answers': answers, 'contexts': []}
            title, text = ctx.split('\n')
            answer_exist = has_answers(text, answers, tokenizer, args.regex)
            if args.store_raw:
                retrieval[question_id]['contexts'].append(
                    {'docid': doc_id,
                     'score': score,
                     'text': ctx,
                     'has_answer': answer_exist}
                )
            else:
                retrieval[question_id]['contexts'].append(
                    {'docid': doc_id, 'score': score, 'has_answer': answer_exist}
                )

    json.dump(retrieval, open(args.output, 'w'), indent=4, ensure_ascii=False)
