# miracl-v1.0-fr

Lucene index for MIRACL v1.0 (French).

This index was generated on 2022/10/04 at Anserini commit [`b5ecc5`](https://github.com/castorini/anserini/commit/b5ecc5aff79ddfc82b175f6bd3048f5039f0480f) on `orca` with the following command:
```
lang=fr
target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MIRACL/miracl-corpus-v1.0-fr \
    -index lucene-index.miracl-v1.0-fr \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language fr
```
