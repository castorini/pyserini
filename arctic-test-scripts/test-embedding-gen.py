import argparse
import json
import torch
from pyserini.encode import JsonlCollectionIterator, ArcticDocumentEncoder, ArcticQueryEncoder, AnceDocumentEncoder

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
        print(doc)
        embedding = doc_encoder.encode(doc['text'][0])  # Unwrap the list
        print(embedding[0])
        doc_embeddings.append({
            'id': doc['id'][0],  # Unwrap the list
            'contents': doc['text'][0],  # Unwrap the list
            'vector': embedding[0].tolist()
        })


    # Save document embeddings
    with open(args.output + '_docs.jsonl', 'w') as f:
        for doc_embedding in doc_embeddings:
            f.write(json.dumps(doc_embedding, ensure_ascii=False) + '\n')

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
        query_embeddings.append({
            'id': query['id'],
            'contents': query['text'],  # Single string, not a list
            'vector': embedding.tolist()  # Single list, not nested
        })

    # Save query embeddings
    with open(args.output + '_queries.jsonl', 'w') as f:
        for query_embedding in query_embeddings:
            f.write(json.dumps(query_embedding, ensure_ascii=False) + '\n')

if __name__ == '__main__':
    main()
