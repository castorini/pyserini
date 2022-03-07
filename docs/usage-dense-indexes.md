# Pyserini: Guide to Dense Indexes

## How do I build index from my encoded collections?
Once the collections are [encoded](usage-encode.md) into vectors,
we can start to build the index.

Pyserini supports four types of index so far:

### 1. [HNSWPQ](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexHNSWPQ.html#struct-faiss-indexhnswpq)
```bash
python -m pyserini.index.faiss \
    --input path/to/encoded/corpus \  # either in the Faiss or the jsonl format
    --output path/to/output/index \
    --hnsw \
    --pq
```

### 2. [HNSW](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexHNSW.html#struct-faiss-indexhnsw)
```bash
python -m pyserini.index.faiss \
    --input path/to/encoded/corpus \  # either in the Faiss or the jsonl format
    --output path/to/output/index \
    --hnsw
```

### 3. [PQ](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexPQ.html)
```bash
python -m pyserini.index.faiss \
    --input path/to/encoded/corpus \  # either in the Faiss or the jsonl format
    --output path/to/output/index \
    --pq
```

### 4. [Flat](https://faiss.ai/cpp_api/struct/structfaiss_1_1IndexFlat.html)
This would generate the same files with `pyserini.encode` when `--to-faiss` was specified in the encoding script.
```bash
python -m pyserini.index.faiss \
    --input path/to/encoded/corpus \  # either in the Faiss or the jsonl format
    --output path/to/output/index \
```