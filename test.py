import argparse
import os
import json
import torch
from pyserini.encode import JsonlRepresentationWriter, JsonlCollectionIterator
from pyserini.encode import ArcticDocumentEncoder, ArcticQueryEncoder

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--corpus', type=str, required=True, help='Path to corpus file in jsonl format.')
    parser.add_argument('--queries', type=str, required=True, help='Path to queries file in jsonl format.')
    parser.add_argument('--output', type=str, required=True, help='Path to output embeddings file.')
    parser.add_argument('--batchsize', type=int, default=1, help='Batch size for processing')
    parser.add_argument('--device', type=str, default='cpu', help='Device to use for encoding (cpu or cuda)')
    args = parser.parse_args()

    # Clear CUDA cache if using GPU
    if 'cuda' in args.device:
        torch.cuda.empty_cache()

    # Encode documents
    doc_encoder = ArcticDocumentEncoder(device=args.device)
    corpus_iterator = JsonlCollectionIterator(args.corpus, fields=['text'])
    doc_embeddings = []
    for doc in corpus_iterator:
        embedding = doc_encoder.encode(doc['text'])
        doc_embeddings.append({'id': doc['id'], 'embedding': embedding.tolist()})

    # Save document embeddings
    with open(args.output + '_docs.json', 'w') as f:
        json.dump(doc_embeddings, f)

    # Clear CUDA cache before loading the model again for query encoding
    del doc_encoder
    del doc_embeddings
    torch.cuda.empty_cache()

    # Encode queries
    query_encoder = ArcticQueryEncoder(device=args.device)
    with open(args.queries, 'r') as f:
        queries = [json.loads(line) for line in f]
    query_embeddings = []
    for query in queries:
        embedding = query_encoder.encode(query['text'])
        query_embeddings.append({'id': query['id'], 'embedding': embedding.tolist()})

    # Save query embeddings
    with open(args.output + '_queries.json', 'w') as f:
        json.dump(query_embeddings, f)

if __name__ == '__main__':
    main()
