import argparse
import faiss
import faiss_vector_extractor

TREC_DOT_PRODUCT_OUTPUT_FILE_PATH = "/store/scratch/x59song/trec_dot_product_output.txt"
    
def run_benchmark(trec_output_file_path, metric, query_index_path, adaptor):
    query_vector_map = load_index_and_docids(query_index_path)
    adaptor.run_benchmark(query_vector_map, table_name, metric, 20, 768, trec_output_file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FAISS Vector DB Index Constructor')
    parser.add_argument('--index_name', type=str, required=True, help='name of the FAISS index file')
    parser.add_argument('--metric', type=str, required=True, help='metric of the FAISS index')
    parser.add_argument('--table_name', type=str, required=True, help='name of the table to store the vectors')
    args = parser.parse_args()

    DBConfig = {
        'temp_directory': '/store/scratch/x59song/temp',
        'memory_limit': '50GB'
    }

    adaptor = DuckDBVectorDBFaissIndexAdaptor(args.index_name, DBConfig)
    adaptor.extract_vectors_and_construct_index(args.table_name, args.metric)
    run_benchmark(TREC_DOT_PRODUCT_OUTPUT_FILE_PATH, args.metric, args.index_name, adaptor)

    