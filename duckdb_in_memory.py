import duckdb
import faiss_vector_extractor

# Open the file-based DuckDB database
file_con = duckdb.connect('my_database.duckdb')

# Create an in-memory DuckDB database
mem_con = duckdb.connect(database=':memory:')

# Extract data from the file-based msmarco table into a Pandas DataFrame
df = file_con.execute("SELECT * FROM msmarco").fetchdf()

# Register the DataFrame in the in-memory DuckDB database
mem_con.register('msmarco', df)

# Now you can create the HNSW index on the msmarco table in the in-memory database
mem_con.execute(f"CREATE INDEX hnsw_idx ON msmarco USING HNSW(vector) WITH (metric = 'ip')")

# Continue with your operations...
