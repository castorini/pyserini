# SPLADEv3 Indexes for MS MARCO V1 Passage

These are Lucene impact indexes for MS MARCO V1 Passage using SPLADEv3:

+ `msmarco-v1-passage.splade-v3` (3.1G uncompressed): minimal TF index.
+ `msmarco-v1-passage.splade-v3-docvectors` (70G uncompressed): with docvectors stored.
+ `msmarco-v1-passage.splade-v3-text` (18G uncompressed): with text stored.

These indexes were generated on 2025/03/29 at Anserini commit [`4f4c68`](https://github.com/castorini/anserini/commit/4f4c68a1b4aa0cf6470cc44710219fe339e51c63) on `orca` with the following commands:

```bash
bin/run.sh io.anserini.index.IndexCollection \
  -collection JsonVectorCollection \
  -input /store/collections/msmarco/msmarco-passage-splade-v3 \
  -index indexes/lucene-inverted.msmarco-v1-passage-splade-v3.20250329.4f4c68/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.msmarco-v1-passage-splade-v3.20250329.4f4c68 &

bin/run.sh io.anserini.index.IndexCollection \
  -collection JsonVectorCollection \
  -input /store/collections/msmarco/msmarco-passage-splade-v3 \
  -index indexes/lucene-inverted.msmarco-v1-passage-splade-v3-docvectors.20250329.4f4c68/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -storeDocvectors -optimize \
  >& logs/log.msmarco-v1-passage-splade-v3-docvectors.20250329.4f4c68 &

bin/run.sh io.anserini.index.IndexCollection \
  -collection JsonVectorCollection \
  -input /store/collections/msmarco/msmarco-passage-splade-v3 \
  -index indexes/lucene-inverted.msmarco-v1-passage-splade-v3-text.20250329.4f4c68/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -storeRaw -optimize \
  >& logs/log.msmarco-v1-passage-splade-v3-text.20250329.4f4c68 &
```
