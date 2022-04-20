set -e

sep_collection_dir=all-mbert-mrtydi-corpus  # the dir to the combined collection 
merged_collection_dir=merged-mbert-mrtydi-corpus  # the dir to the combined collection 
index_dir=all-language-index-optimized

mkdir -p $sep_collection_dir
mkdir -p $merged_collection_dir

# download files
for lang in arabic  bengali  english finnish  indonesian  japanese  korean  russian  swahili  telugu  thai ; do
	echo "Downloading $lang corpus"
	lang_dir=$sep_collection_dir/$lang
	mkdir -p $lang_dir
	wget "https://huggingface.co/datasets/crystina-z/mbert-mrtydi-corpus/resolve/main/mr-tydi-v1.1-mbert-tokenize-$lang/corpus.jsonl.gz" -P $lang_dir
done

python scripts/mrtydi/combine_corpus.py -i $sep_collection_dir -o $merged_collection_dir

# index
python -m pyserini.index  \
    -collection MrTyDiCollection \
    -generator DefaultLuceneDocumentGenerator \
    -threads 12 \
    -input $merged_collection_dir \
    -index $index_dir \
    -storePositions -storeRaw -storeDocvectors \
    -pretokenized -optimize

