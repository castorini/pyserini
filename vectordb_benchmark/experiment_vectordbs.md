# Overview
This document contains instructions for setting up and running benchmarks for querying MSMarco and NFCorpus using DuckDB and PGVector.

# Prerequisites
- Pyserini Setup 
- DuckDB 0.10.0+ installed
- PostgreSQL 14.0+ preferred
- PGVector 0.6.0+ installed

# Database setup
## DuckDB
Duckdb is relatively easy to set up, as it is an in-memory database that can be embedded into a process. Therefore, a simple
`pip install duckdb` will suffice. Then, you should supply a config file, `duckdb_db_config.txt`, to specify the database configuration. The only parameter you need to tune is how much memory you want to allocate to the database. 
```
memory_limit:100GB
```
Then, you can simply run the following, to run the benchmark. 

```
$ python3 vectordb_benchmark/run_benchmark.py \
        --index_name='msmarco-v1-passage.bge-base-en-v1.5' \
        --table_name='msmarco' \
        --metric='ip' \
        --query_index_path='pyserini/indexes/msmarco-dev.bge-base-en-v1.5' \
        --db_type='duckdb' 
        --db_config_file='duckdb_db_config.txt' \
```
The entire process may take over a day to complete, depending on your hardware set up. This code will download the index, extract the embedded vectors of the index, build the table in duckdb and run the benchmark.

## PGVector
PGVector is an extension of PostgreSQL, so you will need to install PostgreSQL and PGVector. Here, it is assumed that you have a PostgreSQL server running on your local machine, and you have the PGVector extension installed and enabled in PostgreSQL. Make sure you supply the correct database configuration in the `db_config.txt` file. For example:

```
dbname: main_db
user: main_user
password: 123456
host: localhost
port: 5432
```

Then, you can run the benchmark by running the following command. 

```
$ python3 vectordb_benchmark/run_benchmark.py \
        --index_name='msmarco-v1-passage.bge-base-en-v1.5' \
        --table_name='msmarco' \
        --metric='ip' \
        --query_index_path='pyserini/indexes/msmarco-dev.bge-base-en-v1.5' \
        --db_type='pgvector' \
        --db_config_file='pgvector_db_config.txt' \
```

# Encoding and Benchmarking NFCorpus using DuckDB and PGVector

This document contains instructions for encoding and benchmarking NFCorpus using DuckDB and PGVector.

## 1. Encode the Corpus
Create a directory for document embeddings and encode the corpus using the specified encoder.

```bash
mkdir indexes/non-faiss-nfcorpus/documents
python -m pyserini.encode \
  input   --corpus collections/nfcorpus/corpus.jsonl \
          --fields title text \
  output  --embeddings indexes/non-faiss-nfcorpus/documents \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --fields title text \
          --batch 32
```

## 2. Encode the Queries
Create a directory for query embeddings and encode the queries using the specified encoder.

```bash
mkdir indexes/non-faiss-nfcorpus/queries
python -m pyserini.encode \
  input   --corpus collections/nfcorpus/queries.jsonl \
          --fields title text \
  output  --embeddings indexes/non-faiss-nfcorpus/queries \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --fields title text \
          --batch 32
```

## 3. Run Benchmarks

```bash
python3 benchmark_duckdb.py 
python3 benchmark_pgvector.py
