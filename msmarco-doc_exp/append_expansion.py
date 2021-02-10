'''Converts MSMARCO's tsv collection to Anserini jsonl files with field configurations.'''
import argparse
import json
import os
from pyserini.analysis import Analyzer, get_lucene_analyzer

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Converts MSMARCO\'s tsv collection to Anserini jsonl '
                    'files.')
    parser.add_argument('--jsonl_path', required=True, help='MS MARCO .jsonl collection file')
    parser.add_argument('--predictions', required=True, help='File containing predicted queries.')
    parser.add_argument('--output', required=True, help='output')
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
            output_jsonl_file = open(args.output, 'w')
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