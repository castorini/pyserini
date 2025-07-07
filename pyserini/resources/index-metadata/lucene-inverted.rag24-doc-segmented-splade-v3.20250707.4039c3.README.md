# TREC 2024 RAG Track: SPLADE-v3 Indexes

The Lucene impact indexes for SPLADE-v3 were generated on 2025/07/07 at Anserini commit [`4039c3`](https://github.com/castorini/anserini/commit/4039c3054c961e80dc1562899609396142bc869b) on `orca` with the following commands:

```bash
#!/bin/bash
bin/run.sh io.anserini.index.IndexCollection \
  -collection JsonVectorCollection \
  -input /mnt/collections/msmarco/msmarco_v2.1_doc_segmented_splade-v3 \
  -index indexes/lucene-inverted.msmarco-v2.1-doc-segmented.splade-v3.20250707.4039c3 \
  -generator DefaultLuceneDocumentGenerator \
  -threads 16 -impact -pretokenized -optimize \
```
