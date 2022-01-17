This index was generated on 2020/12/04 at

+ docTTTTTquery commit 5be1af130b4657ea117781f761c4e5d15c77cb42 (2020/12/01).
+ anserini commit f50dcceb6cd0ec3403c1e77066aa51bb3275d24e (2020/12/04).

with the following command:

sh anserini/target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 1 \
  -input msmarco-doc-passage -index index-msmarco-doc-per-passage-20201204-f50dcc -storeRaw -optimize

Note that to reduce index size:

+ positions are not indexed (so no phrase queries)
+ document vectors are not stored (so no query expansion)

However, the raw documents are stored, so they can be fetched and fed to further downstream reranking components.

index-msmarco-doc-per-passage-20201204-f50dcc.tar.gz MD5 checksum = 797367406a7542b649cefa6b41cf4c33
