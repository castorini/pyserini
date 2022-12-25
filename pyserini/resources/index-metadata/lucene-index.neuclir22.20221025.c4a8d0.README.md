# NeuCLIR 2022 Indexes

Lucene indexes for the NeuCLIR 2022 corpora (Persian, Russian, and Chinese).

These indexes was generated on 2022/10/25 at Anserini commit [`c4a8d0`](https://github.com/castorini/anserini/commit/c4a8d00e3c218ed89dca8a4e51c3b2c7d577db00) on `tuna` with the following commands:

```bash
# NeuCLIR22 fa
nohup target/appassembler/bin/IndexCollection \
  -collection NeuClirCollection \
  -input /tuna1/collections/multilingual/neuclir22-fa \
  -index indexes/lucene-index.neuclir22-fa.20221025.c4a8d0 \
  -generator DefaultLuceneDocumentGenerator \
  -threads 8 -storePositions -storeDocvectors -storeRaw -language fa -optimize \
  >& logs/log.neuclir22-fa.20221025.c4a8d0 &

# NeuCLIR22 ru
nohup target/appassembler/bin/IndexCollection \
  -collection NeuClirCollection \
  -input /tuna1/collections/multilingual/neuclir22-ru \
  -index indexes/lucene-index.neuclir22-ru.20221025.c4a8d0 \
  -generator DefaultLuceneDocumentGenerator \
  -threads 8 -storePositions -storeDocvectors -storeRaw -language ru -optimize \
  >& logs/log.neuclir22-ru.20221025.c4a8d0 &

# NeuCLIR22 zh
nohup target/appassembler/bin/IndexCollection \
  -collection NeuClirCollection \
  -input /tuna1/collections/multilingual/neuclir22-zh \
  -index indexes/lucene-index.neuclir22-zh.20221025.c4a8d0 \
  -generator DefaultLuceneDocumentGenerator \
  -threads 8 -storePositions -storeDocvectors -storeRaw -language zh -optimize \
  >& logs/log.neuclir22-zh.20221025.c4a8d0 &
```
