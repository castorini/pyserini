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
sys.path.append('..')
sys.path.append('../pyserini')
import subprocess
from pyserini.pyclass import autoclass, JString

from enum import Enum
from typing import List
from typing import List, Set

import spacy
import struct
import math


JSimpleSearcher = autoclass('io.anserini.search.SimpleSearcher')
JIndexReader = autoclass('io.anserini.index.IndexReaderUtils')
JTerm = autoclass('org.apache.lucene.index.Term')
JDocumentFieldContext = autoclass('io.anserini.ltr.DocumentFieldContext')
JQueryFieldContext = autoclass('io.anserini.ltr.QueryFieldContext')
selfTrans = 0.05
minProb=5e-4
lambdaValue = 0.1
alpha=0

def normalize(scores):
    low = min(scores)
    high = max(scores)
    width = high - low

    return [(s-low)/width for s in scores]



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


def get_doc_to_id_from_qrun_by_topic(path: str, topic: str):
    res = {}
    with open(path, 'r') as f:
        for line in f:
            tokens = line.strip().split()
            t = tokens[0]
            if topic != t:
                continue
            doc_id = tokens[2]
            score = float(tokens[-2])
            res[doc_id] = score

    return res


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


def get_X_Y_from_qrels_by_topic(path: str, topic: str, R: List[int]):
    # always include topic 0
    R.append(0)
    qrels = [qrel for qrel in read_qrels(path) if qrel['topic'] == topic and qrel['relevance'] in R]
    x, y = [], []
    for pack in qrels:
        x.append(pack['doc_id'])
        label = 0 if pack['relevance'] == 0 else 1
        y.append(label)

    return x, y

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
    if curdir.endswith('clprf'):
       anserini_root = '../../../anserini'
    else:
       anserini_root = '../anserini'
    prefix = f"{anserini_root} {qrels_path}"
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



def get_ibm_score(query_text_lst,doc_token_lst, docSize,reader, fieldName,totalTermFreq,sourceLookup,targetLookup,tran):
    totalQueryProb = 0
    for querytoken in query_text_lst:
        totTranProb = 0
        collectProb = max(reader.totalTermFreq(JTerm(fieldName, querytoken))/totalTermFreq, 1e-9)
        if querytoken in targetLookup.keys():
            queryWordId = targetLookup[querytoken]
            for doctoken in doc_token_lst:
                tranProb = 0
                docWordId = 0
                if querytoken==doctoken:
                    tranProb = selfTrans   
                if doctoken in sourceLookup.keys():
                    docWordId = sourceLookup[doctoken]
                if docWordId in tran.keys():
                    targetMap = tran[docWordId]
                    if queryWordId in targetMap.keys():
                        tranProb = max(targetMap[queryWordId],tranProb)
                if (tranProb >= minProb):
                    totTranProb += (tranProb * ((1.0* doc_token_lst.count(doctoken)) / docSize))
            queryWordProb = totTranProb*(1-lambdaValue)+lambdaValue*collectProb
            #queryWordProb=math.log((1 - lambdaValue) * totTranProb + lambdaValue * collectProb) - math.log(lambdaValue * collectProb)
            if totalQueryProb ==0:
                totalQueryProb = queryWordProb
            else:
                #totalQueryProb = totalQueryProb+queryWordProb
                totalQueryProb = totalQueryProb*queryWordProb

    return totalQueryProb

def query_loader():
    queries = {}
    with open(f'../ltr/queries.dev.small.json') as f:
        for line in f:
            query = json.loads(line)
            qid = query.pop('id')
            query['analyzed'] = query['analyzed'].split(" ")
            query['text'] = query['text_unlemm'].split(" ")
            query['text_unlemm'] = query['text_unlemm'].split(" ")
            query['text_bert_tok'] = query['text_bert_tok'].split(" ")
            queries[qid] = query
    return queries


def intBitsToFloat(b):
   s = struct.pack('>l', b)
   return struct.unpack('>f', s)[0]

def _normalize(scores: List[float]):
    low = min(scores)
    high = max(scores)
    width = high - low

    return [(s-low)/width for s in scores]


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
            if sourceID in tranLookup.keys():
                tranLookup[sourceID][targetID] = tranProb
            else:
                tranLookup[sourceID] = {}
                tranLookup[sourceID][targetID] = tranProb
            byte = file.read(4)
    return sourceLookup,targetLookup,tranLookup


def rank(new_qrels: str, base: str,dir_path:str, lucene_index_path: str,output_path:str,score_path:str,fieldName:str, tag: str):

    # build output path
    searcher = JSimpleSearcher(JString(lucene_index_path))
    reader = JIndexReader().getReader(JString(lucene_index_path))
    sourceLookup,targetLookup,tran = load_tranProbsTable(dir_path)
    nlp = spacy.load('en_core_web_sm')
    totalTermFreq = reader.getSumTotalTermFreq(fieldName)
    doc_dic = get_docs_from_qrun_by_topic(base)
    

    f = open(output_path, 'w')

    skipped_topics = set()
    topics = get_topics_from_qrun(base)
    query= query_loader()
    i = 0
    for topic in topics:
        [test_docs, base_scores] = doc_dic[topic]
        rank_scores = []
        print(f"Reranking {i} query")
        j = 0
        i=i+1
        for test_doc in test_docs:
            document_text= json.loads(searcher.documentRaw(test_doc))[fieldName]
            doc_tokens = nlp(document_text)
            doc_token_lst  = [i.text for i in doc_tokens]
            docSize = len(doc_token_lst)
            query_text_lst = query[topic][fieldName]
            rank_score = get_ibm_score(query_text_lst,doc_token_lst, docSize,reader, fieldName,totalTermFreq,sourceLookup,targetLookup,tran)
            rank_scores.append(rank_score)      
            j=j+1
        ibm_scores = _normalize([p for p in rank_scores])
        base_scores = _normalize([p for p in base_scores])

        interpolated_scores = [a * alpha + b * (1-alpha) for a, b in zip(base_scores, ibm_scores)]

        preds, docs = sort_dual_list(interpolated_scores, test_docs)
        for index, (score, doc_id) in enumerate(zip(preds, docs)):
            rank = index + 1
            f.write(f'{topic} Q0 {doc_id} {rank} {score} {tag}\n')

    for topic in sort_str_topics_list(list(skipped_topics)):
        lines = get_lines_by_topic(base, topic, tag)
        print(f'Copying over skipped topic {topic} with {len(lines)} lines')
        for line in lines:
            f.write(f'{line}\n')

    f.close()
    map_score,ndcg_score = evaluate(new_qrels, output_path)
    with open(score_path, 'w') as outfile:
    	json.dump({'map':map_score,'ndcg':ndcg_score}, outfile)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='use tfidf vectorizer on cord-19 dataset with ccrf technique')
    parser.add_argument('-tag', type=str, default="ibm",
                        metavar="tag_name", help='tag name for resulting Qrun')
    parser.add_argument('-new_qrels', type=str, default="../tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt",
                        metavar="path_to_new_qrels", help='path to new_qrels file')
    parser.add_argument('-base', type=str, default="../ltr/run.msmarco-passage.bm25tuned.trec",
                        metavar="path_to_base_run", help='path to base run')
    parser.add_argument('-dir_path', type=str, default="../ltr/",
                        metavar="directory path", help='directory path')
    parser.add_argument('-index', type=str, default="../ltr/index-msmarco-passage-ltr-20210519-e25e33f",
                        metavar="path_to_lucene_index", help='path to lucene index folder')
    parser.add_argument('-output', type=str, default="../ltr/result-unittest.txt",
                        metavar="path_to_reranked_run", help='the path to reranked run file')
    parser.add_argument('-score_path', type=str, default="../ltr/result.json",
                        metavar="path_to_base_run", help='the path to map and ndcg scores')
    parser.add_argument('-fieldName', type=str, default="text_unlemm",
                        metavar="type of field", help='type of field used for training')
    args = parser.parse_args()

    print('Using base run:', args.base)
    rank(args.new_qrels, args.base, args.dir_path, args.index, args.output, args.score_path,args.fieldName, args.tag)
