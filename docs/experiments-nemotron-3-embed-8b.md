# Pyserini: Nemotron-3-Embed-8B for BEIR and TREC Deep Learning

This guide reproduces dense retrieval with NVIDIA's
[Nemotron-3-Embed-8B-BF16](https://huggingface.co/nvidia/Nemotron-3-Embed-8B-BF16) on BEIR and on
the TREC Deep Learning tracks DL19 through DL23, using the `nemotron` encoder class.

## The model's contract

The encoder class implements the model card exactly, so the commands below need no prompt flags:

| property | value | where it comes from |
|---|---|---|
| query prefix | `query: ` | `config_sentence_transformers.json` |
| document prefix | `passage: ` | `config_sentence_transformers.json` |
| prefix pooled with the text | yes | `1_Pooling/config.json`, `include_prompt: true` |
| pooling | mean over unpadded tokens | `1_Pooling/config.json`, `pooling_mode_mean_tokens: true` |
| normalisation | L2, so inner product == cosine | model card |
| padding side | left | model card snippets |
| dimension | 4096 | `1_Pooling/config.json` |
| dtype / attention | bfloat16, FlashAttention-2 with an SDPA fallback | model card |

Because the embeddings are normalised, a flat inner-product Faiss index reproduces the cosine
similarities on the model card. `--l2-norm` is applied by the class whether or not the flag is given;
the prefixes default to the values above and can be overridden with `--prefix` (documents) and
`--query-prefix` (queries).

A GPU with at least 20 GB is enough for inference: the checkpoint is ~16 GB in bfloat16.

## BEIR

Replace `${dataset}` with a BEIR dataset name, e.g. `nfcorpus`, `scifact`, `trec-covid`.
Corpora come from
[castorini/collections-beir](https://huggingface.co/datasets/castorini/collections-beir).

### Encode and index

```bash
dataset=nfcorpus
model=nvidia/Nemotron-3-Embed-8B-BF16

python -m pyserini.encode \
  input   --corpus collections/beir-v1.0.0/${dataset}/corpus.jsonl \
          --fields title text \
  output  --embeddings indexes/faiss-flat.beir-v1.0.0-${dataset}.nemotron-3-embed-8b \
          --to-faiss \
  encoder --encoder ${model} \
          --encoder-class nemotron \
          --fields title text \
          --batch-size 8 \
          --max-length 8192 \
          --dimension 4096 \
          --fp16 \
          --device cuda:0
```

`--max-length 8192` is a throughput choice, not a correctness one: BEIR passages are far shorter than
the model's 32,768-token window, and the class defaults to the full window when the flag is omitted.

### Search and evaluate

```bash
python -m pyserini.search.faiss \
  --encoder ${model} \
  --encoder-class nemotron \
  --index indexes/faiss-flat.beir-v1.0.0-${dataset}.nemotron-3-embed-8b \
  --topics beir-v1.0.0-${dataset}-test \
  --output runs/run.beir-v1.0.0-${dataset}.nemotron-3-embed-8b.txt \
  --batch-size 32 --threads 16 \
  --hits 1000 --remove-query

python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 beir-v1.0.0-${dataset}-test \
  runs/run.beir-v1.0.0-${dataset}.nemotron-3-embed-8b.txt
python -m pyserini.eval.trec_eval -c -m recall.100 -m recall.1000 beir-v1.0.0-${dataset}-test \
  runs/run.beir-v1.0.0-${dataset}.nemotron-3-embed-8b.txt
```

## TREC Deep Learning

DL19 and DL20 rerank the MS MARCO v1 passage corpus; DL21, DL22 and DL23 use the v2 segmented
corpus. The encoding commands are identical apart from the corpus and the index name.

### MS MARCO v1 passage (DL19, DL20)

```bash
python -m pyserini.encode \
  input   --corpus collections/msmarco-passage/corpus.jsonl \
          --fields text \
          --shard-id 0 --shard-num 8 \
  output  --embeddings indexes/faiss-flat.msmarco-v1-passage.nemotron-3-embed-8b.shard0 \
          --to-faiss \
  encoder --encoder nvidia/Nemotron-3-Embed-8B-BF16 \
          --encoder-class nemotron \
          --fields text --batch-size 8 --max-length 512 \
          --dimension 4096 --fp16 --device cuda:0
```

Shard the corpus across GPUs with `--shard-id`/`--shard-num` and merge with
`python -m pyserini.encode.merge_faiss_index`; 8.8M passages on one GPU is impractical for an 8B
encoder.

Then, for `topics` in `dl19-passage` and `dl20-passage`:

```bash
python -m pyserini.search.faiss \
  --encoder nvidia/Nemotron-3-Embed-8B-BF16 --encoder-class nemotron \
  --index indexes/faiss-flat.msmarco-v1-passage.nemotron-3-embed-8b \
  --topics ${topics} \
  --output runs/run.${topics}.nemotron-3-embed-8b.txt \
  --batch-size 32 --threads 16 --hits 1000

python -m pyserini.eval.trec_eval -c -l 2 -m map -m ndcg_cut.10 ${topics} \
  runs/run.${topics}.nemotron-3-embed-8b.txt
```

### MS MARCO v2 passage (DL21, DL22, DL23)

Same two commands against `collections/msmarco-v2-passage` and
`--topics dl21-passage` / `dl22-passage` / `dl23-passage`, evaluated with the v2 qrels. The v2
corpus is 138M segments, so shard aggressively.

## Two-click reproductions

A 2CR entry for this model additionally requires the Faiss indexes to be built and hosted as
pyserini prebuilt indexes, since `pyserini/2cr/beir.yaml` and the `msmarco-v1-passage` /
`msmarco-v2-passage` configs reference indexes by name rather than encoding at run time. Once the
indexes above are uploaded and registered in `pyserini/prebuilt_index_info.py`, an entry takes the
shape of the existing dense rows, for example:

```yaml
  - name: nemotron-3-embed-8b.faiss
    command: python -m pyserini.search.faiss --threads ${dense_threads} --batch-size ${dense_batch_size} --encoder-class nemotron --encoder nvidia/Nemotron-3-Embed-8B-BF16 --index beir-v1.0.0-${dataset}.nemotron-3-embed-8b --topics beir-v1.0.0-${dataset}-test --output $output --hits 1000 --remove-query
    datasets:
      - dataset: nfcorpus
        scores:
          - nDCG@10: 0.0000     # fill in from the run above
            R@100: 0.0000
            R@1000: 0.0000
```

The scores must come from actual runs; this PR deliberately does not add 2CR rows with
placeholder numbers, because `pyserini/2cr/beir.py` would then report regressions against values
nobody has measured.

## Testing the integration

`tests/core/test_nemotron_encoder.py` covers the pooling contract without downloading the
checkpoint. The end-to-end test reproduces the similarity matrix published on the model card and is
gated behind an environment variable, since it needs the 16 GB checkpoint and a GPU:

```bash
PYSERINI_TEST_NEMOTRON=1 python -m unittest tests.core.test_nemotron_encoder -v
```
