# Pyserini: Reproducing Bright leaderboard with Diver Model - Finetuned from Qwen3


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
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100 \
  bright-${dataset_name} \
  runs/run.bright-${dataset_name}.${model_name}.txt
```


## Reproduction Log[*](reproducibility.md)