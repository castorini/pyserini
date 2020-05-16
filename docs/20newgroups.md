# 20 Newsgroup Replication

From root path, run the following:
```
# download the pre-process dataset & lucene index
sh scripts/get-20newsgroup-data.sh
# train classifier
python bin/20newsgroup-replication.py
```

You should get a score of `0.8099420314961255`.
