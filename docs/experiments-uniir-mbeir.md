# Pyserini: Evaluating M-BEIR Dataset with UniIR Models

This guide contains instructions for running baselines on the CIRR dataset (one of the M-BEIR datasets) and document test collections with UniIR ClipSF model from the following paper:

> Cong Wei, Yang Chen, Haonan Chen, Hexiang Hu, Ge Zhang, Jie Fu, Alan Ritter, and Wenhu Chen. [UniIR : Training and Benchmarking Universal Multimodal Information Retrievers](https://arxiv.org/abs/2106.14807) _arXiv:2311.17136_.

## Data Prep
 
First, download the CIRR dataset from [here](https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/cand_pool/local/mbeir_cirr_task7_cand_pool.jsonl) to the `collections/m-beir/CIRR` folder inside pyserini.

Then, download the 4 parts of the image dataset from [here](https://huggingface.co/datasets/TIGER-Lab/M-BEIR/tree/main), merge them into 1 tar.gz file and extract it. Make sure the extracted folder is in the same directory as the mbeir_cirr_task7_cand_pool.jsonl file.

Finally, download the [topics](https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/query/test/mbeir_cirr_task7_test.jsonl) file and the [qrels](https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/qrels/test/mbeir_cirr_task7_test_qrels.txt) file to the same directory as well.

## Passage Collection

To run UniIR models, you must first make sure you have properly set up pyserini, follow the installation guide's UniIR section if you haven't.

To encode the corpus, use the following command:
```bash
python -m pyserini.encode \
  input --corpus collections/m-beir/CIRR/mbeir_cirr_task7_cand_pool.jsonl \
        --fields img_path modality txt did \
        --docid-field did \
  output --embeddings encode/mbeir-cirr.clipsf \
  encoder --encoder clip_sf_large \
          --encoder-class uniir \
          --device cuda:1 \
          --fields img_path modality txt did
```

To index the embeddings with FAISS, run:

```bash
python -m pyserini.index.faiss \
    --input encode/mbeir-cirr.clipsf \
    --output indexes/faiss.mbeir-cirr.clipsf \
    --metric inner
```

The above minimal index should be ~64 MB.

Perform a run on the test queries without instructions:

```bash
python -m pyserini.search.faiss \
    --encoder-class uniir \
    --encoder clip_sf_large \
    --topics-format mbeir \
    --topics collections/m-beir/CIRR/topics_mbeir_cirr_task7_test.jsonl \
    --index indexes/faiss.mbeir-cirr.clipsf \
    --output runs/mbeir-cirr.no-instr.clipsf.txt \
    --hits 1000
```

If you want to use UniIR with M-BEIR query instructions, download it from [here](https://huggingface.co/datasets/TIGER-Lab/M-BEIR/blob/main/instructions/query_instructions.tsv)
Then, create a yaml file like this:
```yaml
instruction_file: absolute/path/to/query_instructions.tsv
candidate_modality: image
dataset_id: 8 # the id for CIRR is 8
random_instruction: False # set to true if you want to use a random instruction for each query
```

Then, run the following command:

```bash
python -m pyserini.search.faiss \
    --encoder-class uniir \
    --encoder clip_sf_large \
    --topics-format mbeir \
    --topics collections/m-beir/CIRR/topics_mbeir_cirr_task7_test.jsonl \
    --index indexes/faiss.mbeir-cirr.clipsf \
    --output runs/mbeir-cirr.instr.clipsf.txt \
    --instruction-config path/to/instruction_config.yaml \
    --hits 1000
```

Evaluation:

First we will need to fix the qrels file to proper TREC format so it is compatible with pyserini's trec_eval:
```bash
cut -d' ' -f1-4 mbeir_cirr_task7_test_qrels.txt > mbeir_cirr_task7_test_qrels_fixed.txt
```

_Without instructions_
```bash
python -m pyserini.eval.trec_eval -c -m recall.5 collections/m-beir/CIRR/mbeir_cirr_task7_test_qrels_fixed.txt runs/mbeir-cirr.no-instr.clipsf.txt

Results:
recall_5           	all	0.3876
```

_With instructions_
```bash
python -m pyserini.eval.trec_eval -c -m recall.5 collections/m-beir/CIRR/mbeir_cirr_task7_test_qrels_fixed.txt runs/mbeir-cirr.instr.clipsf.txt

Results:
recall_5           	all	0.4519
```


## Reproduction Log[*](reproducibility.md)

