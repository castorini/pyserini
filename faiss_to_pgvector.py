from pyserini.util import download_prebuilt_index
import faiss
import numpy as np

# Path to the FAISS index file
index_path = '/Users/seansong/.cache/pyserini/indexes/faiss-flat.msmarco-v1-passage.bge-base-en-v1.5.20240107.b21fb6abee3be6da3b6f39c9f6d9f280/index'

# Read the index from the file
index = faiss.read_index(index_path)

# Retrieve the vectors from the index
# Assuming the index is flat, use index.reconstruct_n to get all vectors
num_vectors = index.ntotal  # Total number of vectors in the index
dim = index.d  # Dimension of the vectors

vectors = np.zeros((num_vectors, dim), dtype='float32')
# for i in range(num_vectors):
#     vectors[i] = index.reconstruct(i)
try:
    index_dir = download_prebuilt_index('msmarco-v1-passage.bge-base-en-v1.5', verbose=True)
except ValueError as e:
    print(str(e))
    exit(1)
