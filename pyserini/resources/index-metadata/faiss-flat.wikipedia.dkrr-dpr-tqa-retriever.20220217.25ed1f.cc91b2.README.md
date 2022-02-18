This index was generated on 2022/02/17 at

+ pyserini commit cc91b22f549702068cea1283f91b31d28d127b2f (2022/02/17)
+ FiD (https://github.com/facebookresearch/FiD) commit 25ed1ff0fe0288b80fb5e9e5de8d6346b94b8d48 (2022/02/17)


with the following command (from FiD repo):

```bash
python3 generate_passage_embeddings.py \
        --model_path tqa_retriever \
        --passages passages.tsv \
        --output_path wikipedia_embeddings_tqa \
        --shard_id 0 \
        --num_shards 1 \
        --per_gpu_batch_size 500 \
```

faiss-flat.wikipedia.dkrr-dpr-tqa-retriever.20220217.25ed1f.cc91b2.tar.gz MD5 checksum = 7c59e305533030cf6ccecc8d7229523b
