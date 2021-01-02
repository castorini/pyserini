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



def query_loader():
    queries = {}
    with open('queries.train.small.Flex.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            del query['raw']
            queries[qid] = query
    with open('queries.dev.small.Flex.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            del query['raw']
            queries[qid] = query
    with open('queries.eval.small.Flex.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            del query['raw']
            queries[qid] = query
    return queries


def batch_extract(df, queries, fe):
    tasks = []
    task_infos = []

    info_dfs = []
    feature_dfs = []
    group_dfs = []

    for qid, group in tqdm(df.groupby('qid')):
        task = {
            "qid": str(qid),
            "docIds": [],
            "rels": [],
            "query_dict": queries[str(qid)]
        }
        for t in group.reset_index().itertuples():
            task["docIds"].append(str(t.pid))
            task_infos.append((qid, t.pid, t.rel))
        tasks.append(task)
        if len(tasks) == 10000:
            features = fe.batch_extract(tasks)
            task_infos = pd.DataFrame(task_infos, columns=['qid', 'pid', 'rel'])
            group = task_infos.groupby('qid').agg(count=('pid', 'count'))['count']
            print(features.shape)
            print(task_infos.qid.drop_duplicates().shape)
            print(group.mean())
            print(features.head(10))
            print(features.info())
            info_dfs.append(task_infos)
            feature_dfs.append(features)
            group_dfs.append(group)
            tasks = []
            task_infos = []
    # deal with rest
    if len(tasks) > 0:
        features = fe.batch_extract(tasks)
        task_infos = pd.DataFrame(task_infos, columns=['qid', 'pid', 'rel'])
        group = task_infos.groupby('qid').agg(count=('pid', 'count'))['count']
        print(features.shape)
        print(task_infos.qid.drop_duplicates().shape)
        print(group.mean())
        print(features.head(10))
        print(features.info())
        info_dfs.append(task_infos)
        feature_dfs.append(features)
        group_dfs.append(group)
    info_dfs = pd.concat(info_dfs, axis=0, ignore_index=True)
    feature_dfs = pd.concat(feature_dfs, axis=0, ignore_index=True, copy=False)
    group_dfs = pd.concat(group_dfs, axis=0, ignore_index=True)
    return info_dfs, feature_dfs, group_dfs


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
        print(res['info'].shape)
        print(res['info'].qid.drop_duplicates().shape)
        print(res['group'].mean())
        return res
    else:
        if task == 'train' or task == 'dev':
            info, data, group = batch_extract(df, queries, fe)
            obj = {'info':info, 'data': data, 'group': group,
                   'df_hash': df_hash, 'jar_hash': jar_hash, 'fe_hash': fe_hash}
            print(info.shape)
            print(info.qid.drop_duplicates().shape)
            print(group.mean())
            pickle.dump(obj, open(f'{task}_{df_hash}_{jar_hash}_{fe_hash}.pickle', 'wb'))
            return obj
        else:
            raise Exception('unknown parameters')

def gen_dev_group_rel_num(dev_qrel, dev_extracted):
    dev_rel_num = dev_qrel[dev_qrel['rel']>0].groupby('qid').count()['rel']
    prev_qid = None
    dev_rel_num_list = []
    for t in dev_extracted['info'].itertuples():
        if prev_qid is None or t.qid != prev_qid:
            prev_qid = t.qid
            dev_rel_num_list.append(dev_rel_num.loc[t.qid])
        else:
            continue

    def recall_at_200(preds, dataset):
        labels = dataset.get_label()
        groups = dataset.get_group()
        idx = 0
        recall = 0
        for g, gnum in zip(groups, dev_rel_num_list):
            top_preds = labels[idx:idx + g][np.argsort(preds[idx:idx + g])]
            recall += np.sum(top_preds[-200:]) / gnum
            idx += g
        assert idx == len(preds)
        return 'recall@200', recall / len(groups), True

    return recall_at_200


def train(train_extracted, dev_extracted, feature_name, eval_fn):
    train_X = train_extracted['data'].loc[:, feature_name]
    train_Y = train_extracted['info']['rel']
    dev_X = dev_extracted['data'].loc[:, feature_name]
    dev_Y = dev_extracted['info']['rel']
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
        # 'bagging_fraction': 0.8,
        # 'bagging_freq': 50,
        'feature_fraction': 1,
        'learning_rate': 0.1,
        'num_boost_round': 1000,
        'early_stopping_round': 200,
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
                    feval=eval_fn,
                    feature_name=feature_name,
                    verbose_eval=True)
    dev_extracted['info']['score'] = gbm.predict(dev_X)
    best_score = gbm.best_score['valid_0']['recall@200']
    print(best_score)
    best_iteration = gbm.best_iteration
    print(best_iteration)
    feature_importances = sorted(list(zip(feature_name, gbm.feature_importance().tolist())),
                                 key=lambda x: x[1], reverse=True)
    print(feature_importances)
    params['num_boost_round'] = num_boost_round
    params['early_stopping_round'] = early_stopping_round
    return {'model': [gbm], 'params': params,
            'feature_names': feature_name,
            'feature_importances': feature_importances}


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
    dev_extracted['info'][['qid', 'pid', 'score']].to_json(f'{dirname}/output.json')
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
        'feature_names': train_res['feature_names'],
        'feature_importances': train_res['feature_importances'],
        'params': train_res['params'],
        'score_tie': eval_res['score_tie'],
        'mrr_10': eval_res['mrr_10']
    }
    json.dump(metadata, open(f'{dirname}/metadata.json', 'w'))
    shutil.copytree('../anserini_ltr_source', f'{dirname}/anserini_ltr_source')
    shutil.copytree('../pyserini_ltr_source', f'{dirname}/pyserini_ltr_source')
    shutil.copy('train_passage.py', f'{dirname}/train_passage.py')


if __name__ == '__main__':
    sampled_train = train_data_loader(task='triple', neg_sample=20)
    dev, dev_qrel = dev_data_loader(task='pygaggle')
    queries = query_loader()

    fe = FeatureExtractor('../indexes/msmarco-passage/lucene-index-msmarco-flex/', max(multiprocessing.cpu_count()//2, 1))
    for qfield, ifield in [('analyzed', 'contents'),
                           ('text', 'text'),
                           ('text_unlemm', 'text_unlemm'),
                           ('text_bert_tok', 'text_bert_tok')]:
        print(qfield, ifield)
        fe.add(BM25(k1=0.9, b=0.4, field=ifield, qfield=qfield))
        fe.add(BM25(k1=1.2, b=0.75, field=ifield, qfield=qfield))
        fe.add(BM25(k1=2.0, b=0.75, field=ifield, qfield=qfield))

        fe.add(LMDir(mu=1000, field=ifield, qfield=qfield))
        fe.add(LMDir(mu=1500, field=ifield, qfield=qfield))
        fe.add(LMDir(mu=2500, field=ifield, qfield=qfield))

        fe.add(LMJM(0.1, field=ifield, qfield=qfield))
        fe.add(LMJM(0.4, field=ifield, qfield=qfield))
        fe.add(LMJM(0.7, field=ifield, qfield=qfield))

        fe.add(NTFIDF(field=ifield, qfield=qfield))
        fe.add(ProbalitySum(field=ifield, qfield=qfield))

        fe.add(DFR_GL2(field=ifield, qfield=qfield))
        fe.add(DFR_In_expB2(field=ifield, qfield=qfield))
        fe.add(DPH(field=ifield, qfield=qfield))

        fe.add(Proximity(field=ifield, qfield=qfield))
        fe.add(TPscore(field=ifield, qfield=qfield))
        fe.add(tpDist(field=ifield, qfield=qfield))

        fe.add(DocSize(field=ifield))

        fe.add(QueryLength(qfield=qfield))
        fe.add(QueryCoverageRatio(qfield=qfield))
        fe.add(UniqueTermCount(qfield=qfield))
        fe.add(MatchingTermCount(field=ifield, qfield=qfield))
        fe.add(SCS(field=ifield, qfield=qfield))

        fe.add(tfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(tfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(tfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(tfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(tfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(tfStat(VarPooler(), field=ifield, qfield=qfield))
        fe.add(tfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))
        fe.add(tfStat(ConfidencePooler(), field=ifield, qfield=qfield))

        fe.add(tfIdfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(tfIdfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(tfIdfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(tfIdfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(tfIdfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(tfIdfStat(VarPooler(), field=ifield, qfield=qfield))
        fe.add(tfIdfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))
        fe.add(tfIdfStat(ConfidencePooler(), field=ifield, qfield=qfield))

        fe.add(scqStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(scqStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(scqStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(scqStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(scqStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(scqStat(VarPooler(), field=ifield, qfield=qfield))
        fe.add(scqStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))
        fe.add(scqStat(ConfidencePooler(), field=ifield, qfield=qfield))

        fe.add(normalizedTfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(normalizedTfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(normalizedTfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(normalizedTfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(normalizedTfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(normalizedTfStat(VarPooler(), field=ifield, qfield=qfield))
        fe.add(normalizedTfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))
        fe.add(normalizedTfStat(ConfidencePooler(), field=ifield, qfield=qfield))

        fe.add(idfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(idfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(idfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(idfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(idfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(idfStat(VarPooler(), field=ifield, qfield=qfield))
        fe.add(idfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))
        fe.add(idfStat(ConfidencePooler(), field=ifield, qfield=qfield))

        fe.add(ictfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(ictfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(ictfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(ictfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(ictfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(ictfStat(VarPooler(), field=ifield, qfield=qfield))
        fe.add(ictfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))
        fe.add(ictfStat(ConfidencePooler(), field=ifield, qfield=qfield))

        fe.add(UnorderedSequentialPairs(3, field=ifield, qfield=qfield))
        fe.add(UnorderedSequentialPairs(8, field=ifield, qfield=qfield))
        fe.add(UnorderedSequentialPairs(15, field=ifield, qfield=qfield))
        fe.add(OrderedSequentialPairs(3, field=ifield, qfield=qfield))
        fe.add(OrderedSequentialPairs(8, field=ifield, qfield=qfield))
        fe.add(OrderedSequentialPairs(15, field=ifield, qfield=qfield))
        fe.add(UnorderedQueryPairs(3, field=ifield, qfield=qfield))
        fe.add(UnorderedQueryPairs(8, field=ifield, qfield=qfield))
        fe.add(UnorderedQueryPairs(15, field=ifield, qfield=qfield))
        fe.add(OrderedQueryPairs(3, field=ifield, qfield=qfield))
        fe.add(OrderedQueryPairs(8, field=ifield, qfield=qfield))
        fe.add(OrderedQueryPairs(15, field=ifield, qfield=qfield))

    fe.add(IBMModel1("../FlexNeuART/collections/msmarco_doc/derived_data/giza/title_unlemm", "text_unlemm",
                     "title_unlemm", "text_unlemm"))
    print("IBM Model loaded")
    fe.add(IBMModel1("../FlexNeuART/collections/msmarco_doc/derived_data/giza/url_unlemm", "text_unlemm",
                     "url_unlemm", "text_unlemm"))
    print("IBM Model loaded")
    fe.add(IBMModel1("../FlexNeuART/collections/msmarco_doc/derived_data/giza/body", "text_unlemm",
                     "body", "text_unlemm"))
    print("IBM Model loaded")
    fe.add(IBMModel1("../FlexNeuART/collections/msmarco_doc/derived_data/giza/text_bert_tok", "text_bert_tok",
                     "text_bert_tok", "text_bert_tok"))
    print("IBM Model loaded")

    train_extracted = data_loader('train', sampled_train, queries, fe)
    dev_extracted = data_loader('dev', dev, queries, fe)
    feature_name = fe.feature_names()
    del sampled_train, dev, queries, fe

    eval_fn = gen_dev_group_rel_num(dev_qrel, dev_extracted)
    train_res = train(train_extracted, dev_extracted, feature_name, eval_fn)
    eval_res = eval_mrr(dev_extracted['info'])
    eval_res.update(eval_recall(dev_qrel, dev_extracted['info']))

    dirname = gen_exp_dir()
    save_exp(dirname, train_extracted, dev_extracted, train_res, eval_res)
