This index was generated on 2021/05/19 at commit e25e33f4a06e9c1ab4d795908cae4474fa019643 2021-05-17 21:48:48 -0400 
with the following command:

sh target/appassembler/bin/IndexCollection -collection JsonCollection \
 -generator DefaultLuceneDocumentGenerator -input collections/msmarco-ltr-passage/ltr_collection_jsonl \
 -index index-msmarco-passage-ltr-20210519-e25e33f -threads 9 -storeRaw -optimize -storePositions -storeDocvectors -pretokenizdd

Note, pretokenized option is used to keep preprocessed tokenization.
This is built with spacy 3.0.6.

index-msmarco-passage-ltr-20210519-e25e33f MD5 checksum = a5de642c268ac1ed5892c069bdc29ae3
