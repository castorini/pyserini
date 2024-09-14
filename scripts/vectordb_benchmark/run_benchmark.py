import faiss_vector_extractor
import duckdb_faiss_index_adaptor
import pgvector_faiss_index_adaptor
import faiss_index_adaptor
import argparse
from faiss_vector_extractor import run_benchmark, run_benchmark_on_file

TREC_DOT_PRODUCT_OUTPUT_FILE_PATH = "../../trec_dot_product_output.txt"


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='FAISS Vector DB Index Constructor')
    parser.add_argument('--index_name', type=str, required=True, help='name of the FAISS index file')
    parser.add_argument('--metric', type=str, required=True, help='metric of the FAISS index')
    parser.add_argument('--table_name', type=str, required=True, help='name of the table to store the vectors')
    parser.add_argument('--query_index_path', type=str, required=True, help='optional, if given, run benchmark on the query index')
    parser.add_argument('--db_type', type=str, required=True, help='type of the database')
    parser.add_argument('--db_config_file', type=str, required=True, help='config of the database, separated by end of line, key:value')

    args = parser.parse_args()

    # parse the db_config_file
    with open(args.db_config_file, 'r') as f:
        db_config = f.readlines()
    DBConfig = {line.strip().split(':')[0]: line.strip().split(':')[1] for line in db_config}
    
    if args.db_type == 'duckdb':
        adaptor = duckdb_faiss_index_adaptor.DuckDBVectorDBFaissIndexAdaptor(args.index_name, DBConfig)
    elif args.db_type == 'pgvector':
        adaptor = pgvector_faiss_index_adaptor.PGVectorFaissIndexAdaptor(args.index_name, DBConfig)
    
    if args.file_path:
        run_benchmark_on_file(TREC_DOT_PRODUCT_OUTPUT_FILE_PATH, args.metric, args.query_index_path, adaptor, args.table_name)
    else:
        adaptor.extract_vectors_and_construct_index(args.table_name, args.metric)
        run_benchmark(TREC_DOT_PRODUCT_OUTPUT_FILE_PATH, args.metric, args.query_index_path, adaptor, args.table_name)

    

