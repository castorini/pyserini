import faiss_index_adaptor
import psycopg2
import pandas as pd
import numpy as np
import time

class PGVectorFaissIndexAdaptor(faiss_index_adaptor.VectorDBFaissIndexAdaptor):
    def __init__(self, index_name, DBConfig):
        super().__init__(index_name, DBConfig)
        self.con = None
    
    def initialize_database_and_table(self, table_name, DBConfig, vector_size):
        # connect to the database
        conn = psycopg2.connect(
            dbname=DBConfig['dbname'],
            user=DBConfig['user'],
            password=DBConfig['password'],
            host=DBConfig['host'],
            port=DBConfig['port']
        )
        cur = conn.cursor()
        cur.execute(f"DROP TABLE IF EXISTS {table_name};")
        cur.execute(f"DROP INDEX IF EXISTS {table_name}_vector_ip_ops_idx;")
        cur.execute(f"DROP INDEX IF EXISTS {table_name}_vector_l2_ops_idx;")
        cur.execute(f"DROP INDEX IF EXISTS {table_name}_vector_cosine_ops_idx;")
        # Create documents table
        cur.execute(f"""
        CREATE TABLE {table_name} (
            id INT,
            vector VECTOR({vector_size})
        )
        """)
        conn.commit()
        self.con = conn
        self.cur = cur
        print(f"created table {table_name}")
    
    def construct_index(self, table_name, metric):
        start_time = time.time()
        self.cur.execute(f"CREATE INDEX ON {table_name} USING HNSW (vector vector_{metric}_ops);")
        end_time = time.time()
        print(f"Index constructed for {table_name} using {metric} metric in {end_time - start_time} seconds")

    def insert_vector_map_into_table(self, table_name, metric):
        # Convert the numpy array to a list before inserting
        insert_data = [(key, vector.tolist()) for key, vector in self.vector_map.items()]

        # Execute the SQL command with the list data
        self.cur.executemany(
            f"INSERT INTO {table_name} (id, vector) VALUES (%s, %s::vector)",
            insert_data
        )
        self.con.commit()  # Use `conn.commit()` to commit the transaction

    def get_connection(self):
        return self.con
    
    # close the connection
    def close(self):
        self.con.close()
    
    def run_benchmark(self, table_name, metric, K, vector_size, trec_file_path, query_vector_map=None):
        print(f"running benchmark for {table_name} with metric {metric}")
        with open(trec_file_path, 'w') as trec_file:
            count = 0
            query_times = []
            sql_query = ""
            for query_id, query_vector in query_vector_map.items():
                # Select appropriate SQL query based on the metric
                if metric == 'l2sq':
                    sql_query = f"SELECT id, vector <-> %s::vector AS score FROM {table_name} ORDER BY score LIMIT %s"
                elif metric == 'ip':
                    sql_query = f"SELECT id, (vector <#> %s::vector) * -1 AS score FROM {table_name} ORDER BY score DESC LIMIT %s"
                elif metric == 'cosine':
                    sql_query = f"SELECT id, 1 - (vector <=> %s::vector) AS score FROM {table_name} ORDER BY score DESC LIMIT %s"
                
                # time the execution
                start_time = time.time()
                self.cur.execute(sql_query, (query_vector.tolist(), K))  # Execute the query
                results = self.cur.fetchall()  # Fetch all results from the executed query
                end_time = time.time()
                query_time = end_time - start_time
                query_times.append(query_time)

                # Write results in TREC format
                for rank, (doc_id, score) in enumerate(results, start=1):
                    trec_file.write(f"{query_id} Q0 {doc_id} {rank} {score} PGVector\n")
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

