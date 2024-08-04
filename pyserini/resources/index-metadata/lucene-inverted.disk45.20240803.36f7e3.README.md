# disk45

Lucene index of [TREC Disks 4 & 5](https://trec.nist.gov/data/cd45/index.html) (minus Congressional Records), used in the TREC 2004 Robust Track.
This index was built on 2024/08/03 at Anserini commit [`36f7e3`](https://github.com/castorini/anserini/commit/36f7e314d6c07f6cc4a23ce30cd1821c920ba231) on `orca` with the following command:

```bash
nohup bin/run.sh io.anserini.index.IndexCollection \
  -collection TrecCollection \
  -input /store/collections/newswire/disk45 \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/lucene-inverted.disk45/ \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.disk45 &
```
