#Title: TREC_COVID_Round1_OHSU.py
#Author: Jimmy Chen, School of Medicine, OHSU
#Description: Generate 1000 documents per topic in Round 1 TREC_COVID and get trec_eval metrics

# To replicate OSHU_RUN2
# Results: https://ir.nist.gov/covidSubmit/archive/round1/OHSU_RUN2.pdf
#
# In root pyserini directory:
#
# 1. wget https://www.dropbox.com/s/gtq2c3xq81mjowk/lucene-index-covid-full-text-2020-04-10.tar.gz
# 2. tar xvfz lucene-index-covid-full-text-2020-04-10.tar.gz
# 3. python bin/generate_trec_covid_round1_OSHU_RUN2.py
# 4. trec_eval -c -q -M1000 -m all_trec qrels-rnd1.txt Round1_data/full_R1.txt 

import sys
sys.path.insert(0, "./")

import pandas as pd
import numpy as np
#import torch
import os
from tqdm.auto import tqdm
import json
from pyserini.search import pysearch
import xml.etree.ElementTree as ET
import requests
import urllib.request
from trectools import misc, TrecRun, TrecQrel, procedures
from pyserini.analysis.pyanalysis import get_lucene_analyzer, Analyzer
import nltk
from nltk.corpus import stopwords

#Round 1 indexes
#Replace with url to folder containing your index
R1_fulltext = 'lucene-index-covid-full-text-2020-04-10'

#Download round 1 topics and parse into dataframe
tree = ET.fromstring(requests.get('https://ir.nist.gov/covidSubmit/data/topics-rnd1.xml').text)
topicid = []
query = []
question = []
narrative = []
for child in tree.iter():
    tag =child.tag
    text = child.text
    attrib = child.attrib
    if (tag == 'topic'):
        topicid.append(attrib['number'])
    if (tag == 'query'):
        query.append(text)
    if (tag == 'question'):
        question.append(text)
    if (tag == 'narrative'):
        narrative.append(text)

#Join to CSV
my_dict  = {'Topic':topicid, 'Query':query, 'Question':question , 'Narrative':narrative}
R1_topics = pd.DataFrame(my_dict)
R1_topics = R1_topics[['Topic', 'Query', 'Question', 'Narrative']]

curr_dir = os.getcwd()
Pyserini_files = os.path.join(curr_dir, 'Round1_data')
if (os.path.exists(Pyserini_files) == False):
    os.mkdir(Pyserini_files)

#Topics
full_searcher = pysearch.SimpleSearcher(R1_fulltext)

#Configure searcher parameters
full_searcher.set_bm25_similarity(k1=1.5, b=0.4)
full_searcher.set_lm_dirichlet_similarity(mu = 2000)
full_searcher.set_rm3_reranker(fb_terms=10, fb_docs=10, original_query_weight=0.5)

#Stopwords for tokenization - manual review
stopwords_manual = ['seek', 'seeking', 'look', 'looking', 'studies', 'study', 'information',
             'about', 'range', 'studies', 'its', 'coronaviru',
            'other', '2', '19', 'well', ' will', 'from', 'have', 'more', 'covid', 'any', 'what',
            'should', 'may', 'due', 'help', 'non', 's', 'those', 'people', 'ways', 'all', 'gain',
            'possible', 'toward', 'specifically', 'learned', 'number', 'proportion', 'including',
            'etc', 'still', 'while', 'human', 'specific', 'result', 'results', 'assess', 'need',
            'between', 'take', 'taking', 'patient', 'type', 'cause' ,'frequency', 'less', 'face',
            'likely', 'infect', 'upon', 'develop', 'represent', 'promising', 'step', 'related',
            'papers', 'describe', 'also', 'relevant', 'who', 'show', 'science', 'basic', 'complete',
            'do', 'how', 'been', 'against', 'use', 'to', 'had', 'has', 'approach', 'Studies', 'Stud', 'Inst', 'Divi' ,'Thomae',
            'Brigham', 'Young', 'Univ', 'studies', 'volition', 'severe acute respiratory syndrome', 'affect', 'affected']

#NLTK stopwords
nltk.download('stopwords')
stopwords = list(set(stopwords.words('English')))
stopwords_manual = list(np.append(stopwords_manual, stopwords))

token_narrative_list = []

#Extract important narrative text
for i in range(len(R1_topics)):
    analyzer = Analyzer(get_lucene_analyzer(stemmer='krovetz'))
    tokens = analyzer.analyze(R1_topics['Narrative'][i])
    #Remove stopwords and duplicates from token
    tokens = [w for w in tokens if not w in stopwords_manual]
    tokens = list(set(tokens))
    token_narrative_list.append(tokens)

#Tokenize question
token_question_list = []

#Extract important question text - NOT USED YET
for i in range(len(R1_topics)):
    analyzer = Analyzer(get_lucene_analyzer(stemmer='krovetz'))
    tokens = analyzer.analyze(R1_topics['Question'][i])
    #Remove stopwords and duplicates from token
    tokens = [w for w in tokens if not w in stopwords_manual]
    tokens = list(set(tokens))
    token_question_list.append(tokens)

#Anserini searcher can take both query and keywords
#keywords_list = '2019-nCoV, SARS-CoV-2, COVID-19'
keywords_list = 'COVID-19'

#Extract search results from the searcher
docid_list = []
rank_list = []
score_list = []
topic_id_list = []
title_list = []
doi_list = []

print('Searching topics for documents')
#Search extra - will drop duplicates and excess to 1000
n_papers = 1100
for ii, row in R1_topics.iterrows():
    query = R1_topics['Query'][ii]
    question = R1_topics['Question'][ii]
    topic_num = R1_topics['Topic'][ii]
    token_topic = ', '.join(token_narrative_list[ii])
    token_question = ','.join(token_question_list[ii])
    input_query = query + '. ' + token_question + '. ' +  token_topic + ' . ' + keywords_list

    hits = full_searcher.search(q = input_query, k=n_papers)
    print(topic_num)
    #Each key is a qid, value is the anserini search list
    for i in tqdm(range(0, n_papers), position = 0, leave = True):
        topic_id_list.append(topic_num)
        docid_list.append(hits[i].docid)
        rank_list.append(str(i+1))
        score_list.append(hits[i].score)
        title_list.append(hits[i].lucene_document.get("title"))
        doi_list.append('https://doi.org/' + str(hits[i].lucene_document.get("doi")))


#Make dataframe from lists generated from search
def TREC_df(topic_id_list, docid_list, rank_list, score_list, title_list, doi_list, run_param):
    #Run-tag for TREC run requirements
    Q0 = ['q0'] * len(topic_id_list)
    qid = [run_param] * len(topic_id_list)

    df  = {'topic': topic_id_list , 'q0':Q0, 'docid':docid_list, 'rank':rank_list,
                                 'score':score_list, 'title': title_list, 'doi':doi_list, 'qid':qid}
    df = pd.DataFrame(df)
    df = df[['topic', 'q0', 'docid', 'rank', 'score', 'title', 'doi', 'qid']]

    #Remove duplicates
    df.drop_duplicates(subset=['topic', 'docid'], keep='first', inplace = True)

    #Re-rank
    df['rank'] = df.groupby('topic')['score'].rank(ascending=False)
    df['rank'] = df['rank'].astype(int)

    df = df[df['rank'] <= 1000]
    #Reset index
    df.reset_index(drop=True, inplace=True)

    #Get columns for submission
    succinct_results = df[['topic', 'q0', 'docid', 'rank', 'score', 'qid']]

    return succinct_results

full_df = TREC_df(topic_id_list, docid_list, rank_list, score_list, title_list, doi_list, 'FullTxt_run')
full_df.to_csv(os.path.join(Pyserini_files, 'full_R1.txt'), sep=' ', index=False, header=None)

#Use Trec Eval to evaluate initial runs
#Run TREC_Eval
print('Running trec_eval on search results')
r = requests.get('https://ir.nist.gov/covidSubmit/data/qrels-rnd1.txt')
qrels_file = os.path.join(os.getcwd(), 'qrels.txt')
with open(qrels_file, 'wb') as f:
    f.write(r.content)
qrels = TrecQrel(qrels_file)

#Generate metrics for all 3 indices (1000 docs retrieved for each)
runs = procedures.list_of_runs_from_path(Pyserini_files, "*.txt")
results = procedures.evaluate_runs(runs, qrels, per_query=True)
p5 = procedures.extract_metric_from_results(results, "P_5")
p10 = procedures.extract_metric_from_results(results, "P_10")
Bpref = procedures.extract_metric_from_results(results, "bpref")
Mean_avgP = procedures.extract_metric_from_results(results, 'map')

#Aggregate results to dataframe
runs_names = [os.path.basename(str(x)).split('.')[0] for x in runs]
p5_list = []
p10_list = []
map_list = []
bpref_list = []
ndcg_list = []

for i in range(len(runs)):
    p5_list.append(p5[i][1])
    p10_list.append(p10[i][1])
    map_list.append(Mean_avgP[i][1])
    bpref_list.append(Bpref[i][1])

Result_df  = {'Run':runs_names, 'P@5': p5_list, 'P@10': p10_list, 'MAP': map_list, 'Bpref': bpref_list}
Result_df = pd.DataFrame(Result_df)

with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    print(Result_df)
