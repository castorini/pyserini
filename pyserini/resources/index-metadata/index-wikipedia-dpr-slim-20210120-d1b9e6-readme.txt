This index was generated on 2021/01/20 at

+ anserini commit d1b9e67928aa60fa557113ace5d209b0c58e994c (2021/01/19).

with the following command:

sh anserini/target/appassembler/bin/IndexCollection -collection JsonCollection \
  -generator DefaultLuceneDocumentGenerator -threads 22 \
  -input wikipedia-dpr-jsonl -index index-wikipedia-dpr-slim-20210120-d1b9e6 -optimize

This minimal index does not store any "extras" (positions, document vectors, raw documents, etc.).

index-wikipedia-dpr-slim-20210120-d1b9e6.tar.gz MD5 checksum = 7d40604a824b5df37a1ae9d25ea38071
