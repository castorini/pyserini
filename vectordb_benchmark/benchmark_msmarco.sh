python3 vectordb_benchmark/run_benchmark.py \
--index_name='msmarco-v1-passage.bge-base-en-v1.5' \
--table_name='msmarco' \
--metric='ip' \
--query_index_path='/store/scratch/x59song/Research/pyserini/indexes/msmarco-dev.bge-base-en-v1.5' \
--db_type='pgvector' \
