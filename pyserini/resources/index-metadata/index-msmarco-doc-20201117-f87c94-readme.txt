This index was generated on 2020/11/17 at commit f87c945fd1c1e4174468194c72e3c05688dc45dd Mon Nov 16 16:17:20 2020 -0500
with the following command:

sh target/appassembler/bin/IndexCollection -collection CleanTrecCollection \
 -generator DefaultLuceneDocumentGenerator -input collections/msmarco-doc \
 -index index-msmarco-doc-20201117-f87c94 -threads 1 -storeRaw -optimize

Note that to reduce index size:

+ positions are not indexed (so no phrase queries)
+ document vectors are not stored (so no query expansion)

However, the raw documents are stored, so they can be fetched and fed to further downstream reranking components.

index-msmarco-doc-20201117-f87c94.tar.gz MD5 checksum = ac747860e7a37aed37cc30ed3990f273
