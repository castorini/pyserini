python3 tools/scripts/msmarco-passage/encode_queries.py \
 --encoder=bge-base-en-v1.5 \
 --input=collections/msmarco-passage/queries.dev.small.tsv \
 --output=collections/faiss-queries/msmarco-passage/queries.pkl

python -m pyserini.encode \
  input   --corpus collections/faiss-queries/msmarco-passage/queries.jsonl \
  output  --embeddings indexes/msmarco-dev.bge-base-en-v1.5 \
          --to-faiss \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --batch 32