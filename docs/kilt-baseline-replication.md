# Replication guide KILT

## Setup env

```bash
# Create a virtual env
conda create -n kilt37 -y python=3.7 && conda activate kilt37

# Get the development installation of pyserini
git clone https://github.com/castorini/pyserini.git
pip install pyserini

# Get KILT scripts, input and gold data, and install the package
git clone https://github.com/facebookresearch/KILT.git
cd KILT
pip install -r requirements.txt
pip install .
mkdir data
python scripts/donwload_all_kilt_data.py
python scripts/get_triviaqa_input.py
cd ..

# Get NLTK dependencies
python -m nltk.downloader punkt
python -m nltk.downloader stopwords

# Get the KILT knowledge source / wikipedia dump (34.76GiB)
cd pyserini/collections/
wget http://dl.fbaipublicfiles.com/KILT/kilt_knowledgesource.json

# We'll split it in multiple files to make processing faster
mkdir kilt_knowledge_split
cd kilt_knowledge_split
split -l500000 ../kilt_knowledgesource.json kilt_ks.
cd ../../..
```

The rest of the instructions assume you are working at the following directory:

```
<dir>/ (*) <- here
    KILT/
    pyserini/
```

## Index the knowledge source

Convert to passage or document level JSONL format indexable by Pyserini (takes 1-2hr if bigrams is enabled):

### Document-level

```bash
mkdir pyserini/collections/kilt_document
for filename in pyserini/collections/kilt_knowledge_split/kilt_ks.??; do
    [ -e "$filename" ] || continue
    nohup python pyserini/scripts/kilt/convert_kilt_to_document_jsonl.py \
        --input "$filename" \
        --output pyserini/collections/kilt_document/$(basename "$filename") \
        --bigrams --stem \
        --flen 500000 \
        > nohup_$(basename "$filename").out &
done

# Once it's done, convert back into 1 file:
cat pyserini/collections/kilt_document/kilt_ks.?? > pyserini/collections/kilt_document/dump.jsonl
rm pyserini/collections/kilt_document/kilt_ks.??
# Sanity check (should give the same # of lines):
wc -l pyserini/collections/kilt_knowledgesource.json
wc -l pyserini/collections/kilt_document/dump.jsonl
```

If `--bigrams` is enabled, each document will be appended with tokens concatenated to form bigrams. By default, stopwords and punctuation are filtered.

If `--stem` is enabled, the tokens used to form bigrams will be stemmed using NLTK's SnowballStemmer.

### Passage-level

```bash
mkdir pyserini/collections/kilt_passage
for filename in pyserini/collections/kilt_knowledge_split/kilt_ks.??; do
    [ -e "$filename" ] || continue
    nohup python pyserini/scripts/kilt/convert_kilt_to_passage_jsonl.py \
        --input "$filename" \
        --output pyserini/collections/kilt_passage/$(basename "$filename") \
        --sections --bigrams --stem \
        --flen 500000 \
        > nohup_$(basename "$filename").out &
done

# Once it's done, convert back into 1 file:
cat pyserini/collections/kilt_passage/kilt_ks.?? > pyserini/collections/kilt_passage/dump.jsonl
rm pyserini/collections/kilt_passage/kilt_ks.??
``` 

If `--bigrams` is enabled, each document will be appended with tokens concatenated to form bigrams. By default, stopwords and punctuation are filtered.

If `--stem` is enabled, the tokens used to form bigrams will be stemmed using NLTK's SnowballStemmer.

If `--sections` is enabled, passages will instead be delimited by section headers, rather than the default newlines.

### Index into Anserini (about 1hr)

These instructions are the same whether you are using document or passage level index (just change the path accordingly):

```bash
nohup python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 40 -input <path to dump.jsonl e.g. pyserini/collections/kilt_document/> \
 -index pyserini/indexes/<index_name> -storePositions -storeDocvectors -storeContents &
```

## Create runs

Compute a run for a given index. Tasks can be configured using `--config`, I recommend ignoring the Entity Linking task, as it is slow and Anserini performs very poorly on it. You can increase the number of threads, but you may encounter OOM issues. I find that 8 is usually a good amount. This will take a few hours.

```bash
nohup python pyserini/scripts/kilt/run_retrieval.py \
 --config pyserini/scripts/kilt/dev_data.json \
 --index_dir pyserini/indexes/<index_name> \
 --output_dir pyserini/runs \
 --threads 8 \
 --topk 1000 \
 --name <name of run> \
 --bigrams --stem &

```

You can also use `pyserini/scripts/kilt/dev_data_no_entity_linking.json`

Make sure to enable `--bigrams` and `--stem` accordingly if you used them in your index

## Evaluate

```bash
# Evaluate runs (takes a few minutes if you used topk 1000)
nohup ./pyserini/scripts/kilt/eval_runs.sh pyserini/runs/<name of run> 1,100,1000 > results.out &
```

## Results

For R-Precision:


| model | FEV | AY2 | WnWi | WnCw | T-REx | zsRE | NQ | HoPo | TQA | ELI5 | WoW |
|-|-|-|-|-|-|-|-|-|-|-|-|
| baseline drqa (tfidf + bigram hashing) | 50.75 | 2.44 | 0.15 | 1.27 | 43.43 | 60.63 | 28.59 | 34.63 | 45.70 | 11.02 | 41.82 |
| anserini (document) | 38.21 | 3.43 | 0.09 | 2.71 | 44.64 | 50.08 | 29.93 | 38.37 | 36.76 | 7.17 | 22.27 |
| anserini (document + bigram) | 43.97 | - | - | - | 46.24 | 52.93 | 30.95 | 42.96 | 32.54 | 7.23 | 33.58 |
| anserini (document + stopword filter + bigram) | 40.13 | - | - | - | 54.36 | 70.84 | 27.63 | 45.34 | 29.76 | 7.37 | 30.94 |
| anserini (document + stopword filter + stem + bigram) | 39.89 | - | - | - | 54.22 | 70.09 | 26.89 | 45.04 | 29.65 | 7.23 | 31.36 |
| anserini (passage) | 43.04 | 3.18 | 0.15 | 2.75 | 55.06 | 67.50 | 24.64 | 41.43 | 24.95 | 5.84 | 24.85 |
| anserini (100w passages) | 52.04 | 3.03 | 0.06 | 2.96 | 34.00 | 57.81 | 26.33 | 41.41 | 31.74 | 6.83 | 28.74 |
| anserini (passage + stopword filter + stem + bigram) | 25.13 | - | - | - | 23.6 | 37.94 | 12.16 | 34.23 | 13.85 | 3.78 | 30.09 |
| anserini (sections) | 44.72 | - | - | - | 49.9 | 60.20 | 25.06 | 40.84 | 30.7 | 7.1 | 21.55 |
| anserini (sections + stopword filter + bigram) | 35.98 | - | - | - | 40.72 | 59.96 | 19.95 | 41.39 | 21.42 | 5.51 | 30.54 |
| anserini (sections + stopword filter + stem + bigram) | 35.61 | - | - | - | 37.42 | 59.34 | 19.77 | 41.23 | 21.10 | 5.11 | 30.94 |

For Recall@100/1000:

| model | FEV | AY2 | WnWi | WnCw | T-REx | zsRE | NQ | HoPo | TQA | ELI5 | WoW |
|-|-|-|-|-|-|-|-|-|-|-|-|
| baseline drqa (tfidf + bigram hashing) | 91.87/96.54 | - | - | - | 84.82/94.16 | 94.12/97.29 | 70.98/84.99 | 62.32/80.57 | 87.04/94.95 | 39.98/56.77 | 91.53/96.47 |
| anserini (document) | 88.41/95.65 | - | - | - | 83.24/92.36 | 91.83/97.82 | 75.12/87.59 | 59.66/78.59 | 81.21/92.36 | 34.00/53.12 | 69.95/83.58 |
| anserini (document + stopword filter + stem + bigram) | 89.89/96.60 | - | - | - | 88.07/95.10 | 98.31/99.73 | 75.21/87.87 | 68.09/83.84 | 79.37/91.98 | 34.52/52.22 | 75.83/87.02 |
| anserini (passage) | 91.99/95.79 | - | - | - | 88.03/94.25 | 98.01/99.25 | 75.55/87.08 | 61.52/77.80 | 80.18/91.32 | 32.50/47.85 | 65.96/78.45 |
| anserini (100w passages) | 91.36/95.09 | - | - | - | 54.25/58.95 | 84.56/86.49 | 75.76/86.53 | 56.89/70.14 | 81.92/91.80 | 32.62/48.62 | 69.00/81.43 |
| anserini (passage + stopword filter + stem + bigram) | 85.91/94.74 | - | - | - | 82.32/92.77 | 97.45/99.54 | 67.39/83.99 | 57.61/77.23 | 70.25/87.27 | 27.73/43.38 | 67.79/79.63 |
| anserini (sections) | 91.79/96.15 | - | - | - | 87.13/93.77 | 95.86/98.85 | 76.87/88.16 | 61.59/79.11 | 82.58/92.60 | 32.99/49.98 | 65.43/79.27 |
| anserini (sections + stopword filter + stem + bigram) | 89.36/96.01 | - | - | - | 84.19/93.61 | 98.95/99.68 | 72.34/86.64 | 63.32/80.91 | 76.73/90.41 | 31.24/47.71 | 69.91/82.63 |

