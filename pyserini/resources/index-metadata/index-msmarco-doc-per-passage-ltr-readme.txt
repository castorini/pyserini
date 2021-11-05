This index was generated on 2021/10/31 at commit 33e4151e6d58f5b8ea0ef0768dc5308ec48b1aae 2021-10-31 16:53:36 +0800 
with the following command:

sh target/appassembler/bin/IndexCollection -collection JsonCollection \
 -generator DefaultLuceneDocumentGenerator -input collections/msmarco-ltr-document/ltr_msmarco_pass_doc_jsonl \
 -index index-msmarco-doc-per-passage-ltr-20211031-33e4151 -threads 21 -storeRaw -optimize -storePositions -storeDocvectors -pretokenizdd

Note, pretokenized option is used to keep preprocessed tokenization.
This is built with spacy 3.0.6.
The max length is 3 and stride is 1.

index-msmarco-passage-ltr-20210519-e25e33f MD5 checksum = bd60e89041b4ebbabc4bf0cfac608a87
