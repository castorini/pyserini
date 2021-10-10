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
from pyserini.index import IndexReader

"""
Running prediction on candidates
"""
def dev_data_loader(file, format, index, top):
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
    #empty = ['D2678125#0', 'D2702064#1', 'D2702064#2', 'D2702064#3', 'D2702064#4', 'D2702064#5', 'D2702064#10', 'D2702064#11', 'D2702064#12', 'D2702064#13', 'D1449555#0', 'D373675#0', 'D118630#0', 'D453334#0', 'D2158073#0', 'D700793#0', 'D2488975#0', 'D3488583#0', 'D1513567#19', 'D1480207#4', 'D1480207#5', 'D1480207#6', 'D1480207#7', 'D1480207#8', 'D1480207#9', 'D2830694#0', 'D1950298#0', 'D3294124#52', 'D3294124#53', 'D3294124#54', 'D1993713#4', 'D1993713#5', 'D1993713#6', 'D1993713#7', 'D1993713#8', 'D1993713#9', 'D1993713#10', 'D1993713#11', 'D1993713#12', 'D1993713#13', 'D3155926#0', 'D654450#0', 'D3122032#0', 'D2434762#1', 'D319435#0', 'D1744921#0', 'D2956295#1', 'D908750#11', 'D908750#12', 'D176857#0', 'D3236444#0', 'D3073913#1', 'D3073913#2', 'D3499927#0', 'D2627823#0', 'D63619#0', 'D3248276#0', 'D3071480#0', 'D3545844#18', 'D3158344#0', 'D2259853#0', 'D1304071#0', 'D432128#0', 'D3117106#0', 'D755747#0', 'D2457589#0', 'D368125#120', 'D368125#135', 'D2967976#1', 'D2967976#2', 'D2967976#3', 'D2967976#4', 'D2967976#5', 'D2967976#6', 'D2967976#7', 'D501086#0', 'D2282501#5', 'D2282501#6', 'D3359644#2', 'D3118653#0', 'D2706215#0', 'D2876596#0', 'D1334381#1', 'D1334381#2', 'D1334381#3', 'D1334381#4', 'D1334381#5', 'D1334381#6', 'D1334381#7', 'D1334381#8', 'D1334381#9', 'D1334381#10', 'D1334381#11', 'D1334381#12', 'D1334381#13', 'D1304294#0', 'D531211#0', 'D3279799#0', 'D792692#0', 'D2034590#0', 'D179603#0', 'D1780978#3', 'D2199178#0', 'D1020946#0', 'D1909343#0', 'D2702708#0', 'D789890#3', 'D3501712#0', 'D1235350#0', 'D2762875#0', 'D2967570#0', 'D324027#0', 'D1459422#0', 'D2323002#0', 'D2911709#2', 'D2911709#3', 'D2911709#4', 'D2911709#5', 'D2911709#6', 'D2911709#7', 'D2911709#8', 'D2911709#9', 'D2911709#10', 'D2911709#11', 'D2911709#12', 'D2911709#13', 'D2911709#14', 'D2911709#15', 'D2911709#16', 'D2911709#17', 'D2911709#18', 'D2911709#19', 'D2911709#20', 'D2911709#21', 'D2911709#22', 'D2911709#23', 'D2911709#24', 'D2911709#25', 'D2911709#26', 'D2911709#27', 'D188871#0', 'D586242#0', 'D14391#0', 'D881676#0', 'D3552537#0', 'D712008#6', 'D3386336#9', 'D3386336#10', 'D3386336#11', 'D3386336#12', 'D250119#0', 'D396605#7', 'D530106#0', 'D216281#0', 'D1266112#0', 'D945002#0', 'D2507602#0', 'D3190426#0', 'D126263#0', 'D2738829#0', 'D2123382#0', 'D1871070#1', 'D1871070#2', 'D1871070#3', 'D1871070#4', 'D1871070#5', 'D1871070#6', 'D1871070#7', 'D1871070#8', 'D974080#0', 'D958285#0', 'D46929#0', 'D2371808#3', 'D1389152#0', 'D1883125#5']
    #dev = dev.loc[~dev.pid.isin(empty)]
    print(dev.shape)
    dev_qrel = pd.read_csv('tools/topics-and-qrels/qrels.msmarco-doc.dev.txt', sep="\t",
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


def output(file, dev_data,format):
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
            if (format == 'tsv'):
                output_file.write(f"{qid}\t{t.pid}\t{rank}\n")
            else:
                output_file.write(f"{qid}\tq0\t{t.pid}\t{rank}\t{t.score}\tltr\n")

    score_tie = f'score_tie occurs {score_tie_counter} times in {len(score_tie_query)} queries'
    print(score_tie)

if __name__ == "__main__":
    os.environ["ANSERINI_CLASSPATH"] = "./pyserini/resources/jars"
    parser = argparse.ArgumentParser(description='Learning to rank reranking')
    parser.add_argument('--input', required=True)
    parser.add_argument('--reranking-top', type=int, default=10000)
    parser.add_argument('--input-format', required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--index', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--ibm-model',default='./collections/msmarco-ltr-passage/ibm_model/')
    parser.add_argument('--queries',default='./collections/msmarco-ltr-document/')
    parser.add_argument('--output-format',default='trec')

    args = parser.parse_args()
    print("load dev")
    dev, dev_qrel = dev_data_loader(args.input, args.input_format, args.index, args.reranking_top)
    print("load queries")
    queries = query_loader()
    searcher = MsmarcoPassageLtrSearcher(args.model, args.ibm_model, args.index)
    searcher.add_fe()

    batch_info = searcher.search(dev, queries)
    del dev, queries

    eval_res = eval_mrr(batch_info)
    eval_recall(dev_qrel, batch_info)
    output(args.output, batch_info, args.output_format)
    print('Done!')