# Pyserini: Reproducing ColBERT End-to-End Results on MS MARCO (V1) Passage Dataset

This guide provides instructions to reproduce end-to-end ColBERT passage DEV results on MS MARCO (V1) using Pyserini ColBERT encoder and searcher.

## Our Implementation
This document only covers reproducing results using Pyserini ColBERT implementation. Please refer to [this repository](https://github.com/stanford-futuredata/ColBERT/commits/master) for the original ColBERT implementation.

We currently only cover end-to-end retrieval. Additionally, this reproduction does not include ColBERT training. We use an existing private checkpoint directly (located at Uwaterloo ORCA machine `/store/share/colbert-ckpt/colbert-400000.dnn`, MD5 checksum: `4f589d27fdbc41d0031562d7ef0748a7`, please keep it private if you do have access). However, results are generated with Pyserini indexer and searcher for ColBERT, and they are very much following the original ColBERT implementation. The major differences are
* We omit some optimization tricks (like grouping by 90-percentile  document length at retrieval phase, index bucketing tricks, etc.)
* We seek simplicity and readability of the code, for a better understanding of the ColBERT model, with newly added comments in our source code. However, the skeleton of the two versions of code remains similar.
* Our implementation use sharded index and does not require loading all the word vectors into memory (in contrast to [the original implementation](https://github.com/stanford-futuredata/ColBERT/blob/49d7fb69bdb2d7340780bad2926b06f6ce14d928/colbert/ranking/index_part.py#L34)), which can be too costly to run for typical hardware resources. Instead, our implementation can specify a retrieval-phase "shard divisor" to split the index into "divisions", and also the range of divisions for each process to fully load into main memory. In our implementation, each division will need to fit into GPU memory during ColBERT scoring. In theory, our implementation can perform end-to-end ColBERT search with any scale of data and limited hardware resources.

## Environment, speed, and index size
Experiments are running on the ComputeCanada Narval cluster.
The A100 GPUs on Narval make it much faster for ColBERT indexing and inference.

On ComputeCanada, we use the following python package dependencies:
```sh
export PYTHONPATH=""
export PIP_CONFIG_FILE=""
#conda create --yes --name py38 python=3.7.10
#conda activate py38
conda install --yes pytorch cudatoolkit=11.1 -c pytorch # pytorch=1.10.0
pip install faiss-gpu==1.6.5
conda install --yes openjdk=11 -c conda-forge
pip install transformers==4.9.2
conda install --yes pandas scikit-learn tqdm
pip install pyjnius onnxruntime fire
```

The resulting speed and index size for MS MARCO passage DEV set (containing 6980 queries):

| Indexing  | Inference | Index Size |
|:----------|----------:|-----------:|
| 8 hr 30 m | 3 hr 51 m | 277 GiB    |

Here queries are running slower than the original implementation because we load and spill each "division" into GPU for each query in order to support loading unlimited index shards for one process.

## Result reproduction

### Convert and prepare checkpoint
The original check point is in native Pytorch tensor, we need to first convert the checkpoint,
```sh
python scripts/tct_colbert/colbert_utils.py convert_vanilla_colbert /path/to/colbert-400000.dnn
```
this will generate a huggingface-compatible checkpoint `colbert_vanilla_128` (under current directory) which can be loaded by `from_pretrained()` method later.

Alternatively, there is a converted snapshot made available on ORCA: `/store/share/colbert-ckpt/colbert_vanilla_128.tar.gz` (MD5 checksum: `750b17d8b9d23e011094fb611b1292a5`)

Optionally, you can do a sanity check on an example query passage pair:
```sh
python scripts/tct_colbert/colbert_utils.py test_scoring --query_augment=True --device=cuda:0 --visualize=True ./colbert_vanilla_128 bert-base-uncased
```
the above command will generate a query passage word cross score PNG image.
If you find exact words can be well aligned, then the model checkpoint should be fine.

![](https://i.imgur.com/vUFE6MD.png)

Pass an additional `--emphasis` argument to above command for highlighting the best matched passage keywords:

![](https://i.imgur.com/c4cIRD3.png)

**Note:** For some of ComputeCanada computation cluster node where you do not have access to Internet, use the following one-line command to generate local tokenizer checkpoints before login to computation node:
```sh
python <<-EOF
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
tokenizer.save_pretrained("bert-base-uncased")
EOF
```

### Download MS MARCO passage corpus
Download a jsonl-format MS MARCO passage corpus.
```sh
wget https://huggingface.co/datasets/Tevatron/msmarco-passage-corpus/resolve/main/corpus.jsonl.gz -O corpus.jsonl.gz
gzip -d corpus.jsonl.gz
```

To allow Pyserini to load this jsonl corpus successfully, you will need to patch the code (for `JsonlCollectionIterator` to load this format):
```sh
wget https://vault.cs.uwaterloo.ca/s/qtGMgLjcRQX9xAA/download -O corpus-docid.patch
git apply corpus-docid.patch
```

### Encode and indexing
Here we provide a sbatch script (for running on A100) example to encode and index the corpus:
```sh
#!/bin/bash
#SBATCH --nodes=1           # total nodes
#SBATCH --gres=gpu:1        # how many GPUs per node
#SBATCH --cpus-per-task=4   # Cores proportional to GPUs
#SBATCH --mem=128gb         # Memory proportional to GPUs
#SBATCH --time=0-10:10      # 10 hours and 10 minutes
#SBATCH --output=job-%j-%N.out
set -x
export SLURM_ACCOUNT=def-jimmylin
export SBATCH_ACCOUNT=$SLURM_ACCOUNT
export SALLOC_ACCOUNT=$SLURM_ACCOUNT

srun --unbuffered python -m pyserini.encode \
        input --corpus /path/to/jsonl-corpus \
        encoder --encoder ./colbert_vanilla_128 \
        --tokenizer ./bert-base-uncased \
        --batch 90 --fp16 --device cuda:0 \
        output --embeddings ~/scratch/msmarco-passage-index-$SLURM_JOBID
```

The resulting index will contain 89 shards (100,000 documents per shard).
`doc_ids.<shard>.pkl` contains document IDs (stored as string), `doc_len.<shard>.pkl` has information for the length of each document, and `word_emb.<shard>.pt` contains all the word vectors in a flat matrix. In addition, `word_emb.faiss` is the FAISS index for all document words, it is used only for first-stage candidate words retrieval (1024 candidates per query token, following the original ColBERT implementation. See [code here](https://github.com/stanford-futuredata/ColBERT/blob/abb5b684e4cda297f3ff58b52e70d5b90270e900/colbert/retrieve.py#L24)). ColBERT scoring will only be performed against all those retrieved words.

### Searcher test (optional)
Optionally, before performing retrieval on all queries, you can issue a single handcrafted query to test searching on the first 10% of the newly generated ColBERT index (suppose your generated index is done by job #386523):
```sh
python -m pyserini.dsearch._colbert --device cuda:0 \
        --encoder ./colbert_vanilla_128 \
        --tokenizer ./bert-base-uncased \
        --index ~/scratch/msmarco-passage-index-386523 \
        --div 10 --div-selection 0 1 \
        --query "which organ system makes red blood cells"
```
Example output:
```
#divisions: 10
selection: [0, 1]
Using vanilla ColBERT: ../encoders/colbert_vanilla_128 ../encoders/tokenizer-bert-base-uncased
Reading FAISS index...
dim=128, code_sz=16
Total embedding vectors: 672,821,234
Reading docIDs...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████| 89/89 [00:01<00:00, 48.02it/s]
Generating in-memory offset index...
100%|████████████████████████████████████████████████████████████████████████████████████████████████████| 89/89 [00:23<00:00,  3.72it/s]
Total documents: 8,841,823
Loading flat tensors ranged from [0:66,840,619]
 10%|██████████▏                                                                                          | 9/89 [00:39<05:55,  4.44s/it]
Flat tensor memory usage = 16,318 MiB
[test query] which organ system makes red blood cells
Loading embs offset [0:66,840,619] to cuda:0
1 595001         20.6119384765625
2 873826         20.1416015625
3 540104         19.880126953125
4 544378         19.879150390625
5 803427         19.742919921875
6 594996         19.645751953125
7 117807         19.421875
8 416200         19.3740234375
9 490991         19.3433837890625
10 117644        19.0743408203125
```
where the first result is from passage#595001:
> Red blood cells are produced in the bone marrow (the spongy tissue inside the bone).
> In order to make red blood cells, the body maintains an adequate supply of erythropoietin (EPO), a hormone that is produced by the kidney.

this can give you an idea if the indexer and searcher are working.

### Passage Retrieval
In order to perform full retrieval, create a sbatch script named `sbatch-search.sh`
```sh
#!/bin/bash
#SBATCH --nodes=1           # total nodes
#SBATCH --gres=gpu:1        # how many GPUs per node
#SBATCH --cpus-per-task=4   # Cores proportional to GPUs
#SBATCH --mem=128gb         # Memory proportional to GPUs
#SBATCH --time=0-10:10      # 10 hours and 10 minutes
#SBATCH --output=job-%j-%N.out
set -x
export SLURM_ACCOUNT=def-jimmylin
export SBATCH_ACCOUNT=$SLURM_ACCOUNT
export SALLOC_ACCOUNT=$SLURM_ACCOUNT

SRCH_RANGE=${1-10_5_10} # or 10_0_5

srun --unbuffered python -m pyserini.dsearch \
        --topics msmarco-passage-dev-subset \
        --index ~/scratch/msmarco-passage-index-386523 \
        --device cuda:0 \
        --encoder ./colbert_vanilla_128 \
        --tokenizer ./bert-base-uncased \
        --search-range $(echo $SRCH_RANGE | sed -e 's/_/ /g') \
        --output msmarco-passage-$SLURM_JOBID-$SRCH_RANGE.run
```

To run this script, you will also need to pass an argument to specify the range of divisions/parts that will be evaluated and loaded into main memory.
For example, the following command
```sh
sbatch sbatch-search.sh 10_0_5
```
will use a divisor of 10 (split the entire index into 10 parts for retrieval, each part will be loaded into GPU memory), and only search for the `0..5` parts. But you will need to make sure these parts do not exceed the capacity of main memory.

On Narval, use the following shortcut script to issue 10 jobs with each only searching 1/10 of the index (each part will be fit into A100 GPU memory for maximum retrieval speed)
```sh
#!/bin/bash
set -x
for i in {0..9}; do
        j=$((i+1))
        sbatch sbatch-search.sh 10_${i}_${j}
done
```

After all 10 jobs are finished, you will need to merge these 10 run files generated by all finished jobs.
To do this, issue the following commands (suppose all the job IDs start with `3928`).
```sh
ls msmarco-passage-3928*.run | tr '\n' ',' | sed 's/,$//' > runfiles-sep-by-comma.txt
python scripts/trecfile_merge.py $(cat runfiles-sep-by-comma.txt)
```

Convert merged TREC run file into MS MARCO run file type:
```sh
cat merged.run | awk '{print $1 "\t" $3 "\t" $4}' > merged.run.msmacro.run
```

### Evaluation
Use Pyserini evaluation tools to get MRR results:
```sh
python tools/scripts/msmarco/msmarco_passage_eval.py \
        tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
        merged.run.msmacro.run
```
```txt
#####################
MRR @10: 0.3611133851821534
QueriesRanked: 6980
#####################
```
and for recall and MAP:
```sh
./tools/eval/trec_eval.9.0.4/trec_eval tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt ./merged.run -m recall.50
recall_50               all     0.8189
./tools/eval/trec_eval.9.0.4/trec_eval tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt ./merged.run -m recall.200
recall_200              all     0.9105
./tools/eval/trec_eval.9.0.4/trec_eval tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt ./merged.run -m recall.1000
recall_1000             all     0.9503
./tools/eval/trec_eval.9.0.4/trec_eval tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt ./merged.run -m map
map                     all     0.3672
```

For reference, our reproduced run files are made available for download:
https://vault.cs.uwaterloo.ca/s/EEgJxEP4MptcQqf

## Reproduction Log[*](reproducibility.md)
