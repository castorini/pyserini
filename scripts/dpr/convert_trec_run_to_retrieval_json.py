import argparse
import json
import os
from pyserini.search import SimpleSearcher

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert an TREC run to DPR retrieval result json.')
    parser.add_argument('--qas', required=True, help='Topic json file')
    parser.add_argument('--index', required=True, help='Anserini Index that contains raw')
    parser.add_argument('--input', required=True, help='Input TREC run file.')
    parser.add_argument('--output', required=True, help='Output DPR Retrieval json file.')
    args = parser.parse_args()

    qas = json.load(open(args.qas))

    if os.path.exists(args.index):
        searcher = SimpleSearcher(args.index)
    else:
        searcher = SimpleSearcher.from_prebuilt_index(args.index)
    if not searcher:
        exit()

    retrieval = {}
    with open(args.input) as f_in:
        for line in f_in:
            question_id, _, doc_id, _, score, _ = line.strip().split()
            question = qas[question_id]['title']
            answers = qas[question_id]['answers']
            ctx = searcher.doc(doc_id).raw()
            if question_id not in retrieval:
                retrieval[question_id] = {'question': question, 'answers': answers, 'contexts': []}
            retrieval[question_id]['contexts'].append(
                {'docid': doc_id, 'score': score, 'text': ctx}
            )

    json.dump(retrieval, open(args.output, 'w'))
