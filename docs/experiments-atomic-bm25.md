
# Pyserini: Reproducing AToMiC BM 25 Baselines

Pyserini provides the following pre-built indexes for the AToMiC dataset to reproduce the baselines in the [AToMiC paper](https://arxiv.org/pdf/2304.01961.pdf):
- `atomic_text_v0.2.1_small_validation`
- `atomic_text_v0.2.1_base`
- `atomic_text_v0.2.1_large`
- `atomic_image_v0.2_small_validation`
- `atomic_image_v0.2_base`
- `atomic_image_v0.2_large`

## Data Prep
We need the topic files (`topics.atomic.validation.text.jsonl` and `topics.atomic.validation.image-caption.jsonl`) and the qrels files (`qrels.atomic.validation.t2i.trec` and `qrels.atomic.validation.i2t.trec`) to reproduce the baselines given in the paper.

The required files are located under [`pyserini/tools/topics-and-qrels/`](https://github.com/castorini/anserini-tools/tree/7b84f773225b5973b4533dfa0aa18653409a6146/topics-and-qrels). If you have a dev installation of pyserini, you can simply access the files there.
Otherwise,
```bash
export DATA_DIR="https://huggingface.co/spaces/dlrudwo1269/AToMiC_bm25_files/resolve/main" # TODO: replace with link from anserini-tools repo once merged

mkdir topics
wget ${DATA_DIR}/topics/topics.atomic.validation.text.jsonl -P topics
wget ${DATA_DIR}/topics/topics.atomic.validation.image-caption.jsonl -P topics

mkdir qrels
wget ${DATA_DIR}/qrels/qrels.atomic.validation.i2t.trec -P qrels
wget ${DATA_DIR}/qrels/qrels.atomic.validation.t2i.trec -P qrels
```

## Batch Retrieval Run
We can perform a batch retrieval run as follows, replacing `{setting}` with the desired setting (`small.validation`, `base`, `large`):
```bash
# Text to Image
python -m pyserini.search.lucene \
  --index atomic_text_v0.2.1_{setting} \
  --topics topics.atomic.validation.text.jsonl \
  --output runs/run.validation.bm25-anserini-default.t2i.{setting}.trec \
  --bm25 --hits 1000 --threads 16 --batch-size 64
  
# Image to Text
python -m pyserini.search.lucene \
  --index atomic_image_v0.2_{setting} \
  --topics topics.atomic.validation.image-caption.jsonl\
  --output runs/run.validation.bm25-anserini-default.i2t.{setting}.trec \
  --bm25 --hits 1000 --threads 16 --batch-size 64
```

We can evaluate using `trec_eval`:
```bash
# Text to Image
python -m pyserini.eval.trec_eval -c -m recip_rank -M 10 qrels.atomic.validation.t2i.trec runs/run.validation.bm25-anserini-default.t2i.{setting}.trec
python -m pyserini.eval.trec_eval -c -m recall.10,1000 qrels.atomic.validation.t2i.trec runs/run.validation.bm25-anserini-default.t2i.{setting}.trec

# Image to Text
python -m pyserini.eval.trec_eval -c -m recip_rank -M 10 qrels.atomic.validation.i2t.trec runs/run.validation.bm25-anserini-default.i2t.{setting}.trec
python -m pyserini.eval.trec_eval -c -m recall.10,1000 qrels.atomic.validation.i2t.trec runs/run.validation.bm25-anserini-default.i2t.{setting}.trec
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
