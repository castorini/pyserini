# africlirmatrix-v1.0

Lucene index for AfriClirMatrix.

This index was generated on 2022/01/08 at Anserini commit [`7cb7016`](https://github.com/castorini/anserini/commit/7cb7016d91b7e002ab4f9f47edc389832a427e4a) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection \
    -collection JsonCollection \
    -input $input_dir/${lang}_collection_clir \
    -index $index_dir \
    -generator DefaultLuceneDocumentGenerator \
    -threads 16 -storePositions -storeDocvectors -storeRaw -pretokenized
```
