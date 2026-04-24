# Pyserini: Reproducing Bright leaderboard with Models Finetuned from Qwen3
This guide contains steps to reproduce retrieval results for BRIGHT using the Diver and Reason-Embed Models introduced in the following papers:

Meixiu Long and Duolin Sun and Dan Yang and Junjie Wang and Yue Shen and Jian Wang and Peng Wei and Jinjie Gu and Jiahai Wang.
[DIVER: A Multi-Stage Approach for Reasoning-intensive Information Retrieval](https://arxiv.org/abs/2508.07995) _arXiv:2508.07995_

Jianlyu Chen and Junwei Lan and Chaofan Li and Defu Lian and Zheng Liu.
[ReasonEmbed: Enhanced Text Embeddings for Reasoning-Intensive Document Retrieval](https://arxiv.org/abs/2510.08252) _arXiv:2510.08252_


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
Encode documents into dense vectors and create faiss flat index:

### Diver

```bash
model="AQ-MedAI/Diver-Retriever-4B"
model_name="Diver-Retriever-4B"
model_name="${model_name,,}"
dataset_name="pony"
python -m pyserini.encode \
  input   --corpus collections/bright/corpus/${dataset_name}.jsonl \
          --fields text \
          --delimiter "|||~~~|||||~~~~~" \
  output  --embeddings ./indexes/bright/faiss-flat.bright-${dataset_name}.${model_name} \
          --to-faiss \
  encoder --encoder $model \
          --encoder-class qwen3 \
          --fields text \
          --batch-size 16 \
          --max-length 16384 \
          --explicit-truncate \
          --fp16 \
          --l2-norm \
          --dim 2560 \
          --device cuda:0 \
          --prefix 'Represent this text:'
```

### Reason-Embed
```bash
model="hanhainebula/reason-embed-qwen3-4b-0928"
model_name="reason-embed-qwen3-4b-0928"
model_name="${model_name,,}"
dataset_name="pony"
python -m pyserini.encode \
  input   --corpus collections/bright/corpus/${dataset_name}.jsonl \
          --fields text \
          --delimiter "|||~~~|||||~~~~~" \
  output  --embeddings ./indexes/bright/faiss-flat.bright-${dataset_name}.${model_name} \
          --to-faiss \
  encoder --encoder $model \
          --encoder-class qwen3 \
          --fields text \
          --batch-size 16 \
          --fp16 \
          --max-length 8192 \
          --l2-norm \
          --dimension 2560 \
          --device cuda:0
```

## Search

### Diver

```bash
dataset_name="pony"
model="AQ-MedAI/Diver-Retriever-4B"
model_name="Diver-Retriever-4B"
model_name="${model_name,,}"
python -m pyserini.search.faiss \
        --encoder $model \
        --encoder-class qwen3 \
        --index ./indexes/bright/faiss-flat.bright-${dataset_name}.${model_name} \
        --query-prefix $'Instruct: Given a web search query, retrieve relevant passages that answer the query\nQuery:' \
        --topics bright-${dataset_name}-original \
        --output ./runs/bright/run.bright-${dataset_name}.${model_name}.txt \
        --hits 1000 \
        --remove-query \
        --topics-format raw_jsonl \
        --explicit-truncate \
        --fp16 \
        --l2-norm \
        --max-length 16384 \
        --device cuda:0
```

### Reason-Embed
```bash
declare -A INSTRUCTIONS
INSTRUCTIONS["biology"]="Given a Biology post, retrieve relevant passages that help answer the post."
INSTRUCTIONS["earth_science"]="Given an Earth Science post, retrieve relevant passages that help answer the post."
INSTRUCTIONS["economics"]="Given an Economics post, retrieve relevant passages that help answer the post."
INSTRUCTIONS["psychology"]="Given a Psychology post, retrieve relevant passages that help answer the post."
INSTRUCTIONS["robotics"]="Given a Robotics post, retrieve relevant passages that help answer the post."
INSTRUCTIONS["stackoverflow"]="Given a Stack Overflow post, retrieve relevant passages that help answer the post."
INSTRUCTIONS["sustainable_living"]="Given a Sustainable Living post, retrieve relevant passages that help answer the post."
INSTRUCTIONS["leetcode"]="Given a Coding problem, retrieve relevant examples that help answer the problem."
INSTRUCTIONS["pony"]="Given a Pony question, retrieve relevant passages that help answer the question."
INSTRUCTIONS["aops"]="Given a Math problem, retrieve relevant examples that help answer the problem."
INSTRUCTIONS["theoremqa_questions"]="Given a Math problem, retrieve relevant examples that help answer the problem."
INSTRUCTIONS["theoremqa_theorems"]="Given a Math problem, retrieve relevant theorems that help answer the problem."

dataset_name="pony"
model="hanhainebula/reason-embed-qwen3-4b-0928"
model_name="reason-embed-qwen3-4b-0928"
instruction="${INSTRUCTIONS[$dataset_name]}"
python -m pyserini.search.faiss \
        --encoder $model \
        --encoder-class qwen3 \
        --index ./indexes/bright/faiss-flat.bright-${dataset_name}.${model_name} \
        --query-prefix "Instruct: ${instruction}"$'\n'"Query: " \
        --topics bright-${dataset_name}-original \
        --output ./runs/bright/run.bright-${dataset_name}.${model_name}.txt \
        --hits 1000 \
        --remove-query \
        --l2-norm \
        --fp16 \
        --topics-format raw_jsonl \
        --max-length 8192 \
        --device cuda:0
```

Alternatively, you can use our prebuilt indexes by passing `--index bright-${dataset_name}.${model_name}`.
To use faiss-gpu for search specify the faiss device by passing `--faiss-device cuda:<gpu-index>`.

## Evaluation
`nDCG@10` is the metric used in the Bright leaderboard and is what we use here for easior comparison.
```
model_names=(
  "diver-retriever-4b"
  "reason-embed-qwen3-4b-0928"
)
for model_name in "${model_names[@]}"; do
  echo "Results for model: $model_name"
  printf "%-50s | %-10s\n" "Dataset" "nDCG@10"
  echo "-------------------------------------------------------------------"
  score=$(python -m pyserini.eval.trec_eval \
      -c -m ndcg_cut.10 \
      bright-${dataset_name} \
      "./runs/bright/run.bright-${dataset_name}.${model_name}.txt" | grep 'ndcg_cut_10' | awk '{print $3}')
  printf "%-50s | %-10s\n" "$dataset_name" "$score"
  echo "-------------------------------------------------------------------"
  echo ""
done
```
Expected output:
```
Results for model: diver-retriever-4b
Dataset                                            | nDCG@10
-------------------------------------------------------------------
pony                                               | 0.1292
-------------------------------------------------------------------

Results for model: reason-embed-qwen3-4b-0928
Dataset                                            | nDCG@10
-------------------------------------------------------------------
pony                                               | 0.1216
-------------------------------------------------------------------
```

## Reproduction Log[*](reproducibility.md)
+ Results reproduced by [@h79yan](https://github.com/h79yan) on 2026-04-15 (commit [`a8ec37d`](https://github.com/castorini/pyserini/commit/a8ec37db726ef7ba094627f1fe778ab881495015))