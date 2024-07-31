from pyserini.util import download_prebuilt_index
from pyserini.search import FaissSearcher
import argparse
import numpy as np

# Path to the FAISS index file
# index_path = '/u4/x59song/.cache/pyserini/indexes/faiss-flat.msmarco-v1-passage.bge-base-en-v1.5.20240107.b21fb6abee3be6da3b6f39c9f6d9f280/index'

import faiss

class FaissVectorExtractor:
    def __init__(self, index_name, output_file_path, batch_size=10000, start_id=0, num_batches=1):
        try:
            index_dir = download_prebuilt_index(index_name, verbose=True)
        except ValueError as e:
            print(str(e))
            exit(1)
        self.index_file_path = index_dir + '/index'
        self.output_file_path = output_file_path
        self.batch_size = batch_size
        self.index = None
        self.start_id = start_id
        self.num_batches = num_batches

    def load_index(self):
        self.index = faiss.read_index(self.index_file_path)
        if not self.index:
            raise Exception(f"Failed to load index from {self.index_file_path}")

    def extract_vectors(self):
        if self.index is None:
            self.load_index()

        with open(self.output_file_path, "w") as f:
            for batch_start in range(self.start_id, min(self.index.ntotal, self.start_id + self.num_batches * self.batch_size), self.batch_size):
                batch_end = min(batch_start + self.batch_size, self.index.ntotal)
                
                # reconstruct 1000 vectors most, so avoid memory overflow
                vectors = self.index.reconstruct_n(batch_start, batch_end - batch_start)
                for i, vector in enumerate(vectors):
                    vector_str = ",".join(map(str, vector))
                    f.write(f"{batch_start + i}\t{vector_str}\n")

        print(f"Mappings have been written to {self.output_file_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FAISS Vector Extractor')
    parser.add_argument('--index_name', type=str, required=True, help='name of the FAISS index file')
    parser.add_argument('--output_file', type=str, required=True, help='Path to the output file for docid to vector mappings')
    parser.add_argument('--batch_size', type=int, default=10000, help='Batch size for processing vectors (default: 10000)')
    parser.add_argument('--start_id', type=int, default=0, help='Start ID for processing vectors (default: 0)')
    parser.add_argument('--num_batches', type=int, default=1, help='Number of batches to process (default: 1)')

    args = parser.parse_args()

    extractor = FaissVectorExtractor(args.index_name, args.output_file, args.batch_size, args.start_id, args.num_batches)
    extractor.extract_vectors()
