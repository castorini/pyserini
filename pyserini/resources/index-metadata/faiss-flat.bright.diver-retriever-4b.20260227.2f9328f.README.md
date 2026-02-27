# BRIGHT: Diver-Retriever-4B

Faiss flat indexes of BRIGHT corpora using Diver-Retriever-4B.

These indexes were built on 2026/02/27 on `watgpu` (`NVIDIA L40S` and `NVIDIA RTX A6000` gpus) at Pyserini commit [2f9328f](https://github.com/castorini/pyserini/commit/2f9328fcebe4a0a82cface25d9994a3b8094324f).

Here is the command:

```bash
model="AQ-MedAI/Diver-Retriever-4B"
model_name="Diver-Retriever-4B"
for dataset_name in "${datasets[@]}"; do
dataset_name_underscore=${dataset_name//-/_}
dataset_name_dash=${dataset_name//_/-}
echo "Processing dataset: $dataset_name_underscore"
echo "Processing dataset: $dataset_name_dash"
python -m pyserini.encode \
  input   --corpus collections/bright/corpus/${dataset_name_underscore}.jsonl \
          --fields text \
          --delimiter "|||~~~|||||~~~~~" \
  output  --embeddings ./indexes/bright/${dataset_name_dash}.${model_name} \
           --to-faiss \
  encoder --encoder $model \
          --encoder-class qwen3 \
          --fields text \
          --batch-size 16 \
          --max-length 16384 \
          --explicit-truncate \
          --fp16 \
          --l2-norm \
          --dim 2560 \
          --device cuda:0 \
          --prefix 'Represent this text:'
done

```

The strange delimiter is due to BRIGHT documents containing many special characters. 
