# MMEB-visdoc: VLM2Vec-V2

Faiss flat indexes of MMEB-visdoc corpora using VLM2Vec-V2.

These indexes were built on 2026/03/03 on watgpu at Pyserini commit [fa77cbd](https://github.com/castorini/pyserini/commit/fa77cbd0a1162284573b1ba57d9d6cb661650c5e).

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
    "MMLongBench-page"
)

declare -A models
models=(
    # ["gme-Qwen2-VL-2B-Instruct"]="Alibaba-NLP/gme-Qwen2-VL-2B-Instruct"
    ["VLM2Vec-V2.0"]="VLM2Vec/VLM2Vec-V2.0"
)

declare -A dimensions
dimensions=(
    ["gme-Qwen2-VL-2B-Instruct"]=1536
    ["VLM2Vec-V2.0"]=1536
)

for model_name in "${!models[@]}"; do
    model_path=${models[$model_name]}
    echo "Encoding with model: $model_name"
    for dataset_name in "${datasets[@]}"; do
        echo "Processing dataset: $dataset_name with model: $model_name"
        python -m pyserini.encode \
          input   --corpus "corpus/mmeb_visdoc_${dataset_name}.jsonl" \
                  --fields corpus_id image_path \
                  --docid-field corpus_id \
          output  --embeddings "indexes/mmeb-visdoc-${dataset_name}.${model_name}" \
                  --to-faiss \
          encoder --encoder $model_path \
                  --encoder-class mmeb \
                  --fields corpus_id image_path \
                  --multimodal \
                  --pooling eos \
                  --batch-size 16 \
                  --l2-norm \
                  --fp16 \
                  --device cuda:0 \
                  --dimension ${dimensions[$model_name]}
    done
done
```
