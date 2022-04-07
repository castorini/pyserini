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
import numpy as np
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from transformers import AutoTokenizer
from pyserini.search.lucene.ltr._search_msmarco import MsmarcoLtrSearcher
from pyserini.search.lucene.ltr import *
from pyserini.search.lucene import LuceneSearcher
from pyserini.analysis import Analyzer, get_lucene_analyzer

"""
Running prediction on candidates
"""
def dev_data_loader(file, format, topic, rerank, prebuilt, qrel, granularity, top=1000):
    if rerank:
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
        assert dev['qid'].dtype == object
        assert dev['pid'].dtype == object
        assert dev['rank'].dtype == np.int32
        dev = dev[dev['rank']<=top]
    else:
        if prebuilt:
            bm25search = LuceneSearcher.from_prebuilt_index(args.index)
        else:
            bm25search = LuceneSearcher(args.index)
        bm25search.set_bm25(0.82, 0.68)
        dev_dic = {"qid":[], "pid":[], "rank":[]}
        for topic in tqdm(queries.keys()):
            query_text = queries[topic]['raw']
            bm25_dev = bm25search.search(query_text, args.hits)
            doc_ids = [bm25_result.docid for bm25_result in bm25_dev]
            qid = [topic for _ in range(len(doc_ids))]
            rank = [i for i in range(1, len(doc_ids)+1)]
            dev_dic['qid'].extend(qid)
            dev_dic['pid'].extend(doc_ids)
            dev_dic['rank'].extend(rank)
        dev = pd.DataFrame(dev_dic)
        dev['rank'].astype(np.int32)
    if granularity == 'document':
        seperation = "\t"
    else:
        seperation = " "
    dev_qrel = pd.read_csv(qrel, sep=seperation,
                            names=["qid", "q0", "pid", "rel"], usecols=['qid', 'pid', 'rel'],
                            dtype={'qid': 'S','pid': 'S', 'rel':'i'})
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


def query_loader(topic):
    queries = {}
    nlp = SpacyTextParser('en_core_web_sm', keep_only_alpha_num=True, lower_case=True)
    analyzer = Analyzer(get_lucene_analyzer())
    bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
    inp_file = open(topic)
    ln = 0
    for line in tqdm(inp_file):
        ln += 1
        line = line.strip()
        if not line:
            continue
        fields = line.split('\t')
        if len(fields) != 2:
            print('Misformated line %d ignoring:' % ln)
            print(line.replace('\t', '<field delimiter>'))
            continue
        did, query = fields
        query_lemmas, query_unlemm = nlp.proc_text(query)
        analyzed = analyzer.analyze(query)
        for token in analyzed:
            if ' ' in token:
                print(analyzed)
        query_toks = query_lemmas.split()
        if len(query_toks) >= 0:
            query = {"raw" : query,
                "text": query_lemmas.split(' '),
                "text_unlemm": query_unlemm.split(' '),
                "analyzed": analyzed,
                "text_bert_tok": bert_tokenizer.tokenize(query.lower())}
            queries[did] = query

        if ln % 10000 == 0:
            print('Processed %d queries' % ln)

    print('Processed %d queries' % ln)
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


def output(file, dev_data, format, maxp):
    score_tie_counter = 0
    score_tie_query = set()
    output_file = open(file,'w')
    results = defaultdict(dict)
    idx = 0
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
            if maxp:
                docid = t.pid.split('#')[0]
                if qid not in results or docid not in results[qid] or t.score > results[qid][docid]:
                    results[qid][docid] = t.score
            else:
                results[qid][t.pid] = t.score
            

    for qid in tqdm(results.keys()):
        rank = 1
        docid_score = results[qid]
        docid_score = sorted(docid_score.items(),key=lambda kv: kv[1], reverse=True)
        for docid, score in docid_score:
            if format=='trec':
                output_file.write(f"{qid}\tQ0\t{docid}\t{rank}\t{score}\tltr\n")
            else:
                output_file.write(f"{qid}\t{docid}\t{rank}\n")
            rank += 1
    score_tie = f'score_tie occurs {score_tie_counter} times in {len(score_tie_query)} queries'
    print(score_tie)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Learning to rank reranking')
    parser.add_argument('--input', default='')
    parser.add_argument('--hits', type=int, default=1000)
    parser.add_argument('--input-format', default = 'trec')
    parser.add_argument('--model', required=True)
    parser.add_argument('--index', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--ibm-model', required=True)
    parser.add_argument('--topic', required=True)
    parser.add_argument('--output-format', default='tsv')
    parser.add_argument('--max-passage', action='store_true')
    parser.add_argument('--rerank', action='store_true')
    parser.add_argument('--qrel', required=True)
    parser.add_argument('--granularity', default='passage')

    args = parser.parse_args()
    queries = query_loader(args.topic)
    print("---------------------loading dev----------------------------------------")
    prebuilt = args.index == 'msmarco-passage-ltr' or args.index == 'msmarco-doc-per-passage-ltr'
    dev, dev_qrel = dev_data_loader(args.input, args.input_format, args.topic, args.rerank, prebuilt, args.qrel, args.granularity, args.hits)
    searcher = MsmarcoLtrSearcher(args.model, args.ibm_model, args.index, args.granularity, prebuilt, args.topic)
    searcher.add_fe()
    batch_info = searcher.search(dev, queries)
    del dev, queries

    eval_res = eval_mrr(batch_info)
    eval_recall(dev_qrel, batch_info)
    output(args.output, batch_info,args.output_format, args.max_passage)
    print('Done!')