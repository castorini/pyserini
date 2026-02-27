# Pyserini: Reproducing Bright leaderboard with Diver Model - Finetuned from Qwen3
This guide contains steps to reproduce retrieval results for BRIGHT using the Diver Model introduced in the following paper:

Meixiu Long and Duolin Sun and Dan Yang and Junjie Wang and Yue Shen and Jian Wang and Peng Wei and Jinjie Gu and Jiahai Wang.
[DIVER: A Multi-Stage Approach for Reasoning-intensive Information Retrieval](https://arxiv.org/abs/2508.07995) _arXiv:2508.07995_

## Data Preparation
You need to obtain the relevant corpra from [Bright Corpus](https://huggingface.co/datasets/castorini/collections-bright/tree/main/corpus).

For example, for Pony:
```
wget https://huggingface.co/datasets/castorini/collections-bright/resolve/main/corpus/pony/pony.jsonl.gz
```

```
gunzip pony.jsonl.gz
```

## Encoding and indexing the Corpus
For all the following commands, ensure to update the directory paths accordingly.
Encode document screenshots into dense vectors:

```bash
model="AQ-MedAI/Diver-Retriever-4B"
model_name="Diver-Retriever-4B"
dataset_name="pony"
python -m pyserini.encode \
  input   --corpus ../${dataset_name}.jsonl \
          --fields text \
          --delimiter "|||~~~|||||~~~~~" \
  output  --embeddings ./embeddings/${dataset_name}.${model_name} \
  encoder --encoder $model \
          --encoder-class qwen3 \
          --fields text \
          --batch-size 32 \
          --fp16 \
          --max-length 16384 \
          --l2-norm \
          --prefix 'Represent this text: '
```

Now you can index them, the index dimension must match the models' hidden sizes.

```bash
python -m pyserini.index.faiss \
  --input ./embeddings/${dataset_name}.${model_name} \
  --output ./indexes/${dataset_name}.${model_name} \
  --metric inner \
  --dim 2560
```

## Search

```bash
python -m pyserini.search.faiss \
  --encoder $model \
  --encoder-class qwen3 \
  --index ./indexes/${dataset_name}.${model_name} \
  --query-prefix 'Instruct: Given a web search query, retrieve relevant passages that answer the query.\nQuery: ' \
  --topics bright-${dataset_name} \
  --output ./runs/run.bright-${dataset_name}.${model_name}.txt \
  --hits 1000 \
  --remove-query \
  --l2-norm \
  --fp16 \
  --max-length 16384 \
  --device cuda:0
```

## Evaluation
`nDCG@10` is the metric used in the Bright leaderboard and is what we use here for easior comparison.
```
  echo "Results for model: $model_name"
  printf "%-50s | %-10s\n" "Dataset" "nDCG@10"
  echo "-------------------------------------------------------------------"
  score=$(python -m pyserini.eval.trec_eval \
      -c -m ndcg_cut.10 \
      bright-${dataset_name} \
      "runs/run.bright-${dataset_name}.${model_name}.txt" | grep 'ndcg_cut_10' | awk '{print $3}')
  printf "%-50s | %-10s\n" "$dataset_name" "$score"
  echo "-------------------------------------------------------------------"
  echo ""
```
Expected output:
```
Results for model: Diver-Retriever-4B
Dataset                                            | nDCG@5    
-------------------------------------------------------------------
pony                                               | 0.1401    
-------------------------------------------------------------------
```

## Reproduction Log[*](reproducibility.md)