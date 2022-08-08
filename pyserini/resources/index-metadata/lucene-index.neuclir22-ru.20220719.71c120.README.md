# neuclir22-ru

Lucene index for Neuclir22 (Russian).

This index was generated on 2022/07/19 at Anserini commit [`71c120`](https://github.com/castorini/anserini/commit/71c1200d36ce17615cf4da510ac4ef2d2f0121f6) on `orca` with the following command:


```
target/appassembler/bin/IndexCollection -collection NeuClirCollection \
  -generator DefaultLuceneDocumentGenerator -threads 8 \
  -input /store/collections/multilingual/neuclir22-ru \
  -index indexes/lucene-index.neuclir22-ru.20220719.71c120 \
  -storePositions -storeDocvectors -storeRaw -optimize -language ru
```
