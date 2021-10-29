This index was generated on 2020/12/04 at

+ docTTTTTquery commit 5be1af130b4657ea117781f761c4e5d15c77cb42 (2020/12/01).
+ anserini commit f50dcceb6cd0ec3403c1e77066aa51bb3275d24e (2020/12/04).

with the following command:

sh anserini/target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 1 \
  -input msmarco-doc-passage -index index-msmarco-doc-per-passage-slim-20201204-f50dcc -optimize

This minimal index does not store any "extras" (positions, document vectors, raw documents, etc.).

index-msmarco-doc-per-passage-slim-20201204-f50dcc.tar.gz MD5 checksum = 77c2409943a8c9faffabf57cb6adca69
