
# Pyserini: Reproducing AToMiC BM 25 Baselines

Pyserini provides the following pre-built indexes for the AToMiC dataset to reproduce the baselines in the [AToMiC paper](https://arxiv.org/pdf/2304.01961.pdf):
- `lucene-index.atomic.text.flat.small.validation`
- `lucene-index.atomic.text.flat.base`
- `lucene-index.atomic.text.flat.large`
- `lucene-index.atomic.image.flat.small.validation`
- `lucene-index.atomic.image.flat.base`
- `lucene-index.atomic.image.flat.large`

## Data Prep
We need the topic files (`validation.text.search.jsonl` and `validation.image-caption.search.jsonl`) and the qrels files (`validation.qrels.t2i.projected.trec` and `validation.qrels.i2t.projected.trec`) to reproduce the baselines given in the paper.

If you have a dev installation of `pyserini`, the required files are located under `pyserini/tools/topics-and-qrels/`. Otherwise, you can download them at [this repository](https://huggingface.co/spaces/dlrudwo1269/AToMiC_bm25_files/tree/main/). 

## Batch Retrieval Run
We can perform a batch retrieval run as follows, replacing `{setting}` with the desired setting (`small.validation`, `base`, `large`):
```bash
# Text to Image
python -m pyserini.search.lucene \
  --index lucene-index.atomic.image.{setting} \
  --topics validation.text.search.jsonl \
  --output runs/run.validation.bm25-anserini-default.t2i.{setting}.trec
  --bm25 --hits 1000 --threads 16 --batch-size 64
  
# Image to Text
python -m pyserini.search.lucene \
  --index lucene-index.atomic.text.{setting} \
  --topics validation.image-caption.search.jsonl \
  --output runs/run.validation.bm25-anserini-default.i2t.{setting}.trec
  --bm25 --hits 1000 --threads 16 --batch-size 64
```

We can evaluate using `trec_eval`:
```bash
# Text to Image
python -m pyserini.eval.trec_eval -c -m recip_rank -M 10 validation.qrels.t2i.projected.trec runs/run.validation.bm25-anserini-default.t2i.{setting}.trec
python -m pyserini.eval.trec_eval -c -m recall.10,1000 validation.qrels.t2i.projected.trec runs/run.validation.bm25-anserini-default.t2i.{setting}.trec

# Image to Text
python -m pyserini.eval.trec_eval -c -m recip_rank -M 10 validation.qrels.i2t.projected.trec runs/run.validation.bm25-anserini-default.i2t.{setting}.trec
python -m pyserini.eval.trec_eval -c -m recall.10,1000 validation.qrels.i2t.projected.trec runs/run.validation.bm25-anserini-default.i2t.{setting}.trec
```

## Known Issues
We have noticed that using `python -m pyserini.search.lucene` can be slow for certain queries (especially when searching using the `large` indexes). Using Anserini's `SearchCollection` can significantly speed up the search time. This can be done in a Python shell as follows:
```python
from pyserini.pyclass import autoclass
SearchCollection = autoclass("io.anserini.search.SearchCollection")
# Text to Image
t2i_search_args = [
    "-index", "lucene-index.atomic.image.{setting}",
    "-topics", "validation.text.search.jsonl",
    "-topicreader", "JsonString",
    "-topicfield", "title",
    "-output", "runs/run.validation.bm25-anserini-default.t2i.{setting}.trec",
    "-bm25", "-hits", "1000", "-parallelism", "64", "-threads", "64"

]
# Image to Text
i2t_search_args = [
    "-index", "lucene-index.atomic.text.{setting}",
    "-topics", "validation.image-caption.search.jsonl",
    "-topicreader", "JsonString",
    "-topicfield", "title",
    "-output", "runs/run.validation.bm25-anserini-default.i2t.{setting}.trec",
    "-bm25", "-hits", "1000", "-parallelism", "64", "-threads", "64"
]
SearchCollection.main(search_args)
```
