# Replication guide KILT

## Setup env

```bash
# Create a virtual env
conda create -n kilt37 -y python=3.7 && conda activate kilt37

# Install pyserini
pip install pyserini
git clone https://github.com/castorini/pyserini.git

# Get KILT scripts and install kilt package
git clone https://github.com/facebookresearch/KILT.git
cd KILT
pip install -r requirements.txt
pip install .
mkdir data
python scripts/donwload_all_kilt_data.py
python scripts/get_triviaqa_input.py
cd ..

# Get the KILT knowledge source (34.76GiB)
wget http://dl.fbaipublicfiles.com/KILT/kilt_knowledgesource.json
```

## Index the knowledge source

Convert to passage or document level JSONL format indexable by Pyserini (takes 1-2hr if bigrams is enabled):

```bash
# We'll split it in multiple files to make this faster
mkdir kilt_knowledge_split
cd kilt_knowledge_split
split -l500000 ../kilt_knowledgesource.json kilt_ks.
cd ..

# Run conversion script for each file
mkdir dump

# Document:
mkdir dump/doc_dump
for filename in kilt_knowledge_split/kilt_ks.??; do
    [ -e "$filename" ] || continue
    nohup python pyserini/scripts/kilt/convert_kilt_to_document_jsonl.py --input "$filename" --output dump/doc_dump/$(basename "$filename") --bigrams --stem --flen 500000 > nohup_$(basename "$filename").out &
done

# Once it's done, convert back into 1 file:
cat dump/doc_dump/kilt_ks.?? > dump/doc_dump/dump.jsonl
rm dump/doc_dump/kilt_ks.??
# Sanity check (should give the same # of lines):
wc -l kilt_knowledgesource.json
wc -l dump/doc_dump/dump.jsonl

# Passage:
mkdir dump/passage_dump
for filename in kilt_knowledge_split/kilt_ks.??; do
    [ -e "$filename" ] || continue
    nohup python pyserini/scripts/kilt/convert_kilt_to_passage_jsonl.py --input "$filename" --output dump/passage_dump/$(basename "$filename") --sections --bigrams --stem --flen 500000 > nohup_$(basename "$filename").out &
done

# Once it's done, convert back into 1 file:
cat dump/passage_dump/kilt_ks.?? > dump/passage_dump/dump.jsonl
rm dump/passage_dump/kilt_ks.??
``` 

Index into Anserini (about 1hr). These instructions are the same whether you are using document or passage level index (just change the path accordingly).:

```bash
nohup python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
 -threads 40 -input <path to dump.jsonl e.g. dump/doc_dump/dump.jsonl> \
 -index pyserini/indexes/<index_name> -storePositions -storeDocvectors -storeContents &
```

## Create runs

Compute a run for a given index. Tasks can be configured using `--config`, I recommend ignoring the Entity Linking task, as it is slow and Anserini performs very poorly on it. You can increase the number of threads, but you may encounter OOM issues. I find that 8 is usually a good amount. This will take a few hours.

```bash
nohup python pyserini/scripts/kilt/run_retrieval.py \
 --config KILT/kilt/configs/dev_data.json \
 --index_dir pyserini/indexes/<index_name> \
 --output_dir runs \
 --threads 8 \
 --topk 1000 \
 --name <name of run> \
 --bigrams --stem &

 # You can also use pyserini/scripts/kilt/dev_data_no_entity_linking.json
 # Make sure to enable --bigrams and --stem according to if you used them in your index
```

## Evaluate

```bash
# Evaluate runs (takes a few minutes if you used topk 1000)
nohup ./pyserini/scripts/kilt/eval_runs.sh runs/<name of run> 1,100,1000 &
```

## Results

| model | FEV | AY2 | WnWi | WnCw | T-REx | zsRE | NQ | HoPo | TQA | ELI5 | WoW |
|-|-|-|-|-|-|-|-|-|-|-|-|
| drqa (tfidf + bigram hashing) | 50.75 | 2.44 | 0.15 | 1.27 | 43.43 | 60.63 | 28.59 | 34.63 | 45.70 | 11.02 | 41.82 |
| anserini (document) | 38.21 | 3.43 | 0.09 | 2.71 | 44.64 | 50.08 | 29.93 | 38.37 | 36.76 | 7.17 | 22.27 |
| anserini (passage) | 43.04 | 3.18 | 0.15 | 2.75 | 55.06 | 67.50 | 24.64 | 41.43 | 24.95 | 5.84 | 24.85 |
| anserini (sections) | 44.72 | - | - | - | 49.9 | 60.20 | 25.06 | 40.84 | 30.7 | 7.1 | 21.55 |
| anserini (100w passages) | 52.04 | 3.03 | 0.06 | 2.96 | 34.00 | 57.81 | 26.33 | 41.41 | 31.74 | 6.83 | 28.74 |

