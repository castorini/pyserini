# miracl-v1.0-mdpr-tied-pft-msmarco-ft-miracl-${lang}

This index was generated on 2023/03/21 using [tevatron](https://github.com/texttron/tevatron) with the following commands:

## Create Train Directory

> **`create_train_dir.py`**
> ```python
> import json
> from pyserini.search.lucene import LuceneSearcher
> from datasets import load_dataset
> from random import shuffle
> from tqdm import tqdm
> 
> searcher = LuceneSearcher.from_prebuilt_index('miracl-v1.0-${lang}')
> searcher.set_language('${lang}')
> 
> miracl_train = load_dataset('miracl/miracl', '${lang}', split='train')
> with open('miracl_train_bm25_neg_top100_random30.${lang}.jsonl', 'w') as f:
>     for data in tqdm(miracl_train):
>         query = data['query']
>         positives = data['positive_passages']
>         negatives = data['negative_passages']
>         positive_ids = [p['docid'] for p in positives]
>         negative_ids = [p['docid'] for p in negatives]
>         hits = searcher.search(query, k=100)
>         bm25_negatives = []
>         for hit in hits:
>             info = json.loads(hit.raw)
>             if info['docid'] not in positive_ids and info['docid'] not in negative_ids:
>                 bm25_negatives.append(info)
>         all_negatives = negatives + bm25_negatives
>         shuffle(all_negatives)
>         random_30_negatives = all_negatives[:30]
>         data['negative_passages'] = random_30_negatives
>         if len(random_30_negatives) > 0:
>             f.write(json.dumps(data, ensure_ascii=False)+'\n')
> ```

```bash
python create_train_dir.py
```

## Train
```bash
CUDA_VISIBLE_DEVICES=0 python -m tevatron.driver.train \
  --output_dir model_miracl_${lang} \
  --model_name_or_path castorini/mdpr-tied-pft-msmarco \
  --tokenizer_name bert-base-multilingual-cased \
  --save_steps 20000 \
  --dataset_name Tevatron/msmarco-passage \
  --per_device_train_batch_size 64 \
  --train_dir miracl_train_bm25_neg_top100_random30.${lang}.jsonl \
  --train_n_passages 2 \
  --learning_rate 1e-5 \
  --q_max_len 32 \
  --p_max_len 256 \
  --num_train_epochs 40 \
  --logging_steps 10 \
  --overwrite_output_dir \
  --fp16
```

## Encode Corpus
```bash
CUDA_VISIBLE_DEVICES=0 python -m tevatron.driver.encode \
  --output_dir=temp_out \
  --model_name_or_path model_miracl_${lang} \
  --fp16 \
  --per_device_eval_batch_size 256 \
  --dataset_name miracl/miracl-corpus:${lang} \
  --p_max_len 256 \
  --encoded_save_path model_miracl_${lang}_corpus/${lang}_corpus_emb.pt 
```

## Convert Index

> #### **`convert_index.py`**
> ```python
> import numpy as np
> import faiss
> import pickle
> import os
> from tqdm import tqdm
> import argparse
> 
> parser = argparse.ArgumentParser()
> parser.add_argument('--input', type=str, required=True)
> parser.add_argument('--output', type=str, required=True)
> args = parser.parse_args()
> 
> def pickle_load(path):
>     with open(path, 'rb') as f:
>         reps, lookup = pickle.load(f)
>     return np.array(reps), lookup
> 
> index = faiss.IndexFlatIP(768)
> 
> all_ids = []
> for name in tqdm(os.listdir(args.input)):
>     if 'corpus_emb' not in name:
>         continue
>     path = os.path.join(args.input, name)
>     reps, ids = pickle_load(path)
>     all_ids.extend(ids)
>     index.add(reps)
> 
> faiss.write_index(index, f'{args.output}/index')
> with open(f'{args.output}/docid', 'w') as f:
>     for i in all_ids:
>         f.write(f'{i}\n')
> ```

```bash
python test.py --input=model_miracl_${lang}_corpus --output=${lang}_index
```


## Index from Pyserini
Tested to use the same checkpoint to index directly via Pyserini using the following command, got the same score. (on basilisk)
(only tested on Swahili)
```bash
encoder=castorini/mdpr-tied-pft-msmarco-ft-miracl-$lang

index_dir=miracl-v1.0-$lang-mdpr-tied-pft-msmarco-ft-miracl-$lang
echo $index_dir


CUDA_VISIBLE_DEVICES=1 \
python -m pyserini.encode   input   --corpus $corpus \
                                    --fields title text \
                                    --delimiter "\n\n" \
                                    --shard-id $shard_id \
                                    --shard-num $shard_num \
                            output  --embeddings  $index_dir \
                                    --to-faiss \
                            encoder --encoder $encoder \
                                    --fields title text \
                                    --batch 128 \
                                    --encoder-class 'auto' \
                                    --fp16
```
