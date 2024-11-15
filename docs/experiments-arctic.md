# Pyserini: Reproducing Arctic Results

## MS marco v2.1 doc
In order to handle msmarco v2.1 dataset's large size, we have the indexes divided in two partitions. Thus we need to perform retrieval runs for both of the indexes.

```bash
python -m pyserini.search.faiss --index msmarco-v2.1-doc-segmented-shard01.arctic-embed-l \
--topics msmarco-v2-doc.dev \ 
--encoder Snowflake/snowflake-arctic-embed-l \
--output run.msmarco-v2.1-doc.arctic-embed-l-1.dev.txt \
--hits 2000 --threads 16 --batch-size 128 --max-passage-hits 1000 --max-passage


python -m pyserini.search.faiss --index msmarco-v2.1-doc-segmented-shard02.arctic-embed-l \
--topics msmarco-v2-doc.dev \ 
--encoder Snowflake/snowflake-arctic-embed-l \
--output run.msmarco-v2.1-doc.arctic-embed-l-2.dev.txt \
--hits 2000 --threads 16 --batch-size 128 --max-passage-hits 1000 --max-passage
```

### Merging and compiling docwise results
As the available embeddings refer to doc segments, we need to complile doc wise results. Thus we merge and compile them with:
```bash
python scripts/arctic/merge_retrieved_results.py --arctic_run_folder arctic_runs \
--output_file run.msmarco-v2.1-doc.arctic-embed-l-merged.dev.txt \
--k 1000
```

### Evaluation
```bash
python -m pyserini.eval.trec_eval -c -m recall.1000 -m recall.100 -m ndcg_cut.10 msmarco-v2.1-doc.dev run.msmarco-v2.1-doc.arctic-embed-l-merged.dev.txt
Results:
recall_1000           	all	0.9408
recall_100            	all	0.8513
ndcg_cut_10           	all	0.3583
```

## BEIR
Retrieval run on NQ subdataset:
```bash
python -m pyserini.search.faiss --threads 16 --batch-size 512 --index beir-v1.0.0-nq.arctic-embed-m-v1.5 --topics beir-v1.0.0-nq-test --encoded-queries snowflake-arctic-embed-m-v1.5-beir-v1.0.0-nq-test  --output run.beir.arctic-embed.nq.txt --hits 1000
```

### Evaluation
```bash
python -m pyserini.eval.trec_eval   -c -m ndcg_cut.10  -m recall.1000 -m recall.100 beir-v1.0.0-nq-test   run.beir.arctic-embed.nq.txt
Results:
recall_1000             all     0.9951
ndcg_cut_10             all     0.6244
```