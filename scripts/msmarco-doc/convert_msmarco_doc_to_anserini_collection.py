import argparse
import gzip
import json
import os
from tqdm import tqdm


def generate_output_dict(doc):
    doc_id, doc_url, doc_title, doc_text = doc[0], doc[1], doc[2], doc[3]
    doc_text = doc_text.strip()
    doc_text = f'{doc_url}\n{doc_title}\n{doc_text}'
    output_dict = {'id': doc_id, 'contents': doc_text}
    return output_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert MS MARCO V1 document ranking corpus to anserini\'s default jsonl collection format')
    parser.add_argument('--original_docs_path', required=True, help='Original corpus file.')
    parser.add_argument('--output_docs_path', required=True, help='Output file in the anserini jsonl format.')

    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output_docs_path), exist_ok=True)

    f_corpus = gzip.open(args.original_docs_path, mode='rt')
    f_out = open(args.output_docs_path, 'w')

    for line in tqdm(f_corpus):
        output_dict = generate_output_dict(line.split('\t'))
        f_out.write(json.dumps(output_dict) + '\n')
    print('Done!')
