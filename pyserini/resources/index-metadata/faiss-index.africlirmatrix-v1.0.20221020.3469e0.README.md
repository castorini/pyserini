# africlirmatrix-v1.0-mdpr-tied-pft-msmarco

Faiss index for AfriClirMatrix.

This index was generated on 2022/10/20 at Pyserini commit [`3469e0`](https://github.com/castorini/pyserini/commit/3469e010d6c1d4f237c1f649245307c298596942) on `basilisk` with the following command: 

```
corpus=./corpus/africlirmatrix-corpus-v1.0-${lang}
encoder=castorini/mdpr-tied-pft-msmarco

python -m pyserini.encode   input   --corpus $corpus \
                                    --fields text \
                                    --shard-id 0 \
                                    --shard-num 1 \
                            output  --embeddings  $index \
                                    --to-faiss \
                            encoder --encoder $encoder \
                                    --fields text \
                                    --batch 128 \
                                    --encoder-class 'auto' \
                                    --fp16
```