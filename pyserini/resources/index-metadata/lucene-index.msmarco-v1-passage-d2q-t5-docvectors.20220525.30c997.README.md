# msmarco-v1-passage-d2q-t5-docvectors

Lucene index (+docvectors) of the MS MARCO V1 passage corpus, with doc2query-T5 expansions.

This index was generated on 2022/05/25 at Anserini commit [`30c997`](https://github.com/castorini/anserini/commit/30c9974f495a06c94d576d0e9c2c5861515e0e19) on `damiano` with the following command:

```
target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 18 \
  -input /scratch2/collections/msmarco/msmarco-passage-docTTTTTquery/ \
  -index indexes/lucene-index.msmarco-v1-passage-d2q-t5-docvectors.20220525.30c997/ \
  -storeDocvectors -optimize
```

Note that this index stores term frequencies along with the docvectors: bag-of-words queries and relevance feedback are supported, but not phrase queries.
The raw text is not stored.
