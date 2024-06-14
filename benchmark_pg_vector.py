import psycopg2
import json
import subprocess

# Paths to embedding, query, and output files
DOCUMENT_JSONL_FILE_PATH = 'indexes/non-faiss-nfcorpus/documents/embeddings.jsonl'
QUERY_JSONL_FILE_PATH = 'indexes/non-faiss-nfcorpus/queries/embeddings.jsonl'
TREC_DOT_PRODUCT_OUTPUT_FILE_PATH = 'runs/.run-non-faiss-nfcorpus-result_dot_product.txt'
TREC_COSINE_OUTPUT_FILE_PATH = 'runs/.run-non-faiss-nfcorpus-result_cosine.txt'
TREC_L2SQ_OUTPUT_FILE_PATH = 'runs/.run-non-faiss-nfcorpus-result_l2sq.txt'
VECTOR_SIZE = 768
K = 10  # Number of nearest neighbors to retrieve
RUN_ID = "PostgresHNSW"

def insert_data_into_table(cur, id, content, vector):
    """Inserts data into the PostgreSQL table."""
    cur.execute("INSERT INTO documents (id, content, vector) VALUES (%s, %s, %s)", (id, content, vector))

def setup_database():
    """Sets up the PostgreSQL database and inserts document data."""
    conn = psycopg2.connect(
        dbname='main_database',
        user='mainuser',
        password='password',
        host='localhost',
        port='5432'
    )
    cur = conn.cursor()

    # Create documents table
    cur.execute(f"""
        CREATE TABLE documents (
            id TEXT PRIMARY KEY,
            content TEXT,
            vector VECTOR({VECTOR_SIZE})
        )
    """)
    conn.commit()

    # Insert data from JSONL file
    with open(DOCUMENT_JSONL_FILE_PATH, 'r') as file:
        for line in file:
            data = json.loads(line)
            insert_data_into_table(cur, data['id'], data['contents'], data['vector'])
    conn.commit()

    # Create indexes with pgvector
    cur.execute("CREATE INDEX ON documents USING ivfflat (vector vector_l2_ops);")
    cur.execute("CREATE INDEX ON documents USING ivfflat (vector vector_cosine_ops);")
    cur.execute("CREATE INDEX ON documents USING ivfflat (vector vector_ip_ops);")
    conn.commit()

    return cur, conn

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

def run_benchmark(cur, trec_output_file_path, metric):
    """Runs the benchmark and writes results in TREC format."""
    with open(trec_output_file_path, 'w') as trec_file:
        with open(QUERY_JSONL_FILE_PATH, 'r') as query_file:
            for line in query_file:
                data = json.loads(line)
                query_id = data['id']
                vector = data['vector']

                # Select appropriate SQL query based on the metric
                if metric == 'l2sq':
                    sql_query = "SELECT id, vector <-> %s::vector AS score FROM documents ORDER BY vector <-> %s::vector LIMIT %s"
                elif metric == 'ip':
                    sql_query = "SELECT id, vector <#> %s::vector AS score FROM documents ORDER BY vector <#> %s::vector LIMIT %s"
                elif metric == 'cosine':
                    sql_query = "SELECT id, vector <=> %s::vector AS score FROM documents ORDER BY vector <=> %s::vector DESC LIMIT %s"

                cur.execute(sql_query, (vector, vector, K))
                results = cur.fetchall()

                # Write results in TREC format
                for rank, (doc_id, score) in enumerate(results, start=1):
                    trec_file.write(f"{query_id} Q0 {doc_id} {rank} {score} {RUN_ID}\n")

    print(f"TREC results written to {trec_output_file_path}")
    run_trec_eval(trec_output_file_path)

if __name__ == "__main__":
    cur, conn = setup_database()

    # Running the benchmarks
    run_benchmark(cur, TREC_L2SQ_OUTPUT_FILE_PATH, 'l2sq')
    run_benchmark(cur, TREC_COSINE_OUTPUT_FILE_PATH, 'cosine')
    run_benchmark(cur, TREC_DOT_PRODUCT_OUTPUT_FILE_PATH, 'ip')

    # Close PostgreSQL connection
    cur.close()
    conn.close()
