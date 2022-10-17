# miracl-v1.0-mdpr-tied-pft-msmarco

This index was generated on 2022/10/04 at Pyserini commit [`2b2856`](https://github.com/castorini/pyserini/commit/2b2856a9037c11061470cbf3d0961c7d041f1342) on `basilisk` with the following command: 

```
corpus=./corpus/miracl-corpus-v1.0-${lang}

encoder=castorini/mdpr-tied-pft-msmarco
shard_id=0
shard_num=1

python -m pyserini.encode   input   --corpus $corpus \
                                    --fields title text \
                                    --delimiter "\n\n" \
                                    --shard-id $shard_id \
                                    --shard-num $shard_num \
                            output  --embeddings  $index_dir-$shard_id \
                                    --to-faiss \
                            encoder --encoder $encoder \
                                    --fields title text \
                                    --batch 128 \
                                    --encoder-class 'auto' \
                                    --fp16
```