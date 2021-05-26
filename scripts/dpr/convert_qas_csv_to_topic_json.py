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


def parse_qa_csv_file(location):
    with open(location) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            question = row[0]
            answers = eval(row[1])
            yield question, answers


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, metavar='path',
                        help="Path to question answers csv file")
    parser.add_argument('--output', type=str, metavar='path',
                        help="Path to topic json file")
    args = parser.parse_args()

    topic = {}
    for idx, (question, answers) in enumerate(parse_qa_csv_file(args.input)):
        topic[str(idx)] = {'title': question, 'answers': answers}

    json.dump(topic, open(args.output, 'w'), indent=4)
