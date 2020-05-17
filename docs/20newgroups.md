# 20 Newsgroup Replication

Download the pre-process dataset & lucene index
```
sh bin/get-20newsgroups-data.sh
```

Train classifier
```
python scripts/20newsgroups-replication.py
```

You should get a score of `0.8099420314961255`.
