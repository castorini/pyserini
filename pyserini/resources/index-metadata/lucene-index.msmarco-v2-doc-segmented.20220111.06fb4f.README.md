# msmarco-v2-doc-segmented

Lucene index of the MS MARCO V2 segmented document corpus.

This index was generated on 2022/01/11 at Anserini commit [`06fb4f`](https://github.com/castorini/anserini/commit/06fb4f9947ff2167c276d8893287453af7680786) on `orca` with the following command:

```
target/appassembler/bin/IndexCollection -collection MsMarcoV2DocCollection \
  -generator DefaultLuceneDocumentGenerator -threads 18 \
  -input /store/collections/msmarco/msmarco_v2_doc_segmented/ \
  -index indexes/lucene-index.msmarco-v2-doc-segmented.20220111.06fb4f/ \
  -storeRaw -optimize
```

Note that there are three variants of this index:

+ `msmarco-v2-doc-segmented` (128G uncompressed): the "default" version, which stores term frequencies and the raw text. This supports bag-of-words queries, but no phrase queries and no relevance feedback.
+ `msmarco-v2-doc-segmented-slim` (25G uncompressed): the "slim" version, which stores term frequencies only. This supports bag-of-words queries, but no phrase queries and no relevance feedback. There is no way to fetch the raw text from this index.
+ `msmarco-v2-doc-segmented-full` (217G uncompressed): the "full" version, which stores term frequencies, term positions, document vectors, and the raw text. This supports bag-of-words queries, phrase queries, and relevance feedback.

This is the "default" version.