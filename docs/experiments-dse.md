# Pyserini: Document Screenshot Embedding (DSE) Experiments

This guide provides instructions for reproducing DSE experiments using Pyserini.

DSE (Document Screenshot Embedding) is a novel retrieval paradigm that directly encodes document screenshots into dense representations, bypassing traditional document parsing and content extraction.

> Xueguang Ma, Sheng-Chieh Lin, Minghan Li, Wenhu Chen, Jimmy Lin. [Unifying Multimodal Retrieval via Document Screenshot Embedding](https://arxiv.org/abs/2406.11251). _arXiv:2406.11251_, 2024.

## Setup

DSE requires a vision-language model. We use the Phi-3 based DSE model from the paper:

The model will be downloaded automatically on first use when specified via `--encoder`.

## Wiki-SS: Wikipedia Screenshot Retrieval

The Wiki-SS dataset contains ~1.2M Wikipedia page screenshots for answering Natural Questions.

### Data Preparation

Download the Wiki-SS corpus from HuggingFace:

```bash
python scripts/dse/download_wiki_ss_corpus.py --output-dir collections/wiki-ss
```

### Encoding the Corpus

Encode document screenshots into dense vectors:

```bash
python -m pyserini.encode \
  input   --corpus collections/wiki-ss/corpus.jsonl \
          --fields contents \
  output  --embeddings encode/wiki-ss.dse \
  encoder --encoder Tevatron/dse-phi3-v1.0 \
          --encoder-class dse \
          --fields contents \
          --multimodal \
          --pooling last \
          --batch-size 16 \
          --device cuda:0
```

### Building the Index

Build a Faiss index from the embeddings:

```bash
python -m pyserini.index.faiss \
  --input encode/wiki-ss.dse \
  --output indexes/wiki-ss.dse \
  --dim 3072
```

### Retrieval

Run retrieval on NQ test questions:

```bash
python -m pyserini.search.faiss \
  --encoder-class dse \
  --encoder Tevatron/dse-phi3-v1.0 \
  --topics tools/topics-and-qrels/topics.wiki-ss-nq.test.tsv \
  --pooling last \
  --index indexes/wiki-ss.dse \
  --output runs/run.wiki-ss.dse.txt \
  --hits 20 \
  --device cuda:0 \
  --batch-size 1
```

### Evaluation

Evaluate retrieval accuracy with the built-in script (Top-k answer match):

```bash
python scripts/dse/evaluate_wiki_ss_run.py --run_file runs/run.wiki-ss.dse.txt --k 1
```

Expected results:

| Metric      | DSE    |
|-------------|--------|
| Top-1 Acc   | 43.0   |
| Top-5 Acc   | 65.5   |
| Top-10 Acc  | 71.3   |
| Top-20 Acc  | 76.0   |

## SlideVQA: Slide Retrieval

DSE is particularly effective for slide retrieval where visual layout matters. The SlideVQA dataset contains ~50k slide images for open-domain retrieval.

### Data Preparation

Download the SlideVQA corpus (images + corpus.jsonl):

```bash
python scripts/dse/download_slidevqa_corpus.py --output-dir collections/slidevqa
```

### Encoding the Corpus

Encode slide images into dense vectors:

```bash
python -m pyserini.encode \
  input   --corpus collections/slidevqa/corpus.jsonl \
          --fields contents \
  output  --embeddings encode/slidevqa.dse \
  encoder --encoder Tevatron/dse-phi3-v1.0 \
          --encoder-class dse \
          --fields contents \
          --multimodal \
          --pooling last \
          --batch-size 1 \
          --device cuda:0
```

### Building the Index

Build a Faiss index from the embeddings:

```bash
python -m pyserini.index.faiss \
  --input encode/slidevqa.dse \
  --output indexes/slidevqa.dse \
  --dim 3072
```

### Retrieval

Run retrieval on test questions:

```bash
python -m pyserini.search.faiss \
  --encoder-class dse \
  --encoder Tevatron/dse-phi3-v1.0 \
  --topics tools/topics-and-qrels/topics.slidevqa.test.tsv \
  --pooling last \
  --index indexes/slidevqa.dse \
  --output runs/run.slidevqa.dse.txt \
  --hits 20 \
  --device cuda:0
```

### Evaluation

Evaluate retrieval accuracy with trec_eval:

```bash
python -m pyserini.eval.trec_eval \
  -c -m ndcg_cut.10 -m recall.10 \
  tools/topics-and-qrels/qrels.slidevqa.test.txt \
  runs/run.slidevqa.dse.txt
```

Expected results:

| Method      | nDCG@10 | Recall@10 |
|-------------|---------|-----------|
| **DSE**     | **73.1**| **83.2**  |


## References

If you use DSE in your research, please cite:

```bibtex
@article{ma2024dse,
  title={Unifying Multimodal Retrieval via Document Screenshot Embedding},
  author={Ma, Xueguang and Lin, Sheng-Chieh and Li, Minghan and Chen, Wenhu and Lin, Jimmy},
  journal={arXiv preprint arXiv:2406.11251},
  year={2024}
}
```

## Reproduction Log[*](reproducibility.md)
