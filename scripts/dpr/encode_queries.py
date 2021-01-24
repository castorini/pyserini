import argparse
import csv

import pandas as pd
from tqdm import tqdm
from transformers import DPRQuestionEncoder, DPRQuestionEncoderTokenizer


def parse_qa_csv_file(location):
    with open(location) as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            question = row[0]
            answers = eval(row[1])
            yield question, answers


def encode_query(text, tokenizer, model, device='cpu'):
    input_ids = tokenizer(text, return_tensors='pt')
    input_ids.to(device)
    embeddings = model(input_ids["input_ids"]).pooler_output.detach().cpu().numpy()
    return embeddings.flatten()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--encoder', type=str, help='encoder name or path', required=True)
    parser.add_argument('--input', type=str, help='qas csv file', required=True)
    parser.add_argument('--output', type=str, help='path to store query embeddings', required=True)
    parser.add_argument('--device', type=str,
                        help='device cpu or cuda [cuda:0, cuda:1...]', default='cpu', required=False)
    args = parser.parse_args()

    tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(args.encoder)
    model = DPRQuestionEncoder.from_pretrained(args.encoder)
    model.to(args.device)

    embeddings = {'id': [], 'text': [], 'embedding': []}
    for qid, (question, answers) in enumerate(tqdm(list(parse_qa_csv_file(args.input)))):
        embeddings['id'].append(qid)
        embeddings['text'].append(question)
        embeddings['embedding'].append(encode_query(question, tokenizer, model, args.device))
    embeddings = pd.DataFrame(embeddings)
    embeddings.to_pickle(args.output)
