# BEIR (v1.0.0): SPLADE++ (CoCondenser-EnsembleDistil) Indexes

The Lucene impact indexes for SPLADE++ (CoCondenser-EnsembleDistil) were generated on 2023/11/24 at Anserini commit [`a66f86f`](https://github.com/castorini/anserini/commit/a66f86fb463db76df521f58992b000dd4ab39548) on `orca` with the following commands:

```
nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/arguana \ 
  -index indexes/lucene-index.beir-v1.0.0-arguana.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--arguana.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/bioasq \ 
  -index indexes/lucene-index.beir-v1.0.0-bioasq.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--bioasq.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/climate-fever \ 
  -index indexes/lucene-index.beir-v1.0.0-climate-fever.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--climate-fever.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-android \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-android.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-android.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-english \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-english.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-english.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-gaming \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-gaming.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-gis \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gis.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-gis.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-mathematica \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-mathematica.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-mathematica.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-physics \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-physics.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-physics.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-programmers \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-programmers.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-programmers.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-stats \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-stats.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-stats.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-tex \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-tex.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-tex.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-unix \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-unix.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-unix.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-webmasters \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-webmasters.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-webmasters.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/cqadupstack-wordpress \ 
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-wordpress.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--cqadupstack-wordpress.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/dbpedia-entity \ 
  -index indexes/lucene-index.beir-v1.0.0-dbpedia-entity.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--dbpedia-entity.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/fever \ 
  -index indexes/lucene-index.beir-v1.0.0-fever.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--fever.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/fiqa \ 
  -index indexes/lucene-index.beir-v1.0.0-fiqa.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--fiqa.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/hotpotqa \ 
  -index indexes/lucene-index.beir-v1.0.0-hotpotqa.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--hotpotqa.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/nfcorpus \ 
  -index indexes/lucene-index.beir-v1.0.0-nfcorpus.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--nfcorpus.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/nq \ 
  -index indexes/lucene-index.beir-v1.0.0-nq.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--nq.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/quora \ 
  -index indexes/lucene-index.beir-v1.0.0-quora.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--quora.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/robust04 \ 
  -index indexes/lucene-index.beir-v1.0.0-robust04.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--robust04.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/scidocs \ 
  -index indexes/lucene-index.beir-v1.0.0-scidocs.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--scidocs.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/scifact \ 
  -index indexes/lucene-index.beir-v1.0.0-scifact.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--scifact.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/signal1m \ 
  -index indexes/lucene-index.beir-v1.0.0-signal1m.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--signal1m.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/trec-covid \ 
  -index indexes/lucene-index.beir-v1.0.0-trec-covid.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--trec-covid.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/trec-news \ 
  -index indexes/lucene-index.beir-v1.0.0-trec-news.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--trec-news.splade-pp-ed.20231124.a66f86f & 

nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/webis-touche2020 \ 
  -index indexes/lucene-index.beir-v1.0.0-webis-touche2020.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--webis-touche2020.splade-pp-ed.20231124.a66f86f & 
```

In April 2024, indexes were repackaged to adopt a more consistent naming scheme.
