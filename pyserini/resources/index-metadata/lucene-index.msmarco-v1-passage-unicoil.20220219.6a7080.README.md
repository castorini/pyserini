# msmarco-v1-passage-unicoil

Lucene impact index of the MS MARCO V1 passage corpus for uniCOIL.

This index was generated on 2022/02/19 at Anserini commit [`9ea315`](https://github.com/castorini/anserini/commit/6a708047f71528f7d516c0dd45485204a36e6b1d) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /store/collections/msmarco/msmarco-passage-unicoil \
  -index indexes/lucene-index.msmarco-v1-passage-unicoil.20220219.6a7080/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -optimize
```
