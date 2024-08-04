# aquaint

Lucene index of the [AQUAINT collection](https://tac.nist.gov//data/data_desc.html#AQUAINT), used in the TREC 2005 Robust Track.
This index was built on 2024/08/03 at Anserini commit [`36f7e3`](https://github.com/castorini/anserini/commit/36f7e314d6c07f6cc4a23ce30cd1821c920ba231) on `orca` with the following command:

```bash
nohup bin/run.sh io.anserini.index.IndexCollection \
  -collection TrecCollection \
  -input /store/collections/newswire/AQUAINT \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/lucene-inverted.aquaint/ \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.aquaint &
```
