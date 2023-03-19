This index was generated on 2023/02/20 with the following command:

python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/slimr_qtopk20_ptopk20_hardneg7_nobalanced_hardneg_distilled \
  --index lucene-index.msmarco-v1-passage-slimr-pp.20230220 \
  --generator DefaultLuceneDocumentGenerator \
  --threads 48 \
  --impact --pretokenized

lucene-index.msmarco-v1-passage-slimr-pp.20230220.tar.gz MD5 checksum = 17b2edd909bcda4980a93fb0ab87e72b
