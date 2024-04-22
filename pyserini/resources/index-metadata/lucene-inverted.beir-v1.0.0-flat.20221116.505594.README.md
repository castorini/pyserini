# BEIR (v1.0.0): "flat" Lucene indexes

These "flat" Lucene indexes were generated on 2022/11/16 at Anserini commit [`505594`](https://github.com/castorini/anserini/commit/505594b6573294a9a4c72a8feee3416f8a9bd2d9) on `tuna` with the following commands:

```bash
nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/trec-covid \
  -index indexes/lucene-index.beir-v1.0.0-trec-covid-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-trec-covid-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/bioasq \
  -index indexes/lucene-index.beir-v1.0.0-bioasq-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-bioasq-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/nfcorpus \
  -index indexes/lucene-index.beir-v1.0.0-nfcorpus-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-nfcorpus-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/nq \
  -index indexes/lucene-index.beir-v1.0.0-nq-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-nq-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/hotpotqa \
  -index indexes/lucene-index.beir-v1.0.0-hotpotqa-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-hotpotqa-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/fiqa \
  -index indexes/lucene-index.beir-v1.0.0-fiqa-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-fiqa-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/signal1m \
  -index indexes/lucene-index.beir-v1.0.0-signal1m-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-signal1m-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/trec-news \
  -index indexes/lucene-index.beir-v1.0.0-trec-news-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-trec-news-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/robust04 \
  -index indexes/lucene-index.beir-v1.0.0-robust04-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-robust04-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/arguana \
  -index indexes/lucene-index.beir-v1.0.0-arguana-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-arguana-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/webis-touche2020 \
  -index indexes/lucene-index.beir-v1.0.0-webis-touche2020-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-webis-touche2020-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-android \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-android-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-android-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-english \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-english-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-english-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-gaming \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-gaming-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-gis \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-gis-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-mathematica \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-mathematica-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-physics \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-physics-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-programmers \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-programmers-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-stats \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-stats-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-tex \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-tex-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-unix \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-unix-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-webmasters \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-webmasters-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/cqadupstack-wordpress \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-wordpress-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/quora \
  -index indexes/lucene-index.beir-v1.0.0-quora-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-quora-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/dbpedia-entity \
  -index indexes/lucene-index.beir-v1.0.0-dbpedia-entity-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-dbpedia-entity-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/scidocs \
  -index indexes/lucene-index.beir-v1.0.0-scidocs-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-scidocs-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/fever \
  -index indexes/lucene-index.beir-v1.0.0-fever-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-fever-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/climate-fever \
  -index indexes/lucene-index.beir-v1.0.0-climate-fever-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-climate-fever-flat.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection BeirFlatCollection \
  -input /tuna1/collections/beir-v1.0.0/corpus/scifact \
  -index indexes/lucene-index.beir-v1.0.0-scifact-flat.20221116.505594/ \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -storePositions -storeDocvectors -storeRaw -optimize \
  >& logs/log.beir-v1.0.0-scifact-flat.20221116.505594 &
```
