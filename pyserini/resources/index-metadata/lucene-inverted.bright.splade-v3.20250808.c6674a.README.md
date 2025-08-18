# BRIGHT: SPLADE-v3 Indexes

The Lucene impact indexes for SPLADE-v3 were generated on 2025/06/03 at Anserini commit [`c6674a`](https://github.com/castorini/anserini/commit/c6674a9ce86509007f48625be460538469f4fca6) on `basilisk` with the following commands:

```bash
#!/bin/bash

CORPORA=(biology earth_science economics psychology robotics stackoverflow sustainable_living pony leetcode aops theoremqa_theorems theoremqa_questions); 
for c in "${CORPORA[@]}"
do
    echo $c
    java -cp anserini-1.1.2-SNAPSHOT-fatjar.jar --add-modules jdk.incubator.vector \
        io.anserini.index.IndexCollection \
        -collection JsonVectorCollection  \
        -generator DefaultLuceneDocumentGenerator \
        -threads 16 \
        -input ./encode/spladev3/$c.splade \
        -index ./indexes/spladev3/lucene-inverted.bright-$c.splade-v3.20250808.c6674a \
        -impact -pretokenized -optimize
done

echo "done"
```