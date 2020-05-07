# Working with the [COVID-19 Open Research Dataset](https://pages.semanticscholar.org/coronavirus-research)

This document describes various tools for working with the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research) from the [Allen Institute for AI](https://allenai.org/).

The latest distribution available is from 2020/05/01.
First, download the data:

```bash
DATE=2020-05-01
DATA_DIR=./cord19-"${DATE}"
mkdir "${DATA_DIR}"

wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/comm_use_subset.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/noncomm_use_subset.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/custom_license.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/biorxiv_medrxiv.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/arxiv.tar.gz -P "${DATA_DIR}"
wget https://ai2-semanticscholar-cord-19.s3-us-west-2.amazonaws.com/latest/metadata.csv -P "${DATA_DIR}"

ls "${DATA_DIR}"/*.tar.gz | xargs -I {} tar -zxvf {} -C "${DATA_DIR}"
# If the above doesn't work due to cross-OS compatibility issues with xargs, untar all folders individually
# tar -zxvf "${DATA_DIR}"/comm_use_subset.tar.gz -C "${DATA_DIR}"
# tar -zxvf "${DATA_DIR}"/noncomm_use_subset.tar.gz -C "${DATA_DIR}"
# tar -zxvf "${DATA_DIR}"/custom_license.tar.gz -C "${DATA_DIR}"
# tar -zxvf "${DATA_DIR}"/biorxiv_medrxiv.tar.gz -C "${DATA_DIR}"
# tar -zxvf "${DATA_DIR}"/arxiv.tar.gz -C "${DATA_DIR}"
```


```
from pyserini.collection import pycollection

collection = pycollection.Collection('Cord19AbstractCollection', 'cord19-2020-05-01')

cnt = 0;
full_text = {True : 0, False: 0}

articles = collection.__next__()
for (i, d) in enumerate(articles):
    article = pycollection.Cord19Article(d.raw)
    cnt = cnt + 1
    full_text[article.is_full_text()] += 1
    if cnt % 1000 == 0:
        print(f'{cnt} articles read...')
```

```
from pyserini.collection import pycollection

collection = pycollection.Collection('Cord19AbstractCollection', 'cord19-2020-05-01')

articles = collection.__next__()
article = None
for (i, d) in enumerate(articles):
    article = pycollection.Cord19Article(d.raw)
    if article.is_full_text():
       break

article.cord_uid()
article.is_full_text()
article.metadata()
article.title()
article.abstract()
len(article.body())
```
