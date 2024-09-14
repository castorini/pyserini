# Overview
This document contains instructions for setting up and running benchmarks for querying MSMarco and NFCorpus using DuckDB and PGVector.

# Prerequisites
- Pyserini Setup 

# Database setup
First, activate a Conda environment, for example your pyserini environment.

```bash
conda activate pyserini
```
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

# PGVector
PGVector is an extension of PostgreSQL, so you will need to install both PostgreSQL and PGVector. 

## PostgreSQL and pgvector Installation Guide (Conda)

This guide provides step-by-step instructions on how to install PostgreSQL using Conda and manually install the `pgvector` extension. By following these instructions, you'll be able to set up PostgreSQL and create the `pgvector` extension successfully.

### Install PostgreSQL
```bash
conda install -c conda-forge postgresql
```

### Initialize and start the database
```bash
initdb -D /path/to/your/database_directory
pg_ctl -D /path/to/your/database_directory start
```

### Install and activate PGVector
To manually install pgvector, first install the necessary build tools (gcc and make) using Conda:
```bash
conda install -c conda-forge gcc_linux-64 make
```

```bash
git clone https://github.com/pgvector/pgvector.git
cd pgvector
make PG_CONFIG=$(which pg_config)
make install
```

After the installation, verify that the pgvector.control file and library were installed correctly:
```bash
ls $(pg_config --sharedir)/extension/pgvector.control
ls $(pg_config --pkglibdir)/vector.so
```
If both files are present, the installation was successful.

Restart PostgreSQL to enable the pgvector extension:
```bash
pg_ctl -D /path/to/your/database_directory stop
pg_ctl -D /path/to/your/database_directory start
```

```bash
psql postgres
CREATE EXTENSION pgvector;
```

Now that you have the PGVector extension installed and enabled in PostgreSQL. You can start running the benchmark, but first, make sure you supply the correct database configuration in the `pgvector_db_config.txt` file. For example:

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

Note that after one run, your postgresql will contain the table data, so you may want to drop the table after running the benchmark. Later, we will add an option to skip table creation and index building, so that you can run the benchmark multiple times without having to re-create the table and index every time.

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
python3 benchmark_nfcorpus_duckdb.py 
python3 benchmark_nfcorpus_pgvector.py
