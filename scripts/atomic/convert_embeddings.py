from reader import NumpyReader
from tqdm import tqdm
import pandas as pd
import os
import json
import argparse
from data import AtomicDataset

def get_args_parser():
    parser = argparse.ArgumentParser('Encode embeddings', add_help=False)
    parser.add_argument('--inputs', type=str, help='directory of the AToMiC prebuilt topic embeddings', required=True)
    parser.add_argument('--encode-type', type=str, default='text', choices=['text', 'image'], required=True)
    parser.add_argument('--topics-output', type=str, help='directory to store topics file', default='')
    parser.add_argument('--embeddings-output', type=str, help='directory to store embeddings file', default='')

    # only required for text datasets, to process the raw text
    parser.add_argument('--dataset', type=str, default='TREC-AToMiC/AToMiC-Texts-v0.2.1')
    parser.add_argument('--id-column', type=str, default='text_id')
    parser.add_argument('--split', type=str, default='validation')
    parser.add_argument('--qrels', type=str, default='TREC-AToMiC/AToMiC-Qrels-v0.2')

    return parser

def main(args):
    reader = NumpyReader(args.inputs)

    if args.encode_type == 'text':
        dataset = AtomicDataset(
            data_name_or_path=args.dataset,
            id_column=args.id_column,
            qrel_name_or_path=args.qrels,
        )
        if args.split:
            dataset = dataset.get_split(args.split)
        dataset_dict = dataset.to_dict()
        field_col=['page_title', 'section_title', 'hierachy', 'context_section_description', 'context_page_description']
        
    query_file = {'id': [], 'text': [], 'embedding': []}
    topic_file = {}
    for item in tqdm(reader, total=len(reader), desc='converting...'):
        id = item['id']
        vec = item['vector']
        query_file['id'].append(id)
        query_file['embedding'].append(vec)
        if args.encode_type == 'text':
            content = []
            index = index = dataset_dict['text_id'].index(id)
            if isinstance(field_col, list):
                for field in field_col:
                    # if the column val is a list, concat again
                    value = dataset_dict[field][index]
                    if isinstance(value, list):
                        content.append(' '.join(value))
                    else:
                        content.append(value)
            else:
                content.append(dataset_dict[field_col][index])
            
            text = ' '.join(content)
            query_file['text'].append(text)
            topic_file[id] = {'title': text}
        else:
            # image dataset doesn't provide text to encode, so we use its ID to delineate it
            query_file['text'].append(id)
            topic_file[id] = {'title': id}

    df = pd.DataFrame(query_file)
    df.to_pickle(os.path.join(args.embeddings_output, 'embedding.pkl'))

    with open(os.path.join(args.topics_output, 'topics.json'), 'w') as f:
        json.dump(topic_file, f)

if __name__ == "__main__":
    parser = get_args_parser()
    args = parser.parse_args()

    main(args)