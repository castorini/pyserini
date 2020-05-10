# Working with the COVID-19 Open Research Dataset

This page describes how to use Pyserini's Collection API to work with the [COVID-19 Open Research Dataset (CORD-19)](https://pages.semanticscholar.org/coronavirus-research) from the [Allen Institute for AI](https://allenai.org/).
This API provides access to the raw collection, independent of search.
If you want to actually search the collection, consult [this guide](https://github.com/castorini/anserini/blob/master/docs/experiments-cord19.md).

## Data Prep

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

## Collection Access

The follow snippet of code allows you to iterate through all articles in the collection (note that although we use the `Cord19AbstractCollection`, `raw` _does_ provide access to the entire full-text:

```python
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

The above snippet of code tallies the number of full-text articles in the collection.

CORD-19 comes in two parts, `metadata.csv` and the actual full-text JSON (if available).
What this code gives you is a JSON that has both integrated, along with a bunch of convenience methods.
For full-text articles, i.e., `is_full_text()` returns `True`, the metadata are provided with the `metadata()` method.
For articles without full text, only the metadata are available.

Let's examine the first full-text article in the collection:

```python
from pyserini.collection import pycollection

# All this snippet of code does is to advance to the frist full-text article:
collection = pycollection.Collection('Cord19AbstractCollection', 'cord19-2020-05-01')

articles = collection.__next__()
article = None
for (i, d) in enumerate(articles):
    article = pycollection.Cord19Article(d.raw)
    if article.is_full_text():
       break

# Now article contains the first full-text article.

# Let's print basic information:
print(f'cord_uid {article.cord_uid()}, full-text? {article.is_full_text()}')
print(f'title: {article.title()}')
print(f'abstract: {article.abstract()}')

# We can fetch the matadata:
metadata = article.metadata()

# For example, the DOI:
print(f'DOI: {metadata["doi"]}')

# The body() method returns an array of str corresponding to the full text.
print(f'The full text contains {len(article.body())} paragraphs')

# If you really want to manipulate the raw JSON:
article.json
```

For an article that does not contain full text, all the above methods behave the same way, except that `body()` returns an empty array.
