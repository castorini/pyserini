# Overview
We are going to run benchmarks for MSMarco and NFCorpus using DuckDB and PGVector on HNSW indexes.

# MSMarco

## Data Prep
Similar to the onboarding docs, we must first download and setup the collections and indexes if they are not already downloaded. Except this time, we only need to index the queries, the index itself will be downloaded and extracted by the faiss_index_extractor. First, we need to download the MSMarco Dataset.

```bash
mkdir collections/msmarco-passage

wget https://msmarco.blob.core.windows.net/msmarcoranking/collectionandqueries.tar.gz -P collections/msmarco-passage

# Alternative mirror:
# wget https://www.dropbox.com/s/9f54jg2f71ray3b/collectionandqueries.tar.gz -P collections/msmarco-passage

tar xvfz collections/msmarco-passage/collectionandqueries.tar.gz -C collections/msmarco-passage
```

Next, we need to convert the MS MARCO tsv queries into Pyserini's jsonl files (which have one json object per line):

```bash
python tools/scripts/msmarco/convert_collection_to_jsonl.py \
 --collection-path collections/msmarco-passage/queries.dev.small.tsv \
 --output-folder collections/msmarco-passage/queries_jsonl
```

Now, we need to convert the jsonl queries into a faiss index.

```bash
python -m pyserini.encode \
  input   --corpus collections/msmarco-passage/queries_jsonl \
  output  --embeddings collections/msmarco-passage/queries_faiss \
          --to-faiss \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --batch 32
```

Now, after the data is prepared, we can run the benchmark on DuckDB.

# Database setup
First, activate a Conda environment, for example your pyserini environment.

```bash
conda activate pyserini
```
## DuckDB
Duckdb is relatively easy to set up, as it is an in-memory database that can be embedded into a process. Therefore, you only need to install this database via commandline: 
```
pip install duckdb
```
Then, you can simply run the following, to run the benchmark. 

```
$ python3 vectordb_benchmark/run_benchmark.py \
        --index_name='msmarco-v1-passage.bge-base-en-v1.5' \
        --table_name='msmarco' \
        --metric='ip' \
        --query_index_path='collections/msmarco-passage/queries_faiss' \
        --db_type='duckdb' \
        --db_config_file='./scripts/vectordb_benchmark/duckdb_db_config.txt' 
```
The db_config_file should be a text file, it specifies how much memory you would allow DuckDB to allocate, you can modify this file if you want, by default the memory limit is 100GB. The entire process may take over a day to complete, depending on your hardware set up. This code will download the index, extract the embedded vectors of the index, build the table in duckdb and run the benchmark. Alternatively, you can run the script `./scripts/vectordb_benchmark/benchmark_msmarco_duckdb.sh` to run the benchmark.

## PGVector
Now that we have DuckDB experiment finished, we can run the same experiment on PGVector. PGVector is an extension of PostgreSQL, so you will need to install both PostgreSQL and PGVector for this experiment.

# Install PostgreSQL
```bash
conda install -c conda-forge postgresql
```

# Install PGVector
To manually install pgvector, first install the necessary build tools (gcc and make) using Conda:
```bash
conda install -c conda-forge gcc_linux-64 make
```
Then, you can clone the pgvector repository, and make and install the extension.

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

# Start Database Server
Now that installations are done, you can finally initialize the database, create the vector extension, create a user and database for your experiment and start your postgresql server. The script `vectordb_benchmark/init_and_start_postgres.sh` will do all of these for you, it will initialize the database, create a database called `main_database` and a user called `main_user`, and enable the vector extension. Therefore, you can simply run:
```bash
./init_and_start_postgres.sh ~/pgdata
```
and your postgresql server will be up and running on port 5432. The only argument is the directory for the database data, you can modify this if you want.

# Run the Benchmark
Now that you have the PGVector extension installed and enabled in PostgreSQL. You can start running the benchmark, but first, make sure you supply the correct database configuration in the `pgvector_db_config.txt` file. For example, by default:

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
        --query_index_path='collections/msmarco-passage/queries_faiss' \
        --db_type='pgvector' \
        --db_config_file='./scripts/vectordb_benchmark/pgvector_db_config.txt' \
```
or simply run the script `./scripts/vectordb_benchmark/benchmark_msmarco_pgvector.sh`

Note that after one run, your postgresql will contain the table data, the current behaviour is to drop the table and index if they exist when the benchmark started. Later, we will add an option to skip table creation and index building, so that you can run the benchmark multiple times without having to re-create the table and index every time.

# NFCorpus

## Data Prep
Similar to the onboarding docs, we must first download the NFCorpus Dataset.

```bash
wget https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/nfcorpus.zip -P collections
unzip collections/nfcorpus.zip -d collections
```

## 1. Encode the Corpus
Create a directory for document embeddings and encode the corpus using the specified encoder.

```bash
mkdir indexes/faiss-nfcorpus
mkdir indexes/faiss-nfcorpus/documents
python -m pyserini.encode \
  input   --corpus collections/nfcorpus/corpus.jsonl \
  output  --embeddings indexes/faiss-nfcorpus/documents \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --batch 32
```

## 2. Encode the Queries
Create a directory for query embeddings and encode the queries using the specified encoder.

```bash
mkdir indexes/faiss-nfcorpus/queries
python -m pyserini.encode \
  input   --corpus collections/nfcorpus/queries.jsonl \
  output  --embeddings indexes/faiss-nfcorpus/queries \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --batch 32
```

## 3. Run Benchmarks

```bash
python3 ./scripts/vectordb_benchmark/benchmark_nfcorpus_duckdb.py 
python3 ./scripts/vectordb_benchmark/benchmark_nfcorpus_pgvector.py
