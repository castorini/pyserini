# nyt

Lucene index of the [New York Times Annotated Corpus](https://catalog.ldc.upenn.edu/LDC2008T19), used in the TREC 2017 Common Core Track.
This index was built on 2024/08/03 at Anserini commit [`36f7e3`](https://github.com/castorini/anserini/commit/36f7e314d6c07f6cc4a23ce30cd1821c920ba231) on `orca` with the following command:

```bash
nohup bin/run.sh io.anserini.index.IndexCollection \
  -collection NewYorkTimesCollection \
  -input /store/collections/newswire/NYTcorpus/ \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/lucene-inverted.nyt/ \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.nyt &
```
