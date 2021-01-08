import argparse
import os

import faiss
import numpy as np
import pandas as pd

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--embedding", type=str, help='encoder name or path', required=True)
    parser.add_argument("--index-type", type=str, help='doc file to get encoded.', required=True)
    parser.add_argument("--index-dir", type=str, help='doc type, [passage, query]', required=True)
    args = parser.parse_args()

    print('Loading Embeddings')
    embedding_df = pd.read_pickle(args.embedding)
    embeddings = np.stack(embedding_df['embedding'])
    dimension = embeddings.shape[1]
    docids = embedding_df['id'].to_numpy()

    print('Indexing')
    if args.index_type == 'hnsw':
        index = faiss.IndexHNSWFlat(dimension, 256, faiss.METRIC_INNER_PRODUCT)
        index.hnsw.efConstruction = 256  # hardcode for now
        index.hnsw.efSearch = 256  # hardcode for now
    else:
        index = faiss.IndexFlatIP(dimension)
    index.add(embeddings)
    faiss.write_index(index, os.path.join(args.index_dir, 'index'))
    with open(os.path.join(args.index_dir, 'docid'), 'w') as f:
        for docid in docids:
            f.write(f'{str(docid)}\n')

    print("Done!")
