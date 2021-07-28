# Pyserini: Guide to Dense Indexes

## How do I index and search my own documents (Dense)?

Pyserini create dense index for collections with JSONL format:

```json
{
  "id": "doc1",
  "contents": "this is the contents."
}
```

A document is simply comprised of two fields, a `docid` and `contents`.
Pyserini accepts collections comprised of these documents organized in folder with files, each of which contains an array of JSON documents, like [this](integrations/resources/sample_collection_json_array).

So, the quickest way to get started is to write a script that converts your documents into the above format.
Then, you can invoke the indexer:

Here we provide an example to index collections with DPR passage encoder
```bash
python -m pyserini.dindex --corpus integrations/resources/sample_collection_jsonl \
                          --encoder facebook/dpr-ctx_encoder-multiset-base \
                          --index indexes/dindex-sample-dpr-multi \
                          --batch 64 \
                          --device cuda:0 \
                          --title-delimiter '\n' 
```

Once this is done, you can use `SimpleDenseSearcher` to search the index:
```python
from pyserini.dsearch import SimpleDenseSearcher

searcher = SimpleDenseSearcher(
    'indexes/dindex-sample-dpr-multi', 'facebook/dpr-question_encoder-multiset-base'
)
hits = searcher.search('what is a lobster roll')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')
```

If you want to speed up the passage embedding generation, you can run create the index in shard way.
e.g. the command below create a sub-index for the first 1/4 of the collection.
```bash
python -m pyserini.dindex --corpus integrations/resources/sample_collection_jsonl \
                          --encoder facebook/dpr-ctx_encoder-multiset-base \
                          --index indexes/dindex-sample-dpr-multi-0 \
                          --batch 64 \
                          --device cuda:0 \
                          --title-delimiter '\n' \ 
                          --shard-id 0 \
                          --shard-num 4
```
you can run 4 process on 4 gpu to speed up the process by 4 times.
Once it down, you can create the full index by merge the sub-indexes by:
```bash
python -m pyserini.dindex.merge_indexes --prefix indexes/dindex-sample-dpr-multi- --shard-num 4
```
