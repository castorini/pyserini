export CUDA_VISIBLE_DEVICES=3

python encode_corpus.py \
		--model_name /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/aggretriever-cocondenser \
		--index /store2/scratch/s269lin/Aggretriever/results/experiments/msmarco/coCondenser-Concatenator \
		--corpus /store2/scratch/s269lin/data/msmarco-passage/corpus/docs.json

# python encode_query.py \
# 		--model_name /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/distilbert-agg \
# 		--corpus_domain beir \
# 		--query /store2/scratch/s269lin/data/nfcorpus/queries.jsonl

# python -m pyserini.search.faiss \
#   --index msmarco-passage-tct_colbert-v2-hn-bf \
#   --topics /store2/scratch/s269lin/data/msmarco-passage/queries/queries.dev.small.tsv \
#   --encoder /store2/scratch/s269lin/Aggretriever/results/experiments/hf_model/distilbert-agg \
#   --output runs/run.msmarco-passage.distilbert-agg.bf.tsv \
#   --output-format msmarco \
#   --batch-size 36 --threads 12