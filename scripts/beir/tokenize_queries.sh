for corpora in arguana bioasq climate-fever dbpedia-entity fever fiqa hotpotqa nfcorpus quora robust04 scidocs scifact signal1m trec-covid trec-news webis-touche2020 
do

#for corpora in android  english  gaming  gis  mathematica  physics  programmers  stats  tex  unix  webmasters  wordpress
#do
#for corpora in nq
#do
#mkdir -p /store/scratch/y247xie/00_data/wp-tokenized/${corpora}/
#mkdir -p /store/scratch/y247xie/00_data/wp-tokenized/cqadupstack/${corpora}
#python tokenize_corpus.py \
#	--input /store/collections/beir-v1.0.0/original/${corpora}/corpus.jsonl \
#	--output /store/scratch/y247xie/00_data/wp-tokenized/${corpora}/corpus.jsonl
#python tokenize_corpus.py \
#	--input /store/collections/beir-v1.0.0/original/cqadupstack/${corpora}/corpus.jsonl \
#	--output /store/scratch/y247xie/00_data/wp-tokenized/cqadupstack/${corpora}/corpus.jsonl
python tokenize_queries.py \
	--input /store/collections/beir-v1.0.0/original/${corpora}/queries.jsonl \
	--output /store/scratch/y247xie/00_data/wp-tokenized/${corpora}/queries.jsonl

done

for corpora in android  english  gaming  gis  mathematica  physics  programmers  stats  tex  unix  webmasters  wordpress
do
python tokenize_queries.py \
	--input /store/collections/beir-v1.0.0/original/cqadupstack/${corpora}/queries.jsonl \
	 --output /store/scratch/y247xie/00_data/wp-tokenized/cqadupstack/${corpora}/queries.jsonl
done

for corpora in nq
do
python tokenize_queries.py \
	--input /store/scratch/y247xie/00_data/nq/queries.jsonl \
	--output /store/scratch/y247xie/00_data/wp-tokenized/${corpora}/queries.jsonl
done



	
