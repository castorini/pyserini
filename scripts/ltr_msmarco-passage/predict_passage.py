#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

import sys

# We're going to explicitly use a local installation of Pyserini (as opposed to a pip-installed one).
# Comment these lines out to use a pip-installed one instead.
sys.path.insert(0, './')

import argparse
import json
import multiprocessing
import os
import pickle
import time

import numpy as np
import pandas as pd
from tqdm import tqdm
from pyserini.ltr import *

"""
Running prediction on candidates
"""
def dev_data_loader(file, format, top=100):
    if format == 'tsv':
        dev = pd.read_csv(file, sep="\t",
                          names=['qid', 'pid', 'rank'],
                          dtype={'qid': 'S','pid': 'S', 'rank':'i',})
    elif format == 'trec':
        dev = pd.read_csv(file, sep="\s+",
                    names=['qid', 'q0', 'pid', 'rank', 'score', 'tag'],
                    usecols=['qid', 'pid', 'rank'],
                    dtype={'qid': 'S','pid': 'S', 'rank':'i',})
    else:
        raise Exception('unknown parameters')
    assert dev['qid'].dtype == np.object
    assert dev['pid'].dtype == np.object
    assert dev['rank'].dtype == np.int32
    dev = dev[dev['rank']<=top]
    dev_qrel = pd.read_csv('./collections/msmarco-passage/qrels.dev.small.tsv', sep="\t",
                           names=["qid", "q0", "pid", "rel"], usecols=['qid', 'pid', 'rel'],
                           dtype={'qid': 'S','pid': 'S', 'rel':'i'})
    assert dev['qid'].dtype == np.object
    assert dev['pid'].dtype == np.object
    assert dev['rank'].dtype == np.int32
    dev = dev.merge(dev_qrel, left_on=['qid', 'pid'], right_on=['qid', 'pid'], how='left')
    dev['rel'] = dev['rel'].fillna(0).astype(np.int32)
    dev = dev.sort_values(['qid', 'pid']).set_index(['qid', 'pid'])

    print(dev.shape)
    print(dev.index.get_level_values('qid').drop_duplicates().shape)
    print(dev.groupby('qid').count().mean())
    print(dev.head(10))
    print(dev.info())

    dev_rel_num = dev_qrel[dev_qrel['rel'] > 0].groupby('qid').count()['rel']

    recall_point = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    recall_curve = {k: [] for k in recall_point}
    for qid, group in tqdm(dev.groupby('qid')):
        group = group.reset_index()
        assert len(group['pid'].tolist()) == len(set(group['pid'].tolist()))
        total_rel = dev_rel_num.loc[qid]
        query_recall = [0 for k in recall_point]
        for t in group.sort_values('rank').itertuples():
            if t.rel > 0:
                for i, p in enumerate(recall_point):
                    if t.rank <= p:
                        query_recall[i] += 1
        for i, p in enumerate(recall_point):
            if total_rel > 0:
                recall_curve[p].append(query_recall[i] / total_rel)
            else:
                recall_curve[p].append(0.)

    for k, v in recall_curve.items():
        avg = np.mean(v)
        print(f'recall@{k}:{avg}')

    return dev, dev_qrel


def query_loader():
    queries = {}
    with open('collections/msmarco-ltr-passage/queries.train.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    with open('collections/msmarco-ltr-passage/queries.dev.small.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    with open('collections/msmarco-ltr-passage/queries.eval.small.json') as f:
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

    for qid, group in tqdm(df.groupby('qid')):
        task = {
            "qid": qid,
            "docIds": [],
            "rels": [],
            "query_dict": queries[qid]
        }
        for t in group.reset_index().itertuples():
            task["docIds"].append(t.pid)
            task_infos.append((qid, t.pid, t.rel))
        tasks.append(task)
        group_lst.append((qid, len(task['docIds'])))
        if len(tasks) == 1000:
            features = fe.batch_extract(tasks)
            task_infos = pd.DataFrame(task_infos, columns=['qid', 'pid', 'rel'])
            group = pd.DataFrame(group_lst, columns=['qid', 'count'])
            print(features.shape)
            print(task_infos.qid.drop_duplicates().shape)
            print(group.mean())
            print(features.head(10))
            print(features.info())
            yield task_infos, features, group
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
        yield task_infos, features, group

    return

def batch_predict(models, dev_extracted, feature_name):
    task_infos, features, group = dev_extracted
    dev_X = features.loc[:, feature_name]

    task_infos['score'] = 0.
    for gbm in models:
        task_infos['score'] += gbm.predict(dev_X)


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

    recall_point = [10,20,50,100,200,250,300,333,400,500,1000]
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
            output_file.write(f"{qid}\t{t.pid}\t{rank}\n")

    score_tie = f'score_tie occurs {score_tie_counter} times in {len(score_tie_query)} queries'
    print(score_tie)


if __name__ == '__main__':
    os.environ["ANSERINI_CLASSPATH"] = "./pyserini/resources/jars"
    parser = argparse.ArgumentParser(description='Learning to rank')
    parser.add_argument('--rank_list_path', required=True)
    parser.add_argument('--rank_list_top', type=int, default=1000)
    parser.add_argument('--rank_list_format', required=True)
    parser.add_argument('--ltr_model_path', required=True)
    parser.add_argument('--ltr_output_path', required=True)

    args = parser.parse_args()
    print("load dev")
    dev, dev_qrel = dev_data_loader(args.rank_list_path, args.rank_list_format, args.rank_list_top)
    print("load queries")
    queries = query_loader()
    print("add feature")
    fe = FeatureExtractor('./indexes/lucene-index-msmarco-passage-ltr', max(multiprocessing.cpu_count()//2, 1))
    for qfield, ifield in [('analyzed', 'contents'),
                           ('text', 'text'),
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
    fe.add(
        IbmModel1("collections/msmarco-ltr-passage/ibm_model/title_unlemm", "text_unlemm", "title_unlemm",
                  "text_unlemm"))
    end = time.time()
    print('IBM model Load takes %.2f seconds' % (end - start))
    start = end
    fe.add(IbmModel1("collections/msmarco-ltr-passage/ibm_model/url_unlemm", "text_unlemm", "url_unlemm",
                     "text_unlemm"))
    end = time.time()
    print('IBM model Load takes %.2f seconds' % (end - start))
    start = end
    fe.add(
        IbmModel1("collections/msmarco-ltr-passage/ibm_model/body", "text_unlemm", "body", "text_unlemm"))
    end = time.time()
    print('IBM model Load takes %.2f seconds' % (end - start))
    start = end
    fe.add(IbmModel1("collections/msmarco-ltr-passage/ibm_model/text_bert_tok", "text_bert_tok",
                     "text_bert_tok", "text_bert_tok"))
    end = time.time()
    print('IBM model Load takes %.2f seconds' % (end - start))
    start = end

    models = pickle.load(open(args.ltr_model_path+'/model.pkl', 'rb'))
    metadata = json.load(open(args.ltr_model_path+'/metadata.json', 'r'))
    feature_used = metadata['feature_names']

    batch_info = []
    start_extract = time.time()
    for dev_extracted in batch_extract(dev, queries, fe):
        end_extract = time.time()
        print(f'extract 1000 queries take {end_extract - start_extract}s')
        task_infos, features, group = dev_extracted
        start_predict = time.time()
        batch_predict(models, dev_extracted, feature_used)
        end_predict = time.time()
        print(f'predict 1000 queries take {end_predict - start_predict}s')
        batch_info.append(task_infos)
        start_extract = time.time()
    batch_info = pd.concat(batch_info, axis=0, ignore_index=True)
    del dev, queries, fe

    eval_res = eval_mrr(batch_info)
    eval_recall(dev_qrel, batch_info)
    output(args.ltr_output_path, batch_info)
    print('Done!')