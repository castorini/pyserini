# BEIR (v1.0.0): "multifield" Lucene indexes

These "multifield" Lucene indexes were generated on 2022/11/16 at Anserini commit [`505594`](https://github.com/castorini/anserini/commit/505594b6573294a9a4c72a8feee3416f8a9bd2d9) on `tuna` with the following commands:

```bash
nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/trec-covid \
  -index indexes/lucene-index.beir-v1.0.0-trec-covid-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-trec-covid-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/bioasq \
  -index indexes/lucene-index.beir-v1.0.0-bioasq-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-bioasq-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/nfcorpus \
  -index indexes/lucene-index.beir-v1.0.0-nfcorpus-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-nfcorpus-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/nq \
  -index indexes/lucene-index.beir-v1.0.0-nq-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-nq-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/hotpotqa \
  -index indexes/lucene-index.beir-v1.0.0-hotpotqa-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-hotpotqa-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/fiqa \
  -index indexes/lucene-index.beir-v1.0.0-fiqa-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-fiqa-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/signal1m \
  -index indexes/lucene-index.beir-v1.0.0-signal1m-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-signal1m-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/trec-news \
  -index indexes/lucene-index.beir-v1.0.0-trec-news-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-trec-news-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/robust04 \
  -index indexes/lucene-index.beir-v1.0.0-robust04-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-robust04-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/arguana \
  -index indexes/lucene-index.beir-v1.0.0-arguana-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-arguana-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/webis-touche2020 \
  -index indexes/lucene-index.beir-v1.0.0-webis-touche2020-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-webis-touche2020-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-android \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-android-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-android-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-english \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-english-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-english-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-gaming \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-gaming-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-gis \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-gis-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-mathematica \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-mathematica-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-physics \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-physics-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-programmers \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-programmers-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-stats \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-stats-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-tex \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-tex-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-unix \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-unix-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-webmasters \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-webmasters-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-wordpress \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-wordpress-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/quora \
  -index indexes/lucene-index.beir-v1.0.0-quora-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-quora-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/dbpedia-entity \
  -index indexes/lucene-index.beir-v1.0.0-dbpedia-entity-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-dbpedia-entity-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/scidocs \
  -index indexes/lucene-index.beir-v1.0.0-scidocs-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-scidocs-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/fever \
  -index indexes/lucene-index.beir-v1.0.0-fever-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-fever-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/climate-fever \
  -index indexes/lucene-index.beir-v1.0.0-climate-fever-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-climate-fever-multifield.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirMultifieldCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/scifact \
  -index indexes/lucene-index.beir-v1.0.0-scifact-multifield.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -fields title -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-scifact-multifield.20221116.505594 &
```
