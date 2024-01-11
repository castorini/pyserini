# BEIR (v1.0.0) - NQ

This Lucene impact index for SPLADE++ (CoCondenser-EnsembleDistil)" was generated on 2023/11/24 at Anserini commit [`a66f86f`](https://github.com/castorini/anserini/commit/a66f86fb463db76df521f58992b000dd4ab39548) on `orca` with the following command:

```
nohup target/appassembler/bin/IndexCollection \ 
  -collection JsonVectorCollection \ 
  -generator DefaultLuceneDocumentGenerator \ 
  -input /store/collections/beir-v1.0.0/splade-pp-ed/nq \ 
  -index indexes/lucene-index.beir-v1.0.0-nq.splade-pp-ed.20231124.a66f86f \ 
  -threads 16 -impact -pretokenized -optimize \ 
  >& logs/log.beir-v1.0.0--nq.splade-pp-ed.20231124.a66f86f & 
```
