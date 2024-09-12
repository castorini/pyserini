python3 ./run_benchmark.py \
--index_name='msmarco-v1-passage.bge-base-en-v1.5' \
--table_name='msmarco' \
--metric='ip' \
--query_index_path='/store/scratch/x59song/Research/pyserini/indexes/msmarco-dev.bge-base-en-v1.5' \
--db_config_file='duckdb_db_config.txt' \
--db_type='duckdb' \
