This index was generated on 2021/01/20 at

+ anserini commit d1b9e67928aa60fa557113ace5d209b0c58e994c (2021/01/19).

with the following command:

sh anserini/target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 22 \
  -input wikipedia-dpr-jsonl -index index-wikipedia-dpr-20210120-d1b9e6 -storeRaw -optimize

Note that to reduce index size:

+ positions are not indexed (so no phrase queries)
+ document vectors are not stored (so no query expansion)

However, the raw documents are stored, so they can be fetched and fed to further downstream reranking components.

index-wikipedia-dpr-20210120-d1b9e6.tar.gz MD5 checksum = c28f3a56b2dfcef25bf3bf755c264d04
