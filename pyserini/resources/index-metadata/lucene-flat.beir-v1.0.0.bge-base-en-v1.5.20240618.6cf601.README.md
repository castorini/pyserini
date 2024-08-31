# beir-v1.0.0.bge-base-en-v1.5 (Flat)

Lucene flat dense vector indexes of BEIR corpora using BGE-base-en-v1.5.

These indexes were built 2024/06/18 on `orca` at Anserini commit [`6cf601`](https://github.com/castorini/anserini/commit/6e9ce8f56d08f9c72746b79f14208e45e3b7a81e) (2024/06/17), with Lucene 9.9.1.

Here's the indexing command for `arguana`:

```bash
bin/run.sh io.anserini.index.IndexFlatDenseVectors \
  -collection JsonDenseVectorCollection \
  -input /store/collections/beir-v1.0.0/bge-base-en-v1.5/arguana \
  -generator DenseVectorDocumentGenerator \
  -index indexes/lucene-flat.beir-v1.0.0-arguana.bge-base-en-v1.5/ \
  -threads 16 -optimize \
  >& logs/log.flat.beir-v1.0.0-arguana.bge-base-en-v1.5.txt &
```

And the same for all the other collections.
Note that the indexes are optimized, i.e., merged down to a single segment.
