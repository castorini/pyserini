# BEIR (v1.0.0): SPLADE-distill CoCodenser-medium

These Lucene impact indexes for SPLADE-distill CoCodenser-medium were generated on 2022/11/16 at Anserini commit [`505594`](https://github.com/castorini/anserini/commit/505594b6573294a9a4c72a8feee3416f8a9bd2d9) on `tuna` with the following commands:

```bash
nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/trec-covid \
  -index indexes/lucene-index.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-trec-covid-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/bioasq \
  -index indexes/lucene-index.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-bioasq-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/nfcorpus \
  -index indexes/lucene-index.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-nfcorpus-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/nq \
  -index indexes/lucene-index.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-nq-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/hotpotqa \
  -index indexes/lucene-index.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-hotpotqa-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/fiqa \
  -index indexes/lucene-index.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-fiqa-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/signal1m \
  -index indexes/lucene-index.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-signal1m-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/trec-news \
  -index indexes/lucene-index.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-trec-news-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/robust04 \
  -index indexes/lucene-index.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-robust04-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/arguana \
  -index indexes/lucene-index.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-arguana-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/webis-touche2020 \
  -index indexes/lucene-index.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-webis-touche2020-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-android \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-android-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-english \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-english-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-gaming \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-gis \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-gis-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-mathematica \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-mathematica-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-physics \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-physics-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-programmers \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-programmers-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-stats \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-stats-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-tex \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-tex-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-unix \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-unix-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-webmasters \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-webmasters-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-wordpress \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-wordpress-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/quora \
  -index indexes/lucene-index.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-quora-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/dbpedia-entity \
  -index indexes/lucene-index.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-dbpedia-entity-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/scidocs \
  -index indexes/lucene-index.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-scidocs-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/fever \
  -index indexes/lucene-index.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-fever-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/climate-fever \
  -index indexes/lucene-index.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-climate-fever-splade_distil_cocodenser_medium.20221116.505594 &

nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /tuna1/collections/beir-v1.0.0/splade_distil_cocodenser_medium/scifact \
  -index indexes/lucene-index.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20221116.505594/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-scifact-splade_distil_cocodenser_medium.20221116.505594 &
```
