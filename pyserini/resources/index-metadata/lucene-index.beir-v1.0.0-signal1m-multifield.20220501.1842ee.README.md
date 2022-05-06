# BEIR (v1.0.0) — Signal-1M

This **"multifield" Lucene index** was generated on 2022/05/01 at Anserini commit [`1842ee`](https://github.com/castorini/anserini/commit/1842eeffcbf4d18698d401b1c5a4b1c868f32fc6) on `damiano` with the following command:

```
nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /scratch2/collections/beir-v1.0.0/corpus/signal1m \
  -index indexes/lucene-index.beir-v1.0.0-signal1m-multifield.20220501.1842ee/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-signal1m-multifield.20220501.1842ee &
```
