# msmarco-v1-doc

Lucene index of the MS MARCO V1 document corpus.

This index was generated on 2022/01/31 at Anserini commit [`9ea315`](https://github.com/castorini/anserini/commit/9ea3159adeeffd84e10e197af4c36febb5b74c7b) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 7 \
  -input /store/collections/msmarco/msmarco-doc/ \
  -index indexes/lucene-index.msmarco-v1-doc.20220131.9ea315/ \
  -storeRaw -optimize
```

Note that there are three variants of this index:

+ `msmarco-v1-doc` (16G uncompressed): the "default" version, which stores term frequencies and the raw text. This supports bag-of-words queries, but no phrase queries and no relevance feedback.
+ `msmarco-v1-doc-slim` (2.0G uncompressed): the "slim" version, which stores term frequencies only. This supports bag-of-words queries, but no phrase queries and no relevance feedback. There is no way to fetch the raw text from this index.
+ `msmarco-v1-doc-full` (28G uncompressed): the "full" version, which stores term frequencies, term positions, document vectors, and the raw text. This supports bag-of-words queries, phrase queries, and relevance feedback.

This is the "default" version.