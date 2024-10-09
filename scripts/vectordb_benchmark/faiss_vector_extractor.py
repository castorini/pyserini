from pyserini.util import download_prebuilt_index
from pyserini.search import FaissSearcher
import argparse
import numpy as np
import duckdb
import faiss

TREC_DOT_PRODUCT_OUTPUT_FILE_PATH = '../../runs/.run-faiss-msmarco-passage-result_dot_product.txt'

class FaissVectorExtractor:
    def __init__(self, index_name):
        try:
            index_dir = download_prebuilt_index(index_name, verbose=True)
        except ValueError as e:
            print(str(e))
            exit(1)
        self.index_file_path = index_dir + '/index'
        self.docid_file_path = index_dir + '/docid'
        self.index = None
        self.docids = None

    def load_index(self):
        self.index = faiss.read_index(self.index_file_path)
        self.docids = FaissSearcher.load_docids(self.docid_file_path)
        if not self.index:
            raise Exception(f"Failed to load index from {self.index_file_path}")
    
    def extract_all_vectors(self):
        if self.index is None:
            self.load_index()
        vectors = self.index.reconstruct_n(0, self.index.ntotal)
        vector_map = {self.docids[i]: vector for i, vector in enumerate(vectors)}

        print("Finished loading index and reconstructed all vectors")
        return vector_map

    def extract_one_batch_of_vectors(self, start_id, batch_size):
        if self.index is None:
            print("Loading index")
            self.load_index()
        batch_end = min(start_id + batch_size, self.index.ntotal)
        vectors = self.index.reconstruct_n(start_id, batch_end - start_id)
        vector_map = {self.docids[i+start_id]: vector for i, vector in enumerate(vectors)}
        return vector_map

def load_index_and_docids(query_index_path):
    docids = FaissSearcher.load_docids(query_index_path + '/docid')
    index = faiss.read_index(query_index_path + '/index')
    vector_map = {}
    for i in range(index.ntotal):
        docid = docids[i]
        vector = index.reconstruct(i)
        vector_map[docid] = vector
    return vector_map
    
def run_benchmark(trec_output_file_path, metric, query_index_path, adaptor, table_name):
    query_vector_map = load_index_and_docids(query_index_path)
    adaptor.run_benchmark(table_name, metric, 20, 768, trec_output_file_path, query_vector_map)

def run_benchmark_on_file(trec_output_file_path, metric, file_path, table_name, adaptor):
    adaptor.create_in_memory_hnsw_index_on_file(file_path, table_name)
    adaptor.run_benchmark(table_name, metric, 20, 768, trec_output_file_path)
    