# Pyserini: SlideOn on MS MARCO V1 Passage Ranking

This page describes MS MARCO V1 passage retrieval with [LightOn's SlideOn](https://huggingface.co/lightonai/SlideOn), using the dev subset and TREC Deep Learning 2019 and 2020 queries.
SlideOn represents queries and documents as sparse vectors of latent features.
Pyserini converts the weights to integer impacts for Lucene retrieval.

The default configuration is **d512/q64/s100**: at most 512 active document dimensions, at most 64 active query dimensions, and a weight scale of 100.

## Prerequisites

| Dependency | Tested version | Used for |
|---|---|---|
| Python | 3.12.3 | Both paths |
| PyTorch | 2.15.0 | PyTorch inference |
| Transformers | 5.22.1 | PyTorch inference |
| Java | 21 | Lucene search and ONNX inference |
| Anserini | 2.3.1-SNAPSHOT with runtime-`top_k` support (included in `287efc44`) | ONNX `SlideOnEncoder` support |

## Prebuilt Index

> These experiments use the prebuilt index; no document encoding or indexing is required.

Use `--index msmarco-v1-passage.slideon` to automatically download, verify, unpack, and cache the index from the public [Castorini MS MARCO V1 repository](https://huggingface.co/datasets/castorini/prebuilt-indexes-msmarco-v1/tree/main/passage/original/lucene-inverted/slideon).
Subsequent searches reuse the cached index.

The index contains **8,841,823 passages** with **d512/s100** representations.
The archive is 4.9 GB, with MD5 checksum `94e458ad39eaa847d4fc70e61e7c76ee`.
Allow additional disk space for the extracted index.

The documents come from [official precomputed SlideOn vectors](https://huggingface.co/datasets/lightonai/SlideOn-sparse-vectors/tree/96e5ef60b4c4edef039693371c192157361adccf).
As described in the [index README](https://huggingface.co/datasets/castorini/prebuilt-indexes-msmarco-v1/blob/main/passage/original/lucene-inverted/slideon/lucene-inverted.msmarco-v1-passage.slideon-d512-s100.20261025.43c2471.README.md), construction retained the first 512 entries of each stored descending-weight vector, multiplied weights by 100 in float32, rounded ties to even, and discarded zero impacts.

The document cap is fixed when building the index. Changing a **query** cap does not change the document representations or rebuild the index.

## Retrieval with PyTorch

Run from the repository root with a compatible Python environment activated. Retrieve Dev, DL19, and DL20, encoding queries on the fly using the CPU:

```bash
mkdir -p runs
for topics in msmarco-v1-passage.dev dl19-passage dl20-passage; do
  python -m pyserini.search.lucene \
    --index msmarco-v1-passage.slideon \
    --impact \
    --encoder lightonai/SlideOn \
    --max-active-dims 64 \
    --threads 16 --batch-size 128 \
    --topics ${topics} \
    --hits 1000 \
    --output runs/run.${topics}.slideon-pytorch.d512.q64.trec
done
```

`--impact` selects impact scoring. The model supplies task-specific query prompts automatically; do not prepend them manually.
In the **search CLI**, `--max-active-dims` controls the query cap only:

- Omitted: use 64.
- Positive integer: use that cap, for example `--max-active-dims 128`.
- `--max-active-dims None`: disable the final dimension cap.
- Zero and negative values are invalid.

PyTorch passes the cap to the official model, which prunes **before its final FP16 rounding**.
Pyserini then multiplies output weights by 100 in float32, rounds ties to even, and removes zero impacts.
`None` disables the final cap even if a checkpoint has a saved cap; it does not disable the model's internal token-level sparsification.

## Retrieval with ONNX

The [published ONNX model](https://huggingface.co/castorini/slideon-onnx) is loaded by Anserini, not Python ONNX Runtime.
Use the Java encoder name `SlideOn`, rather than a Hugging Face repository ID:

```bash
mkdir -p runs
for topics in msmarco-v1-passage.dev dl19-passage dl20-passage; do
  python -m pyserini.search.lucene \
    --index msmarco-v1-passage.slideon \
    --impact \
    --onnx-encoder SlideOn \
    --threads 16 --batch-size 128 \
    --topics ${topics} \
    --hits 1000 \
    --output runs/run.${topics}.slideon-onnx.d512.q64.trec
done
```

The Java encoder automatically downloads and caches the ONNX model, tokenizer, and configuration from `castorini/slideon-onnx`.
It runs query inference with batch size 1, a default query cap of **64**, and a default scale of **100**.
The current reproduction conditions require the runtime-`top_k` graph published at model revision `a2e29c5` (ONNX SHA-256 `75c906a8a5922a51ffae1ebe8521ca247fb134610d6c24731aa13b82ad35ad80`) and the matching Java encoder.
An old three-input ONNX graph is incompatible with this encoder; replace stale cached model assets if necessary.
`--max-active-dims` also configures ONNX SlideOn with the runtime-top-k Java encoder:

- Omitted: use 64.
- Positive integer: use that query cap, for example `--max-active-dims 128`.
- `--max-active-dims None`: disable final pruning (mapped to Java's `topK=0`).
- Zero and negative values are rejected, matching the PyTorch CLI convention.

For example, add `--max-active-dims 128` to the ONNX command above to search the same d512 index with q128. The d512 document representations are unchanged.
The Python API also accepts `max_active_dims` in `LuceneImpactSearcher(..., encoder_type='onnx')` and `LuceneImpactSearcher.from_prebuilt_index(..., encoder_type='onnx')` when the encoder name is `SlideOn`.

### Pruning and rounding

The current runtime-`top_k` ONNX graph prunes inside the model **before final FP16 rounding**, as does native PyTorch inference.
Both paths then scale the output weights and round ties to even to obtain integer impacts.
Matching pruning order does not guarantee bitwise-identical inference across runtimes or hardware.

## Evaluation

Evaluate all metrics reported below for both backends. Dev uses MRR@10 and Recall@1000 with relevance threshold 1. DL19/DL20 use MAP and Recall@1000 with relevance threshold 2, and nDCG@10 with the original graded judgments:

```bash
for backend in pytorch onnx; do
  python -m pyserini.eval.trec_eval \
    -c -M 10 -m recip_rank \
    msmarco-v1-passage.dev runs/run.msmarco-v1-passage.dev.slideon-${backend}.d512.q64.trec

  python -m pyserini.eval.trec_eval \
    -c -m recall.1000 \
    msmarco-v1-passage.dev runs/run.msmarco-v1-passage.dev.slideon-${backend}.d512.q64.trec

  for topics in dl19-passage dl20-passage; do
    python -m pyserini.eval.trec_eval \
      -c -m ndcg_cut.10 \
      ${topics} runs/run.${topics}.slideon-${backend}.d512.q64.trec

    python -m pyserini.eval.trec_eval \
      -c -l 2 -m map -m recall.1000 \
      ${topics} runs/run.${topics}.slideon-${backend}.d512.q64.trec
  done
done
```

The judged subsets contain **43 DL19 queries** and **54 DL20 queries**.
The topic aliases can include additional unjudged queries. Evaluation with `-c` uses the qrels query set.

### Current reproduction conditions

The [MS MARCO YAML](../pyserini/2cr/msmarco-v1-passage.yaml) contains `slideon-pytorch` and `slideon-onnx` conditions, each covering Dev, DL19, and DL20.
The [HTML summary](2cr/msmarco-v1-passage.html) displays them as separate rows.

| Backend | Dev MRR@10 | Dev R@1000 | DL19 MAP | DL19 nDCG@10 | DL19 R@1000 | DL20 MAP | DL20 nDCG@10 | DL20 R@1000 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| PyTorch | 0.3855 | 0.9878 | 0.4881 | 0.7252 | 0.8742 | 0.5064 | 0.7189 | 0.8744 |
| ONNX (runtime top-k) | 0.3855 | 0.9878 | 0.4881 | 0.7252 | 0.8742 | 0.5064 | 0.7189 | 0.8744 |

Dev uses 6,980 queries. Dev recall uses relevance threshold 1; DL19/DL20 MAP and recall use threshold 2, while nDCG uses the original grades.
Both backends' reference results were measured with CPU inference using the reproduction commands below.

Run and evaluate both MS MARCO conditions with the existing reproduction driver:

```bash
python -m pyserini.2cr.msmarco --collection v1-passage \
  --condition slideon-pytorch --directory runs --display-commands
python -m pyserini.2cr.msmarco --collection v1-passage \
  --condition slideon-onnx --directory runs --display-commands
```

Neural inference can vary across hardware and runtime versions; PyTorch and ONNX results need not be identical. See the [reproducibility notes](reproducibility.md).
