This index was generated on 2023/02/20 with the following command:

python -m pyserini.index.lucene \
  --collection JsonVectorCollection \
  --input collections/slimr_qtopk20_ptopk20_hardneg7_nobalanced \
  --index lucene-index.msmarco-v1-passage-slimr.20230220 \
  --generator DefaultLuceneDocumentGenerator \
  --threads 48 \
  --impact --pretokenized

lucene-index.msmarco-v1-passage-slimr.20230925.tar.gz MD5 checksum = 3532a09a4a47f862d63b8df81b39ecc9
