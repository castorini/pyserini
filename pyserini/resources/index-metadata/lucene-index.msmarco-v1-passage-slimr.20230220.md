This index was generated on 2023/02/20 with the following command:

python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/slimr_qtopk20_ptopk20_hardneg7_nobalanced \
  --index lucene-index.msmarco-v1-passage-slimr.20230220 \
  --generator DefaultLuceneDocumentGenerator \
  --threads 48 \
  --impact --pretokenized

lucene-index.msmarco-v1-passage-slimr.20230220.tar.gz MD5 checksum = 79e566fee4f376096e12a33cf67c8012
