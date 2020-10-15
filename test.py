from pyserini.ltr import FeatureExtractor, AvgICTF, AvgIDF, BM25, DocSize, MatchingTermCount, \
    PMI, QueryLength, SCQ, SCS, SumMatchingTF, TFIDF, UniqueTermCount
from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.search import get_topics_with_reader
import pandas as pd
import numpy as np
from tqdm import tqdm
import json
from lightgbm.sklearn import LGBMRegressor
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import LinearSVC
import argparse

def extract(df,analyzer):
    lines = []
    fetch_later = []
    for qid,group in df.groupby('qid'):
        analyzed_query = analyzer.analyze(queries[qid]['title'])
        docids = [str(did) for did in group['pid'].drop_duplicates().tolist()]
        fe.lazy_extract(str(qid),analyzed_query,docids)
        fetch_later.append(str(qid))
        if len(fetch_later) == 1000:
            for qid in tqdm(fetch_later):
                for doc in fe.get_result(qid):
                    lines.append((int(qid), int(doc['pid']), *doc['features']))
            fetch_later = []
    #deal with rest
    if len(fetch_later) > 0:
        for qid in tqdm(fetch_later):
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
    parser.add_argument('--TFIDF',  action='store_true', help="Use TFIDF")
    parser.add_argument('--UniqueTermCount',  action='store_true', help="Use UniqueTermCount")
    parser.add_argument('--PMI',  action='store_true', help="Use PMI")
    args = parser.parse_args()

    fe = FeatureExtractor('indexes/msmarco-passage/lucene-index-msmarco/', 20)
    if args.default_feature:
        fe.add(AvgICTF())
        fe.add(AvgIDF())
        fe.add(BM25())
        fe.add(DocSize())
        fe.add(MatchingTermCount())
        fe.add(QueryLength())
        fe.add(SCQ())
        fe.add(SCS())
        fe.add(SumMatchingTF())
        fe.add(TFIDF())
        fe.add(UniqueTermCount())
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
            fe.add(SCQ())
        if args.SCS:
            fe.add(SCS())
        if args.SumMatchingTF:
            fe.add(SumMatchingTF())
        if args.TFIDF:
            fe.add(TFIDF())
        if args.UniqueTermCount:
            fe.add(UniqueTermCount())
        if args.PMI:
            fe.add(PMI())
    analyzer = Analyzer(get_lucene_analyzer())
    queries = get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader',\
                                 'collections/msmarco-passage/queries.train.tsv')
    queries.update(get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader',\
                                    'collections/msmarco-passage/queries.dev.tsv'))

    train = pd.read_csv('collections/msmarco-passage/qidpidtriples.train.full.tsv',sep="\t",
                     names=['qid','pos_pid','neg_pid'])
    pos_half = train[['qid','pos_pid']].rename(columns={"pos_pid": "pid"})
    pos_half['rel'] = 1.
    neg_half = train[['qid','neg_pid']].rename(columns={"neg_pid": "pid"})
    neg_half['rel'] = 0.
    train = pd.concat([pos_half,neg_half],axis=0,ignore_index=True)
    del pos_half, neg_half
    sampled_train=train.sample(frac=0.01,random_state=123456)

    print(sampled_train.shape)
    print(sampled_train.qid.drop_duplicates().shape)
    print(sampled_train.groupby('qid').count().mean()['pid'])
    print(sampled_train.head(10))

    dev = pd.read_csv('collections/msmarco-passage/top1000.dev',sep="\t",
                    names=['qid','pid','query','doc'], usecols=['qid','pid'])
    sampled_dev_qid=pd.Series(dev['qid'].unique()).sample(n=500,random_state=123456)
    sampled_dev = dev[dev['qid'].isin(sampled_dev_qid)].reset_index(drop=True).copy(deep=True)
    del dev
    dev_qrel=pd.read_csv('collections/msmarco-passage/qrels.dev.small.tsv', sep="\t", names=["qid","q0","pid","rel"])
    dev_qrel[dev_qrel['qid'].isin(sampled_dev_qid)].to_csv('collections/msmarco-passage/qrels.dev.500.tsv', sep='\t', header=False, index=False)

    print(sampled_dev.shape)
    print(sampled_dev.qid.drop_duplicates().shape)
    print(sampled_dev.groupby('qid').count().mean()['pid'])
    print(sampled_dev.head(10))

    train_data=extract(sampled_train,analyzer)
    dev_data=extract(sampled_dev,analyzer)
    model = LGBMRegressor(random_state=12345)
    # model = LogisticRegression()
    # model = RandomForestRegressor()
    # model = LinearSVC()
    train_X = train_data.loc[:,fe.feature_names()].values
    train_Y = train_data.loc[:,'rel'].values
    model.fit(train_X, train_Y)  

    dev_X = dev_data.loc[:,fe.feature_names()].values
    dev_data['score'] = model.predict(dev_X)

    with open('lambdarank.run','w') as f:
        score_tie_counter = 0
        score_tie_query = set()
        for qid, group in tqdm(dev_data.groupby('qid')):
            rank = 1
            prev_score = -1e10
            prev_pid = ''
            assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
            for t in group.sort_values(['score','pid'],ascending=False).itertuples():
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

os.system("python3 tools/scripts/msmarco/msmarco_eval.py collections/msmarco-passage/qrels.dev.500.tsv lambdarank.run")

    with open('lambdarank.run.trec','w') as f:
        for qid, group in tqdm(dev_data.groupby('qid')):
            rank = 1
            assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
            for t in group.sort_values(['score','pid'],ascending=False).itertuples():
                new_score = t.score - rank*1e-6
                f.write(f'{t.qid}\tQ0\t{t.pid}\t{rank}\t{new_score:.6f}\tlambdarank\n')
                rank+=1
    
os.system("tools/eval/trec_eval.9.0.4/trec_eval -m all_trec collections/msmarco-passage/qrels.dev.500.tsv lambdarank.run.trec | egrep '^map\s|recall_1000'")

