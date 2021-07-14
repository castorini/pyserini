# Pyserini: Guide to Encoding a Collection into Vectors

## How do I encode my own documents?

### Prepare collection
The input should be in JSONL format. 
Each line is a json dictionary containing two fields, i.e .`id` and `contents`.
- `id` is the document id in string.
- `contents` contains all the fields of the documents. fields in contents are separated by `\n` 
```json
{
  "id": "doc1",
  "contents": "www.url.com\ntitle\nthis is the contents.\ndocument expansion"
}
```
In our example, each document has two fields in contents `text` and `expand`

### Encode documents with Dense encoder
```
python -m pyserini.encode input   --corpus msmarco-passage-expanded \
                                  --fields url title text expand \  # fields in collection contents
                          output  --embeddings path/to/output/dir \
                          encoder --encoder castorini/tct_colbert-v2-hnp-msmarco \
                                  --fields title text \  # fields to encode
                                  --batch 32 \
                                  --fp16  # if inference with autocast()
```
> with `--to-faiss`, the generated embeddings will be stored as FaissIndexIP directly.
> It will be stored in jsonl without `--to-faiss`

If in jsonl format, each line contains following info:
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
