# msmarco-v1-doc-segmented-unicoil-noexp

Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL (noexp).

This index was generated on 2022/03/22 at Anserini commit [`2f4058`](https://github.com/castorini/anserini/commit/2f4058fbac852ec483c43e9e43ce9864db5a0027) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /store/collections/msmarco/msmarco-doc-segmented-unicoil-noexp/ \
  -index indexes/lucene-index.msmarco-v1-doc-segmented-unicoil-noexp.20220322.2f4058/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 \
  -impact -pretokenized -optimize
```
