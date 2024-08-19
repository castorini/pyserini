# wapo.v2

Lucene index of the [TREC Washington Post Corpus](https://trec.nist.gov/data/wapost/), used in the TREC 2018 Common Core Track.
This index was built on 2024/08/03 at Anserini commit [`36f7e3`](https://github.com/castorini/anserini/commit/36f7e314d6c07f6cc4a23ce30cd1821c920ba231) on `orca` with the following command:

```bash
nohup bin/run.sh io.anserini.index.IndexCollection \
  -collection WashingtonPostCollection \
  -input /store/collections/newswire/WashingtonPost.v2/data/ \
  -generator WashingtonPostGenerator \
  -index indexes/lucene-inverted.wapo.v2/ \
  -threads 1 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.wapo.v2 &
```
