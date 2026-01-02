# M-BEIR

The Lucene inverted indexes for M-BEIR were generated on 2025/12/27 at Anserini commit [`1c5cd3`](https://github.com/castorini/anserini/commit/1c5cd32b48f03f63eb5752834600ad7c17e5fe7d) on `basilisk` with the following commands:

**Important:** This index is intended for accessing raw document content. It is not designed for embedding-based retrieval, as images are converted to text, which compromises their usefulness for visual similarity searches.

```bash
#!/bin/bash

for c in cirr_task7 fashioniq_task7 oven_task6 webqa_task1 edis_task2 infoseek_task6 mscoco_task3 oven_task8 webqa_task2 fashion200k_task0 infoseek_task8 visualnews_task0 fashion200k_task3 mscoco_task0 nights_task4 visualnews_task3
do

bin/run.sh io.anserini.index.IndexCollection \
  -threads 16 \
  -collection JsonCollection \
  -input collections/m-beir/${c} /  \
  -generator DefaultLuceneDocumentGenerator \
  -index indexes/m-beir/lucene-inverted.m-beir-$c.20251227.1c5cd3 \
  -storePositions -storeDocvectors -storeRaw -optimize

done
```

Documents were generated with the following Python script:

```python
import os
import glob
import base64
import json

input_dir = 'collections/m-beir'
output_root = 'collections/m-beir/lucene-format'
images_path = "put your path here" # For basilisk server, can use "/mnt/users/s8sharif/M-BEIR/" as path

os.makedirs(output_root, exist_ok=True)

for input_file in glob.glob(os.path.join(input_dir, 'mbeir_*_cand_pool.jsonl')):
    filename = os.path.basename(input_file)

    dataset_name = filename[6:-16]

    dataset_dir = os.path.join(output_root, dataset_name)
    os.makedirs(dataset_dir, exist_ok=True)

    output_file = os.path.join(dataset_dir, f'{dataset_name}_multimodal.jsonl')

    with open(input_file) as infile, open(output_file, 'w') as outfile:
        for line in infile:
            doc = json.loads(line)

            encoded_img = None
            if doc.get("img_path"):
                actual_path = os.path.join(sahels_images, doc["img_path"])

                if os.path.exists(actual_path):
                    with open(actual_path, "rb") as f:
                        encoded_img = base64.b64encode(f.read()).decode("utf-8")

            combined = {
                "id": doc["did"],
                "contents": f"{doc.get('txt', '')}",
                "img_path": doc.get("img_path", None),
                "encoded_img": encoded_img,
                "modality": doc["modality"],
            }

            outfile.write(json.dumps(combined) + '\n')
```
