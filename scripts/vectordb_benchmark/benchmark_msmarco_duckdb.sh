python3 ./run_benchmark.py \
--index_name='msmarco-v1-passage.bge-base-en-v1.5' \
--table_name='msmarco' \
--metric='ip' \
--query_index_path='../../indexes/msmarco-dev.bge-base-en-v1.5' \
--db_type='duckdb' \
--db_config_file='duckdb_db_config.txt' 
