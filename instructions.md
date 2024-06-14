# Encoding and Benchmarking Process

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

