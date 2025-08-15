# BRIGHT: bge-large-en-v1.5

Faiss indexes of BRIGHT corpora using BGE-large-en-v1.5.

These indexes were built on 2025/08/08 on `basilisk` at Pyserini commit [44889d](https://github.com/castorini/pyserini/commit/44889de3d151b2e1317934b405b3ad6badd81308).

Here is the command:

```bash
#!/bin/bash
CORPORA=(biology earth_science economics psychology robotics stackoverflow sustainable_living pony leetcode aops theoremqa_theorems theoremqa_questions); 
for c in "${CORPORA[@]}"
do
    echo $c

    python -m pyserini.encode \
    input --corpus corpus/${c}/${c}.jsonl \
    --fields text --delimiter "|||~~~|||||~~~~~"   \
    output --embeddings indexes/bge_large_faiss/${c} --to-faiss \
    encoder --encoder BAAI/bge-large-en-v1.5  \
    --l2-norm  --fields text --batch 32  --dimension 1024 --max-length 512 \

done

echo "done"
```

The strange delimiter is due to BRIGHT documents containing many special characters. 