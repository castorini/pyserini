# CIRAL v1.0 afriberta-dpr-tied-pft-msmarco-ft-latin-mrtydi Indexes

This index was generated on 2024/02/12 at Pyserini commit [`2154e7`](https://github.com/castorini/pyserini/commit/2154e79a63de0287578d4a3b1239e9a729e1c415) on `basilisk` with the following command: 

```
lang=hausa # or yoruba, swahili, somali
encoder=castorini/afriberta-dpr-ptf-msmarco-ft-latin-mrtydi

python -m pyserini.encode   input   --corpus $INPUT_DIR/"$lang".jsonl \
                                    --fields title text url \
                                    --delimiter "\n" \
                                    --shard-id 0 \
                                    --shard-num 1 \
                            output  --embeddings $INDEX_DIR \
                                    --to-faiss \
                            encoder --encoder $encoder \
                                    --encoder-class auto \
                                    --fields text \
                                    --batch 32 \
                                    --fp16 
```