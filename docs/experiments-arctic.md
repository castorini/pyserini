# Pyserini: Reproducing Arctic Results

## MS marco v2.1 doc
In order to handle msmarco v2.1 dataset's large size, we have the indexes divided in two partitions. Thus we need to perform retrieval runs for both of the indexes.

```bash
python -m pyserini.search.faiss --index /store/scratch/sjupadhy/indexes/msmarco-v2.1-snowflake-arctic-embed-l-1 \
--topics /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-l/topics/topics.msmarco-v2-doc.dev.json \ 
--encoded-queries /store/scratch/sjupadhy/queries/msmarco-v2.1-dev-snowflake-arctic-embed-l/ \
--output run.msmarco-v2.1-doc.arctic-embed-l-1.dev.txt \
--hits 2000 --threads 16 --batch-size 128


python -m pyserini.search.faiss --index /store/scratch/sjupadhy/indexes/msmarco-v2.1-snowflake-arctic-embed-l-2 \
--topics /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-l/topics/topics.msmarco-v2-doc.dev.json \ 
--encoded-queries /store/scratch/sjupadhy/queries/msmarco-v2.1-dev-snowflake-arctic-embed-l/ \
--output run.msmarco-v2.1-doc.arctic-embed-l-2.dev.txt \
--hits 2000 --threads 16 --batch-size 128
```

## Marging and compiling docwise results
As the available embeddings refer to doc segments, we need to complile doc wise results. Thus we merge and compile them with:
```bash
python scripts/arctic/merge_retrieved_results.py --arctic_run_folder arctic_runs \
--output_file run.msmarco-v2.1-doc.arctic-embed-l-merged.dev.txt \
--k 1000
```

## Evaluation
```bash
python -m pyserini.eval.trec_eval -c -m recall.1000 -m recall.100 -m ndcg_cut.10 /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-l/qrels/qrels_qrels.msmarco-v2.1-doc.dev.txt run.msmarco-v2.1-doc.arctic-embed-l-merged.dev.txt
Results:
recall_1000           	all	0.9408
recall_100            	all	0.8513
ndcg_cut_10           	all	0.3583
```