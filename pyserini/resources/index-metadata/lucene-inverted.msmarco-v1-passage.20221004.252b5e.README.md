# msmarco-v1-passage

Lucene index of the MS MARCO V1 passage corpus.

Note that there are three variants:

+ `msmarco-v1-passage` (2.6G uncompressed): the "default" version, which stores term frequencies and the raw text. This supports bag-of-words queries, but no phrase queries and no relevance feedback.
+ `msmarco-v1-passage-slim` (627M uncompressed): the "slim" version, which stores term frequencies only. This supports bag-of-words queries, but no phrase queries and no relevance feedback. There is no way to fetch the raw text from this index.
+ `msmarco-v1-passage-full` (4.3G uncompressed): the "full" version, which stores term frequencies, term positions, document vectors, and the raw text. This supports bag-of-words queries, phrase queries, and relevance feedback.

These indexes were generated on 2022/10/04 at Anserini commit [`252b5e`](https://github.com/castorini/anserini/commit/252b5e2087dd7b3b994d41a444d4ae0044519819) on `tuna` with the following commands:

```
nohup target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 9 \
  -input /tuna1/collections/msmarco/passage/ \
  -index indexes/lucene-index.msmarco-v1-passage.20221004.252b5e/ \
  -storeRaw -optimize >& logs/log.msmarco-v1-passage.20221004.252b5e &

nohup target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 9 \
  -input /tuna1/collections/msmarco/passage/ \
  -index indexes/lucene-index.msmarco-v1-passage-slim.20221004.252b5e/ \
  -optimize >& logs/log.msmarco-v1-passage-slim.20221004.252b5e &

nohup target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 9 \
  -input /tuna1/collections/msmarco/passage/ \
  -index indexes/lucene-index.msmarco-v1-passage-full.20221004.252b5e/ \
  -storePositions -storeDocvectors -storeRaw -optimize >& logs/log.msmarco-v1-passage-full.20221004.252b5e &
```
