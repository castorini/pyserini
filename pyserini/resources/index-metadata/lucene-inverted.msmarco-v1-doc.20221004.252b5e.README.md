# msmarco-v1-doc

Lucene index of the MS MARCO V1 document corpus.

Note that there are three variants:

+ `msmarco-v1-doc` (16G uncompressed): the "default" version, which stores term frequencies and the raw text. This supports bag-of-words queries, but no phrase queries and no relevance feedback.
+ `msmarco-v1-doc-slim` (2.0G uncompressed): the "slim" version, which stores term frequencies only. This supports bag-of-words queries, but no phrase queries and no relevance feedback. There is no way to fetch the raw text from this index.
+ `msmarco-v1-doc-full` (28G uncompressed): the "full" version, which stores term frequencies, term positions, document vectors, and the raw text. This supports bag-of-words queries, phrase queries, and relevance feedback.

These indexes were generated on 2022/10/04 at Anserini commit [`252b5e`](https://github.com/castorini/anserini/commit/252b5e2087dd7b3b994d41a444d4ae0044519819) on `tuna` with the following commands:

```
target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 7 \
  -input /tuna1/collections/msmarco/msmarco-doc/ \
  -index indexes/lucene-index.msmarco-v1-doc.20221004.252b5e/ \
  -storeRaw -optimize >& logs/log.msmarco-v1-doc.20221004.252b5e &

target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 7 \
  -input /tuna1/collections/msmarco/msmarco-doc/ \
  -index indexes/lucene-index.msmarco-v1-doc-slim.20221004.252b5e/ \
  -optimize >& logs/log.msmarco-v1-doc-slim.20221004.252b5e &

target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 7 \
  -input /tuna1/collections/msmarco/msmarco-doc/ \
  -index indexes/lucene-index.msmarco-v1-doc-full.20221004.252b5e/ \
  -storePositions -storeDocvectors -storeRaw -optimize >& logs/log.msmarco-v1-doc-full.20221004.252b5e &
```
