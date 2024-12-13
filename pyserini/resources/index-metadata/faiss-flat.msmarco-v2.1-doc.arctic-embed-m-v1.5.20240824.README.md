# msmarco-v2.1-arctic-embed-m-v1.5

Faiss FlatIP indexes of msmarco v2.1 encoded by Snowflake embed-m-v1.5. These indexes were generated on 2024/08/26 on `orca`.

The indexes were generated from indexing embeddings available on [Huggingface](https://huggingface.co/datasets/Snowflake/msmarco-v2.1-snowflake-arctic-embed-m-v1.5).

## Preparation
Due to msmarco v2.1 dataset's large size, indexes needed to be divided in two parts.

```bash
python scripts/arctic/convert_embeddings.py --embeddings_folder /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-m-v1.5/corpus \
--output /store/scratch/sjupadhy/indexes/msmarco-v2.1-dev-snowflake-arctic-embed-m-v1.5-1 \
--indices 0_30

python scripts/arctic/convert_embeddings.py --embeddings_folder /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-m-v1.5/corpus \
--output /store/scratch/sjupadhy/indexes/msmarco-v2.1-dev-snowflake-arctic-embed-m-v1.5-2 \
--indices 30_59
```

### Topic embeddings
```bash
python scripts/arctic/convert_queries.py --embedding_path /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-m-v1.5/topics/snowflake-arctic-embed-m-v1.5-topics.msmarco-v2-doc.dev.parquet \
--output /store/scratch/sjupadhy/queries/msmarco-v2.1-dev-snowflake-arctic-embed-m-v1.5

```

