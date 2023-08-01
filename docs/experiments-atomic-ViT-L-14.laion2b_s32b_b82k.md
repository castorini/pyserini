# Pyserini: Reproducing AToMiC ViT-L-14-laion2B-s32B-b82K Baselines

Pyserini provides the following pre-built indexes for the AToMiC dataset, encoded with [`laion/CLIP-ViT-L-14-laion2B-s32B-b82K`](https://huggingface.co/laion/CLIP-ViT-L-14-laion2B-s32B-b82K):
- `atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.base`
- `atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.large`
- `atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.validation`
- `atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.base`
- `atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.large`
- `atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.validation`

## Data Prep
We need the topic directories (`ViT-L-14.laion2b_s32b_b82k.text.validation` and `ViT-L-14.laion2b_s32b_b82k.image.validation`) and the qrels files (`qrels.atomic.validation.t2i.trec` and `qrels.atomic.validation.i2t.trec`) to reproduce the baselines. This can be done by running the following script:

```bash
cd scripts/atomic
mkdir topics
wget https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/topics/ViT-L-14.laion2b_s32b_b82k.image.validation.tar.gz -P topics
tar -xzvf topics/ViT-L-14.laion2b_s32b_b82k.image.validation.tar.gz -C topics
wget https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/topics/ViT-L-14.laion2b_s32b_b82k.text.validation.tar.gz -P topics
tar -xzvf topics/ViT-L-14.laion2b_s32b_b82k.text.validation.tar.gz -C topics

mkdir qrels
wget https://huggingface.co/spaces/dlrudwo1269/AToMiC_bm25_files/resolve/main/qrels/qrels.atomic.validation.i2t.trec -P qrels
wget https://huggingface.co/spaces/dlrudwo1269/AToMiC_bm25_files/resolve/main/qrels/qrels.atomic.validation.t2i.trec -P qrels
```

## Convert Topics
We can convert the numpy topics to pyserini format as follows:
```bash
mkdir converted.ViT-L-14.laion2b_s32b_b82k.text.validation && mkdir converted.ViT-L-14.laion2b_s32b_b82k.image.validation
# Text
python convert_embeddings.py --encode-type text --inputs topics/ViT-L-14.laion2b_s32b_b82k.text.validation --topics-output converted.ViT-L-14.laion2b_s32b_b82k.text --embeddings-output converted.ViT-L-14.laion2b_s32b_b82k.text
# Image
python convert_embeddings.py --encode-type image --inputs topics/ViT-L-14.laion2b_s32b_b82k.image.validation --topics-output converted.ViT-L-14.laion2b_s32b_b82k.image --embeddings-output converted.ViT-L-14.laion2b_s32b_b82k.image
```

## Batch Retrieval Run
We can perform a batch retrieval run as follows, replacing `{setting}` with the desired setting (`base`, `large`, `validation`):
```bash
# Text to Image
python -m pyserini.search.faiss \
    --topics converted.ViT-L-14.laion2b_s32b_b82k.text.validation/topics.json \
    --index atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.{setting} \
    --hits 1000 \
    --encoder converted.ViT-L-14.laion2b_s32b_b82k.text.validation \
    --batch-size 256 \
    --threads 32 \
    --output run.ViT-L-14.laion2b_s32b_b82k.t2i.{setting}.trec
  
# Image to Text
python -m pyserini.search.faiss \
    --topics converted.ViT-L-14.laion2b_s32b_b82k.image.validation/topics.json \
    --index atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.{setting} \
    --hits 1000 \
    --encoded-queries converted.ViT-L-14.laion2b_s32b_b82k.image.validation \
    --batch-size 256 \
    --threads 32 \
    --output run.ViT-L-14.laion2b_s32b_b82k.i2t.{setting}.trec
```

We can evaluate using `trec_eval`:
```bash
# Text to Image
python -m pyserini.eval.trec_eval -c -m recip_rank -M 10 qrels/qrels.atomic.validation.t2i.trec run.ViT-L-14.laion2b_s32b_b82k.t2i.{setting}.trec
python -m pyserini.eval.trec_eval -c -m recall.10,1000 qrels/qrels.atomic.validation.t2i.trec run.ViT-L-14.laion2b_s32b_b82k.t2i.{setting}.trec

# Image to Text
python -m pyserini.eval.trec_eval -c -m recip_rank -M 10 qrels/qrels.atomic.validation.i2t.trec run.ViT-L-14.laion2b_s32b_b82k.i2t.{setting}.trec
python -m pyserini.eval.trec_eval -c -m recall.10,1000 qrels/qrels.atomic.validation.i2t.trec run.ViT-L-14.laion2b_s32b_b82k.i2t.{setting}.trec
```

The results should line up with [this spreadsheet](https://docs.google.com/spreadsheets/d/1wSi_79Qx3GA1WAirwvoapiWJ4m2bPRM_rtUWRZ2qRIo).