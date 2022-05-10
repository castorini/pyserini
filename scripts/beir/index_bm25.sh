#mkdir -p indexes

#for corpora in arguana bioasq climate-fever dbpedia-entity fever hotpotqa nfcorpus quora robust04 scidocs scifact signal1m trec-covid trec-news webis-touche2020 fiqa nq
#do

#for corpora in android  english  gaming  gis  mathematica  physics  programmers  stats  tex  unix  webmasters  wordpress
#for corpora in fiqa # BeirFlatCollection
for corpora in msmarco
do
python -m pyserini.index -collection JsonCollection -generator DefaultLuceneDocumentGenerator \
	-threads 20 -input /store/scratch/y247xie/00_data/wp-tokenized/${corpora} \
	-index indexes/lucene-index-beir-${corpora} -storePositions -storeDocvectors -storeRaw -pretokenized
done
