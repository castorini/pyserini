import faiss_index_adaptor
import duckdb
import faiss_vector_extractor
import time
import numpy as np

class DuckDBVectorDBFaissIndexAdaptor(faiss_index_adaptor.VectorDBFaissIndexAdaptor):
    def __init__(self, index_name, DBConfig):
        super().__init__(index_name, DBConfig)
        self.con = None
    
    def initialize_database_and_table(self, table_name, DBConfig, vector_size):
        memory_limit = DBConfig['memory_limit']
        self.con = duckdb.connect(database=':memory:')
        self.con.execute("INSTALL vss")
        self.con.execute("LOAD vss")
        self.con.execute(f"PRAGMA memory_limit='{memory_limit}'")

        # Create documents table
        self.con.execute(f"""
        CREATE TABLE {table_name} (
            id INT,
            vector FLOAT[{vector_size}]
        )
        """)
        print(f"created table {table_name}")
    
    def construct_index(self, table_name, metric):
        self.con.execute(f"CREATE INDEX {metric}_idx ON {table_name} USING HNSW(vector) WITH (metric = '{metric}')")
        print(f"Index constructed for {table_name} using {metric} metric")

    def insert_vector_map_into_table(self, table_name, metric):
        start_time = time.time()
        for id, vector in self.vector_map.items():
            self.con.execute(f"INSERT INTO {table_name} (id, vector) VALUES (?, ?)", (id, vector))
        self.con.commit()
        end_time = time.time()
        print(f"Inserted {len(self.vector_map)} vectors into {table_name} in {end_time - start_time} seconds")
    
    def get_connection(self):
        return self.con
    
    # close the connection
    def close(self):
        self.con.close()
    
    def run_benchmark(self, table_name, metric, K, vector_size, trec_file_path, query_vector_map=None):
        print(f"running benchmark for {table_name} with metric {metric}")
         # Select appropriate SQL query based on the metric
        if metric == 'l2sq':
            evaluation_metric = 'array_distance'
        elif metric == 'cosine':
            evaluation_metric = 'array_cosine_similarity'
        elif metric == 'ip':
            evaluation_metric = 'array_inner_product'
        with open(trec_file_path, 'w') as trec_file:
            count = 0
            query_times = []
            for query_id, query_vector in query_vector_map.items():
                sql_query = f"SELECT id, {evaluation_metric}(vector, ?::FLOAT[{vector_size}]) as score FROM {table_name} ORDER BY score DESC LIMIT ?"
                # time the execution
                start_time = time.time()
                results = self.con.execute(sql_query, (query_vector, K)).fetchall()
                end_time = time.time()

                # Calculate the time for this query and add it to the list
                query_time = end_time - start_time
                query_times.append(query_time)

                # Write results in TREC format
                for rank, (doc_id, score) in enumerate(results, start=1):
                    trec_file.write(f"{query_id} Q0 {doc_id} {rank} {score} DuckDB\n")
                count += 1
                if count % 100 == 0:
                    print(f"processed {count} queries")
        
        print(f"TREC results written to {trec_file_path}")
        ans = self.run_trec_eval(trec_file_path)
        # Aggregate statistics
        total_time = sum(query_times)
        mean_time = np.mean(query_times)
        variance_time = np.var(query_times)
        min_time = min(query_times)
        max_time = max(query_times)
        # create a file to store results
        with open(f"{table_name}_benchmark_results.txt", "w") as f:
            f.write(f"Total time: {total_time}\n")
            f.write(f"Mean time: {mean_time}\n")
            f.write(f"Variance time: {variance_time}\n")
            f.write(f"Min time: {min_time}\n")
            f.write(f"Max time: {max_time}\n")
            f.write(f"TREC eval output: {ans}\n")
        return total_time, mean_time, variance_time, min_time, max_time
    
    def create_in_memory_hnsw_index_on_file(self, file_path, table_name):
        # Open the file-based DuckDB database
        file_con = duckdb.connect(file_path)

        # Create an in-memory DuckDB database
        self.con = duckdb.connect(database=':memory:')
        self.con.execute("INSTALL vss")
        self.con.execute("LOAD vss")

        # Extract data from the file-based table into a Pandas DataFrame
        df = file_con.execute(f"SELECT * FROM {table_name}").fetchdf()

        df['vector'] = df['vector'].apply(lambda x: x if isinstance(x, list) else list(x))

        # Create a new table in the in-memory DuckDB database
        self.con.execute("CREATE TABLE msmarco AS SELECT * FROM df")

        # Cast the vector column to the required FLOAT[N] type if necessary
        self.con.execute("ALTER TABLE msmarco ALTER COLUMN vector SET DATA TYPE FLOAT[]")

        # Now you can create the HNSW index on the msmarco table in the in-memory database
        self.con.execute(f"CREATE INDEX hnsw_idx ON msmarco USING HNSW(vector) WITH (metric = 'ip')")
