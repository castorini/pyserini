# A virtual class that takes in an index name, and creates a FaissVectorExtractor,
# Extract the vectors, and then construct a vector db index
import faiss_vector_extractor
import time
import subprocess

class VectorDBFaissIndexAdaptor:
    def __init__(self, index_name, DBConfig):
        self.index_name = index_name
        self.extractor = faiss_vector_extractor.FaissVectorExtractor(index_name)
        self.vector_map = None
        self.table_name = None
        self.DBConfig = DBConfig
    
    def extract_vectors_and_construct_index(self, table_name, metric, extract_all_vectors=False, vector_size=768):
        self.initialize_database_and_table(table_name, self.DBConfig, vector_size)
        # if extract all vectors, extract all, otherwise extract by batch via a while loop
        # if extract_all_vectors:
        #     self.vector_map = self.extractor.extract_all_vectors()
        #     self.insert_vector_map_into_table(table_name, metric)
        # else:
        #     startid = 0
        #     batch_size = 100000
        #     self.extractor.load_index()
        #     while startid < self.extractor.index.ntotal:
        #         # time extraction
        #         start_time = time.time()
        #         self.vector_map = self.extractor.extract_one_batch_of_vectors(startid, batch_size)
        #         end_time = time.time()
        #         print(f"Extracted {batch_size} vectors in {end_time - start_time} seconds")
        #         self.insert_vector_map_into_table(table_name, metric)
        #         startid += batch_size
        self.construct_index(table_name, metric)
    
    def insert_vector_map_into_table(self, table_name, metric):
        pass
    
    def construct_index(self, table_name, metric):
        pass      
    
    def initialize_database_and_table(self, table_name, DBConfig, vector_size):
        pass
    
    def get_connection(self):
        pass

    def run_benchmark(self, table_name, metric, K, vector_size, trec_file_path, query_vector_map=None):
        pass

    def run_trec_eval(self, trec_output_file_path):
        """Runs TREC evaluation and prints ndcg@10."""
        command = [
            "python", "-m", "pyserini.eval.trec_eval",
            "-c", "-M", "10", "-m", "recip_rank",
            "collections/msmarco-passage/qrels.dev.small.trec",
            trec_output_file_path
        ]
        return subprocess.run(command)
    

