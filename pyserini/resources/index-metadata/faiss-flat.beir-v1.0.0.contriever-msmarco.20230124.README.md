# BEIR v1.0.0 contriever-msmarco

This index was generated on 20230124 using Tevatron with following command: 

```
python -m tevatron.driver.encode \
--output_dir=temp \
--model_name_or_path facebook/contriever-msmarco \
--fp16 \
--tokenizer_name bert-base-uncased \
--per_device_eval_batch_size 156 \
--p_max_len 512 \
--dataset_name Tevatron/beir-corpus:$subdataset \
--encoded_save_path beir_embeddings/corpus_emb.$subdataset.pkl
```

where the `subdataset` is one of the BEIR dataset, e.g. `scifact`.

The Embedding is then converted to Pyserini index format.

In April 2024, indexes were repackaged to adopt a more consistent naming scheme.
