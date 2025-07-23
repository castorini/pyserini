# BRIGHT

The Lucene inverted indexes for BRIGHT were generated on 2025/07/05 at Anserini commit [`44ae8e`](https://github.com/castorini/anserini/commit/44ae8e487760a2cd21bdcdb11e18735e46606a86) on `orca` with the following commands:

```bash
#!/bin/bash

for c in biology earth-science economics psychology robotics stackoverflow sustainable-living pony leetcode aops theoremqa-theorems theoremqa-questions
do

bin/run.sh  io.anserini.index.IndexCollection \
  -threads 16 \
  -collection JsonCollection \
  -input collections/bright/${c}/  \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/bright/lucene-inverted.bright-$c.20250705.44ae8e \
  -storePositions -storeDocvectors -storeRaw -optimize

done
```

Documents were generated with the following Python script:

```python
from datasets import load_dataset
import json
from tqdm import tqdm
import os

bright_corpus = load_dataset("xlangai/BRIGHT", 'documents')
splits = list(bright_corpus.keys())
print(splits)

for split in splits:
    exist_docids = set()
    os.makedirs(f'collections/bright/{split}', exist_ok=True)
    corpus = bright_corpus[split]
    print(split)
    with open(f'collections/bright/{split}/{split}.jsonl', 'w') as f:
        for doc in tqdm(corpus):
            id_ = doc['id']
            # replace spaces with underscores
            id_ = id_.replace(' ', '_')
            contents = doc['content']
            if id_ in exist_docids:
                print(f'Duplicate document id found: {id_}')
                continue
            exist_docids.add(id_)
            f.write(json.dumps({'id': id_, 'contents': contents}) + '\n')
```

The processed documents can be found on Hugging Face [here](https://huggingface.co/datasets/castorini/collections-bright). 