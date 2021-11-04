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
from pyserini.analysis import Analyzer, get_lucene_analyzer
"""
append d2q prediction as an extra field to collection jsonl
"""
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts MSMARCO\'s tsv collection to Anserini jsonl files.')
    parser.add_argument('--collection_path', required=True, help='MS MARCO .tsv collection file')
    parser.add_argument('--predictions', required=True, help='File containing predicted queries.')
    parser.add_argument('--output_folder', required=True, help='output folder')
    parser.add_argument('--max_docs_per_file', default=1000000, type=int,
                        help='maximum number of documents in each jsonl file.')

    args = parser.parse_args()
    if not os.path.exists(args.output_folder):
        os.makedirs(args.output_folder)
    analyzer = Analyzer(get_lucene_analyzer())
    print('Converting collection...')

    file_index = 0
    new_words = 0
    total_words = 0

    with open(args.collection_path) as f_corpus, open(args.predictions) as f_pred:
        for i, (line_doc, line_pred) in enumerate(zip(f_corpus, f_pred)):
            # Write to a new file when the current one reaches maximum capacity.
            if i % args.max_docs_per_file == 0:
                if i > 0:
                    output_jsonl_file.close()
                output_path = os.path.join(args.output_folder, f'docs{file_index:02d}.json')
                output_jsonl_file = open(output_path, 'w')
                file_index += 1

            doc_json = json.loads(line_doc)
            pred_text = line_pred.rstrip()

            predict_text = pred_text + ' '
            analyzed = analyzer.analyze(predict_text)
            for token in analyzed:
                assert ' ' not in token
            predict = ' '.join(analyzed)

            doc_json['predict'] = predict
            output_jsonl_file.write(json.dumps(doc_json) + '\n')

            if i % 100000 == 0:
                print('Converted {} docs in {} files'.format(i, file_index))

    output_jsonl_file.close()
    print('Done!')