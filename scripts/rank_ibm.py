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
from multiprocessing.pool import ThreadPool
import subprocess
from pyserini.pyclass import autoclass, JString

from typing import List, Set, Dict


import struct
import math


JSimpleSearcher = autoclass('io.anserini.search.SimpleSearcher')
JIndexReader = autoclass('io.anserini.index.IndexReaderUtils')
JTerm = autoclass('org.apache.lucene.index.Term')

SELF_TRAN = 0.35
MIN_PROB=0.0025
LAMBDA_VALUE = 0.3
MIN_COLLECT_PROB=1e-9

def normalize(scores: List[float]):
    low = min(scores)
    high = max(scores)
    width = high - low
    if width!=0:
        return [(s-low)/width for s in scores]
    else:
        return scores


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
    return str(map_score),str(ndcg_score)

def sort_dual_list(pred: List[float], docs: List[str]):
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
    field_name = arguments['field_name']
    source_lookup = arguments['source_lookup']
    target_lookup = arguments['target_lookup']
    tran = arguments['tran']
    collect_probs = arguments['collect_probs']

    if searcher.documentRaw(test_doc) ==None:
        print(f'{test_doc} is not found in searcher')
    document_text= json.loads(searcher.documentRaw(test_doc))[field_name]
    doc_token_lst  = document_text.split(" ")
    total_query_prob = 0
    doc_size = len(doc_token_lst)
    query_size = len(query_text_lst)
    for querytoken in query_text_lst:
        target_map = {}
        total_tran_prob = 0
        collect_prob = collect_probs[querytoken]
        if querytoken in target_lookup.keys():
            query_word_id = target_lookup[querytoken]
            if query_word_id in tran.keys():
                target_map = tran[query_word_id]
                for doctoken in doc_token_lst:
                    tran_prob = 0
                    doc_word_id = 0
                    if querytoken==doctoken:
                        tran_prob = SELF_TRAN  
                    if doctoken in source_lookup.keys():
                        doc_word_id = source_lookup[doctoken] 
                        if doc_word_id in target_map.keys():
                            tran_prob = max(target_map[doc_word_id],tran_prob)
                            total_tran_prob += (tran_prob/doc_size)

        query_word_prob=math.log((1 - LAMBDA_VALUE) * total_tran_prob + LAMBDA_VALUE * collect_prob) 

        total_query_prob += query_word_prob
    return total_query_prob /query_size



def query_loader(query_path: str):
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


def intbits_to_float(b: bytes):
   s = struct.pack('>l', b)
   return struct.unpack('>f', s)[0]

def rescale(source_lookup: Dict[str,int],target_lookup: Dict[str,int],tran_lookup: Dict[str,Dict[str,float]],\
            target_voc: Dict[int,str],source_voc: Dict[int,str]):
    for target_id in tran_lookup:
        target_probs = tran_lookup[target_id]
        if target_id > 0:
            adjust_mult = (1 - SELF_TRAN) 
        else:
            adjust_mult = 1
        #adjust the prob with adjust_mult and add SELF_TRAN prob to self-translation pair
        for source_id in target_probs.keys():
            tran_prob = target_probs[source_id]
            if source_id >0:
                source_word = source_voc[source_id]
                target_word = target_voc[target_id]
                tran_prob *= adjust_mult
                if (source_word== target_word):
                    tran_prob += SELF_TRAN
                target_probs[source_id]= tran_prob
        # in case if self-translation pair was not included in TransTable
        if target_id not in target_probs.keys():
            target_probs[target_id]= SELF_TRAN
    return source_lookup,target_lookup,tran_lookup



def load_tranprobs_table(dir_path: str):
    source_path = dir_path +"/source.vcb"
    source_lookup = {}
    source_voc={}
    with open(source_path) as f:
        lines = f.readlines()
    for line in lines:
        id, voc,freq = line.split(" ")
        source_voc[int(id)] = voc
        source_lookup[voc]=int(id)

    target_path = dir_path +"/target.vcb"
    target_lookup = {}
    target_voc = {}
    with open(target_path) as f:
        lines = f.readlines()
    for line in lines:
        id, voc,freq = line.split(" ")
        target_voc[int(id)] = voc
        target_lookup[voc]=int(id)
    
    tran_path = dir_path + "/output.t1.5.bin"
    tran_lookup = {}
    with open(tran_path, "rb") as file:
        byte = file.read(4)
        while byte:
            source_id = int.from_bytes(byte,"big")
            assert(source_id == 0 or source_id in source_voc.keys())
            byte = file.read(4)
            target_id = int.from_bytes(byte,"big")
            assert(target_id in target_voc.keys())
            byte = file.read(4)
            tran_prob = intbits_to_float(int.from_bytes(byte,"big"))
            if (target_id in tran_lookup.keys()) and (tran_prob>MIN_PROB):
                tran_lookup[target_id][source_id] = tran_prob
            elif tran_prob>MIN_PROB:
                tran_lookup[target_id] = {}
                tran_lookup[target_id][source_id] = tran_prob
            byte = file.read(4)
    return rescale(source_lookup,target_lookup,tran_lookup,target_voc,source_voc)


def rank(qrels: str, base: str,tran_path:str, query_path:str, lucene_index_path: str,output_path:str, \
        score_path:str,field_name:str, tag: str,alpha:int,num_threads:int):

    pool = ThreadPool(num_threads)
    searcher = JSimpleSearcher(JString(lucene_index_path))
    reader = JIndexReader().getReader(JString(lucene_index_path))

    source_lookup,target_lookup,tran = load_tranprobs_table(tran_path)
    total_term_freq = reader.getSumTotalTermFreq(field_name)
    doc_dic = get_docs_from_qrun_by_topic(base)
    
    f = open(output_path, 'w')

    topics = get_topics_from_qrun(base)
    query= query_loader(query_path)
    
    i = 0
    for topic in topics:
        [test_docs, base_scores] = doc_dic[topic]
        rank_scores = []
        if i % 100==0:
            print(f"Reranking {i} query")
        i=i+1
        query_text_lst = query[topic][field_name]
        collect_probs ={}
        for querytoken in query_text_lst:
            collect_probs[querytoken] = max(reader.totalTermFreq(JTerm(field_name, querytoken))/total_term_freq, MIN_COLLECT_PROB)
        arguments = [{"query_text_lst":query_text_lst,"test_doc":test_doc, "searcher":searcher,\
                "field_name":field_name,"source_lookup":source_lookup,"target_lookup":target_lookup,\
                "tran":tran,"collect_probs":collect_probs} for test_doc in test_docs]
        rank_scores = pool.map(get_ibm_score, arguments)   

        ibm_scores = normalize([p for p in rank_scores])
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
    parser.add_argument('-tran_path', type=str, default="../ibm/ibm_model/text_bert_tok",
                        metavar="directory_path", help='directory path to source.vcb target.vcb and Transtable bin file')
    parser.add_argument('-query_path', type=str, default="../ibm/queries.dev.small.json",
                        metavar="path_to_query", help='path to dev queries file')
    parser.add_argument('-index', type=str, default="../ibm/index-msmarco-passage-ltr-20210519-e25e33f",
                        metavar="path_to_lucene_index", help='path to lucene index folder')
    parser.add_argument('-output', type=str, default="../ibm/runs/result-text-bert-tuned0.1.txt",
                        metavar="path_to_reranked_run", help='the path to store reranked run file')
    parser.add_argument('-score_path', type=str, default="../ibm/result-ibm-0.1.json",
                        metavar="path_to_base_run", help='the path to map and ndcg scores')
    parser.add_argument('-field_name', type=str, default="text_bert_tok",
                        metavar="type of field", help='type of field used for training')
    parser.add_argument('-alpha', type=float, default="0.1",
                        metavar="type of field", help='interpolation weight')
    parser.add_argument('-num_threads', type=int, default="12",
                        metavar="num_of_threads", help='number of threads to use')
    args = parser.parse_args()

    print('Using base run:', args.base)

    rank(args.qrels, args.base, args.tran_path, args.query_path, args.index, args.output, \
        args.score_path,args.field_name, args.tag,args.alpha,args.num_threads)
