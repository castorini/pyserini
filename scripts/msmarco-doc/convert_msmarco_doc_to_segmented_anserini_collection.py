import argparse
import gzip
import json
import os
# Uses space==2.1.6
import spacy
from tqdm import tqdm


def generate_output_dicts(doc, nlp, max_length, stride):
    doc_id, doc_url, doc_title, doc_text = doc[0], doc[1], doc[2], doc[3]
    doc_text = doc_text.strip()
    doc = nlp(doc_text[:10000])
    sentences = [sent.string.strip() for sent in doc.sents]
    output_dicts = []
    for ind, pos in enumerate(range(0, len(sentences), stride)):
        segment = ' '.join(sentences[pos:pos + max_length])
        doc_text = f'{doc_url}\n{doc_title}\n{segment}'
        output_dicts.append({'id': f'{doc_id}#{ind}', 'contents': doc_text})
        if pos + max_length >= len(sentences):
            break
    return output_dicts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Convert MS MARCO V1 document ranking corpus to seg anserini\'s default jsonl collection format')
    parser.add_argument('--original_docs_path', required=True, help='Original corpus file.')
    parser.add_argument('--output_docs_path', required=True, help='Output file in the anserini jsonl format.')
    parser.add_argument('--stride', default=5, help='Sliding-window stride')
    parser.add_argument('--max_length', default=10, help='Sliding-window length')
    args = parser.parse_args()

    # Load spacy model
    nlp = spacy.blank("en")
    nlp.add_pipe(nlp.create_pipe("sentencizer"))

    os.makedirs(os.path.dirname(args.output_docs_path), exist_ok=True)

    f_corpus = gzip.open(args.original_docs_path, mode='rt')
    f_out = open(args.output_docs_path, 'w')

    print('Creating collection...')
    for line in tqdm(f_corpus):
        output_dicts = generate_output_dicts(line.split('\t'), nlp, args.max_length, args.stride)
        for output_dict in output_dicts:
            f_out.write(json.dumps(output_dict) + '\n')
    print('Done!')
