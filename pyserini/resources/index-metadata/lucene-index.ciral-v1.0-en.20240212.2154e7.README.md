# CIRAL v1.0 BM25 English Indexes

Lucene indexes for English translations of CIRAL covering all four languages.

This index was generated on 2024/02/12 at Pyserini commit [`2154e7`](https://github.com/castorini/pyserini/commit/2154e79a63de0287578d4a3b1239e9a729e1c415) on `basilisk` with the following command: 

```bash
lang=ha # or yo, sw, so

target/appassembler/bin/IndexCollection \
        -collection MrTyDiCollection \
        -input ciral-passages-$lang-en/ \
        -index lucene-index.ciral-v1.0-$lang-en \
        -generator DefaultLuceneDocumentGenerator \
        -threads 9 \
        -optimize \
        -storePositions -storeDocvectors -storeRaw
```