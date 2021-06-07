# Pyserini: BM25 Baselines for KILT

The guide describes reproducing competitive BM25 baselinse for [KILT](https://github.com/facebookresearch/KILT): a benchmark for Knowledge Intensive Language Tasks.

**Note**: this guide requires ~100 GB of disk space available, since we will be working with snapshots of Wikipedia.

## Set Up Environment

Do the following:

```bash
# Create a virtual env
conda create -n kilt37 -y python=3.7 && conda activate kilt37

# Get the development installation of pyserini
git clone https://github.com/castorini/pyserini.git
pip install pyserini

# Get KILT scripts, input and gold data, and install the package
git clone https://github.com/facebookresearch/KILT.git
cd KILT

# go back to an older version
git reset 2130aafaaee0671bdbd03d781b1fa57ee02650d2
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

# Feel free to delete the kilt_knowledgesource.json file now if you need more disk space.
```

The rest of the instructions assume you are working at the following directory:

```
<dir>/ (*) <- here
    KILT/
    pyserini/
```

## Index the Corpus

Convert to passage or document level JSONL format indexable by Pyserini. You can inspect the individual nohup output files using `tail -f <file>`:

### Document-Level Sources

```bash
mkdir pyserini/collections/kilt_document
for filename in pyserini/collections/kilt_knowledge_split/kilt_ks.??; do
    [ -e "$filename" ] || continue
    nohup python pyserini/scripts/kilt/convert_kilt_to_document_jsonl.py \
        --input "$filename" \
        --output pyserini/collections/kilt_document/$(basename "$filename") \
        --flen 500000 \
        > nohup_$(basename "$filename").out &
done

# Once it's done, convert back into 1 file:
cat pyserini/collections/kilt_document/kilt_ks.?? > pyserini/collections/kilt_document/dump.jsonl
rm pyserini/collections/kilt_document/kilt_ks.??
# Sanity check (should give the same # of lines):
wc -l pyserini/collections/kilt_knowledgesource.json
wc -l pyserini/collections/kilt_document/dump.jsonl

# Finally, index into Anserini (about 1hr):
nohup python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 40 -input pyserini/collections/kilt_document/ \
 -index pyserini/indexes/kilt_document -storePositions -storeDocvectors -storeContents &
```

### Passage-Level Sources

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

# Finally, index into Anserini (about 1hr):
nohup python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 40 -input pyserini/collections/kilt_passage/ \
 -index pyserini/indexes/kilt_passage -storePositions -storeDocvectors -storeContents &
``` 

## Create Baseline Runs

Compute a run for a given index. Tasks can be configured using `--config`. You can increase the number of threads, but you may encounter OOM issues. I find that 8-20 is usually a good amount. This will take a 1-2 hours.

```bash
nohup python pyserini/scripts/kilt/run_retrieval.py \
 --config pyserini/scripts/kilt/dev_data.json \
 --index_dir pyserini/indexes/kilt_document \
 --output_dir pyserini/runs \
 --threads 8 \
 --topk 1000 \
 --name kilt_document &

```

You can use `kilt_passage` instead to run retrieval using the passage-level index.

## Evaluate

```bash
# Evaluate runs (takes a few minutes if you used topk 1000)
nohup ./pyserini/scripts/kilt/eval_runs.sh pyserini/runs/kilt_document 1,100,1000 > results.out &
```
You can use `kilt_passage` instead to run evaluation using the passage-level run.

## Results

Your results should look like this:

For R-Precision:

| model | FEV | AY2 | WnWi | WnCw | T-REx | zsRE | NQ | HoPo | TQA | ELI5 | WoW |
|-|-|-|-|-|-|-|-|-|-|-|-|
| baseline drqa (tfidf + bigram hashing) | 50.75 | 2.44 | 0.15 | 1.27 | 43.43 | 60.63 | 28.59 | 34.63 | 45.70 | 11.02 | 41.82 |
| anserini (document) | 38.21 | 3.43 | 0.09 | 2.71 | 44.64 | 50.08 | 29.93 | 38.37 | 36.76 | 7.17 | 22.27 |
| anserini (passage) | 43.04 | 3.18 | 0.15 | 2.75 | 55.06 | 67.50 | 24.64 | 41.43 | 24.95 | 5.84 | 24.85 |

For Recall@100/1000:

| model | FEV | AY2 | WnWi | WnCw | T-REx | zsRE | NQ | HoPo | TQA | ELI5 | WoW |
|-|-|-|-|-|-|-|-|-|-|-|-|
| baseline drqa (tfidf + bigram hashing) | 91.87/96.54 | - | - | - | 84.82/94.16 | 94.12/97.29 | 70.98/84.99 | 62.32/80.57 | 87.04/94.95 | 39.98/56.77 | 91.53/96.47 |
| anserini (document) | 88.41/95.65 | - | - | - | 83.24/92.36 | 91.83/97.82 | 75.12/87.59 | 59.66/78.59 | 81.21/92.36 | 34.00/53.12 | 69.95/83.58 |
| anserini (passage) | 91.99/95.79 | - | - | - | 88.03/94.25 | 98.01/99.25 | 75.55/87.08 | 61.52/77.80 | 80.18/91.32 | 32.50/47.85 | 65.96/78.45 |

## Reproduction Log[*](reproducibility.md)

+ Results reproduced by [@ArthurChen189](https://github.com/ArthurChen189) on 2021-05-03 (commit [`6d48609`](https://github.com/castorini/pyserini/commit/6d486094137a26c8a0a57652a06ab4d42d5bce32))
