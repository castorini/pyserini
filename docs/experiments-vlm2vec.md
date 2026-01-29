# Pyserini: Reproducing MMEB leaderboard with Visual Document Retrieval tasks
This guide contains steps to run 24 visdoc tasks from the MMEB benchmark with `Alibaba-NLP/gme-Qwen2-VL-2B-Instruct`, `VLM2Vec/VLM2Vec-V2.0`, and `code-kunkun/LamRA-Ret` multimodal VLMs.
The benchmark along with `VLM2Vec-V2.0` are introduced in the following paper:

Rui Meng and Ziyan Jiang and Ye Liu and Mingyi Su and Xinyi Yang and Yuepeng Fu and Can Qin and Zeyuan Chen and Ran Xu and Caiming Xiong and Yingbo Zhou and Wenhu Chen and Semih Yavuz. [VLM2Vec-V2: Advancing Multimodal Embedding for Videos, Images, and Visual Documents](https://arxiv.org/abs/2507.04590) _arXiv:2507.04590_

## Setup
You need to install vlm2vec-for-pyserini:
```
pip install vlm2vec-for-pyserini
```
Its requirements.txt have `torch`, and `flash-attn` pinned so that they are compatible with each other without the need to rebuild flash attention.
The `transformers` version is also pinned since the codebase doesn't work with versions >=5.0.0
and some of the models used here require even older versions. 

## Data Prepration
1. Download the visdoc datasets
```bash
LOCAL_DIR="./MMEB-V2" # <--- change this to the desired local directory
PYSERINI_DATA_DIR="$LOCAL_DIR/visdoc-tasks/pyserini"
python -m vlm2vec_for_pyserini.pyserini_integration.download_visdoc --local-dir $LOCAL_DIR
```

2. Exctract them
```bash
tar -zxf $LOCAL_DIR/visdoc-tasks/visdoc-tasks.data.tar.gz -C $LOCAL_DIR/visdoc-tasks
tar -zxf $LOCAL_DIR/visdoc-tasks/visdoc-tasks.images.tar.gz -C $LOCAL_DIR/visdoc-tasks
```

3. Process parquet files and store topics and qrels in pyserini compatible formats. For images
`save_pyserini_data` will store them locally and save their path in the corpus.
```bash
VLM2VEC_PKG_DIR=$(python - <<'EOF'
import importlib.util
spec = importlib.util.find_spec("vlm2vec_for_pyserini")
print(spec.submodule_search_locations[0])
EOF
)

VISDOC_YAML="$VLM2VEC_PKG_DIR/pyserini_integration/visdoc.yaml"

python -m vlm2vec_for_pyserini.pyserini_integration.save_pyserini_data \
    --yaml_file $VISDOC_YAML \
    --data_basedir $LOCAL_DIR/visdoc-tasks \
    --output_dir $PYSERINI_DATA_DIR \
    --num_workers 4
```
## Encoding and indexing the Corpus
Encode document screenshots into dense vectors:

```bash
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
    "MMLongBench-page"
    "MMLongBench-doc"
)

declare -A models
models=(
    ["gme-Qwen2-VL-2B-Instruct"]="Alibaba-NLP/gme-Qwen2-VL-2B-Instruct"
    ["VLM2Vec-V2.0"]="VLM2Vec/VLM2Vec-V2.0"
    ["LamRA-Ret"]="code-kunkun/LamRA-Ret"
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
```
Now you can index them, the index dimension must match the models' hidden sizes.

```bash
dimensions=(
    ["gme-Qwen2-VL-2B-Instruct"]=1536
    ["VLM2Vec-V2.0"]=1536
    ["LamRA-Ret"]=3584
)
for model_name in "${!dimensions[@]}"; do
    dimension=${dimensions[$model_name]}
    for dataset_name in "${datasets[@]}"; do
        echo "Processing embeddings of dataset: $dataset_name with model: $model_name"
        python -m pyserini.index.faiss \
            --input  "encode/mmeb-visdoc-${dataset_name}.${model_name}" \
            --output "indexes/mmeb-visdoc-${dataset_name}.${model_name}" \
            --metric inner \
            --dim dimension
    done
done
```

## Search
For VisRAG datasets the training split is used in MMEB and that is what we will use here as well.

```bash
for model_name in "${!models[@]}"; do
    model_path=${models[$model_name]}
    echo "Searching with model: $model_name"
    for dataset_name in "${datasets[@]}"; do
        echo "Searching queries of dataset: $dataset_name with model: $model_name"
        split=test
        if visrag in dataset_name.lower():
            split=train
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

## Evaluation
`ndcg@5` is the metric used in the MMEB leaderboard and is what we use here for easior comparison.
```bash
for model_name in "${!models[@]}"; do
    model_path=${models[$model_name]}
    echo "Results for model: $model_name"
    printf "%-50s | %-10s\n" "Dataset" "nDCG@5"
    echo "-------------------------------------------------------------------"
    for dataset_name in "${datasets[@]}"; do
        split=test
        if [[ "$dataset_name" == *"VisRAG"* ]]; then
            split=train
        fi
        score=$(python -m pyserini.eval.trec_eval \
            -c -m ndcg_cut.5 \
            "tools/topics-and-qrels/qrels.mmeb-visdoc-${dataset_name}.${split}.txt" \
            "runs_v1/run.mmeb-visdoc-${dataset_name}.${model_name}.txt" | grep 'ndcg_cut_5' | awk '{print $3}')
        printf "%-50s | %-10s\n" "$dataset_name" "$score"
    done
    echo "-------------------------------------------------------------------"
    echo ""
done
```

Expected output:
```
TODO: 
```
## Reproduction Log[*](reproducibility.md)