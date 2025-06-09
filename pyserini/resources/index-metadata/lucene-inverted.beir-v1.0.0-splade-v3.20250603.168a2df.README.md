# BEIR (v1.0.0): SPLADE-v3 Indexes

The Lucene impact indexes for SPLADE-v3 were generated on 2025/06/03 at Anserini commit [`168a2d`](https://github.com/castorini/anserini/commit/168a2dfd31a9fc2c90003e70b4fba8d7c68ebef8) on `orca` with the following commands:

```bash
#!/bin/bash

ENCODE_DIR="/store/collections/beir-v1.0.0/splade-v3"
INDEX_DIR="indexes"
COMMIT_HASH="168a2d"
DATE="20250603"

mkdir -p "${INDEX_DIR}"

for dataset in $(ls "${ENCODE_DIR}"); do
  python -m pyserini.index.lucene \
    --collection JsonVectorCollection \
    --input "${ENCODE_DIR}/${dataset}" \
    --index "${INDEX_DIR}/lucene-index.beir-v1.0.0-${dataset}.splade-v3.${DATE}.${COMMIT_HASH}" \
    --generator DefaultLuceneDocumentGenerator \
    --threads 16 \
    --impact \
    --pretokenized \
    --optimize || {
      echo "Error indexing ${dataset}"
      exit 1
    }
done
```