# msmarco-v1-passage.cosdpr-distil

Lucene HNSW indexes of MS MARCO V1 Passage using cosDPR-distil.

These indexes were built 2024/01/07 on `orca` at Anserini commit [`825148`](https://github.com/castorini/anserini/commit/825148afba0303276c37dd838be897b8443d9774) (2023/12/24), with Lucene 9.9.1.

Here are the indexing commands for the non-quantized and quantized versions:

```bash
target/appassembler/bin/IndexHnswDenseVectors \
  -collection JsonDenseVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-cos-dpr-distil/ \
  -generator HnswDenseVectorDocumentGenerator \
  -index indexes/lucene-hnsw.msmarco-passage-cos-dpr-distil.efC1000.1/ \
  -threads 8 -M 16 -efC 1000 -memoryBuffer 65536 -optimize \
  >& logs/log.msmarco-passage-cos-dpr-distil.efC1000.1 &

target/appassembler/bin/IndexHnswDenseVectors \
  -collection JsonDenseVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-cos-dpr-distil/ \
  -generator HnswDenseVectorDocumentGenerator \
  -index indexes/lucene-hnsw.msmarco-passage-cos-dpr-distil-int8.efC1000.1/ \
  -threads 8 -M 16 -efC 1000 -memoryBuffer 65536 -optimize -quantize.int8 \
  >& logs/log.msmarco-passage-cos-dpr-distil-int8.efC1000.1 &
```

I ran four trials and picked the index instance that yielded the highest retrieval scores.
Most of the trials yielded scores that were close; I selected the "best" based on eyeballing.
