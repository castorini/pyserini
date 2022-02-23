set -e

collection_dir=all-mbert-mrtydi-corpus  # the dir to the combined collection 
index_dir=all-language-index-optimized

mkdir -p $collection_dir

# download files
for lang in arabic  bengali  english finnish  indonesian  japanese  korean  russian  swahili  telugu  thai ; do
	echo "Downloading $lang corpus"
	lang_dir=$collection_dir/$lang
	mkdir -p $lang_dir
	wget "https://huggingface.co/datasets/crystina-z/mbert-mrtydi-corpus/resolve/main/mr-tydi-v1.1-mbert-tokenize-$lang/corpus.jsonl.gz" -P $lang_dir
done


# index
python -m pyserini.index  \
    -collection MrTyDiCollection \
    -generator DefaultLuceneDocumentGenerator \
    -threads 12 \
    -input $collection_dir \
    -index $index_dir \
    -storePositions -storeRaw -storeDocvectors \
    -pretokenized -optimized

