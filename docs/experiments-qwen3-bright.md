# Pyserini: Reproducing Bright leaderboard with Diver Model - Finetuned from Qwen3


## Data Preparation
You need to obtain the relevant corpuses from [Bright Corpus](https://huggingface.co/datasets/castorini/collections-bright/tree/main/corpus).

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

```
python -m pyserini.encode \
  input   --corpus ../pony.jsonl \
          --fields text \
          --delimiter "|||~~~|||||~~~~~" \
  output  --embeddings ../embeddings \
  encoder --encoder AQ-MedAI/Diver-Retriever-4B \
          --encoder-class qwen3 \
          --fields text \
          --batch-size 32 \
          --fp16 \
          --l2-norm
```

Now you can index them, the index dimension must match the models' hidden sizes.

```
python -m pyserini.index.faiss \
  --input ../embeddings \
  --output ../index \
  --dim 2560
```

## Search

```
python -m pyserini.search.faiss \
  --encoder AQ-MedAI/Diver-Retriever-4B \
  --encoder-class qwen3 \
  --query-prefix 'Instruct: Given a web search query, retrieve relevant passages that answer the query.\nQuery:' \
  --index ../index/ \
  --topics tools/topics-and-qrels/topics.bright-pony.tsv.gz \
  --output runs/run.bright-pony.diver-4b.txt \
  --hits 1000 \
  --l2-norm
```

## Evaluation
`nDCG@10` is the metric used in the Bright leaderboard and is what we use here for easior comparison.
```
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 -m recall.100 \
  tools/topics-and-qrels/qrels.bright-pony.txt \
  runs/run.bright-pony.diver-4b.txt
```


## Reproduction Log[*](reproducibility.md)