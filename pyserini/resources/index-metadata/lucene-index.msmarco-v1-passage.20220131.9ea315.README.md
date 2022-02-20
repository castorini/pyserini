# msmarco-v1-passage

Lucene index of the MS MARCO V1 passage corpus.

This index was generated on 2022/01/31 at Anserini commit [`9ea315`](https://github.com/castorini/anserini/commit/9ea3159adeeffd84e10e197af4c36febb5b74c7b) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 9 \
  -input /store/collections/msmarco/passage/ \
  -index indexes/lucene-index.msmarco-v1-passage.20220131.9ea315/ \
  -storeRaw -optimize
```

Note that there are three variants of this index:

+ `msmarco-v1-passage` (2.5G uncompressed): the "default" version, which stores term frequencies and the raw text. This supports bag-of-words queries, but no phrase queries and no relevance feedback.
+ `msmarco-v1-passage-slim` (616M uncompressed): the "slim" version, which stores term frequencies only. This supports bag-of-words queries, but no phrase queries and no relevance feedback. There is no way to fetch the raw text from this index.
+ `msmarco-v1-passage-full` (4.3G uncompressed): the "full" version, which stores term frequencies, term positions, document vectors, and the raw text. This supports bag-of-words queries, phrase queries, and relevance feedback.

This is the "default" version.