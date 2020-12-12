import argparse
import datetime
import glob
import hashlib
import json
import multiprocessing
import pickle
import os
import shutil
import subprocess
import uuid

import numpy as np
import pandas as pd
import lightgbm as lgb
from collections import defaultdict
from tqdm import tqdm

from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.ltr import *
from pyserini.search import get_topics_with_reader


def dev_data_loader(file, format):
    if format == 'tsv':
        dev = pd.read_csv(file, sep="\t",
                          names=['qid', 'pid', 'rank'], dtype=np.int32)
    elif format == 'trec':
        dev = pd.read_csv(file, sep="\s+",
                    names=['qid', 'q0', 'pid', 'rank', 'score', 'tag'],
                    usecols=['qid', 'pid', 'rank'], dtype=np.int32)
    else:
        raise Exception('unknown parameters')

    dev['pid'] = dev['pid'].astype(str)
    assert dev['qid'].dtype == np.int32
    assert dev['pid'].dtype == np.object
    dev_qrel = pd.read_csv('collections/msmarco-passage/qrels.dev.small.tsv', sep="\t",
                           names=["qid", "q0", "pid", "rel"], usecols=['qid', 'pid', 'rel'], dtype=np.int32)
    dev_qrel['pid'] = dev_qrel['pid'].astype(str)
    assert dev_qrel['qid'].dtype == np.int32
    assert dev_qrel['pid'].dtype == np.object
    dev = dev.merge(dev_qrel, left_on=['qid', 'pid'], right_on=['qid', 'pid'], how='left')
    dev['rel'] = dev['rel'].fillna(0).astype(np.int32)
    dev = dev.sort_values(['qid', 'pid']).set_index(['qid', 'pid'])

    print(dev.shape)
    print(dev.index.get_level_values('qid').drop_duplicates().shape)
    print(dev.groupby('qid').count().mean())
    print(dev.head(10))
    print(dev.info())

    return dev, dev_qrel


def query_loader():
    analyzer = Analyzer(get_lucene_analyzer())
    nonStopAnalyzer = Analyzer(get_lucene_analyzer(stopwords=False))
    queries = get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader', \
                                          'collections/msmarco-passage/queries.dev.tsv')
    for qid, value in queries.items():
        assert 'tokenized' not in value and 'nonSW' not in value
        value['nonSW'] = nonStopAnalyzer.analyze(value['title'])
        value['tokenized'] = analyzer.analyze(value['title'])

    return queries


def extract(df, queries, fe):
    df_pieces = []
    fetch_later = []
    qidpid2rel = defaultdict(dict)
    need_rows = 0
    for qid, group in tqdm(df.groupby('qid')):
        for t in group.reset_index().itertuples():
            assert t.pid not in qidpid2rel[t.qid]
            qidpid2rel[t.qid][t.pid] = t.rel
            need_rows += 1
        #test.py has bug here, it does not convert pid to str, not sure why it does not cause problem in java
        #but here we make sure it is str in loader
        fe.lazy_extract(str(qid), queries[qid]['nonSW'], queries[qid]['tokenized'], list(qidpid2rel[t.qid].keys()))
        fetch_later.append(str(qid))
        if len(fetch_later) == 1000:
            info = []
            feature = np.zeros(shape=(need_rows, len(fe.feature_names())), dtype=np.float32)
            idx = 0
            for qid in tqdm(fetch_later):
                for doc in fe.get_result(qid):
                    info.append((int(qid), doc['pid'], qidpid2rel[int(qid)][doc['pid']]))
                    feature[idx, :] = doc['features']
                    idx += 1
            info = pd.DataFrame(info, columns=['qid', 'pid', 'rel'])
            info['qid'] = info['qid'].astype(np.int32)
            info['rel'] = info['rel'].astype(np.int32)
            assert info['qid'].dtype == np.int32
            assert info['rel'].dtype == np.int32
            assert info['pid'].dtype == np.object
            feature = pd.DataFrame(feature, columns=fe.feature_names())
            df_pieces.append(pd.concat([info, feature], axis=1))
            del info, feature
            fetch_later = []
            need_rows = 0
    # deal with rest
    if len(fetch_later) > 0:
        info = []
        feature = np.zeros(shape=(need_rows, len(fe.feature_names())), dtype=np.float32)
        idx = 0
        for qid in tqdm(fetch_later):
            for doc in fe.get_result(qid):
                info.append((int(qid), doc['pid'], qidpid2rel[int(qid)][doc['pid']]))
                feature[idx, :] = doc['features']
                idx += 1
        info = pd.DataFrame(info, columns=['qid', 'pid', 'rel'])
        info['qid'] = info['qid'].astype(np.int32)
        info['rel'] = info['rel'].astype(np.int32)
        assert info['qid'].dtype == np.int32
        assert info['rel'].dtype == np.int32
        assert info['pid'].dtype == np.object
        feature = pd.DataFrame(feature, columns=fe.feature_names())
        df_pieces.append(pd.concat([info, feature], axis=1))
        del info, feature
    data = pd.concat(df_pieces, axis=0, ignore_index=True)
    del df_pieces
    data = data.sort_values(by='qid', kind='mergesort')
    group = data.groupby('qid').agg(count=('pid', 'count'))['count']
    print(data.shape)
    print(data.qid.drop_duplicates().shape)
    print(group.mean())
    print(data.head(10))
    print(data.info())
    return data, group


def hash_df(df):
    h = pd.util.hash_pandas_object(df)
    return hex(h.sum().astype(np.uint64))


def hash_anserini_jar():
    find = glob.glob(os.environ['ANSERINI_CLASSPATH'] + "/*fatjar.jar")
    assert len(find) == 1
    md5Hash = hashlib.md5(open(find[0], 'rb').read())
    return md5Hash.hexdigest()


def hash_fe(fe):
    return hashlib.md5(','.join(sorted(fe.feature_names())).encode()).hexdigest()


def data_loader(file, df, queries, fe):
    df_hash = hash_df(df)
    jar_hash = hash_anserini_jar()
    fe_hash = hash_fe(fe)
    task = 'predict'
    if os.path.exists(f'{task}_{df_hash}_{jar_hash}_{fe_hash}.pickle'):
        res = pickle.load(open(f'{task}_{df_hash}_{jar_hash}_{fe_hash}.pickle', 'rb'))
        print(res['data'].shape)
        print(res['data'].qid.drop_duplicates().shape)
        print(res['group'].mean())
        print(res['data'].head(10))
        print(res['data'].info())
        return res
    else:
        data, group = extract(df, queries, fe)
        obj = {'data': data, 'group': group, 'df_hash': df_hash, 'jar_hash': jar_hash, 'fe_hash': fe_hash}
        print(data.shape)
        print(data.qid.drop_duplicates().shape)
        print(group.mean())
        print(data.head(10))
        print(data.info())
        pickle.dump(obj, open(f'{task}_{df_hash}_{jar_hash}_{fe_hash}.pickle', 'wb'))
        return obj


def predict(models, dev_extracted, feature_name):
    dev_X = dev_extracted['data'].loc[:, feature_name]

    dev_extracted['data']['score'] = 0.
    for gbm in models:
        dev_extracted['data']['score'] += gbm.predict(dev_X)


def eval_mrr(dev_data):
    score_tie_counter = 0
    score_tie_query = set()
    MRR = []
    for qid, group in tqdm(dev_data.groupby('qid')):
        group = group.reset_index()
        rank = 0
        prev_score = None
        assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
        # stable sort is also used in LightGBM

        for t in group.sort_values('score', ascending=False, kind='mergesort').itertuples():
            if prev_score is not None and abs(t.score - prev_score) < 1e-8:
                score_tie_counter += 1
                score_tie_query.add(qid)
            prev_score = t.score
            rank += 1
            if t.rel > 0:
                MRR.append(1.0 / rank)
                break
            elif rank == 10 or rank == len(group):
                MRR.append(0.)
                break

    score_tie = f'score_tie occurs {score_tie_counter} times in {len(score_tie_query)} queries'
    print(score_tie)
    mrr_10 = np.mean(MRR).item()
    print(f'MRR@10:{mrr_10} with {len(MRR)} queries')
    return {'score_tie': score_tie, 'mrr_10': mrr_10}


def eval_recall(dev_qrel, dev_data):
    dev_rel_num = dev_qrel[dev_qrel['rel'] > 0].groupby('qid').count()['rel']

    score_tie_counter = 0
    score_tie_query = set()

    recall_point = [10, 20, 50, 100, 200, 500, 1000]
    recall_curve = {k: [] for k in recall_point}
    for qid, group in tqdm(dev_data.groupby('qid')):
        group = group.reset_index()
        rank = 0
        prev_score = None
        assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
        # stable sort is also used in LightGBM
        total_rel = dev_rel_num.loc[qid]
        query_recall = [0 for k in recall_point]
        for t in group.sort_values('score', ascending=False, kind='mergesort').itertuples():
            if prev_score is not None and abs(t.score - prev_score) < 1e-8:
                score_tie_counter += 1
                score_tie_query.add(qid)
            prev_score = t.score
            rank += 1
            if t.rel > 0:
                for i, p in enumerate(recall_point):
                    if rank <= p:
                        query_recall[i] += 1
        for i, p in enumerate(recall_point):
            if total_rel > 0:
                recall_curve[p].append(query_recall[i] / total_rel)
            else:
                recall_curve[p].append(0.)

    score_tie = f'score_tie occurs {score_tie_counter} times in {len(score_tie_query)} queries'
    print(score_tie)
    res = {'score_tie': score_tie}

    for k, v in recall_curve.items():
        avg = np.mean(v)
        print(f'recall@{k}:{avg}')
        res[f'recall@{k}'] = avg

    return res


def output(file, dev_data):
    score_tie_counter = 0
    score_tie_query = set()
    output_file = open(file,'w')

    for qid, group in tqdm(dev_data.groupby('qid')):
        group = group.reset_index()
        rank = 0
        prev_score = None
        assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
        # stable sort is also used in LightGBM

        for t in group.sort_values('score', ascending=False, kind='mergesort').itertuples():
            if prev_score is not None and abs(t.score - prev_score) < 1e-8:
                score_tie_counter += 1
                score_tie_query.add(qid)
            prev_score = t.score
            rank += 1
            output_file.write(f"{qid}\tQ0\t{t.pid}\t{rank}\t{t.score}\t'ltr'\n")

    score_tie = f'score_tie occurs {score_tie_counter} times in {len(score_tie_query)} queries'
    print(score_tie)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Learning to rank')
    parser.add_argument('--rank_list_path', required=True)
    parser.add_argument('--rank_list_format', required=True)
    parser.add_argument('--ltr_model_path', required=True)
    parser.add_argument('--ltr_output_path', required=True)

    args = parser.parse_args()
    dev, dev_qrel = dev_data_loader(args.rank_list_path, args.rank_list_format)
    queries = query_loader()

    fe = FeatureExtractor('indexes/msmarco-passage/lucene-index-msmarco/', max(multiprocessing.cpu_count()//2, 1))
    fe.add(BM25(k1=0.9, b=0.4))
    fe.add(BM25(k1=1.2, b=0.75))
    fe.add(BM25(k1=2.0, b=0.75))

    fe.add(LMDir(mu=1000))
    fe.add(LMDir(mu=1500))
    fe.add(LMDir(mu=2500))

    fe.add(LMJM(0.1))
    fe.add(LMJM(0.4))
    fe.add(LMJM(0.7))

    fe.add(NTFIDF())
    fe.add(ProbalitySum())

    fe.add(DFR_GL2())
    fe.add(DFR_In_expB2())
    fe.add(DPH())

    fe.add(Proximity())
    fe.add(TPscore())
    fe.add(tpDist())

    fe.add(DocSize())
    fe.add(Entropy())
    fe.add(StopCover())
    fe.add(StopRatio())

    fe.add(QueryLength())
    fe.add(QueryLengthNonStopWords())
    fe.add(QueryCoverageRatio())
    fe.add(UniqueTermCount())
    fe.add(MatchingTermCount())
    fe.add(SCS())

    fe.add(tfStat(AvgPooler()))
    fe.add(tfStat(SumPooler()))
    fe.add(tfStat(MinPooler()))
    fe.add(tfStat(MaxPooler()))
    fe.add(tfStat(VarPooler()))
    fe.add(tfIdfStat(AvgPooler()))
    fe.add(tfIdfStat(SumPooler()))
    fe.add(tfIdfStat(MinPooler()))
    fe.add(tfIdfStat(MaxPooler()))
    fe.add(tfIdfStat(VarPooler()))
    fe.add(scqStat(AvgPooler()))
    fe.add(scqStat(SumPooler()))
    fe.add(scqStat(MinPooler()))
    fe.add(scqStat(MaxPooler()))
    fe.add(scqStat(VarPooler()))
    fe.add(normalizedTfStat(AvgPooler()))
    fe.add(normalizedTfStat(SumPooler()))
    fe.add(normalizedTfStat(MinPooler()))
    fe.add(normalizedTfStat(MaxPooler()))
    fe.add(normalizedTfStat(VarPooler()))

    fe.add(idfStat(AvgPooler()))
    fe.add(idfStat(SumPooler()))
    fe.add(idfStat(MinPooler()))
    fe.add(idfStat(MaxPooler()))
    fe.add(idfStat(VarPooler()))
    fe.add(idfStat(MaxMinRatioPooler()))
    fe.add(idfStat(ConfidencePooler()))
    fe.add(ictfStat(AvgPooler()))
    fe.add(ictfStat(SumPooler()))
    fe.add(ictfStat(MinPooler()))
    fe.add(ictfStat(MaxPooler()))
    fe.add(ictfStat(VarPooler()))
    fe.add(ictfStat(MaxMinRatioPooler()))
    fe.add(ictfStat(ConfidencePooler()))

    fe.add(UnorderedSequentialPairs(3))
    fe.add(UnorderedSequentialPairs(8))
    fe.add(UnorderedSequentialPairs(15))
    fe.add(OrderedSequentialPairs(3))
    fe.add(OrderedSequentialPairs(8))
    fe.add(OrderedSequentialPairs(15))
    fe.add(UnorderedQueryPairs(3))
    fe.add(UnorderedQueryPairs(8))
    fe.add(UnorderedQueryPairs(15))
    fe.add(OrderedQueryPairs(3))
    fe.add(OrderedQueryPairs(8))
    fe.add(OrderedQueryPairs(15))

    dev_extracted = data_loader(args.rank_list_path, dev, queries, fe)
    feature_names = fe.feature_names()
    del dev, queries, fe

    models =  pickle.load(open(args.ltr_model_path,'rb'))
    predict(models, dev_extracted, feature_names)
    eval_res = eval_mrr(dev_extracted['data'])
    eval_recall(dev_qrel, dev_extracted['data'])
    output(args.ltr_output_path, dev_extracted['data'])
