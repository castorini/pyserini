# M-BEIR: blip-ff-large

Faiss flat indexes of M-BEIR corpora using blip-ff-large.

These indexes were built on 2026/03/02 on `watgpu` at Pyserini commit [fa77cbd](https://github.com/castorini/pyserini/commit/fa77cbd0a1162284573b1ba57d9d6cb661650c5e).

Here is the command for local candidates:

```bash
datasets=(
    cirr_task7
    edis_task2
    fashion200k_task0
    fashion200k_task3
    fashioniq_task7
    infoseek_task6
    infoseek_task8
    mscoco_task0
    mscoco_task3
    nights_task4
    oven_task6
    oven_task8
    visualnews_task0
    visualnews_task3
    webqa_task1
    webqa_task2
)
for dataset in "${datasets[@]}"; do
    dataset_name_underscore=${dataset//-/_}
    dataset_name_dash=${dataset//_/-}
    python -m pyserini.encode \
        input --corpus collections/m-beir/mbeir_${dataset_name_underscore}_cand_pool.jsonl \
                --fields img_path modality txt did \
                --docid-field did \
        output --embeddings indexes/m-beir-${dataset_name_dash}.blip-ff-large \
               --to-faiss \
        encoder --encoder blip_ff_large \
                --encoder-class uniir \
                --device cuda:0 \
                --fp16 \
                --multimodal \
                --batch-size 512 \
                --l2-norm \
                --fields img_path modality txt did
done
```

Here is the command for the global (union) candidates:

```bash
for i in {0..49}; do
    python -m pyserini.encode \
        input --corpus collections/m-beir/mbeir_union_test_cand_pool.jsonl \
                --fields img_path modality txt did \
                --docid-field did \
                --shard-id $i \
                --shard-num 50 \
        output  --embeddings indexes/m-beir-union_test.blip-ff-large.${i} \
                --to-faiss \
        encoder --encoder blip_ff_large \
                --encoder-class uniir \
                --device cuda:0 \
                --fp16 \
                --multimodal \
                --batch-size 512 \
                --l2-norm \
                --fields img_path modality txt did
done

python -m pyserini.index.merge_faiss_indexes \
    --prefix indexes/m-beir-union_test.blip-ff-large. \
    --shard-num 50
```
 