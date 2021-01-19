import csv
import json
from tqdm import tqdm
import argparse
from pyserini.search import SimpleSearcher
from pyserini.dsearch import DPRQueryEncoder, SimpleDenseSearcher


def parse_qa_csv_file(location):
    with open(location) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            question = row[0]
            answers = eval(row[1])
            yield question, answers


parser = argparse.ArgumentParser()
parser.add_argument('--dense-index', type=str, metavar='path to index or index name', required=True,
                    help="Path to faiss index or name of prebuilt index.")
parser.add_argument('--sparse-index', type=str, metavar='path to index or index name', required=True,
                    help="Path to sparse index or name of prebuilt index.")
parser.add_argument('--encoder', type=str, metavar='path to query encoder checkpoint or encoder name', required=True,
                    help="Path to query encoder pytorch checkpoint or hgf encoder model name")
parser.add_argument('--qas', type=str, metavar='path to qas', required=True,
                    help="path to question/answers file, csv file")
parser.add_argument('--hits', type=int, metavar='num',
                    required=False, default=1000, help="Number of hits.")
parser.add_argument('--output', type=str, metavar='path',
                    help="Path to output file.")
parser.add_argument('--batch', type=int, metavar='num', required=False,
                    default=1, help="Specify batch size to search the collection concurrently.")
parser.add_argument('--threads', type=int, metavar='num', required=False,
                    default=1, help="Maximum number of threads to use.")
args = parser.parse_args()

encoder = DPRQueryEncoder(encoder_dir=args.encoder)
dsearcher = SimpleDenseSearcher.from_prebuilt_index(args.dense_index, encoder)

ssearcher = SimpleSearcher(args.sparse_index)

questions, answers = zip(*list(parse_qa_csv_file(args.qas)))
question_ids = [str(i) for i in range(len(questions))]

result = {}
for i in tqdm(range(0, len(questions), args.batch)):
    question_batch = questions[i: i + args.batch]
    results = dsearcher.batch_search(question_batch, question_ids, k=args.hits, threads=args.threads)
    for question_id in results:
        ans_choices = answers[int(question_id)]
        question = questions[int(question_id)]
        result[question_id] = {'question': question, 'answers': question, 'contexts': []}
        for idx, hit in enumerate(results[question_id]):
            result[question_id]['contexts'].append(
                {
                    'docid': hit.docid,
                    'score': hit.score,
                    'text': ssearcher.doc(hit.docid).raw()
                }
            )

json.dump(result, open(args.output, 'w'), indent=4)
