# CIRAL v1.0 BM25 Indexes

Lucene indexes for CIRAL covering all four languages.

This index was generated on 2023/07/21 at Anserini commit [`e850ea`](https://github.com/castorini/anserini/commit/e850eaa5b0e3c0e406628cb1dbcf788ae46caf50) on `basilisk` with the following command:

```bash
lang=ha # or yo, sw, so
target/appassembler/bin/IndexCollection \
        -collection MrTyDiCollection \
        -input ciral-passages-$lang/ \
        -index lucene-index.ciral-v1.0-$lang \ 
        -generator DefaultLuceneDocumentGenerator \
        -threads 16 \
        -language $lang \
        -pretokenized \
        -optimize \
        -storePositions -storeDocvectors -storeRaw
```