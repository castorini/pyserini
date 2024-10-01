# msmarco-v1-passage.bge-base-en-v1.5

Lucene HNSW indexes of MS MARCO V1 Passage using BGE-base-en-v1.5.

These indexes were built 2024/01/17 on `orca` at Anserini commit [`53514b`](https://github.com/castorini/anserini/commit/53514b1ab29398a4bb6ff4a315b7394e509e6be5) (2024/01/13), with Lucene 9.9.1.

Here are the indexing commands for the non-quantized and quantized versions:

```bash
target/appassembler/bin/IndexHnswDenseVectors \
  -collection JsonDenseVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-bge-base-en-v1.5/ \
  -generator HnswDenseVectorDocumentGenerator \
  -index indexes/lucene-hnsw.msmarco-passage-bge-base-en-v1.5.efC1000.1/ \
  -threads 8 -M 16 -efC 1000 -memoryBuffer 65536 -optimize \
  >& logs/log.msmarco-passage-bge-base-en-v1.5.efC1000.1 &

target/appassembler/bin/IndexHnswDenseVectors \
  -collection JsonDenseVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-bge-base-en-v1.5/ \
  -generator HnswDenseVectorDocumentGenerator \
  -index indexes/lucene-hnsw.msmarco-passage-bge-base-en-v1.5-int8.efC1000.1/ \
  -threads 8 -M 16 -efC 1000 -memoryBuffer 65536 -optimize -quantize.int8 \
  >& logs/log.msmarco-passage-bge-base-en-v1.5-int8.efC1000.1 &
```

I ran four trials and picked the index instance that yielded the highest retrieval scores.
Most of the trials yielded scores that were close; I selected the "best" based on eyeballing.
