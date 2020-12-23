import argparse
import datetime
import glob
import hashlib
import json
import multiprocessing
import pickle
import os
import random
import shutil
import subprocess
import uuid
import json

import sys
sys.path.append('..')

import numpy as np
import pandas as pd
import lightgbm as lgb
from collections import defaultdict
from tqdm import tqdm
from pyserini.analysis import Analyzer, get_lucene_analyzer
from pyserini.ltr import *
from pyserini.search import get_topics_with_reader


def train_data_loader(task='triple', neg_sample=10, random_seed=12345):
    if os.path.exists(f'train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle'):
        sampled_train = pd.read_pickle(f'train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle')
        print(sampled_train.shape)
        print(sampled_train.index.get_level_values('qid').drop_duplicates().shape)
        print(sampled_train.groupby('qid').count().mean())
        print(sampled_train.head(10))
        print(sampled_train.info())
        return sampled_train
    else:
        if task == 'triple':
            train = pd.read_csv('../collections/msmarco-passage/qidpidtriples.train.full.2.tsv', sep="\t",
                                names=['qid', 'pos_pid', 'neg_pid'], dtype=np.int32)
            pos_half = train[['qid', 'pos_pid']].rename(columns={"pos_pid": "pid"}).drop_duplicates()
            pos_half['rel'] = np.int32(1)
            neg_half = train[['qid', 'neg_pid']].rename(columns={"neg_pid": "pid"}).drop_duplicates()
            neg_half['rel'] = np.int32(0)
            del train
            sampled_neg_half = []
            for qid, group in tqdm(neg_half.groupby('qid')):
                sampled_neg_half.append(group.sample(n=min(neg_sample, len(group)), random_state=random_seed))
            sampled_train = pd.concat([pos_half] + sampled_neg_half, axis=0, ignore_index=True)
            sampled_train = sampled_train.sort_values(['qid', 'pid']).set_index(['qid', 'pid'])
            print(sampled_train.shape)
            print(sampled_train.index.get_level_values('qid').drop_duplicates().shape)
            print(sampled_train.groupby('qid').count().mean())
            print(sampled_train.head(10))
            print(sampled_train.info())

            sampled_train.to_pickle(f'train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle')
        elif task == 'rank':
            qrel = defaultdict(list)
            with open("../collections/msmarco-passage/qrels.train.tsv") as f:
                for line in f:
                    topicid, _, docid, rel = line.strip().split('\t')
                    assert rel == "1", line.split(' ')
                    qrel[topicid].append(docid)

            qid2pos = defaultdict(list)
            qid2neg = defaultdict(list)
            with open("../runs/msmarco-passage/run.train.small.tsv") as f:
                for line in tqdm(f):
                    topicid, docid, rank = line.split()
                    assert topicid in qrel
                    if docid in qrel[topicid]:
                        qid2pos[topicid].append(docid)
                    else:
                        qid2neg[topicid].append(docid)
            sampled_train = []
            for topicid, pos_list in tqdm(qid2pos.items()):
                neg_list = random.sample(qid2neg[topicid], min(len(qid2neg[topicid]), neg_sample))
                for positive_docid in pos_list:
                    sampled_train.append((int(topicid), int(positive_docid), 1))
                for negative_docid in neg_list:
                    sampled_train.append((int(topicid), int(negative_docid), 0))
            sampled_train = pd.DataFrame(sampled_train, columns=['qid', 'pid', 'rel'], dtype=np.int32)
            sampled_train = sampled_train.sort_values(['qid', 'pid']).set_index(['qid', 'pid'])
            print(sampled_train.shape)
            print(sampled_train.index.get_level_values('qid').drop_duplicates().shape)
            print(sampled_train.groupby('qid').count().mean())
            print(sampled_train.head(10))
            print(sampled_train.info())

            sampled_train.to_pickle(f'train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle')
        else:
            raise Exception('unknown parameters')
        return sampled_train


def dev_data_loader(task='pygaggle'):
    if os.path.exists(f'dev_{task}.pickle'):
        dev = pd.read_pickle(f'dev_{task}.pickle')
        print(dev.shape)
        print(dev.index.get_level_values('qid').drop_duplicates().shape)
        print(dev.groupby('qid').count().mean())
        print(dev.head(10))
        print(dev.info())
        dev_qrel = pd.read_pickle(f'dev_qrel.pickle')
        return dev, dev_qrel
    else:
        if task == 'rerank':
            dev = pd.read_csv('../collections/msmarco-passage/top1000.dev', sep="\t",
                              names=['qid', 'pid', 'query', 'doc'], usecols=['qid', 'pid'], dtype=np.int32)
        elif task == 'anserini':
            dev = pd.read_csv('../runs/msmarco-passage/run.msmarco-passage.dev.small.tsv', sep="\t",
                              names=['qid', 'pid', 'rank'], dtype=np.int32)
        elif task == 'pygaggle':
            dev = pd.read_csv('../../pygaggle/data/msmarco_ans_entire/run.dev.small.tsv', sep="\t",
                              names=['qid', 'pid', 'rank'], dtype=np.int32)
        else:
            raise Exception('unknown parameters')
        dev_qrel = pd.read_csv('../collections/msmarco-passage/qrels.dev.small.tsv', sep="\t",
                               names=["qid", "q0", "pid", "rel"], usecols=['qid', 'pid', 'rel'], dtype=np.int32)
        dev = dev.merge(dev_qrel, left_on=['qid', 'pid'], right_on=['qid', 'pid'], how='left')
        dev['rel'] = dev['rel'].fillna(0).astype(np.int32)
        dev = dev.sort_values(['qid', 'pid']).set_index(['qid', 'pid'])

        print(dev.shape)
        print(dev.index.get_level_values('qid').drop_duplicates().shape)
        print(dev.groupby('qid').count().mean())
        print(dev.head(10))
        print(dev.info())

        dev.to_pickle(f'dev_{task}.pickle')
        dev_qrel.to_pickle(f'dev_qrel.pickle')
        return dev, dev_qrel



def query_loader(choice='default'):
    if os.path.exists(f'query_{choice}_tokenized.pickle'):
        return pickle.load(open(f'query_{choice}_tokenized.pickle', 'rb'))
    else:
        if choice == 'default':
            analyzer = Analyzer(get_lucene_analyzer())
            nonStopAnalyzer = Analyzer(get_lucene_analyzer(stopwords=False))
            queries = get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader', \
                                             '../collections/msmarco-passage/queries.train.tsv')
            #although not queries.dev.small.tsv but all dev rank list only contain 6980 queries
            queries.update(get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader', \
                                                  '../collections/msmarco-passage/queries.dev.tsv'))
            ibm = {}
            with open('../ibm_query.json') as f:
                lines = f.readlines()
                for line in lines:
                    temp = json.loads(line)
                    ibm[temp['id']] = temp
            for qid, value in queries.items():
                assert 'tokenized' not in value and 'nonSW' not in value
                value['nonSW'] = nonStopAnalyzer.analyze(value['title'])
                value['tokenized'] = analyzer.analyze(value['title'])
                value['text_unlemm'] = list(ibm[str(qid)]['text_unlemm'].split(" "))
                value['text_bert_tok'] = list(ibm[str(qid)]['text_bert_tok'].split(" "))
            pickle.dump(queries,open(f'query_{choice}_tokenized.pickle','wb'))
            return queries
        else:
            raise Exception('unknown parameters')


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
        fe.lazy_extract(str(qid), queries[qid]['nonSW'], queries[qid]['tokenized'], [str(pid) for pid in qidpid2rel[t.qid].keys()], queries[qid]['text_unlemm'],queries[qid]['text_bert_tok'])
        fetch_later.append(str(qid))
        if len(fetch_later) == 10000:
            info = np.zeros(shape=(need_rows, 3), dtype=np.int32)
            feature = np.zeros(shape=(need_rows, len(fe.feature_names())), dtype=np.float32)
            idx = 0
            for qid in fetch_later:
                for doc in fe.get_result(qid):
                    info[idx, 0] = int(qid)
                    info[idx, 1] = int(doc['pid'])
                    info[idx, 2] = qidpid2rel[int(qid)][int(doc['pid'])]
                    feature[idx, :] = doc['features']
                    idx += 1
            info = pd.DataFrame(info, columns=['qid', 'pid', 'rel'])
            feature = pd.DataFrame(feature, columns=fe.feature_names())
            df_pieces.append(pd.concat([info, feature], axis=1))
            fetch_later = []
            need_rows = 0
    # deal with rest
    if len(fetch_later) > 0:
        info = np.zeros(shape=(need_rows, 3), dtype=np.int32)
        feature = np.zeros(shape=(need_rows, len(fe.feature_names())), dtype=np.float32)
        idx = 0
        for qid in fetch_later:
            for doc in fe.get_result(qid):
                info[idx, 0] = int(qid)
                info[idx, 1] = int(doc['pid'])
                info[idx, 2] = qidpid2rel[int(qid)][int(doc['pid'])]
                feature[idx, :] = doc['features']
                idx += 1
        info = pd.DataFrame(info, columns=['qid', 'pid', 'rel'])
        feature = pd.DataFrame(feature, columns=fe.feature_names())
        df_pieces.append(pd.concat([info, feature], axis=1))
    data = pd.concat(df_pieces, axis=0, ignore_index=True)
    data = data.sort_values(by='qid', kind='mergesort')
    group = data.groupby('qid').agg(count=('pid', 'count'))['count']
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


def data_loader(task, df, queries, fe):
    df_hash = hash_df(df)
    jar_hash = hash_anserini_jar()
    fe_hash = hash_fe(fe)
    if os.path.exists(f'{task}_{df_hash}_{jar_hash}_{fe_hash}.pickle'):
        res = pickle.load(open(f'{task}_{df_hash}_{jar_hash}_{fe_hash}.pickle', 'rb'))
        print(res['data'].shape)
        print(res['data'].qid.drop_duplicates().shape)
        print(res['group'].mean())
        print(res['data'].head(10))
        print(res['data'].info())
        return res
    else:
        if task == 'train' or task == 'dev':
            data, group = extract(df, queries, fe)
            obj = {'data': data, 'group': group, 'df_hash': df_hash, 'jar_hash': jar_hash, 'fe_hash': fe_hash}
            print(data.shape)
            print(data.qid.drop_duplicates().shape)
            print(group.mean())
            print(data.head(10))
            print(data.info())
            pickle.dump(obj, open(f'{task}_{df_hash}_{jar_hash}_{fe_hash}.pickle', 'wb'))
            return obj
        else:
            raise Exception('unknown parameters')

def gen_dev_group_rel_num(dev_qrel, dev_extracted, feature_name):
    dev_rel_num = dev_qrel[dev_qrel['rel']>0].groupby('qid').count()['rel']
    gid = 0
    sample_id = 0
    dev_group_rel_num = []
    for qid,group in dev_extracted['data'].groupby('qid'):
        group = group.sort_values(['pid'])
        assert len(group) == dev_extracted['group'].iloc[gid]
        assert np.isclose(group.iloc[0,:].loc[feature_name],
                          dev_extracted['data'].iloc[sample_id,:].loc[feature_name], equal_nan=True).all()
        dev_group_rel_num.append(dev_rel_num.loc[qid])
        gid += 1
        sample_id += len(group)
    return dev_group_rel_num, dev_extracted['group']

def recall_at_200(preds, dataset):
    global dev_group_rel_num
    global dev_group
    labels = dataset.get_label()
    groups = dataset.get_group()
    assert np.equal(groups, dev_group).all()
    idx = 0
    recall = 0
    for g,gnum in zip(groups, dev_group_rel_num):
        top_preds = labels[idx:idx+g][np.argsort(preds[idx:idx+g])]
        recall += np.sum(top_preds[-200:])/gnum
        idx += g
    assert idx == len(preds)
    return 'recall@200', recall/len(groups), True

def train(train_extracted, dev_extracted, feature_name):
    train_X = train_extracted['data'].loc[:, feature_name]
    train_Y = train_extracted['data']['rel']
    dev_X = dev_extracted['data'].loc[:, feature_name]
    dev_Y = dev_extracted['data']['rel']
    lgb_train = lgb.Dataset(train_X, label=train_Y, group=train_extracted['group'])
    lgb_valid = lgb.Dataset(dev_X, label=dev_Y, group=dev_extracted['group'])
    #max_leaves = -1 seems to work better for many settings, although 10 is also good
    params = {
        'boosting_type': 'gbdt',
        'objective': 'lambdarank',
        'max_bin': 255,
        'num_leaves': 63,
        'max_depth': -1,
        'min_data_in_leaf': 30,
        'min_sum_hessian_in_leaf': 0,
        'bagging_fraction': 0.8,
        'bagging_freq': 50,
        'feature_fraction': 1,
        'learning_rate': 0.1,
        'num_boost_round': 1000,
        'early_stopping_round': 300,
        'metric': 'custom',
        'label_gain': [0, 1],
        'lambdarank_truncation_level': 20,
        'seed': 12345,
        'num_threads': max(multiprocessing.cpu_count() // 2, 1)
    }
    num_boost_round = params.pop('num_boost_round')
    early_stopping_round = params.pop('early_stopping_round')
    gbm = lgb.train(params, lgb_train,
                    valid_sets=lgb_valid,
                    num_boost_round=num_boost_round,
                    early_stopping_rounds=early_stopping_round,
                    feval=recall_at_200,
                    feature_name=feature_name,
                    verbose_eval=True)
    dev_extracted['data']['score'] = gbm.predict(dev_X)
    best_score = gbm.best_score['valid_0']['recall@200']
    print(best_score)
    best_iteration = gbm.best_iteration
    print(best_iteration)
    feature_importances = sorted(list(zip(feature_name, gbm.feature_importance().tolist())),
                                 key=lambda x: x[1], reverse=True)
    print(feature_importances)
    params['num_boost_round'] = num_boost_round
    params['early_stopping_round'] = early_stopping_round
    return {'model': [gbm], 'params': params, 'feature_importances': feature_importances}


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


def gen_exp_dir():
    dirname = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S') + '_' + str(uuid.uuid1())
    assert not os.path.exists(dirname)
    os.mkdir(dirname)
    return dirname


def save_exp(dirname,
             train_extracted, dev_extracted,
             train_res, eval_res):
    dev_extracted['data'][['qid', 'pid', 'score']].to_json(f'{dirname}/output.json')
    subprocess.check_output(['gzip', f'{dirname}/output.json'])
    with open(f'{dirname}/model.pkl', 'wb') as f:
        pickle.dump(train_res['model'], f)
    metadata = {
        'train_df_hash': train_extracted['df_hash'],
        'train_jar_hash': train_extracted['jar_hash'],
        'train_fe_hash': train_extracted['fe_hash'],
        'dev_df_hash': dev_extracted['df_hash'],
        'dev_jar_hash': dev_extracted['jar_hash'],
        'dev_fe_hash': dev_extracted['fe_hash'],
        'feature_importances': train_res['feature_importances'],
        'params': train_res['params'],
        'score_tie': eval_res['score_tie'],
        'mrr_10': eval_res['mrr_10']
    }
    json.dump(metadata, open(f'{dirname}/metadata.json', 'w'))
    shutil.copytree('anserini_ltr_source', f'{dirname}/anserini_ltr_source')
    shutil.copytree('pyserini_ltr_source', f'{dirname}/pyserini_ltr_source')
    shutil.copy('test.py', f'{dirname}/test.py')


if __name__ == '__main__':
    sampled_train = train_data_loader(task='triple', neg_sample=10)
    dev, dev_qrel = dev_data_loader(task='pygaggle')
    queries = query_loader()

    fe = FeatureExtractor('../indexes/msmarco-passage/new-lucene-index-msmarco/', max(multiprocessing.cpu_count()//2, 1))
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

    fe.add(BM25Conf(MaxPooler()))
    fe.add(BM25Conf(MinPooler()))
    fe.add(BM25Mean(MaxPooler()))
    fe.add(BM25Mean(MinPooler()))
    fe.add(BM25Min(MaxPooler()))
    fe.add(BM25Min(MinPooler()))
    fe.add(BM25Max(MaxPooler()))
    fe.add(BM25Max(MinPooler()))
    fe.add(BM25HMean(MaxPooler()))
    fe.add(BM25HMean(MinPooler()))
    fe.add(BM25Var(MaxPooler()))
    fe.add(BM25Var(MinPooler()))
    fe.add(BM25Quartile(MaxPooler()))
    fe.add(BM25Quartile(MinPooler()))
    fe.add(IBMModel1('../collections/msmarco-passage/body','Unlemma'))
    fe.add(IBMModel1('../collections/msmarco-passage/text_bert_tok','Bert'))

    train_extracted = data_loader('train', sampled_train, queries, fe)
    dev_extracted = data_loader('dev', dev, queries, fe)
    feature_name = fe.feature_names()
    del sampled_train, dev, queries, fe

    dev_group_rel_num, dev_group = gen_dev_group_rel_num(dev_qrel, dev_extracted, feature_name)
    train_res = train(train_extracted, dev_extracted, feature_name)
    eval_res = eval_mrr(dev_extracted['data'])
    eval_res.update(eval_recall(dev_qrel, dev_extracted['data']))

    dirname = gen_exp_dir()
    save_exp(dirname, train_extracted, dev_extracted, train_res, eval_res)
