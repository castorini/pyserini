# msmarco-v1-doc-segmented-unicoil-noexp

Lucene impact index of the MS MARCO V1 segmented document corpus for uniCOIL (noexp) with title prepended.

This index was generated on 2022/04/19 at Pyserini commit [`c47993`](https://github.com/castorini/pyserini/commit/c47993aa2bebb8ab0a418214cfd299c0d0351c81) on `orca` with the following command:

```
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input embeddings_msmarco-v1-doc-segmented-unicoil-noexp \
  --index indexes/lucene-index.msmarco-v1-doc-segmented-unicoil-noexp \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --impact --pretokenized --optimize
```
