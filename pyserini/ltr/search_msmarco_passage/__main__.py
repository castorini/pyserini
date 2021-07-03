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
from pyserini.ltr.search_msmarco_passage._search_msmarco_passage import MsmarcoPassageLtrSearcher
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
    dev_qrel = pd.read_csv('tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt', sep=" ",
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
    with open(f'{args.queries}/queries.dev.small.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    return queries


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

if __name__ == "__main__":
    os.environ["ANSERINI_CLASSPATH"] = "./pyserini/resources/jars"
    parser = argparse.ArgumentParser(description='Learning to rank reranking')
    parser.add_argument('--input', required=True)
    parser.add_argument('--reranking-top', type=int, default=1000)
    parser.add_argument('--input-format', required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--index', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--ibm-model',default='./collections/msmarco-ltr-passage/ibm_model/')
    parser.add_argument('--queries',default='./collections/msmarco-ltr-passage/')

    args = parser.parse_args()
    searcher = MsmarcoPassageLtrSearcher(args.model, args.ibm_model, args.index)
    searcher.add_fe()
    print("load dev")
    dev, dev_qrel = dev_data_loader(args.input, args.input_format, args.reranking_top)
    print("load queries")
    queries = query_loader()

    batch_info = searcher.search(dev, queries)
    del dev, queries

    eval_res = eval_mrr(batch_info)
    eval_recall(dev_qrel, batch_info)
    output(args.output, batch_info)
    print('Done!')


