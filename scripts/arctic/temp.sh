mv ArguAna faiss-flat.beir-v1.0.0-arguana.arctic-embed-m-v1.5.20241031
tar -zcvf faiss-flat.beir-v1.0.0-arguana.arctic-embed-m-v1.5.20241031.tar.gz faiss-flat.beir-v1.0.0-arguana.arctic-embed-m-v1.5.20241031

items=('ArguAna' 'CQADupstackAndroidRetrieval' 'CQADupstackEnglishRetrieval' 'CQADupstackGamingRetrieval' 
       'CQADupstackGisRetrieval' 'CQADupstackMathematicaRetrieval' 'CQADupstackPhysicsRetrieval' 
       'CQADupstackProgrammersRetrieval' 'CQADupstackStatsRetrieval' 'CQADupstackTexRetrieval' 
       'CQADupstackUnixRetrieval' 'CQADupstackWebmastersRetrieval' 'CQADupstackWordpressRetrieval' 
       'ClimateFEVER' 'DBPedia' 'FEVER' 'FiQA2018' 'HotpotQA' 'MSMARCO' 'NFCorpus' 'NQ' 
       'QuoraRetrieval' 'SCIDOCS' 'SciFact' 'TRECCOVID' 'Touche2020')
topics=('arguana' 'cqadupstack-android' 'cqadupstack-english' 'cqadupstack-gaming' 'cqadupstack-gis' 
        'cqadupstack-mathematica' 'cqadupstack-physics' 'cqadupstack-programmers' 'cqadupstack-stats'
        'cqadupstack-tex' 'cqadupstack-unix' 'cqadupstack-webmasters' 'cqadupstack-wordpress' 'climate-fever'
        'dbpedia-entity' 'fever' 'fiqa' 'hotpotqa' 'msmarco' 'nfcorpus' 'nq' 'quora' 'scidocs' 'scifact' 
        'trec-covid' 'webis-touche2020')

for i in "${!items[@]}"; do
  echo "${items[$i]} - ${topics[$i]}"
  folder=${items[$i]}
  topic=${topics[$i]}
  mv $folder faiss-flat.beir-v1.0.0-$topic.arctic-embed-m-v1.5.20241031
  tar -zcvf faiss-flat.beir-v1.0.0-$topic.arctic-embed-m-v1.5.20241031.tar.gz faiss-flat.beir-v1.0.0-$topic.arctic-embed-m-v1.5.20241031
done