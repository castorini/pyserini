This index was generated on 2020/11/17 at commit f87c945fd1c1e4174468194c72e3c05688dc45dd Mon Nov 16 16:17:20 2020 -0500
with the following command:

sh target/appassembler/bin/IndexCollection -collection JsonCollection \
 -generator DefaultLuceneDocumentGenerator -input collections/msmarco-passage/collection_jsonl \
 -index index-msmarco-passage-20201117-f87c94 -threads 9 -storeRaw -optimize

Note that to reduce index size:

+ positions are not indexed (so no phrase queries)
+ document vectors are not stored (so no query expansion)

However, the raw passages are stored, so they can be fetched and fed to further downstream reranking components.

index-msmarco-passage-20201117-f87c94.tar.gz MD5 checksum = 1efad4f1ae6a77e235042eff4be1612d
