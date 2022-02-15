This index was generated on 2022/02/07 at commit [5df364](https://github.com/castorini/pyserini/commit/5df3649b128ece125ce8a9171ed4001ce3a6ef23) on narval with the following command:
(manually change the delimiter in encoding from \n into \n\n).

```bash
lang=japanese

tarfn=mrtydi-v1.1-$lang.tar.gz
encoder=models/mdpr-context-encoder
corpus=mrtydi-v1.1-$lang/collection/docs.jsonl
index_dir=mrtydi-mdpr-dindex/$lang

wget https://git.uwaterloo.ca/jimmylin/mr.tydi/-/raw/master/data/$tarfn
tar –xvf $tarfn
gzip -cvf $corpus.gz > $corpus

mkdir -p $index_dir

python -m pyserini.encode   input   --corpus $corpus \
                                    --fields title text \
                                    --delimiter "\n\n" \
                            output  --embeddings  $index_dir \
                                    --to-faiss \
                            encoder --encoder $encoder \
                                    --fields title text \
                                    --batch 128 \
                                    --fp16
``` 

which can be dsearched using:
```bash
set_name=test
python -m pyserini.dsearch \
  --encoder castorini/mdpr-question-nq \
  --topics mrtydi-v1.1-${lang}-${set_name} \
  --index ${index_dir} \
  --output runs/run.mrtydi-v1.1-$lang.${set_name}.txt
  --batch-size 36 \
  --threads 12
```