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
#

"""
This module provides Pyserini's Python ltr search interface on MS MARCO passage. The main entry point is the ``MsmarcoPassageLtrSearcher``
class.
"""

import logging
import multiprocessing
import time
import os
from tqdm import tqdm
import pickle
from pyserini.index.lucene import IndexReader
from pyserini.search.lucene import LuceneSearcher
from pyserini.util import get_cache_home

from pyserini.search.lucene.ltr._base import *


logger = logging.getLogger(__name__)

class MsmarcoLtrSearcher:
    def __init__(self, model: str, ibm_model:str, index:str, data: str, prebuilt: bool, topic: str):
        #msmarco-ltr-passage
        self.model = model
        self.ibm_model = ibm_model
        if prebuilt:
            self.lucene_searcher = LuceneSearcher.from_prebuilt_index(index)
            index_directory = os.path.join(get_cache_home(), 'indexes')
            if data == 'passage':
                index_path = os.path.join(index_directory, 'index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3')
            else:
                index_path = os.path.join(index_directory, 'index-msmarco-doc-per-passage-ltr-20211031-33e4151.bd60e89041b4ebbabc4bf0cfac608a87')
            self.index_reader = IndexReader.from_prebuilt_index(index)
        else:
            index_path = index
            self.index_reader = IndexReader(index)
        self.fe = FeatureExtractor(index_path, max(multiprocessing.cpu_count()//2, 1))
        self.data = data

    
    def add_fe(self):
        #self.fe.add(RunList('collections/msmarco-ltr-passage/run.monot5.run_list.whole.trec','t5'))
        #self.fe.add(RunList('../bert.whole.doc.trec','bert'))
        for qfield, ifield in [('analyzed', 'contents'),
                           ('text_unlemm', 'text_unlemm'),
                           ('text_bert_tok', 'text_bert_tok')]:
            print(qfield, ifield)
            self.fe.add(BM25Stat(SumPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
            self.fe.add(BM25Stat(AvgPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
            self.fe.add(BM25Stat(MedianPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
            self.fe.add(BM25Stat(MaxPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
            self.fe.add(BM25Stat(MinPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))
            self.fe.add(BM25Stat(MaxMinRatioPooler(), k1=2.0, b=0.75, field=ifield, qfield=qfield))

            self.fe.add(LmDirStat(SumPooler(), mu=1000, field=ifield, qfield=qfield))
            self.fe.add(LmDirStat(AvgPooler(), mu=1000, field=ifield, qfield=qfield))
            self.fe.add(LmDirStat(MedianPooler(), mu=1000, field=ifield, qfield=qfield))
            self.fe.add(LmDirStat(MaxPooler(), mu=1000, field=ifield, qfield=qfield))
            self.fe.add(LmDirStat(MinPooler(), mu=1000, field=ifield, qfield=qfield))
            self.fe.add(LmDirStat(MaxMinRatioPooler(), mu=1000, field=ifield, qfield=qfield))

            self.fe.add(NormalizedTfIdf(field=ifield, qfield=qfield))
            self.fe.add(ProbalitySum(field=ifield, qfield=qfield))

            self.fe.add(DfrGl2Stat(SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrGl2Stat(AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrGl2Stat(MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrGl2Stat(MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrGl2Stat(MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrGl2Stat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(DfrInExpB2Stat(SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrInExpB2Stat(AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrInExpB2Stat(MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrInExpB2Stat(MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrInExpB2Stat(MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(DfrInExpB2Stat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(DphStat(SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(DphStat(AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(DphStat(MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(DphStat(MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(DphStat(MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(DphStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(Proximity(field=ifield, qfield=qfield))
            self.fe.add(TpScore(field=ifield, qfield=qfield))
            self.fe.add(TpDist(field=ifield, qfield=qfield))

            self.fe.add(DocSize(field=ifield))

            self.fe.add(QueryLength(qfield=qfield))
            self.fe.add(QueryCoverageRatio(qfield=qfield))
            self.fe.add(UniqueTermCount(qfield=qfield))
            self.fe.add(MatchingTermCount(field=ifield, qfield=qfield))
            self.fe.add(SCS(field=ifield, qfield=qfield))

            self.fe.add(TfStat(AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfStat(MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfStat(SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfStat(MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfStat(MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(TfIdfStat(True, AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfIdfStat(True, MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfIdfStat(True, SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfIdfStat(True, MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfIdfStat(True, MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(TfIdfStat(True, MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(NormalizedTfStat(AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(NormalizedTfStat(MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(NormalizedTfStat(SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(NormalizedTfStat(MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(NormalizedTfStat(MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(NormalizedTfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(IdfStat(AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(IdfStat(MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(IdfStat(SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(IdfStat(MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(IdfStat(MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(IdfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(IcTfStat(AvgPooler(), field=ifield, qfield=qfield))
            self.fe.add(IcTfStat(MedianPooler(), field=ifield, qfield=qfield))
            self.fe.add(IcTfStat(SumPooler(), field=ifield, qfield=qfield))
            self.fe.add(IcTfStat(MinPooler(), field=ifield, qfield=qfield))
            self.fe.add(IcTfStat(MaxPooler(), field=ifield, qfield=qfield))
            self.fe.add(IcTfStat(MaxMinRatioPooler(), field=ifield, qfield=qfield))

            self.fe.add(UnorderedSequentialPairs(3, field=ifield, qfield=qfield))
            self.fe.add(UnorderedSequentialPairs(8, field=ifield, qfield=qfield))
            self.fe.add(UnorderedSequentialPairs(15, field=ifield, qfield=qfield))
            self.fe.add(OrderedSequentialPairs(3, field=ifield, qfield=qfield))
            self.fe.add(OrderedSequentialPairs(8, field=ifield, qfield=qfield))
            self.fe.add(OrderedSequentialPairs(15, field=ifield, qfield=qfield))
            self.fe.add(UnorderedQueryPairs(3, field=ifield, qfield=qfield))
            self.fe.add(UnorderedQueryPairs(8, field=ifield, qfield=qfield))
            self.fe.add(UnorderedQueryPairs(15, field=ifield, qfield=qfield))
            self.fe.add(OrderedQueryPairs(3, field=ifield, qfield=qfield))
            self.fe.add(OrderedQueryPairs(8, field=ifield, qfield=qfield))
            self.fe.add(OrderedQueryPairs(15, field=ifield, qfield=qfield))

        start = time.time()
        self.fe.add(IbmModel1(f"{self.ibm_model}/title_unlemm", "text_unlemm", "title_unlemm", "text_unlemm"))
        end = time.time()
        print('IBM model Load takes %.2f seconds' % (end - start))
        start = end
        self.fe.add(IbmModel1(f"{self.ibm_model}url_unlemm", "text_unlemm", "url_unlemm", "text_unlemm"))
        end = time.time()
        print('IBM model Load takes %.2f seconds' % (end - start))
        start = end
        self.fe.add(IbmModel1(f"{self.ibm_model}body", "text_unlemm", "body", "text_unlemm"))
        end = time.time()
        print('IBM model Load takes %.2f seconds' % (end - start))
        start = end
        self.fe.add(IbmModel1(f"{self.ibm_model}text_bert_tok", "text_bert_tok", "text_bert_tok", "text_bert_tok"))
        end = time.time()
        print('IBM model Load takes %.2f seconds' % (end - start))
        start = end
    
    def batch_extract(self, df, queries, fe):
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
                if self.data == 'document':
                    if self.index_reader.doc(t.pid) != None:
                        task["docIds"].append(t.pid)
                        task_infos.append((qid, t.pid, t.rel))
                else:
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

    def batch_predict(self, models, dev_extracted, feature_name):
        task_infos, features, group = dev_extracted
        dev_X = features.loc[:, feature_name]

        task_infos['score'] = 0.
        for gbm in models:
            task_infos['score'] += gbm.predict(dev_X)
    
    def search(self, dev, queries):
        batch_info = []
        start_extract = time.time()
        models = pickle.load(open(self.model+'/model.pkl', 'rb'))
        metadata = json.load(open(self.model+'/metadata.json', 'r'))
        feature_used = metadata['feature_names']
        for dev_extracted in self.batch_extract(dev, queries, self.fe):
            end_extract = time.time()
            print(f'extract 1000 queries take {end_extract - start_extract}s')
            task_infos, features, group = dev_extracted
            start_predict = time.time()
            self.batch_predict(models, dev_extracted, feature_used)
            end_predict = time.time()
            print(f'predict 1000 queries take {end_predict - start_predict}s')
            batch_info.append(task_infos)
            start_extract = time.time()
        batch_info = pd.concat(batch_info, axis=0, ignore_index=True)
        return batch_info

