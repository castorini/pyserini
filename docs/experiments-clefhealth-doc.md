# Pyserini: BM25 Baseline for CLEF Health Document Retrieval

This guide contains instructions for running BM25 baselines on the [CLEF eHealth Lab Series Adhoc Information Retrieval](https://clefehealth.imag.fr/?page_id=610).

## Data Prep

The guide requires the [development installation](https://github.com/castorini/pyserini/#development-installation) for additional resource that are not shipped with the Python module; for the (more limited) runs that directly work from the Python module installed via `pip`, see [this guide](pypi-reproduction.md).

We're going to use the repository's root directory as the working directory.
First, we need to download and extract the CLEF document dataset:

```
mkdir collections/clef_health
wget -c https://www.dropbox.com/s/ixnqt33u5xeelth/clef2018collection.tar.gz -P collections/clef_health
```

There's is a need to decompress the file as the corpus is not in proper answerini format. Its worth noting that the full corpus is over 500gb and needs to be convered to answerini format so make sure your machine has at least 1tb of free space.
```bash
tar -xf clef2018collection.tar.gz
```
Since the CLEF dataset is not in Answerini format you need to conver it using [a simple conversion script](https://github.com/spacemanidol/pyserini/blob/master/scripts/convert_clef_to_pyserini.py) which is run like this:
```bash
mkdir collections/clef_health_processed 
python convert_clef_to_pyserini.py --input_dir collections/clef_health --output_dir collections/clef_health_processed
wc -l collections/clef_health_processed/*
```

Build the index with the following command:

```
python -m pyserini.index -collection CleanTrecCollection \
 -generator DefaultLuceneDocumentGenerator -threads 1 -input collections/clef_health_processed/ \
 -index indexes/lucene-index-clef-health-doc -storePositions -storeDocvectors -storeRaw
```

Note that the indexing program simply dispatches command-line arguments to an underlying Java program, and so we use the Java single dash convention, e.g., `-index` and not `--index`.

On a modern desktop with an SSD, indexing takes a few hours.
There should be a total of 5,379,303 documents indexed.

## Performing Retrieval on the Dev Queries

The 50 queries from the 2018 task which we can evaluate on. These queries are in xml format

```bash
$ head tools/topics-and-qrels/CLEF2018queries.xml 
<queries>
	<query>
		<id> 151001 </id>
		<en> anemia diet therapy </en>
	</query>
	<query>
		<id> 152001 </id>
		<en> emotional and mental disorders </en>
	</query>
	<query>
$ wc tools/topics-and-qrels/CLEF2018queries.xml 
 201  580 4186 tools/topics-and-qrels/CLEF2018queries.xml
```

Once you load the queries, search is straightforward.
```python
from pyserini.search import SimpleSearcher
import xml.etree.ElementTree as ET

def load_queries(filename):
    qid2query = {}
    tree = ET.parse(filename)
    root = tree.getroot()
    for query in root:
        query_id = 0
        query_text = ''
        for child in query:
            if child.tag == 'id':
                query_id = int(child.text[1:-1])
            if child.tag == 'en':
                query_text = child.text
        if query_id != 0 and query_text != '':
            qid2query[query_id] = query_text
    return qid2query

qid2query = load_queries('tools/topics-and-qrels/CLEF2018queries.xml')
searcher = SimpleSearcher('indexes/lucene-index-clef-health-doc')
with open('pyserini-clefhealth.run','w') as w:
  for qid in qid2query:
    results = searcher.search(qid2query[qid])
    for result in results:
                w.write("{} Q0 {} {} {} pyserini\n".format(qid, result.docid, i, result.score))
```

Once this is done you can evaluate using pyserini's trec_eval and reproduce these results
```bash
python -m pyserini.eval.trec_eval -m ndcg tools/topics-and-qrels/CLEF2018_qtrust_20180914.txt test.run 
Results:
ndcg                  	all	0.0540
```

## Reproduction Log[*](reproducibility.md)
