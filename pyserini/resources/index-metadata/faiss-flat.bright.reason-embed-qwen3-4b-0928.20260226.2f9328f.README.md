# BRIGHT: reason-embed-qwen3-4b-0928

Faiss flat indexes of BRIGHT corpora using reason-embed-qwen3-4b-0928.

These indexes were built on 2026/02/26 on `watgpu` at Pyserini commit [2f9328f](https://github.com/castorini/pyserini/commit/2f9328fcebe4a0a82cface25d9994a3b8094324f).

Here is the command:

```bash
model="hanhainebula/reason-embed-qwen3-4b-0928"
model_name="reason-embed-qwen3-4b-0928"

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
          --fp16 \
          --max-length 8192 \
          --l2-norm \
          --dimension 2560 \
          --device cuda:0
done
```

The strange delimiter is due to BRIGHT documents containing many special characters. 