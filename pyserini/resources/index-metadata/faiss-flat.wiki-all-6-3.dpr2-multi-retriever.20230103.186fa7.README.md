# wiki-all-6-3-dpr2-multi

Faiss FlatIP index of wiki-all-6-3 (https://huggingface.co/datasets/castorini/odqa-wiki-corpora) encoded by a 2nd iteration DPR model trained on multiple QA datasets (castorini/wiki-all-6-3-multi-dpr2-passage-encoder).
This index was generated on 2023/01/03 on `narval` at commits:

+ Pyserini commit ['186fa7'](https://github.com/castorini/pyserini/commit/186fa793867f7572d62dc323322ba92926f12ce4) (2023/01/03)
+ [Tevatron](https://github.com/texttron/tevatron) commit [`7a5afe`](https://github.com/texttron/tevatron/commit/7a5afedb5893009154a0e915a2597e1a95e9d2a8) (2023/01/03)

with the following command to generate the embeddings (from Tevatron repo):

```bash
python -m tevatron.driver.jax_encode \
  --output_dir=temp \
  --model_name_or_path wiki-all-6-3-multi-dpr2-passage-encoder  \
  --per_device_eval_batch_size 1248 \
  --dataset_name wiki_all_6_3.jsonl \
  --encoded_save_path corpus_emb.pkl \
  --p_max_len 256
```
