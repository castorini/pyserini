# MMEB-visdoc: gme-Qwen2-VL-2B-Instruct

Faiss flat indexes of MMEB-visdoc corpora using gme-Qwen2-VL-2B-Instruct.

These indexes were built on 2026/01/30 on `watgpu508` [NVIDIA H200 NVL] at Pyserini commit [ad8e050](https://github.com/castorini/pyserini/commit/ad8e050980a0b71ced425997570dcbc9940e633e).

## Note on Reproducibility
The use of Flash Attention introduces minor variations in the generated embedding vectors across different hardware configurations.

- Variance: While results are not bit-identical, the impact is minimal. The generated vectors maintain a high degree of consistency, with pairwise cosine similarities > 0.9996.

- Cause: These slight discrepancies are a result of hardware-specific optimizations in the Flash Attention custom kernels.

## Generation Command

```bash
#!/bin/bash

datasets=( 
    "ViDoRe_arxivqa"   
    "ViDoRe_docvqa"  
    "ViDoRe_infovqa"
    "ViDoRe_tabfquad"
    "ViDoRe_tatdqa"
    "ViDoRe_shiftproject"
    "ViDoRe_syntheticDocQA_artificial_intelligence"
    "ViDoRe_syntheticDocQA_energy"
    "ViDoRe_syntheticDocQA_government_reports"
    "ViDoRe_syntheticDocQA_healthcare_industry"
    "ViDoRe_esg_reports_human_labeled_v2"
    "ViDoRe_biomedical_lectures_v2_multilingual"
    "ViDoRe_economics_reports_v2_multilingual"
    "ViDoRe_esg_reports_v2_multilingual"
    "VisRAG_ArxivQA"
    "VisRAG_ChartQA"
    "VisRAG_MP-DocVQA"
    "VisRAG_SlideVQA"
    "VisRAG_InfoVQA"
    "VisRAG_PlotQA"
    "ViDoSeek-page"
    "ViDoSeek-doc"
    "MMLongBench-doc"
    "MMLongBench-page"
)

declare -A models
models=(
    ["gme-Qwen2-VL-2B-Instruct"]="Alibaba-NLP/gme-Qwen2-VL-2B-Instruct"
    # ["VLM2Vec-V2.0"]="VLM2Vec/VLM2Vec-V2.0"
    # ["LamRA-Ret"]="code-kunkun/LamRA-Ret"
)

for model_name in "${!models[@]}"; do
    model_path=${models[$model_name]}
    echo "Encoding with model: $model_name"
    for dataset_name in "${datasets[@]}"; do
        echo "Processing dataset: $dataset_name with model: $model_name"
        python -m pyserini.encode \
          input   --corpus "$PYSERINI_DATA_DIR/corpus/mmeb_visdoc_${dataset_name}.jsonl" \
                  --fields corpus_id image_path \
                  --docid-field corpus_id \
          output  --embeddings "encode/mmeb-visdoc-${dataset_name}.${model_name}" \
          encoder --encoder $model_path \
                  --encoder-class mmeb \
                  --fields corpus_id image_path \
                  --multimodal \
                  --pooling eos \
                  --batch-size 16 \
                  --l2-norm \
                  --fp16 \
                  --device cuda:0
    done
done

declare -A dimensions
dimensions=(
    ["gme-Qwen2-VL-2B-Instruct"]=1536
    # ["VLM2Vec-V2.0"]=1536
    # ["LamRA-Ret"]=3584
)
for model_name in "${!dimensions[@]}"; do
    dimension=${dimensions[$model_name]}
    for dataset_name in "${datasets[@]}"; do
        echo "Processing embeddings of dataset: $dataset_name with model: $model_name"
        python -m pyserini.index.faiss \
            --input  "encode/mmeb-visdoc-${dataset_name}.${model_name}" \
            --output "indexes/mmeb-visdoc-${dataset_name}.${model_name}" \
            --metric inner \
            --dim $dimension
    done
done

for model_name in "${!models[@]}"; do
    model_path=${models[$model_name]}
    echo "Searching with model: $model_name"
    for dataset_name in "${datasets[@]}"; do
        echo "Searching queries of dataset: $dataset_name with model: $model_name"
        split=test
        if [[ "$dataset_name" == *"VisRAG"* ]]; then
            split=train
        fi
        python -m pyserini.search.faiss \
            --encoder-class mmeb \
            --encoder $model_path \
            --topics-format mmeb \
            --topics "tools/topics-and-qrels/topics.mmeb-visdoc-${dataset_name}.${split}.jsonl" \
            --index  "indexes/mmeb-visdoc-${dataset_name}.${model_name}" \
            --output "runs/run.mmeb-visdoc-${dataset_name}.${model_name}.txt" \
            --pooling eos \
            --fp16 \
            --l2-norm \
            --hits 1000 \
            --device cuda:0
    done
done
```
