This index was generated on 2020/11/26 at

+ docTTTTTquery commit d2704c025c2bf6db652b4b27f49c4e59714ba898 (2020/11/24).
+ anserini commit 1b4d0a29879a867ca5d1f003f924acc3279455ba (2020/11/25).

with the following command:

sh anserini/target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 1 \
  -input msmarco-doc-expanded-passage -index index-msmarco-doc-expanded-per-passage-20201126-1b4d0a -optimize

Note that this index does not store any "extras" (positions, document vectors, raw documents, etc.).

index-msmarco-doc-expanded-per-passage-20201126-1b4d0a.tar.gz MD5 checksum = 54ea30c64515edf3c3741291b785be53
