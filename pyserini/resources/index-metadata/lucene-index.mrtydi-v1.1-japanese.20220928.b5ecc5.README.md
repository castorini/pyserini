# mrtydi-v1.1-japanese

Lucene index for Mr.TyDi v1.1 (Japanese).

This index was generated on 2022/09/28 at Anserini commit [`b5ecc5`](https://github.com/castorini/anserini/commit/b5ecc5aff79ddfc82b175f6bd3048f5039f0480f) on `orca` with the following command:

```
lang=japanese
abbr=ja

target/appassembler/bin/IndexCollection \
    -collection MrTyDiCollection \
    -input MrTyDi/miracl-corpus-v1.0-$lang \
    -index indexes-miracl/lucene-index.mrtydi-v1.1-$lang \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -language $abbr
```