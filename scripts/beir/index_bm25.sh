mkdir -p indexes

for corpora in arguana bioasq climate-fever dbpedia-entity fever hotpotqa nfcorpus quora robust04 scidocs scifact signal1m trec-covid trec-news webis-touche2020
#for corpora in fiqa
do

python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
	-threads 20 -input /store/scratch/y247xie/00_data/wp-tokenized-anserini/${corpora}/corpus \
	-index indexes/lucene-index-beir-${corpora} -storePositions -storeDocvectors -storeRaw
done
