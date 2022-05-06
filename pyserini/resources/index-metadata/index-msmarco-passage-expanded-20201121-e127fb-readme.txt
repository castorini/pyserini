This index was generated on 2020/11/21 at

+ docTTTTTquery commit 701ea0a72beeb8db46aa409352a72ba52cd2c36b Tue Nov 17 07:13:27 2020 -0500
+ anserini commit e127fbea6f5515d60eb7c325cd866657dbf13cc6 Sat Nov 21 07:58:03 2020 -0500

with the following command:

sh anserini/target/appassembler/bin/IndexCollection \
  -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
  -input msmarco-passage-expanded -index index-msmarco-passage-expanded-20201121-e127fb -threads 9 -optimize

Note that this index does not store any "extras" (positions, document vectors, raw documents, etc.).

index-msmarco-passage-expanded-20201121-e127fb.tar.gz MD5 checksum = e5762e9e065b6fe5000f9c18da778565
