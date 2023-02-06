# wiki-all-6-3-tamber lucene index

This Lucene index was generated on 2023/01/11 at Pyserini commit ['40277a'](https://github.com/castorini/pyserini/commit/40277ae007e4d28882af19d6ce1e899a0af04a68)
with the following commands:

First make sure you have git lfs installed to clone the huggingface repository.
```bash
git lfs install
```

```bash
git clone https://huggingface.co/datasets/castorini/odqa-wiki-corpora

python -m pyserini.index.lucene \
  --collection MrTyDiCollection \
  --input odqa-wiki-corpora/wiki-all-6-3-tamber \
  --index indexes/index-wiki-all-6-3-tamber-20230111-40277a \
  --generator DefaultLuceneDocumentGenerator \
  --threads 12 \
  --optimize \
  --storeRaw
  ```

lucene-index-wiki-all-6-3-tamber-20230111-40277a.tar.gz MD5 checksum = 018b45ee8c6278a879caa3145b2dc05d
