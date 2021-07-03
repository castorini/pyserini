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
import sys

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')

from pyserini.search import SimpleSearcher


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--qrels', type=str, help='qrels file', required=True)
    parser.add_argument('--index', type=str, help='index location', required=True)
    args = parser.parse_args()

    searcher = SimpleSearcher(args.index)
    with open(args.qrels, 'r') as reader:
        for line in reader.readlines():
            arr = line.split('\t')
            doc = json.loads(searcher.doc(arr[2]).raw())['contents']
            print(f'{arr[2]}\t{doc}')
