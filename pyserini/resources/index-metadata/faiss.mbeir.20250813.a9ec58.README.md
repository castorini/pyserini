# M-BEIR Datasets Indexes

Faiss FlatIP index of M-BEIR datasets.

All dataset corpus are downloaded from [here](https://huggingface.co/datasets/TIGER-Lab/M-BEIR/tree/main/cand_pool/local)

These indexes were generated on 2025/08/13 at Anserini commit [`a9ec58`](https://github.com/castorini/anserini/commit/a9ec58ac9208f0246e39a39d7d8c95a431b45b56) on `basilisk` with the following commands:

clip-sf-large model:
```bash
python -m pyserini.encode \
  input --corpus M-BEIR/cand_pool/local/mbeir_{dataset}_cand_pool.jsonl \
        --fields img_path modality txt did \
        --docid-field did \
  output --embeddings encode/m-beir-{dataset}.clipsf  \
  encoder --encoder clip_sf_large \
          --encoder-class uniir \
          --device cuda:0 \
          --fp16 \
          --multimodal \
          --fields img_path modality txt did

python -m pyserini.index.faiss \
    --input encode/m-beir-{dataset}.clipsf \
    --output indexes/m-beir-{dataset}.clip-sf-large.20250813.a9ec58 \
    --metric inner
```

blip-ff-large model:
```bash
python -m pyserini.encode \
  input --corpus M-BEIR/cand_pool/local/mbeir_{dataset}_cand_pool.jsonl \
        --fields img_path modality txt did \
        --docid-field did \
  output --embeddings encode/m-beir-{dataset}.blipff  \
  encoder --encoder blip_ff_large \
          --encoder-class uniir \
          --device cuda:0 \
          --fp16 \
          --multimodal \
          --fields img_path modality txt did

python -m pyserini.index.faiss \
    --input encode/m-beir-{dataset}.blipff \
    --output indexes/m-beir-{dataset}.blip-ff-large.20250813.a9ec58 \
    --metric inner
```

