import csv
import argparse
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
