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

import argparse
import os
import json
import sys
import time
sys.path.append('..')
sys.path.append('../pyserini')
from multiprocessing.pool import ThreadPool
import subprocess
from pyserini.pyclass import autoclass, JString

from typing import List
from typing import List, Set


import struct
import math


JSimpleSearcher = autoclass('io.anserini.search.SimpleSearcher')
JIndexReader = autoclass('io.anserini.index.IndexReaderUtils')
JTerm = autoclass('org.apache.lucene.index.Term')

selfTrans = 0.35
minProb=0.0025
lambdaValue = 0.3
minCollectProb=1e-9

def normalize(scores):
    low = min(scores)
    high = max(scores)
    width = high - low
    if width!=0:
        return [(s-low)/width for s in scores]
    else:
        return scores


def get_lines_by_topic(path, topic, tag):
    res = []
    with open(path, 'r') as f:
        for line in f:
            tokens = line.split()
            if tokens[0] != topic:
                continue
            tokens[-1] = tag
            new_line = ' '.join(tokens)
            res.append(new_line)

    return res


def read_qrels(path: str):
    qrels = []

    with open(path, 'r') as f:
        for line in f:
            line = line.strip()
            tokens = line.split()
            topic = tokens[0]
            doc_id = tokens[-2]
            relevance = int(tokens[-1])
            qrels.append({
                'topic': topic,
                'doc_id': doc_id,
                'relevance': relevance
            })

    return qrels


def get_docs_from_qrun_by_topic(path: str):
    result_dic={}
    with open(path, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            t = tokens[0]
            doc_id = tokens[2]
            score = float(tokens[-2])
            if t in result_dic.keys():
                result_dic[t][0].append(doc_id)
                result_dic[t][1].append(score)
            else:
                result_dic[t]=[[doc_id],[score]]

    return result_dic


def get_topics_from_qrun(path: str) -> Set[str]:
    res = set()
    with open(path, 'r') as f:
        for line in f:
            res.add(line.split()[0])
    return sort_str_topics_list(res)

def sort_str_topics_list(topics: List[str]) -> List[str]:
    res = sorted([int(t) for t in topics])
    return [str(t) for t in res]


def evaluate(qrels_path: str, run_path: str, options: str = ''):        
    curdir = os.getcwd()
    if curdir.endswith('scripts'):
       anserini_root = '../../anserini'
    else:
       anserini_root = '../anserini'
    prefix = f"{anserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -c -M1000 -m all_trec {qrels_path}"
    cmd1 = f"{prefix} {run_path} {options} | grep 'ndcg_cut_20 '"
    cmd2 = f"{prefix} {run_path} {options} | grep 'map                   	'"
    ndcg_score = str(subprocess.check_output(cmd1, shell=True)).split('\\t')[-1].split('\\n')[0]
    map_score = str(subprocess.check_output(cmd2, shell=True)).split('\\t')[-1].split('\\n')[0]
    print(str(map_score),str(ndcg_score))
    return str(map_score),str(ndcg_score)

def sort_dual_list(pred, docs):
    zipped_lists = zip(pred, docs)
    sorted_pairs = sorted(zipped_lists)

    tuples = zip(*sorted_pairs)
    pred, docs = [list(tuple) for tuple in tuples]

    pred.reverse()
    docs.reverse()
    return pred, docs



def get_ibm_score(arguments):
    query_text_lst = arguments['query_text_lst']
    test_doc = arguments['test_doc']
    searcher = arguments['searcher']
    fieldName = arguments['fieldName']
    sourceLookup = arguments['sourceLookup']
    targetLookup = arguments['targetLookup']
    tran = arguments['tran']
    collectProbs = arguments['collectProbs']
    #print(time.time())

    document_text= json.loads(searcher.documentRaw(test_doc))[fieldName]
    #print(time.time())
    doc_token_lst  = document_text.split(" ")
    totalQueryProb = 0
    docSize = len(doc_token_lst)
    querySize = len(query_text_lst)
    for querytoken in query_text_lst:
        targetMap = {}
        #print(time.time())
        totTranProb = 0
        collectProb = collectProbs[querytoken]
        if querytoken in targetLookup.keys():
            queryWordId = targetLookup[querytoken]
            if queryWordId in tran.keys():
                targetMap = tran[queryWordId]
                for doctoken in doc_token_lst:
                    tranProb = 0
                    docWordId = 0
                    if querytoken==doctoken:
                        tranProb = selfTrans  
                    if doctoken in sourceLookup.keys():
                        docWordId = sourceLookup[doctoken] 
                        if docWordId in targetMap.keys():
                            tranProb = max(targetMap[docWordId],tranProb)
                            totTranProb += (tranProb/docSize)

        queryWordProb=math.log((1 - lambdaValue) * totTranProb + lambdaValue * collectProb) - math.log(lambdaValue * collectProb)
        totalQueryProb += queryWordProb
    #print(time.time())
    return totalQueryProb /querySize



def query_loader(query_path):
    queries = {}
    with open(query_path) as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    return queries


def intBitsToFloat(b):
   s = struct.pack('>l', b)
   return struct.unpack('>f', s)[0]

def rescale(sourceLookup,targetLookup,tranLookup,targetVoc,sourceVoc):
    for targetID in tranLookup:
        targetProbs = tranLookup[targetID]
        if targetID > 0:
            adjustMult = (1 - selfTrans) 
        else:
            adjustMult = 1
        #adjust the prob with adjustMult and add selfTran prob to self-translation pair
        for sourceID in targetProbs.keys():
            tranProb = targetProbs[sourceID]
            if sourceID >0:
                sourceWord = sourceVoc[sourceID]
                targetWord = targetVoc[targetID]
                tranProb *= adjustMult
                if (sourceWord== targetWord):
                    tranProb += selfTrans
                targetProbs[sourceID]= tranProb
        # in case if self-translation pair was not included in TransTable
        if targetID not in targetProbs.keys():
            targetProbs[targetID]= selfTrans
    return sourceLookup,targetLookup,tranLookup



def load_tranProbsTable(dir_path):
    source_path = dir_path +"/source.vcb"
    sourceLookup = {}
    sourceVoc={}
    with open(source_path) as f:
        lines = f.readlines()
    for line in lines:
        id, voc,freq = line.split(" ")
        sourceVoc[int(id)] = voc
        sourceLookup[voc]=int(id)

    target_path = dir_path +"/target.vcb"
    targetLookup = {}
    targetVoc = {}
    with open(target_path) as f:
        lines = f.readlines()
    for line in lines:
        id, voc,freq = line.split(" ")
        targetVoc[int(id)] = voc
        targetLookup[voc]=int(id)
    
    tran_path = dir_path + "/output.t1.5.bin"
    tranLookup = {}
    with open(tran_path, "rb") as file:
        byte = file.read(4)
        while byte:
            sourceID = int.from_bytes(byte,"big")
            assert(sourceID == 0 or sourceID in sourceVoc.keys())
            byte = file.read(4)
            targetID = int.from_bytes(byte,"big")
            assert(targetID in targetVoc.keys())
            byte = file.read(4)
            #tranProb = float.from_bytes(byte)
            tranProb = intBitsToFloat(int.from_bytes(byte,"big"))
            if (targetID in tranLookup.keys()) and (tranProb>minProb):
                tranLookup[targetID][sourceID] = tranProb
            elif tranProb>minProb:
                tranLookup[targetID] = {}
                tranLookup[targetID][sourceID] = tranProb
            byte = file.read(4)
    return rescale(sourceLookup,targetLookup,tranLookup,targetVoc,sourceVoc)


def rank(qrels: str, base: str,tran_path:str, query_path:str, lucene_index_path: str,output_path:str,score_path:str,fieldName:str, tag: str,alpha:int,num_threads:int):
    #print(time.time())
    # build output path
    pool = ThreadPool(num_threads)
    searcher = JSimpleSearcher(JString(lucene_index_path))
    reader = JIndexReader().getReader(JString(lucene_index_path))

    sourceLookup,targetLookup,tran = load_tranProbsTable(tran_path)
    totalTermFreq = reader.getSumTotalTermFreq(fieldName)
    doc_dic = get_docs_from_qrun_by_topic(base)
    
    f = open(output_path, 'w')

    topics = get_topics_from_qrun(base)
    query= query_loader(query_path)
    
    i = 0
    #print(time.time())
    for topic in topics:
        #print(time.time())
        [test_docs, base_scores] = doc_dic[topic]
        rank_scores = []
        if i % 100==0:
            print(f"Reranking {i} query")
        i=i+1
        query_text_lst = query[topic][fieldName]
        collectProbs ={}
        for querytoken in query_text_lst:
            collectProbs[querytoken] = max(reader.totalTermFreq(JTerm(fieldName, querytoken))/totalTermFreq, minCollectProb)
        arguments = [{"query_text_lst":query_text_lst,"test_doc":test_doc, "searcher":searcher,"fieldName":fieldName,"sourceLookup":sourceLookup,"targetLookup":targetLookup,"tran":tran,"collectProbs":collectProbs} for test_doc in test_docs]
        #print(time.time())
        #print(time.time())
        rank_scores = pool.map(get_ibm_score, arguments)    
        ibm_scores = normalize([p for p in rank_scores])
        #print(time.time())
        base_scores = normalize([p for p in base_scores])

        interpolated_scores = [a * alpha + b * (1-alpha) for a, b in zip(base_scores, ibm_scores)]

        preds, docs = sort_dual_list(interpolated_scores, test_docs)
        for index, (score, doc_id) in enumerate(zip(preds, docs)):
            rank = index + 1
            f.write(f'{topic} Q0 {doc_id} {rank} {score} {tag}\n')


    f.close()
    map_score,ndcg_score = evaluate(qrels, output_path)
    with open(score_path, 'w') as outfile:
    	json.dump({'map':map_score,'ndcg':ndcg_score}, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='use ibm model 1 feature to rerank the base run file')
    parser.add_argument('-tag', type=str, default="ibm",
                        metavar="tag_name", help='tag name for resulting Qrun')
    parser.add_argument('-qrels', type=str, default="../tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt",
                        metavar="path_to_qrels", help='path to new_qrels file')
    parser.add_argument('-base', type=str, default="../ibm/run.msmarco-passage.bm25tuned.trec",
                        metavar="path_to_base_run", help='path to base run')
    parser.add_argument('-tran_path', type=str, default="../ibm/ibm_model/text_bert_tok_raw",
                        metavar="directory_path", help='directory path to source.vcb target.vcb and Transtable bin file')
    parser.add_argument('-query_path', type=str, default="../ibm/queries.dev.small.json",
                        metavar="path_to_query", help='path to dev queries file')
    parser.add_argument('-index', type=str, default="../ibm/index-msmarco-passage-ltr-20210519-e25e33f",
                        metavar="path_to_lucene_index", help='path to lucene index folder')
    parser.add_argument('-output', type=str, default="../ibm/runs/result-text-bert-0.5-new.txt",
                        metavar="path_to_reranked_run", help='the path to store reranked run file')
    parser.add_argument('-score_path', type=str, default="../ibm/result-ibm-0.5-new.json",
                        metavar="path_to_base_run", help='the path to map and ndcg scores')
    parser.add_argument('-fieldName', type=str, default="text_bert_tok",
                        metavar="type of field", help='type of field used for training')
    parser.add_argument('-alpha', type=float, default="0.5",
                        metavar="type of field", help='interpolation weight')
    parser.add_argument('-num_threads', type=int, default="12",
                        metavar="num_of_threads", help='number of threads to use')
    args = parser.parse_args()

    print('Using base run:', args.base)

    rank(args.qrels, args.base, args.tran_path, args.query_path, args.index, args.output, args.score_path,args.fieldName, args.tag,args.alpha,args.num_threads)
