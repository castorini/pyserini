# HC4 v1.0 Indexes

Lucene indexes for HC4 v1.0 (Persian, Russian, and Chinese).

These indexes was generated on 2022/10/25 at Anserini commit [`c4a8d0`](https://github.com/castorini/anserini/commit/c4a8d00e3c218ed89dca8a4e51c3b2c7d577db00) on `tuna` with the following commands:

```bash
# HC4 fa
nohup target/appassembler/bin/IndexCollection \
  -collection NeuClirCollection \
  -input /tuna1/collections/multilingual/hc4-v1.0-fa \
  -index indexes/lucene-index.hc4-v1.0-fa.20221025.c4a8d0 \
  -generator DefaultLuceneDocumentGenerator \
  -threads 8 -storePositions -storeDocvectors -storeRaw -language fa -optimize \
  >& logs/log.hc4-v1.0-fa.20221025.c4a8d0 &

# HC4 ru
nohup target/appassembler/bin/IndexCollection \
  -collection NeuClirCollection \
  -input /tuna1/collections/multilingual/hc4-v1.0-ru \
  -index indexes/lucene-index.hc4-v1.0-ru.20221025.c4a8d0 \
  -generator DefaultLuceneDocumentGenerator \
  -threads 8 -storePositions -storeDocvectors -storeRaw -language ru -optimize \
  >& logs/log.hc4-v1.0-ru.20221025.c4a8d0 &

# HC4 zh
nohup target/appassembler/bin/IndexCollection \
  -collection NeuClirCollection \
  -input /tuna1/collections/multilingual/hc4-v1.0-zh \
  -index indexes/lucene-index.hc4-v1.0-zh.20221025.c4a8d0 \
  -generator DefaultLuceneDocumentGenerator \
  -threads 8 -storePositions -storeDocvectors -storeRaw -language zh -optimize \
  >& logs/log.hc4-v1.0-zh.20221025.c4a8d0 &
```
