# BGE-base for NFCorpus in Database Vector Stores
This guide contains instructions for running a BGE-base baseline for NFCorpus in the following databases:

+ [DuckDB](#duckdb)
+ [ChromaDB](#chromadb)
+ [Weaviate](#weaviate)

The following results can be obtained:

| **Retrieval Method**                                                                                                  | **nDCG@10**  |
|:-------------------------------------------------------------------------------------------------------------|-----------|
| DuckDB BGE-Base (en-v1.5)                                                                                    | 0.3808    |
| ChromaDB BGE-Base (en-v1.5)                                                                                    | 0.3808    |
| Weaviate BGE-Base (en-v1.5)                                                                                    | 0.3808    |
> This exactly matches [that in Pyserini](https://github.com/castorini/pyserini/blob/master/docs/experiments-nfcorpus.md).

## Encoding
Assuming you have completed [this guide](https://github.com/castorini/pyserini/blob/master/docs/experiments-nfcorpus.md) and fetched the data, we start by encoding the corpus and queries to obtain embeddings. 
We will feed these embeddings into the vector stores directly. 

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

Let's define a method for retrieving results for one query. 
We obtain the query embeddings with the query ID passed in and use DuckDB's ```array_cosine_similarity``` method to find the closest document embeddings to our query embeddings. 

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
queries = conn.execute("SELECT id, embedding FROM query").fetchall()
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

which should yield the corresponding results in the table.


## ChromaDB
Now let's do the same thing, but in ChromaDB, an open source vector database. 
Start by installing it with: 

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

We're ready to retrieve! 
While ChromaDB supports searching multiple queries at a time, all the queries at once is too much and throws an error, so we will search for one query at a time. 

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

which should yield the corresponding results in the table.


## Weaviate
Now let's do the same thing again, but in Weaviate, another open source vector database. 
This time, we will use its free cloud to store our embeddings, but it also supports running locally. 
Start by creating an account on its [website](https://console.weaviate.cloud/) and making a sandbox cluster. 
On your cluster's page, find the REST encdpoint and the admin API key and set them as environment variables.

```bash
export WEAVIATE_URL='...'
export WEAVIATE_API_KEY='...'
```

Next, install its Python client.

```bash
pip install -U weaviate-client
```

Following this [guide](https://weaviate.io/developers/wcs/quickstart), we connect to our database and create a collection. 
We specify no vectorizer as we already have embeddings. 

```python
import weaviate, os
import weaviate.classes as wvc
import json

# Set these environment variables
URL = os.getenv("WEAVIATE_URL")
APIKEY = os.getenv("WEAVIATE_API_KEY")

# Connect to Weaviate Cloud
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=URL,
    auth_credentials=wvc.init.Auth.api_key(APIKEY),
)

# Check connection
client.is_ready()

import weaviate.classes as wvc

# Create the collection. Weaviate's autoschema feature will infer properties when importing.
if client.collections.exists("corpus"):
    client.collections.delete("corpus")
documents = client.collections.create(
    "corpus",
    vectorizer_config=wvc.config.Configure.Vectorizer.none(),
)
```

Let's load the corpus into our collection. 
It's more efficient to add in batches, so we will load documents to a list first. 

```python
corpus_file = 'indexes/nfcorpus.bge-base-en-v1.5/corpus_embeddings.jsonl'
query_file = 'indexes/nfcorpus.bge-base-en-v1.5/query_embeddings.jsonl'
docs = []
with open(corpus_file, 'r') as file:
    for line in file:
        row = json.loads(line.strip())
        docs.append(wvc.data.DataObject(properties={"doc_id": row['id']}, vector=row['vector']))

documents.data.insert_many(docs)
```

We're ready to retrieve!    

```python
from weaviate.classes.query import MetadataQuery
from tqdm import tqdm
run_tag = "bge_weaviate"

with open(query_file, "r") as f:
    n_queries = sum(1 for _ in f)

all_results = []
query_ids = []
with open(query_file, 'r') as file:
    for line in tqdm(file, total=n_queries, desc=f"Processing {run_tag}", unit="query"):
        row = json.loads(line.strip())
        query_ids.append(row['id'])
        all_results.append(documents.query.near_vector(near_vector=row['vector'], limit=1000, return_metadata=MetadataQuery(distance=True)))
```

We need to reformat the results before we can write them to file. 

```python
formatted_results = []
for i in range(3237):
    for j in range(1000):
        formatted_results.append((query_ids[i], all_results[i].objects[j].properties['doc_id'], 1 - all_results[i].objects[j].metadata.distance, 1 + j))

run_tag = "bge_weaviate"
with open("runs/weaviate_bge_nfcorpus.txt", 'w') as f:
    for query_id, doc_id, score, rank in formatted_results:
        a = f.write(f"{query_id} Q0 {doc_id} {rank} {score} {run_tag}\n")

client.close()
```

To evaluate our results:

```
python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels runs/weaviate_bge_nfcorpus.txt
```

which should yield the corresponding results in the table.

## Reproduction Log[*](reproducibility.md)
+ Results reproduced by [@Raghav0005](https://github.com/Raghav0005) on 2025-05-21 (commit [`74dce4f`](https://github.com/castorini/pyserini/commit/74dce4f0fde6b82f22d3ba6a2a798ac4d8033f66))
+ Results reproduced by [@JJGreen0](https://github.com/JJGreen0) on 2025-05-30 (commit ['60de330'](https://github.com/castorini/pyserini/commit/60de330278d89e14864fa004602958cb66d48923))
