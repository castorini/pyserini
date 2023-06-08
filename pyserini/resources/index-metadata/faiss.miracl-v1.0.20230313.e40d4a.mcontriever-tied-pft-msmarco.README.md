# miracl-v1.0-mdpr-tied-pft-msmarco-ft-miracl-${lang}

This index was generated on 2023/03/13 on commit 20230313. 

## Index from Pyserini
```bash
lang=ar # or any lang abbreviation

encoder=facebook/mcontriever-msmarco
index_dir=faiss.miracl-v1.0-$lang.mcontriever-tied-pft-msmarco.20230313.e40d4a
echo $index_dir

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
                                    --encoder-class contriever \
                                    --fp16
```

## To use as Search
```
index=
output=run.miracl.mdpr-tied-pft-msmarco.$lang.dev.txt 

python -m pyserini.search.faiss \
    --encoder-class contriever \
    --encoder facebook/mcontriever-msmarco \
    --topics miracl-v1.0-$lang-dev \
    --index miracl-v1.0-$lang-mcontriever-pft-msmarco \
    --output $output \
    --batch 128 --threads 16 --hits 100
```


python -m pyserini.search.faiss --encoder-class contriever --encoder facebook/mcontriever-msmarco --topics miracl-v1.0-$lang-dev --index miracl-v1.0-$lang-mcontriever-pft-msmarco --output $output --batch 128 --threads 16 --hits 100