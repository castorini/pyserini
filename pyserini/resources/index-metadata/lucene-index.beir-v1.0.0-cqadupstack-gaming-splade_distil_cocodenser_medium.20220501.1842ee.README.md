# BEIR (v1.0.0) — CQADupStack-gaming

This Lucene impact index for **SPLADE-distill CoCodenser-medium** was generated on 2022/05/01 at Anserini commit [`1842ee`](https://github.com/castorini/anserini/commit/1842eeffcbf4d18698d401b1c5a4b1c868f32fc6) on `damiano` with the following command:

```
nohup target/appassembler/bin/IndexCollection \
  -collection JsonVectorCollection \
  -generator DefaultLuceneDocumentGenerator \
  -input /scratch2/collections/beir-v1.0.0/splade_distil_cocodenser_medium/cqadupstack-gaming \
  -index indexes/lucene-index.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20220501.1842ee/ \
  -threads 16 -impact -pretokenized -optimize \
  >& logs/log.beir-v1.0.0-cqadupstack-gaming-splade_distil_cocodenser_medium.20220501.1842ee &
```
