# msmarco-v2.1-doc-segmented

Lucene inverted index of the MS MARCO V2.1 segmented document corpus.

Note that there are three variants of this index:

+ `msmarco-v2.1-doc-segmented` (56G uncompressed): the "default" version, which stores term frequencies and the raw text. This supports bag-of-words queries, but no phrase queries and no relevance feedback (unless the documents are parsed on the fly).
+ `msmarco-v2.1-doc-segmented-slim` (15G uncompressed): the "slim" version, which stores term frequencies only. This supports bag-of-words queries, but no phrase queries and no relevance feedback. There is no way to fetch the raw text from this index.
+ `msmarco-v2.1-doc-segmented-full` (137G uncompressed): the "full" version, which stores term frequencies, term positions, document vectors, and the raw text. This supports bag-of-words queries, phrase queries, and relevance feedback.

These indexes were generated on 2024/04/19 at Anserini commit [`4f9675`](https://github.com/castorini/anserini/commit/4f967519baa1bc634f7dd2998d7a408c27120b1c) on `tuna` with the following commands:

```bash
nohup bin/run.sh io.anserini.index.IndexCollection \
  -collection MsMarcoV2DocCollection \
  -input /mnt/collections/msmarco/msmarco_v2.1_doc_segmented/ \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/lucene-inverted.msmarco-v2.1-doc-segmented.20240418.4f9675/ \
  -threads 8 -storeRaw -optimize >& logs/log.msmarco-v2.1-doc-segmented.20240418.4f9675.txt &

nohup bin/run.sh io.anserini.index.IndexCollection \
  -collection MsMarcoV2DocCollection \
  -input /mnt/collections/msmarco/msmarco_v2.1_doc_segmented/ \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/lucene-inverted.msmarco-v2.1-doc-segmented-slim.20240418.4f9675/ \
  -threads 8 -optimize >& logs/log.msmarco-v2.1-doc-segmented-slim.20240418.4f9675.txt &

nohup bin/run.sh io.anserini.index.IndexCollection \
  -collection MsMarcoV2DocCollection \
  -input /mnt/collections/msmarco/msmarco_v2.1_doc_segmented/ \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/lucene-inverted.msmarco-v2.1-doc-segmented-full.20240418.4f9675/ \
  -threads 8 -storePositions -storeDocvectors -storeRaw -optimize >& logs/log.msmarco-v2.1-doc-segmented-full.20240418.4f9675.txt &
```
