#!/bin/bash

# Define a list of items
items=('ArguAna' 'CQADupstackAndroidRetrieval' 'CQADupstackEnglishRetrieval' 'CQADupstackGamingRetrieval' 
       'CQADupstackGisRetrieval' 'CQADupstackMathematicaRetrieval' 'CQADupstackPhysicsRetrieval' 
       'CQADupstackProgrammersRetrieval' 'CQADupstackStatsRetrieval' 'CQADupstackTexRetrieval' 
       'CQADupstackUnixRetrieval' 'CQADupstackWebmastersRetrieval' 'CQADupstackWordpressRetrieval' 
       'ClimateFEVER' 'DBPedia' 'FEVER' 'FiQA2018' 'HotpotQA' 'MSMARCO' 'NFCorpus' 'NQ' 
       'QuoraRetrieval' 'SCIDOCS' 'SciFact' 'TRECCOVID' 'Touche2020')
# items=('NQ')
for item in "${items[@]}"
# do
#     echo "Processing $item"
#     python scripts/arctic/convert_embeddings.py --embeddings_folder "/store/scratch/sjupadhy/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$item/embeddings/" \
#     --output "/store/scratch/sjupadhy/indexes/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$item" \
#     --start_filter documents_part_
# done
do
    echo "Processing $item"
    python scripts/arctic/convert_topics.py --embedding_path "/store/scratch/sjupadhy/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$item/embeddings/queries_part_000000.parquet" \
    --output "/store/scratch/sjupadhy/queries/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$item"
done
# do
#     echo "Processing $item"
#     python -m pyserini.search.faiss --index /store/scratch/sjupadhy/indexes/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$item \
#     --topics /store/scratch/sjupadhy/msmarco-v2.1-snowflake-arctic-embed-l/topics/topics.msmarco-v2-doc.dev.json \ 
#     --encoded-queries /store/scratch/sjupadhy/queries/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$item \
#     --output  \
#     --hits 2000 --threads 16 --batch-size 128
# done
