# BGE-base for NFCorpus in Database Vector Stores
This guide contains instructions for running a BGE-base baseline for NFCorpus in DuckDB and ChromaDB.

## Indexing
Assuming you have completed [this guide](https://github.com/castorini/pyserini/blob/master/docs/experiments-nfcorpus.md) and fetched the data, we start by encoding the corpus and queries to obtain embeddings.

```bash
mkdir indexes/nfcorpus.bge-base-en-v1.5

python -m pyserini.encode \
  input   --corpus collections/nfcorpus/corpus.jsonl \
          --fields title text \
  output  --embeddings indexes/nfcorpus.bge-base-en-v1.5 \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --fields title text \
          --batch 32

mv indexes/nfcorpus.bge-base-en-v1.5/embeddings.jsonl indexes/nfcorpus.bge-base-en-v1.5/corpus_embeddings.jsonl

python -m pyserini.encode \
  input   --corpus collections/nfcorpus/queries.jsonl \
          --fields text \
  output  --embeddings indexes/nfcorpus.bge-base-en-v1.5 \
  encoder --encoder BAAI/bge-base-en-v1.5 --l2-norm \
          --device cpu \
          --pooling mean \
          --fields text \
          --batch 32

mv indexes/nfcorpus.bge-base-en-v1.5/embeddings.jsonl indexes/nfcorpus.bge-base-en-v1.5/query_embeddings.jsonl
```

## DuckDB
Let's start with DuckDB. Install it with:
```bash
pip install duckdb
```

Then, we can connect to the database in Python. 
```python
import duckdb
conn = duckdb.connect(":memory:")
```

Now, we initialize and load tables for our corpus and queries. We use DuckDB's float array to hold our embeddings.
```python
corpus_path = 'indexes/nfcorpus.bge-base-en-v1.5/corpus_embeddings.jsonl'
query_path = 'indexes/nfcorpus.bge-base-en-v1.5/query_embeddings.jsonl'

embd_dim = 0
import json
with open(corpus_path, 'r') as file:
    for line in file:
        row = json.loads(line.strip())
        embd_dim = len(row['vector'])
        break

conn.execute(f"""create table corpus (id varchar primary key, embedding float[{embd_dim}])""")
conn.execute(f"""create table query (id varchar primary key, embedding float[{embd_dim}])""")

def load_jsonl_to_table(file_path, table_name):
    with open(file_path, 'r') as file:
        for line in file:
            row = json.loads(line.strip())
            a = conn.execute(f"""insert into {table_name} (id, embedding) values (?, ?)""", (row['id'], row['vector']))

load_jsonl_to_table(corpus_path, "corpus")
load_jsonl_to_table(query_path, "query")
```

Let's define a method for retrieving results for one query. We obtain the query embeddings with the query ID passed in and use DuckDB's ```array_cosine_similarity``` method to find the closest document embeddings to our query embeddings. 
```python
def embedding_search(query_id, top_n=5):
    query = f"""
    WITH query_embedding AS (
        SELECT embedding FROM query WHERE id = ?
    )
    SELECT corpus.id, 
            array_cosine_similarity(corpus.embedding, query_embedding.embedding) AS score
    FROM corpus, query_embedding
    ORDER BY score DESC
    LIMIT ?
    """
    return conn.execute(query, [query_id, top_n]).fetchall()
```

We call the retrieval method on all our queries to retrieve the top 1000 results for each. 
```python
from tqdm import tqdm
queries = conn.execute("SELECT id, contents FROM query").fetchall()
run_tag = "bge_duckdb"

all_results = []

for query_id, query_string in tqdm(queries, desc=f"Processing {run_tag}", unit="query"):
    results = embedding_search(query_id, top_n=1000)
    for rank, (doc_id, score) in enumerate(results, 1):
        all_results.append((query_id, doc_id, score, rank))

all_results.sort(key=lambda x: (x[0], x[3])) # sort by queryid, then rank

with open("runs/duckdb_bge_nfcorpus.txt", "w") as f:
    for query_id, doc_id, score, rank in all_results:
        a = f.write(f"{query_id} Q0 {doc_id} {rank} {score} {run_tag}\n")
```

To evaluate our results:
```
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels runs/duckdb_bge_nfcorpus.txt
```
which should yield:

| **Retrieval Method**                                                                                                  | **nDCG@10**  |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| BGE-Base (en-v1.5)                                                                                    | 0.3808    |
> This exactly matches [that in Pyserini](https://github.com/castorini/pyserini/blob/master/docs/experiments-nfcorpus.md).


## ChromaDB
Now let's do the same thing, but in ChromaDB, a vector database. Start by installing it with: 
```bash
pip install chromadb
```

We connect to the database in Python and create a 'collection' for our corpus.
```python
import chromadb
client = chromadb.Client()
collection = client.create_collection("corpus")
```

Load the corpus embeddings into our ChromaDB collection. 
```python
import json
embeddings = []
ids = []
corpus_file = 'indexes/nfcorpus.bge-base-en-v1.5/corpus_embeddings.jsonl'
query_file = 'indexes/nfcorpus.bge-base-en-v1.5/query_embeddings.jsonl'

with open(corpus_file, 'r') as file:
    for line in file:
        row = json.loads(line.strip())
        embeddings.append(row['vector'])
        ids.append(row['id'])

collection.add(embeddings=embeddings, ids=ids)
```

Load the queries into Python.
```python
query_ids = []
query_embeddings = []

with open(query_file, 'r') as file:
    for line in file:
        row = json.loads(line.strip())
        query_ids.append(row['id'])
        query_embeddings.append(row['vector'])
```

We're ready to retrieve! While ChromaDB supports searching multiple queries at a time, all the queries at once is too much and throws an error, so we will search for one query at a time. 
```python
from tqdm import tqdm
run_tag = "bge_chroma"
all_results = []

for embd in tqdm(query_embeddings, desc=f"Processing {run_tag}", unit="query"):
    all_results.append(collection.query(query_embeddings=[embd], n_results=1000, include=['distances']))
```

The results aren't formatted very nicely straight out of the box, so we will reformat them before writing them to file. 
```python
formatted_results = []
for i in range(3237):
    for j in range(1000):
        formatted_results.append((query_ids[i], all_results[i]['ids'][0][j], 1 - all_results[i]['distances'][0][j], 1 + j))

with open("runs/chroma_bge_nfcorpus.txt", 'w') as f:
    for query_id, doc_id, score, rank in formatted_results:
        a = f.write(f"{query_id} Q0 {doc_id} {rank} {score} {run_tag}\n")
```

To evaluate our results:
```
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels runs/chroma_bge_nfcorpus.txt
```
which should yield:

| **Retrieval Method**                                                                                                  | **nDCG@10**  |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| BGE-Base (en-v1.5)                                                                                    | 0.3808    |
> This exactly matches [that in Pyserini](https://github.com/castorini/pyserini/blob/master/docs/experiments-nfcorpus.md).