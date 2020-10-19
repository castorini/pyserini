from pyserini.ltr import *
from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.search import get_topics_with_reader
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
import os
from lightgbm.sklearn import LGBMRanker
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
import argparse

def extract(df,analyzer):
    lines = []
    fetch_later = []
    for qid,group in tqdm(df.groupby('qid')):
        analyzed_query = analyzer.analyze(queries[qid]['title'])
        docids = [str(did) for did in group['pid'].drop_duplicates().tolist()]
        fe.lazy_extract(str(qid),analyzed_query,docids)
        fetch_later.append(str(qid))
        if len(fetch_later) == 1000:
            for qid in fetch_later:
                for doc in fe.get_result(qid):
                    lines.append((int(qid), int(doc['pid']), *doc['features']))
            fetch_later = []
    #deal with rest
    if len(fetch_later) > 0:
        for qid in fetch_later:
            for doc in fe.get_result(qid):
                lines.append((int(qid), int(doc['pid']), *doc['features']))
        fetch_later = []
    extracted = pd.DataFrame(lines, columns=['qid','pid']+fe.feature_names())
    return df.merge(extracted,how='inner',left_on=['qid','pid'],right_on=['qid','pid'])

def export(df, analyzer, fn):
    with open(fn,'w') as f:
        for qid,group in df.groupby('qid'):
            line = {}
            line['qid'] = qid
            line['queryTokens'] = analyzer.analyze(queries[qid]['title'])
            line['docIds'] = [str(did) for did in group['pid'].drop_duplicates().tolist()]
            f.write(json.dumps(line)+'\n')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Learning to rank')
    parser.add_argument('--default_feature', action='store_true', help="Use default features: AvgICTF,AvgIDF\
                        BM25,DocSize,MatchingTermCount,QueryLength,SCQ,SCS,SumMatchingTF,TFIDF,UniqueTermCount")
    parser.add_argument('--AvgICTF',  action='store_true', help="Use AvgICTF.")
    parser.add_argument('--AvgIDF',  action='store_true', help="Use AvgIDF")
    parser.add_argument('--BM25',  action='store_true', help="Use BM25")
    parser.add_argument('--DocSize', action='store_true', help="Use DocSize")
    parser.add_argument('--MatchingTermCount',  action='store_true', help="Use MatchingTermCount")
    parser.add_argument('--QueryLength',  action='store_true', help="Use QueryLength")
    parser.add_argument('--SCQ',  action='store_true', help="Use SCQ")
    parser.add_argument('--SCS',  action='store_true', help='Use SCS')
    parser.add_argument('--SumMatchingTF',  action='store_true', help="Use SumMatchingTF")
    parser.add_argument('--UniqueTermCount',  action='store_true', help="Use UniqueTermCount")
    args = parser.parse_args()

    fe = FeatureExtractor('indexes/msmarco-passage/lucene-index-msmarco/', 20)
    if args.default_feature:

        fe.add(BM25(k1=0.9,b=0.4))
        fe.add(BM25(k1=1.2,b=0.75))
        fe.add(BM25(k1=2.0,b=0.75))
        fe.add(LMDir(mu=0))
        fe.add(LMDir(mu=1000))
        fe.add(LMDir(mu=1500))
        fe.add(LMDir(mu=2500))
        fe.add(DFR_GL2())
        fe.add(DFR_In_expB2())
        fe.add(AvgICTF())
        fe.add(AvgIDF())
        fe.add(DocSize())
        fe.add(MatchingTermCount())
        fe.add(QueryLength())
        fe.add(AvgSCQ())
        fe.add(SCS())
        fe.add(SumMatchingTF())
        fe.add(UniqueTermCount())
        fe.add(UnorderedSequentialPairs(3))
        fe.add(UnorderedSequentialPairs(5))
        fe.add(UnorderedSequentialPairs(8))
        fe.add(OrderedSequentialPairs(3))
        fe.add(OrderedSequentialPairs(5))
        fe.add(OrderedSequentialPairs(8))
    else:
        if args.AvgICTF:
            fe.add(AvgICTF())
        if args.AvgIDF:
            fe.add(AvgIDF())
        if args.BM25:
            fe.add(BM25())
        if args.DocSize:
            fe.add(DocSize())
        if args.MatchingTermCount:
            fe.add(MatchingTermCount())
        if args.QueryLength:
            fe.add(QueryLength())
        if args.SCQ:
            fe.add(AvgSCQ())
        if args.SCS:
            fe.add(SCS())
        if args.SumMatchingTF:
            fe.add(SumMatchingTF())
        if args.UniqueTermCount:
            fe.add(UniqueTermCount())

    analyzer = Analyzer(get_lucene_analyzer())
    queries = get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader',\
                                 'collections/msmarco-passage/queries.train.tsv')
    queries.update(get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader',\
                                    'collections/msmarco-passage/queries.dev.tsv'))

    train = pd.read_csv('collections/msmarco-passage/qidpidtriples.train.full.tsv', sep="\t",
                        names=['qid', 'pos_pid', 'neg_pid'])
    pos_half = train[['qid', 'pos_pid']].rename(columns={"pos_pid": "pid"}).drop_duplicates()
    pos_half['rel'] = 1
    neg_half = train[['qid', 'neg_pid']].rename(columns={"neg_pid": "pid"}).drop_duplicates()
    neg_half['rel'] = 0
    del train
    sampled_neg_half = []
    for qid, group in tqdm(neg_half.groupby('qid')):
        sampled_neg_half.append(group.sample(n=min(10, len(group)), random_state=12345))
    sampled_train = pd.concat([pos_half] + sampled_neg_half, axis=0, ignore_index=True)
    del pos_half, neg_half, sampled_neg_half

    print(sampled_train.shape)
    print(sampled_train.qid.drop_duplicates().shape)
    print(sampled_train.groupby('qid').count().mean()['pid'])
    print(sampled_train.head(10))

    dev = pd.read_csv('collections/msmarco-passage/top1000.dev', sep="\t",
                      names=['qid', 'pid', 'query', 'doc'], usecols=['qid', 'pid'])
    dev_qrel = pd.read_csv('collections/msmarco-passage/qrels.dev.small.tsv', sep="\t",
                           names=["qid", "q0", "pid", "rel"], usecols=['qid', 'pid', 'rel'])
    dev = dev.merge(dev_qrel, left_on=['qid', 'pid'], right_on=['qid', 'pid'], how='left')
    dev['rel'] = dev['rel'].fillna(0).astype(np.int)
    del dev_qrel

    print(dev.shape)
    print(dev.qid.drop_duplicates().shape)
    print(dev.groupby('qid').count().mean()['pid'])
    print(dev.head(10))

    train_data=extract(sampled_train,analyzer)
    dev_data=extract(dev,analyzer)

    model = LGBMRanker(objective='lambdarank', random_state=12345)

    feature_name = fe.feature_names()
    train_data = train_data.sort_values(by='qid', kind='mergesort')
    train_X = train_data.loc[:, feature_name]
    train_Y = train_data['rel']
    train_group = train_data.groupby('qid').agg(count=('pid', 'count'))['count']

    dev_data = dev_data.sort_values(by='qid', kind='mergesort')
    dev_X = dev_data.loc[:, feature_name]
    dev_Y = dev_data['rel']
    dev_group = dev_data.groupby('qid').agg(count=('pid', 'count'))['count']

    model.fit(train_X, train_Y, group=train_group)
    dev_data['score'] = model.predict(dev_X)
    print(model.feature_importances_)

    model = LogisticRegression(solver='saga')
    scaler = StandardScaler()
    train_X = scaler.fit_transform(train_X.iloc[:,:9].values)
    train_Y = train_data['rel'].values

    dev_X = scaler.transform(dev_data.iloc[:,:9].values)
    dev_Y = dev_data['rel'].values

    model.fit(train_X, train_Y)
    dev_data['score'] += model.predict(dev_X)*0.01
    print(model.coef_[:])

    with open('lambdarank.run','w') as f:
        score_tie_counter = 0
        score_tie_query = set()
        for qid, group in dev_data.groupby('qid'):
            rank = 1
            prev_score = -1e10
            prev_pid = ''
            assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
            # stable sort is also used in LightGBM
            for t in group.sort_values('score',ascending=False,kind='mergesort').itertuples():
                if abs(t.score-prev_score)<1e-8:
                    score_tie_counter+=1
                    score_tie_query.add(qid)
                assert prev_pid != t.pid
                prev_score = t.score
                prev_pid = t.pid
                f.write(f'{t.qid}\t{t.pid}\t{rank}\n')
                rank += 1
        if score_tie_counter>0:
            print(f'score_tie occurs {score_tie_counter} times in {len(score_tie_query)} queries')

    with open('lambdarank.run.trec','w') as f:
        for qid, group in dev_data.groupby('qid'):
            rank = 1
            assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
            # stable sort is also used in LightGBM
            for t in group.sort_values('score',ascending=False,kind='mergesort').itertuples():
                new_score = t.score - rank*1e-6
                f.write(f'{t.qid}\tQ0\t{t.pid}\t{rank}\t{new_score:.6f}\tlambdarank\n')
                rank+=1

    os.system("python3 tools/scripts/msmarco/msmarco_eval.py collections/msmarco-passage/qrels.dev.small.tsv lambdarank.run")
    os.system("tools/eval/trec_eval.9.0.4/trec_eval -m all_trec collections/msmarco-passage/qrels.dev.small.tsv lambdarank.run.trec | egrep '^map\s|recall_1000'")

