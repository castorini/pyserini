export CUDA_VISIBLE_DEVICES=0

# python encode_corpus.py \
# 		--model_name /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/aggretriever-cocondenser \
# 		--index /store2/scratch/s269lin/Aggretriever/results/experiments/msmarco/coCondenser-Concatenator \
# 		--corpus /store2/scratch/s269lin/data/msmarco-passage/corpus/docs.json

# python encode_query.py \
# 		--model_name /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/distilbert-agg \
# 		--corpus_domain beir \
# 		--query /store2/scratch/s269lin/data/nfcorpus/queries.jsonl

# python -m pyserini.search.faiss \
#   --index /store2/scratch/s269lin/index/aggretriever-distilbert \
#   --topics /store2/scratch/s269lin/data/msmarco-passage/queries/queries.dev.small.tsv \
#   --encoder /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/aggretriever-distilbert \
#   --output runs/run.msmarco-passage.distilbert-agg.bf.tsv \
#   --output-format msmarco \
#   --batch-size 36 --threads 12


python -m pyserini.search.faiss \
  --index /store2/scratch/s269lin/index/aggretriever-cocondenser \
  --topics msmarco-passage-dev-subset \
  --encoded-queries /store2/scratch/s269lin/queries/aggretriever-cocondenser \
  --output runs/run.msmarco-passage.cocondenser-agg.bf.tsv \
  --output-format msmarco \
  --batch-size 36 --threads 12

python -m pyserini.eval.trec_eval -c -M 10 -m recip_rank msmarco-passage-dev-subset \
    runs/run.msmarco-passage.cocondenser-agg.bf.tsv

python -m pyserini.eval.trec_eval -c -mrecall.1000 -mmap msmarco-passage-dev-subset \
    runs/run.msmarco-passage.cocondenser-agg.bf.tsv

  # /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/aggretriever-distilbert 


# python scripts/aggretriever/encode_query.py \
# 		--model_name /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/aggretriever-cocondenser \
# 		--query /store2/scratch/s269lin/data/msmarco-passage/queries/queries.dev.small.tsv \
# 		--output /store2/scratch/s269lin/queries/aggretriever-cocondenser
