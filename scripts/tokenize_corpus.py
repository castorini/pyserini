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
import multiprocessing
import json
import time
from joblib import Parallel, delayed
from transformers import AutoTokenizer
from ltr_msmarco.convert_common import get_retokenized

"""
add fields to jsonl with contents((BERT token)
"""


parser = argparse.ArgumentParser(description='Convert MSMARCO-adhoc documents.')
parser.add_argument('--input', metavar='input file', help='input file',
                    type=str, required=True)
parser.add_argument('--output', metavar='output file', help='output file',
                    type=str, required=True)
parser.add_argument('--workers', metavar='# of processes', help='# of NLP processes to span',
                    type=int, default=multiprocessing.cpu_count() - 2)


args = parser.parse_args()
print(args)
arg_vars = vars(args)

def batch_file(iterable, n=10000):
    batch = []
    for line in iterable:
        batch.append(line)
        if len(batch) == n:
            yield batch
            batch = []
    if len(batch) > 0:
        yield batch
        batch = []
    return


def batch_process(batch):
    bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def process(line):
        if not line:
            return None
        json_line = json.loads(line)
        pid = json_line['id']
        body = json_line['contents']

        doc = {"id": pid,
               "contents": get_retokenized(bert_tokenizer, body.lower())}
        return doc
    res = []
    start = time.time()
    for line in batch:
        res.append(process(line))
        if len(res) % 1000 == 0:
            end = time.time()
            print(f"finish {len(res)} using {end-start}")
            start = end
    return res


if __name__ == '__main__':
    workers = args.workers
    print(f"Spanning {workers} processes")
    pool = Parallel(n_jobs=workers, verbose=10)
    line_num = 0

    with open(args.input) as inpFile:
        with open(args.output, 'w') as outFile:

            for batch_json in pool([delayed(batch_process)(batch) for batch in batch_file(inpFile)]):
                for doc_json in batch_json:
                    line_num = line_num + 1
                    if doc_json is not None:
                        outFile.write(json.dumps(doc_json) + '\n')
                    else:
                        print(f"Ignoring misformatted line {line_num}")

                    if line_num % 100 == 0:
                        print(f"Processed {line_num} passages")

    print(f"Processed {line_num} passages")
