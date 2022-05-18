# msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2

Lucene impact index of the MS MARCO V2 segmented document corpus for uniCOIL (noexp) with title prepended.

This index was generated on 2022/04/19 at Pyserini commit [`c47993`](https://github.com/castorini/pyserini/commit/c47993aa2bebb8ab0a418214cfd299c0d0351c81) on `orca` with the following command:

```
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input embeddings_msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2 \
  --index indexes/lucene-index.msmarco-v2-doc-segmented-unicoil-noexp-0shot-v2 \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --impact --pretokenized --optimize
```
