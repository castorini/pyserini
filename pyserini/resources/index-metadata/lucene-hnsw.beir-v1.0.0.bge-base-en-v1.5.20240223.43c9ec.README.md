# beir-v1.0.0.bge-base-en-v1.5

Lucene HNSW indexes of BEIR corpora using BGE-base-en-v1.5.

These indexes were built 2024/02/23 on `orca` at Anserini commit [`43c9ec`](https://github.com/castorini/anserini/commit/43c9ecca53313ec2f84c8274d88f99ca3ea2e4bd) (2024/02/18), with Lucene 9.9.1.

Here's the indexing command for BioASQ:

```
MODEL="bge-base-en-v1.5-hnsw"
CORPORA="bioasq"

nohup target/appassembler/bin/IndexHnswDenseVectors \
  -collection JsonDenseVectorCollection \
  -input /store/collections/beir-v1.0.0/bge-base-en-v1.5/${CORPORA} \
  -generator HnswDenseVectorDocumentGenerator \
  -index indexes/lucene-hnsw.beir-v1.0.0-${CORPORA}-${MODEL}.efC2000/ \
  -threads 4 -M 16 -efC 2000 > logs/log.beir-v1.0.0-${CORPORA}-${MODEL}.efC2000 2>&1 &
```

Note the indexing parameters.
In particular, the index was _not_ optimized, i.e., merged down to a single segment.

I ran four trials and picked the index instance that yielded the highest retrieval scores.
Most of the trials yielded scores that were close; I selected the "best" based on eyeballing.

For the other indexes:

+ The other "large" collections (`climate-fever`, `dbpedia-entity`, `fever`, `hotpotqa`, `nq`, `signal1m`) were indexed with the following parameters: `-threads 2 -M 16 -efC 2000`
+ The remaining collections (`trec-covid`, `nfcorpus`, `fiqa`, `trec-news`, `robust04`, `arguana`, `webis-touche2020`, `cqadupstack-android`, `cqadupstack-english`, `cqadupstack-gaming`, `cqadupstack-gis`, `cqadupstack-mathematica`, `cqadupstack-physics`, `cqadupstack-programmers`, `cqadupstack-stats`, `cqadupstack-tex`, `cqadupstack-unix`, `cqadupstack-webmasters`, `cqadupstack-wordpress`, `quora`, `scidocs`, `scifact`) were indexed with the following parameters: `-threads 1 -M 16 -efC 2000`.

For these, I also ran four trials and picked the "best" by eyeballing (as with BioASQ).
Similarly, the indexes were _not_ optimized, i.e., merged down to a single segment (although for the smaller collections this made no difference as the entire index fit into a single segment anyway).
