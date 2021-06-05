#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import datetime
import glob
import hashlib
import multiprocessing
import pickle
import os
import random
import subprocess
import uuid
import json
import time

import sys

sys.path.append('..')

import numpy as np
import pandas as pd
import lightgbm as lgb
from collections import defaultdict
from tqdm import tqdm
from pyserini.ltr import *
import argparse

"""
train a LTR model with lambdaRank library and save to pickle for future inference
run from python root dir
"""
def train_data_loader(task='triple', neg_sample=10, random_seed=12345):
    print(f'train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle')
    if os.path.exists(f'./collections/msmarco-ltr-passage/train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle'):
        sampled_train = pd.read_pickle(f'./collections/msmarco-ltr-passage/train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle')
        print(sampled_train.shape)
        print(sampled_train.index.get_level_values('qid').drop_duplicates().shape)
        print(sampled_train.groupby('qid').count().mean())
        print(sampled_train.head(10))
        print(sampled_train.info())
        return sampled_train
    else:
        if task == 'triple':
            train = pd.read_csv('./collections/msmarco-passage/qidpidtriples.train.full.2.tsv', sep="\t",
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

            sampled_train.to_pickle(f'./collections/msmarco-ltr-passage/train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle')
        elif task == 'rank':
            qrel = defaultdict(list)
            with open("./collections/msmarco-passage/qrels.train.tsv") as f:
                for line in f:
                    topicid, _, docid, rel = line.strip().split('\t')
                    assert rel == "1", line.split(' ')
                    qrel[topicid].append(docid)

            qid2pos = defaultdict(list)
            qid2neg = defaultdict(list)
            with open("./runs/msmarco-passage/run.train.small.tsv") as f:
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

            sampled_train.to_pickle(f'./collections/msmarco-ltr-passage/train_{task}_sampled_with_{neg_sample}_{random_seed}.pickle')
        else:
            raise Exception('unknown parameters')
        return sampled_train


def dev_data_loader(task='anserini'):
    if os.path.exists(f'./collections/msmarco-ltr-passage/dev_{task}.pickle'):
        dev = pd.read_pickle(f'./collections/msmarco-ltr-passage/dev_{task}.pickle')
        print(dev.shape)
        print(dev.index.get_level_values('qid').drop_duplicates().shape)
        print(dev.groupby('qid').count().mean())
        print(dev.head(10))
        print(dev.info())
        dev_qrel = pd.read_pickle(f'./collections/msmarco-ltr-passage/dev_qrel.pickle')
        return dev, dev_qrel
    else:
        if task == 'rerank':
            dev = pd.read_csv('./collections/msmarco-passage/top1000.dev', sep="\t",
                              names=['qid', 'pid', 'query', 'doc'], usecols=['qid', 'pid'], dtype=np.int32)
        elif task == 'anserini':
            dev = pd.read_csv('./runs/run.msmarco-passage.bm25tuned.txt', sep="\t",
                              names=['qid', 'pid', 'rank'], dtype=np.int32)
        elif task == 'pygaggle':
            #pygaggle bm25 top 1000 input
            dev = pd.read_csv('./collections/msmarco-passage/run.dev.small.tsv', sep="\t",
                              names=['qid', 'pid', 'rank'], dtype=np.int32)
        else:
            raise Exception('unknown parameters')
        dev_qrel = pd.read_csv('./collections/msmarco-passage/qrels.dev.small.tsv', sep="\t",
                               names=["qid", "q0", "pid", "rel"], usecols=['qid', 'pid', 'rel'], dtype=np.int32)
        dev = dev.merge(dev_qrel, left_on=['qid', 'pid'], right_on=['qid', 'pid'], how='left')
        dev['rel'] = dev['rel'].fillna(0).astype(np.int32)
        dev = dev.sort_values(['qid', 'pid']).set_index(['qid', 'pid'])

        print(dev.shape)
        print(dev.index.get_level_values('qid').drop_duplicates().shape)
        print(dev.groupby('qid').count().mean())
        print(dev.head(10))
        print(dev.info())

        dev.to_pickle(f'./collections/msmarco-ltr-passage/dev_{task}.pickle')
        dev_qrel.to_pickle(f'./collections/msmarco-ltr-passage/dev_qrel.pickle')
        return dev, dev_qrel


def query_loader():
    queries = {}
    with open('./collections/msmarco-ltr-passage/queries.eval.small.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    with open('./collections/msmarco-ltr-passage/queries.dev.small.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    with open('./collections/msmarco-ltr-passage/queries.train.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    return queries


def batch_extract(df, queries, fe):
    tasks = []
    task_infos = []
    group_lst = []

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
        group_lst.append((qid, len(task['docIds'])))
        if len(tasks) == 10000:
            features = fe.batch_extract(tasks)
            task_infos = pd.DataFrame(task_infos, columns=['qid', 'pid', 'rel'])
            group = pd.DataFrame(group_lst, columns=['qid', 'count'])
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
            group_lst = []
    # deal with rest
    if len(tasks) > 0:
        features = fe.batch_extract(tasks)
        task_infos = pd.DataFrame(task_infos, columns=['qid', 'pid', 'rel'])
        group = pd.DataFrame(group_lst, columns=['qid', 'count'])
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
    if task == 'train' or task == 'dev':
        info, data, group = batch_extract(df, queries, fe)
        obj = {'info': info, 'data': data, 'group': group,
                   'df_hash': df_hash, 'jar_hash': jar_hash, 'fe_hash': fe_hash}
        print(info.shape)
        print(info.qid.drop_duplicates().shape)
        print(group.mean())
        return obj
    else:
        raise Exception('unknown parameters')


def gen_dev_group_rel_num(dev_qrel, dev_extracted):
    dev_rel_num = dev_qrel[dev_qrel['rel'] > 0].groupby('qid').count()['rel']
    prev_qid = None
    dev_rel_num_list = []
    for t in dev_extracted['info'].itertuples():
        if prev_qid is None or t.qid != prev_qid:
            prev_qid = t.qid
            dev_rel_num_list.append(dev_rel_num.loc[t.qid])
        else:
            continue
    assert len(dev_rel_num_list) == dev_qrel.qid.drop_duplicates().shape[0]

    def recall_at_200(preds, dataset):
        labels = dataset.get_label()
        groups = dataset.get_group()
        idx = 0
        recall = 0
        assert len(dev_rel_num_list) == len(groups)
        for g, gnum in zip(groups, dev_rel_num_list):
            top_preds = labels[idx:idx + g][np.argsort(preds[idx:idx + g])]
            recall += np.sum(top_preds[-200:]) / gnum
            idx += g
        assert idx == len(preds)
        return 'recall@200', recall / len(groups), True

    return recall_at_200

def mrr_at_10(preds, dataset):
    labels = dataset.get_label()
    groups = dataset.get_group()
    idx = 0
    recall = 0
    MRR = []
    for g in groups:
        top_preds = labels[idx:idx + g][np.argsort(preds[idx:idx + g])][-10:][::-1]
        rank = 0
        while(rank < len(top_preds)):
            if(top_preds[rank] > 0):
                MRR.append(1.0/(rank+1))
                break
            rank += 1
        if (rank == len(top_preds)):
            MRR.append(0.)
        idx += g
    assert idx == len(preds)
    return 'mrr@10', np.mean(MRR).item(), True


def train(train_extracted, dev_extracted, feature_name, eval_fn):
    lgb_train = lgb.Dataset(train_extracted['data'].loc[:, feature_name],
                            label=train_extracted['info']['rel'],
                            group=train_extracted['group']['count'])
    lgb_valid = lgb.Dataset(dev_extracted['data'].loc[:, feature_name],
                            label=dev_extracted['info']['rel'],
                            group=dev_extracted['group']['count'],
                            free_raw_data=False)
    # max_leaves = -1 seems to work better for many settings, although 10 is also good
    params = {
        'boosting_type': 'goss',
        'objective': 'lambdarank',
        'max_bin': 255,
        'num_leaves': 200,
        'max_depth': -1,
        'min_data_in_leaf': 50,
        'min_sum_hessian_in_leaf': 0,
        'feature_fraction': 1,
        'learning_rate': 0.1,
        'num_boost_round': 1000,
        'early_stopping_round': 200,
        'metric': 'custom',
        'label_gain': [0, 1],
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
    del lgb_train
    dev_extracted['info']['score'] = gbm.predict(lgb_valid.get_data())
    best_score = gbm.best_score['valid_0']['mrr@10']
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
    dirname = './runs/'+dirname
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


if __name__ == '__main__':
    os.environ["ANSERINI_CLASSPATH"] = "pyserini/resources/jars"
    parser = argparse.ArgumentParser(description='Learning to rank training')
    parser.add_argument('--index', required=True)
    parser.add_argument('--neg-sample', default=10)
    parser.add_argument('--opt', default='mrr_at_10')
    args = parser.parse_args()
    total_start_time = time.time()
    sampled_train = train_data_loader(task='triple', neg_sample = args.neg_sample)
    dev, dev_qrel = dev_data_loader(task='anserini')
    queries = query_loader()

    fe = FeatureExtractor(args.index,
                          max(multiprocessing.cpu_count() // 2, 1))
    for qfield, ifield in [('analyzed', 'contents'),
                           ('text_unlemm', 'text_unlemm'),
                           ('text_bert_tok', 'text_bert_tok')]:
        print(qfield, ifield)

        fe.add(BM25Stat(SumPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
        fe.add(BM25Stat(AvgPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
        fe.add(BM25Stat(MedianPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
        fe.add(BM25Stat(MaxPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
        fe.add(BM25Stat(MinPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
        fe.add(BM25Stat(MaxMinRatioPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))

        fe.add(LmDirStat(SumPooler(), mu=1000, field=ifield, qfield=qfield))
        fe.add(LmDirStat(AvgPooler(), mu=1000, field=ifield, qfield=qfield))
        fe.add(LmDirStat(MedianPooler(), mu=1000, field=ifield, qfield=qfield))
        fe.add(LmDirStat(MaxPooler(), mu=1000, field=ifield, qfield=qfield))
        fe.add(LmDirStat(MinPooler(), mu=1000, field=ifield, qfield=qfield))
        fe.add(LmDirStat(MaxMinRatioPooler(), mu=1000, field=ifield, qfield=qfield))

        fe.add(NormalizedTfIdf(field=ifield, qfield=qfield))
        fe.add(ProbalitySum(field=ifield, qfield=qfield))

        fe.add(DfrGl2Stat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(DfrGl2Stat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(DfrGl2Stat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(DfrGl2Stat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(DfrGl2Stat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(DfrGl2Stat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

        fe.add(DfrInExpB2Stat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(DfrInExpB2Stat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(DfrInExpB2Stat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(DfrInExpB2Stat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(DfrInExpB2Stat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(DfrInExpB2Stat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

        fe.add(DphStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(DphStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(DphStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(DphStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(DphStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(DphStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

        fe.add(Proximity(field=ifield, qfield=qfield))
        fe.add(TpScore(field=ifield, qfield=qfield))
        fe.add(TpDist(field=ifield, qfield=qfield))

        fe.add(DocSize(field=ifield))

        fe.add(QueryLength(qfield=qfield))
        fe.add(QueryCoverageRatio(qfield=qfield))
        fe.add(UniqueTermCount(qfield=qfield))
        fe.add(MatchingTermCount(field=ifield, qfield=qfield))
        fe.add(SCS(field=ifield, qfield=qfield))

        fe.add(TfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(TfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(TfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(TfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(TfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(TfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

        fe.add(TfIdfStat(True, AvgPooler(), field=ifield, qfield=qfield))
        fe.add(TfIdfStat(True, MedianPooler(), field=ifield, qfield=qfield))
        fe.add(TfIdfStat(True, SumPooler(), field=ifield, qfield=qfield))
        fe.add(TfIdfStat(True, MinPooler(), field=ifield, qfield=qfield))
        fe.add(TfIdfStat(True, MaxPooler(), field=ifield, qfield=qfield))
        fe.add(TfIdfStat(True, MaxMinRatioPooler(), field=ifield, qfield=qfield))

        fe.add(NormalizedTfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(NormalizedTfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(NormalizedTfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(NormalizedTfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(NormalizedTfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(NormalizedTfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

        fe.add(IdfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(IdfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(IdfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(IdfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(IdfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(IdfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

        fe.add(IcTfStat(AvgPooler(), field=ifield, qfield=qfield))
        fe.add(IcTfStat(MedianPooler(), field=ifield, qfield=qfield))
        fe.add(IcTfStat(SumPooler(), field=ifield, qfield=qfield))
        fe.add(IcTfStat(MinPooler(), field=ifield, qfield=qfield))
        fe.add(IcTfStat(MaxPooler(), field=ifield, qfield=qfield))
        fe.add(IcTfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

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

    start = time.time()
    fe.add(IbmModel1("collections/msmarco-ltr-passage/ibm_model/title_unlemm","text_unlemm","title_unlemm","text_unlemm"))
    end = time.time()
    print('IBM model Load takes %.2f seconds'%(end-start))
    start = end
    fe.add(IbmModel1("collections/msmarco-ltr-passage/ibm_model/url_unlemm","text_unlemm","url_unlemm","text_unlemm"))
    end = time.time()
    print('IBM model Load takes %.2f seconds'%(end-start))
    start = end
    fe.add(IbmModel1("collections/msmarco-ltr-passage/ibm_model/body","text_unlemm","body","text_unlemm"))
    end = time.time()
    print('IBM model Load takes %.2f seconds'%(end-start))
    start = end
    fe.add(IbmModel1("collections/msmarco-ltr-passage/ibm_model/text_bert_tok","text_bert_tok","text_bert_tok","text_bert_tok"))
    end = time.time()
    print('IBM model Load takes %.2f seconds'%(end-start))
    start = end

    train_extracted = data_loader('train', sampled_train, queries, fe)
    print("train_extracted")
    dev_extracted = data_loader('dev', dev, queries, fe)
    print("dev extracted")
    feature_name = fe.feature_names()
    del sampled_train, dev, queries, fe
    recall_at_20 = gen_dev_group_rel_num(dev_qrel, dev_extracted)
    print("start train")
    train_res = train(train_extracted, dev_extracted, feature_name, mrr_at_10)
    print("end train")
    eval_res = eval_mrr(dev_extracted['info'])
    eval_res.update(eval_recall(dev_qrel, dev_extracted['info']))

    dirname = gen_exp_dir()
    save_exp(dirname, train_extracted, dev_extracted, train_res, eval_res)
    total_time = (time.time() - total_start_time)
    print(f'Total training time: {total_time:0.3f} s')
    print('Done!')