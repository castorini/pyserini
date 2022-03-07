# Pyserini: Guide to Encoding a Collection and Search

## How do I encode my own documents?
In Pyserini, *encode* refers to the process that generating vectors from the text collections.
These vectors can be used to perform retrieval directly,
or to be further [*indexed*](docs/usage-dense-indexes.md) into, for example, HNSW index.

### Prepare collection
The input should be in JSONL format. 
Each line is a json dictionary containing two fields, i.e .`id` and `contents`.
- `id` is the document id in string.
- `contents` contains all the fields of the documents. By default, Pyserini expects the fields in contents are separated by `\n`.
```json
{
  "id": "doc1",
  "contents": "www.url.com\ntitle\nthis is the contents.\ndocument expansion"
}
```
In the above example, the document has two fields in contents `text` and `expand`.

The field can be controled using `--delimiter` argument under `input`, see the example below.

### Encode documents with Dense encoder
```
python -m pyserini.encode input   --corpus msmarco-passage-expanded \
                                  --fields url title text expand \  # fields in collection contents
                                  --delimiter "\n" \
                          output  --embeddings path/to/output/dir \
                          encoder --encoder castorini/tct_colbert-v2-hnp-msmarco \
                                  --fields title text \  # fields to encode
                                  --batch 32 \
                                  --fp16  # if inference with autocast()
```
> with `--to-faiss`, the generated embeddings will be stored as FaissIndexIP directly.
> Otherwise it will be stored in `.jsonl` format.

If in `.jsonl` format, each line contains following info:
```json
{
  "id": "doc1",
  "contents": "www.url.com\ntitle\nthis is the contents.\ndocument expansion",
  "vector": [0.12, 0.12, 0.13, 0.14]
}
```


### Encode documents with Sparse encoder
```
python -m pyserini.encode input   --corpus msmarco-passage-expanded \
                                  --fields url title text expand \
                          output  --embeddings path/to/output/dir \
                          encoder --encoder castorini/unicoil-d2q-msmarco-passage \
                                  --fields title text expand \
                                  --batch 32 \
                                  --fp16 # if inference with autocast()
```
The output will be stored in jsonl format. Each line contains following info:
```json
{
  "id": "doc1",
  "contents": "www.url.com\ntitle\nthis is the contents.\ndocument expansion",
  "vector": {"this":  0.12, "is":  0.1, "the":  0, "contents": 2.1}
}
```

## How do I search in the encoded collection?

Once the collection is encoded, you can use `FaissSearcher` to search the index:
```python
from pyserini.dsearch import FaissSearcher

searcher = FaissSearcher(
    'indexes/dindex-sample-dpr-multi', 'facebook/dpr-question_encoder-multiset-base'
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

If you want to speed up the passage embedding generation, you can run create the index in shard way.
e.g. the command below create a sub-index for the first 1/4 of the collection.
```bash
python -m pyserini.encode input   --corpus integrations/resources/sample_collection_jsonl \
                                  --fields title text \  # fields in collection contents
                                  --shard-id 0 \   # The id of current shard
                                  --shard-num 4 \  # The total number of shards
                          output  --embeddings indexes/dindex-sample-dpr-multi-0 \
                                  --to-faiss \
                          encoder --encoder facebook/dpr-ctx_encoder-multiset-base \
                                  --fields title text \  # fields to encode
                                  --batch 32
```
Then you can run 4 process on 4 gpu to speed up the process by 4 times.

Once it's done, you can merge the sub-indexes together by:
```bash
python -m pyserini.index.merge_faiss_indexes --prefix indexes/dindex-sample-dpr-multi- --shard-num 4
```