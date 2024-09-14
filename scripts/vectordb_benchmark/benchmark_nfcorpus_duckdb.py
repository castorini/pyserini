import json
import duckdb
import numpy as np
import subprocess
import time

# Paths to embedding, query, and output files
DOCUMENT_JSONL_FILE_PATH = 'indexes/non-faiss-nfcorpus/documents/embeddings.jsonl'
QUERY_JSONL_FILE_PATH = 'indexes/non-faiss-nfcorpus/queries/embeddings.jsonl'
TREC_DOT_PRODUCT_OUTPUT_FILE_PATH = 'runs/.run-non-faiss-nfcorpus-result_dot_product.txt'
TREC_COSINE_OUTPUT_FILE_PATH = 'runs/.run-non-faiss-nfcorpus-result_cosine.txt'
TREC_L2SQ_OUTPUT_FILE_PATH = 'runs/.run-non-faiss-nfcorpus-result_l2sq.txt'
K = 10  # Number of nearest neighbors to retrieve
RUN_ID = "DuckDBHNSW"  # Identifier for the run

def get_vector_size(jsonl_file_path):
    """Determines the size of the vector, assuming vectors all have the same dimension."""
    with open(jsonl_file_path, 'r') as file:
        for line in file:
            data = json.loads(line)
            vector = data.get('vector', [])
            return len(vector)
    return 0

def insert_data_into_table(con, id, content, vector, table):
    """Inserts data into the DuckDB table."""
    con.execute(f"INSERT INTO {table} (id, content, vector) VALUES (?, ?, ?)", (id, content, vector))

def setup_database():
    """Sets up the DuckDB database and inserts document data."""
    con = duckdb.connect(database=':memory:')
    con.execute("INSTALL vss")
    con.execute("LOAD vss")
    con.execute("PRAGMA temp_directory='/tmp/duckdb_temp'")
    con.execute("PRAGMA memory_limit='4GB'")
    
    vector_size = get_vector_size(DOCUMENT_JSONL_FILE_PATH)
    print(f"Vector size: {vector_size}")

    # Create documents table
    con.execute(f"""
        CREATE TABLE documents (
            id STRING,
            content STRING,
            vector FLOAT[{vector_size}]
        )
    """)

    # Insert data from JSONL file
    with open(DOCUMENT_JSONL_FILE_PATH, 'r') as file:
        for line in file:
            data = json.loads(line)
            insert_data_into_table(con, data['id'], data['contents'], data['vector'], 'documents')

    # Create HNSW indices with different metrics
    # print the time taken for each index building
    start_time = time.time()
    con.execute("CREATE INDEX l2sq_idx ON documents USING HNSW(vector) WITH (metric = 'l2sq')")
    print('building l2sq index: ', time.time() - start_time)
    start_time = time.time()
    con.execute("CREATE INDEX cos_idx ON documents USING HNSW(vector) WITH (metric = 'cosine')")
    print('building cosine index: ', time.time() - start_time)
    start_time = time.time()
    con.execute("CREATE INDEX ip_idx ON documents USING HNSW(vector) WITH (metric = 'ip')")
    print('building ip index: ', time.time() - start_time)

    return con

def run_trec_eval(trec_output_file_path):
    """Runs TREC evaluation and prints ndcg@10."""
    command = [
        "python", "-m", "pyserini.eval.trec_eval",
        "-c", "-m", "ndcg_cut.10",
        "collections/nfcorpus/qrels/test.qrels",
        trec_output_file_path
    ]
    print("ndcg@10 for ", trec_output_file_path)
    subprocess.run(command)

def run_benchmark(con, trec_output_file_path, metric):
    """Runs the benchmark and writes results in TREC format."""
    query_times = []
    with open(trec_output_file_path, 'w') as trec_file:
        with open(QUERY_JSONL_FILE_PATH, 'r') as query_file:
            for line in query_file:
                data = json.loads(line)
                query_id = data['id']
                vector = data['vector']

                # Select appropriate SQL query based on the metric
                if metric == 'l2sq':
                    evaluation_metric = 'array_distance'
                elif metric == 'cosine':
                    evaluation_metric = 'array_cosine_similarity'
                elif metric == 'ip':
                    evaluation_metric = 'array_inner_product'

                sql_query = f"SELECT id, {evaluation_metric}(vector, ?::FLOAT[{len(vector)}]) as score FROM documents ORDER BY score DESC LIMIT ?"
                # time the execution
                start_time = time.time()
                results = con.execute(sql_query, (vector, K)).fetchall()
                end_time = time.time()

                # Calculate the time for this query and add it to the list
                query_time = end_time - start_time
                query_times.append(query_time)

                # Write results in TREC format
                for rank, (doc_id, score) in enumerate(results, start=1):
                    trec_file.write(f"{query_id} Q0 {doc_id} {rank} {score} {RUN_ID}\n")

    print(f"TREC results written to {trec_output_file_path}")
    run_trec_eval(trec_output_file_path)
    # Aggregate statistics
    total_time = sum(query_times)
    mean_time = np.mean(query_times)
    variance_time = np.var(query_times)
    min_time = min(query_times)
    max_time = max(query_times)
    return total_time, mean_time, variance_time, min_time, max_time

if __name__ == "__main__":
    con = setup_database()

    # Running the benchmarks
    print('l2sq: ', run_benchmark(con, TREC_L2SQ_OUTPUT_FILE_PATH, 'l2sq'))
    print('cosine: ', run_benchmark(con, TREC_COSINE_OUTPUT_FILE_PATH, 'cosine'))
    print('ip: ', run_benchmark(con, TREC_DOT_PRODUCT_OUTPUT_FILE_PATH, 'ip'))

    # second run
    print("second run")
    print('l2sq: ', run_benchmark(con, TREC_L2SQ_OUTPUT_FILE_PATH, 'l2sq'))
    print('cosine: ', run_benchmark(con, TREC_COSINE_OUTPUT_FILE_PATH, 'cosine'))
    print('ip: ', run_benchmark(con, TREC_DOT_PRODUCT_OUTPUT_FILE_PATH, 'ip'))
