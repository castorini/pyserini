# BRIGHT

The Lucene inverted indexes for M-BEIR were generated on 2025/12/24 at Anserini commit [`1c5cd3`](https://github.com/castorini/anserini/commit/1c5cd32b48f03f63eb5752834600ad7c17e5fe7d) on `basilisk` with the following commands:

```bash
#!/bin/bash

for c in cirr_task7 fashioniq_task7 oven_task6 webqa_task1 edis_task2 infoseek_task6 mscoco_task3 oven_task8 webqa_task2 fashion200k_task0 infoseek_task8 visualnews_task0 fashion200k_task3 mscoco_task0 nights_task4 visualnews_task3
do

bin/run.sh  io.anserini.index.IndexCollection \
  -threads 16 \
  -collection JsonCollection \
  -input collections/m-beir/${c} /  \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/m-beir/lucene-inverted.m-beir-$c.20251224.1c5cd3 \
  -storePositions -storeDocvectors -storeRaw -optimize

done
```

Documents were generated with the following Python script:

```python
import json
import os
import glob

input_dir = 'collections/m-beir'
output_dir = 'collections/m-beir/lucene-format'
os.makedirs(output_dir, exist_ok=True)

for input_file in glob.glob(os.path.join(input_dir, 'mbeir_*_cand_pool.jsonl')):
    filename = os.path.basename(input_file)
    dataset_name = filename[6:-16]
    output_file = os.path.join(output_dir, f'{dataset_name}_multimodal.jsonl')
    
    with open(input_file) as infile, open(output_file, 'w') as outfile:
        for line in infile:
            doc = json.loads(line)
            combined = {
                "id": doc["did"],
                "contents": f"{doc.get('txt', '')} IMAGE_PATH:{doc.get('img_path', None)}",
                "img_path": doc.get("img_path", None),
                "modality": doc["modality"],
            }
            outfile.write(json.dumps(combined) + '\n')
```
