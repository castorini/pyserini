# SPLADE++ Indexes for MS MARCO V1 Passage

These are Lucene impact indexes for MS MARCO V1 Passage using the SPLADE++ models.
There are two separate model variants (SPLADE++ CoCondenser-EnsembleDistil and SPLADE++ CoCondenser-SelfDistil), three index types each:

+ `msmarco-v1-passage-splade-pp-ed` (2.3G uncompressed): SPLADE++ CoCondenser-EnsembleDistil, minimal TF index.
+ `msmarco-v1-passage-splade-pp-ed-docvectors` (61G uncompressed): with docvectors stored.
+ `msmarco-v1-passage-splade-pp-ed-text` (12G uncompressed): with text stored.
+ `msmarco-v1-passage-splade-pp-sd` (2.6G uncompressed): SPLADE++ CoCondenser-SelfDistil, minimal TF index.
+ `msmarco-v1-passage-splade-pp-sd-docvectors` (67G uncompressed): with docvectors stored.
+ `msmarco-v1-passage-splade-pp-sd-text` (13G uncompressed): with text stored.

These indexes were generated on 2024/05/24 at Anserini commit [`a59610`](https://github.com/castorini/anserini/commit/a59610795cf612f9f16264c4f9267c8d05f3a2e9) on `tuna` with the following command:

```bash
target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-splade-pp-ed \
  -index indexes/lucene-index.msmarco-v1-passage-splade-pp-ed.20230524.a59610/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.msmarco-v1-passage-splade-pp-ed.20230524.a59610 &

target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-splade-pp-ed \
  -index indexes/lucene-index.msmarco-v1-passage-splade-pp-ed-docvectors.20230524.a59610/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -storeDocvectors -optimize \
  >& logs/log.msmarco-v1-passage-splade-pp-ed-docvectors.20230524.a59610 &

target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-splade-pp-ed \
  -index indexes/lucene-index.msmarco-v1-passage-splade-pp-ed-text.20230524.a59610/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -storeRaw -optimize \
  >& logs/log.msmarco-v1-passage-splade-pp-ed-text.20230524.a59610 &

target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-splade-pp-sd \
  -index indexes/lucene-index.msmarco-v1-passage-splade-pp-sd.20230524.a59610/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.msmarco-v1-passage-splade-pp-sd.20230524.a59610 &

target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-splade-pp-sd \
  -index indexes/lucene-index.msmarco-v1-passage-splade-pp-sd-docvectors.20230524.a59610/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -storeDocvectors -optimize \
  >& logs/log.msmarco-v1-passage-splade-pp-sd-docvectors.20230524.a59610 &

target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -input /mnt/collections/msmarco/msmarco-passage-splade-pp-sd \
  -index indexes/lucene-index.msmarco-v1-passage-splade-pp-sd-text.20230524.a59610/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -storeRaw -optimize \
  >& logs/log.msmarco-v1-passage-splade-pp-sd-text.20230524.a59610 &
```

In April 2024, indexes were repackaged to adopt a more consistent naming scheme.
