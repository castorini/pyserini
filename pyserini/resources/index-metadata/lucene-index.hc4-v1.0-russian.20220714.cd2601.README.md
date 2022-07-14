# hc4-v1.0-russian

Lucene index for HC4 v1.0 (Russian).

This index was generated on 2022/07/14 at Anserini commit [`cd2601`](https://github.com/castorini/anserini/commit/cd26013fe6f1a8bcaebc440392e6c97c7bd486b7) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection -collection NeuClirCollection \
  -generator DefaultLuceneDocumentGenerator -threads 8 \
  -input /store/collections/multilingual/hc4-v1.0-ru/ \
  -index indexes/lucene-index.hc4-v1.0-russian.20220714.cd2601/ \
  -storePositions -storeDocvectors -storeRaw -optimize -language ru \
```
