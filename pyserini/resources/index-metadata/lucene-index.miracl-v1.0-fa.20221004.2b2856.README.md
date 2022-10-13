# miracl-v1.0-fa

Lucene index for MIRACL v1.0 (Persian).

This index was generated on 2022/10/04 at Anserini commit [`b5ecc5`](https://github.com/castorini/anserini/commit/b5ecc5aff79ddfc82b175f6bd3048f5039f0480f) on `orca` with the following command:
```
lang=fa
target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MIRACL/miracl-corpus-v1.0-fa \
    -index lucene-index.miracl-v1.0-fa \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language fa
```
