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


def load_data(data_path):
    with open(data_path, 'r') as fin:
        data = json.load(fin)
    examples = []
    for k, example in enumerate(data):
        if not 'id' in example:
            example['id'] = k

        example['answers'] = list(map(lambda answer: answer.replace('\xa0', ' ').replace('"','""'), example['answers']))
        examples.append(example)
    return examples



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, metavar='path',
                        help="Path to data json file")
    parser.add_argument('--output', type=str, metavar='path',
                        help="Path to topic json file")
    args = parser.parse_args()

    topic = {}
    with open(args.output, 'w') as fout:
        for idx, example in enumerate(load_data(args.input)):
            fout.write(f"{example['question']}\t{example['answers']}\n")
