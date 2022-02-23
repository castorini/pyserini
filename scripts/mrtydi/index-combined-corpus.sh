collection_dir=$1  # the dir to the combined collection 
index_dir=all-language-optimize

python -m pyserini.index  \
    -collection MrTyDiCollection \
    -generator DefaultLuceneDocumentGenerator \
    -threads 12 \
    -input $collection_dir \
    -index $index_dir \
    -storePositions -storeRaw -storeDocvectors \
    -pretokenized -optimized

