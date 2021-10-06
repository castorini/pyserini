This index was generated on 2021/04/22 at

+ anserini commit f29307a9fb162ec7bef4919a164929a673d2304e (2021/04/21).

with the following command:

python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 40 -input collections/wikipedia-kilt-doc \
 -index indexes/index-wikipedia-kilt-doc-20210421-f29307 -storeRaw -optimize

Note that to reduce index size:

+ positions are not indexed (so no phrase queries)
+ document vectors are not stored (so no query expansion)

However, the raw documents are stored, so they can be fetched and fed to further downstream reranking components.

index-wikipedia-kilt-doc-20210421-f29307.tar.gz MD5 checksum = b8ec8feb654f7aaa86f9901dc6c804a8
