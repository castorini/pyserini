This index was generated on 2023/02/20 with the following command:

```
python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/slimr_qtopk20_ptopk20_hardneg7_nobalanced_hardneg_distilled \
  --index lucene-index.msmarco-v1-passage-slimr-pp.20230220 \
  --generator DefaultLuceneDocumentGenerator \
  --threads 48 \
  --impact --pretokenized
```

lucene-index.msmarco-v1-passage-slimr-pp.20230925.tar.gz MD5 checksum = 5badbe47b6a50cf252cafb8a648743f1

In April 2024, index was repackaged to adopt a more consistent naming scheme.
