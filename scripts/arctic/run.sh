folder="ArguAna"
topic="beir-v1.0.0-arguana-test"

export PYSERINI_CACHE=/store/scratch/sjupadhy/

python scripts/arctic/convert_topics.py \
 --embedding_path "/store/scratch/sjupadhy/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$folder/embeddings/queries_part_000000.parquet" \
 --output "/store/scratch/sjupadhy/queries/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$folder" --topic $topic

python -m pyserini.search.faiss \
 --index /store/scratch/sjupadhy/indexes/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$folder \
 --topics $topic --encoded-queries /store/scratch/sjupadhy/queries/mteb-retrieval-snowflake-arctic-embed-m-v1.5/$folder \
 --output run.beir.arctic.$folder.txt  --hits 2000 --threads 16 --batch-size 128

python -m pyserini.eval.trec_eval \
  -c -m ndcg_cut.10 $topic \
  run.beir.arctic.$folder.txt

python -m pyserini.eval.trec_eval \
  -c -m recall.100 $topic \
  run.beir.arctic.$folder.txt

python -m pyserini.eval.trec_eval \
  -c -m recall.1000 $topic \
  run.beir.arctic.$folder.txt