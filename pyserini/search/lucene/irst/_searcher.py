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
This module provides Pyserini's Python translation probability search
interface on MS MARCO dataset. The main entry point is the
``TranslationProbabilitySearcher`` class.
"""

import json
import math
import os
import pickle
import struct
from multiprocessing.pool import ThreadPool
from typing import Dict

from transformers import AutoTokenizer

from pyserini.pyclass import autoclass
from pyserini.search.lucene import LuceneSearcher
from pyserini.util import download_prebuilt_index, get_cache_home, download_url, download_and_unpack_index
from pyserini.prebuilt_index_info import TF_INDEX_INFO_CURRENT

# Wrappers around Anserini classes
JQuery = autoclass('org.apache.lucene.search.Query')
JLuceneSearcher = autoclass('io.anserini.search.SimpleSearcher')
JIndexReader = autoclass('io.anserini.index.IndexReaderUtils')
JTerm = autoclass('org.apache.lucene.index.Term')


class LuceneIrstSearcher(object):
    SELF_TRAN = 0.35
    MIN_PROB = 0.0025
    LAMBDA_VALUE = 0.3
    MIN_COLLECT_PROB = 1e-9

    def __init__(self, index: str, k1: int, b: int, num_threads: int):
        translation_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/ibm_model_1_bert_tok_20211117.tar.gz'
        translation_directory = os.path.join(get_cache_home(), 'models')
        self.termfreq_dic = self.download_and_load_wp_stats(index)
        # This is used to download and unpack translation model instead of index, we use the function (download_and_unpack_index) for convenience.
        self.translation_model = download_and_unpack_index(translation_url, translation_directory)
        self.bm25search = LuceneSearcher.from_prebuilt_index(index)
        self.bm25search.set_bm25(k1, b)
        index_directory = os.path.join(get_cache_home(), 'indexes')
        if index == 'msmarco-v1-passage':
            index_path = os.path.join(index_directory,
                                      TF_INDEX_INFO_CURRENT['msmarco-v1-passage']['filename'][:-6] +
                                      TF_INDEX_INFO_CURRENT['msmarco-v1-passage']['md5'])
        elif index == 'msmarco-v1-doc':
            index_path = os.path.join(index_directory,
                                      TF_INDEX_INFO_CURRENT['msmarco-v1-doc']['filename'][:-6] +
                                      TF_INDEX_INFO_CURRENT['msmarco-v1-doc']['md5'])
        elif index == 'msmarco-v1-doc-segmented':
            index_path = os.path.join(index_directory,
                                      TF_INDEX_INFO_CURRENT['msmarco-v1-doc-segmented']['filename'][:-6] +
                                      TF_INDEX_INFO_CURRENT['msmarco-v1-doc-segmented']['md5'])
        else:
            print("We currently only support three indexes: msmarco-passage, msmarco-v1-doc and msmarco-v1-doc-segmented but the index you inserted is not one of those")
        self.object = JLuceneSearcher(index_path)
        self.source_lookup, self.target_lookup, self.tran = self.load_tranprobs_table()
        self.bert_tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
        self.pool = ThreadPool(num_threads)


    @classmethod
    def from_prebuilt_index(cls, prebuilt_index_name: str):
        """Build a searcher from a pre-built index; download the index if necessary.

        Parameters
        ----------
        prebuilt_index_name : str
            Prebuilt index name.

        Returns
        -------
        LuceneSearcher
            Searcher built from the prebuilt index.
        """
        print(f'Attempting to initialize pre-built index {prebuilt_index_name}.')
        try:
            index_dir = download_prebuilt_index(prebuilt_index_name)
        except ValueError as e:
            print(str(e))
            return None

        print(f'Initializing {prebuilt_index_name}...')
        return cls(index_dir)

    def download_and_load_wp_stats(self, index: str):
        translation_directory = os.path.join(get_cache_home(), 'models')
        if not os.path.exists(translation_directory):
            os.makedirs(translation_directory)
        if (index == 'msmarco-v1-passage'):
            local_filename = 'bert_wp_term_freq.msmarco-passage.20220411.pickle'
            wp_stats_path = os.path.join(translation_directory, local_filename)
            url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-passage.20220411.pickle'
        elif (index == 'msmarco-v1-doc'):
            local_filename = 'bert_wp_term_freq.msmarco-doc.20220411.pickle'
            wp_stats_path = os.path.join(translation_directory, local_filename)
            url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-doc.20220411.pickle'
        elif (index == 'msmarco-v1-doc-segmented'):
            local_filename = 'bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle'
            wp_stats_path = os.path.join(translation_directory, local_filename)
            url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/data/bert_wp_term_freq.msmarco-doc-segmented.20220411.pickle'

        if os.path.exists(wp_stats_path):
            print(f'{wp_stats_path} already exists, skipping download.')
        else:
            download_url(url, translation_directory, local_filename)
        with open(wp_stats_path, 'rb') as fin:
            termfreq_dic = pickle.load(fin)
        return termfreq_dic

    @staticmethod
    def intbits_to_float(b: bytes):
        s = struct.pack('>l', b)
        return struct.unpack('>f', s)[0]

    def rescale(
            self, source_lookup: Dict[str, int], target_lookup: Dict[str, int],
            tran_lookup: Dict[str, Dict[str, float]],
            target_voc: Dict[int, str], source_voc: Dict[int, str]
            ):

        for target_id in tran_lookup:
            if target_id > 0:
                adjust_mult = (1 - self.SELF_TRAN)
            else:
                adjust_mult = 1
            # adjust the prob with adjust_mult
            # add SELF_TRAN prob to self-translation pair
            for source_id in tran_lookup[target_id].keys():
                tran_prob = tran_lookup[target_id][source_id]
                if source_id > 0:
                    source_word = source_voc[source_id]
                    target_word = target_voc[target_id]
                    tran_prob *= adjust_mult
                    if (source_word == target_word):
                        tran_prob += self.SELF_TRAN
                    tran_lookup[target_id][source_id] = tran_prob
            # in case if self-translation pair was not included in TransTable
            if target_id not in tran_lookup[target_id].keys():
                target_word = target_voc[target_id]
                source_id = source_lookup[target_word]
                tran_lookup[target_id][source_id] = self.SELF_TRAN
        return source_lookup, target_lookup, tran_lookup

    def load_tranprobs_table(self):
        dir_path = self.translation_model
        source_path = dir_path + "/source.vcb"
        source_lookup = {}
        source_voc = {}
        with open(source_path) as f:
            lines = f.readlines()
        for line in lines:
            id, voc, freq = line.split(" ")
            source_voc[int(id)] = voc
            source_lookup[voc] = int(id)

        target_path = dir_path + "/target.vcb"
        target_lookup = {}
        target_voc = {}
        with open(target_path) as f:
            lines = f.readlines()
        for line in lines:
            id, voc, freq = line.split(" ")
            target_voc[int(id)] = voc
            target_lookup[voc] = int(id)
        tran_path = dir_path + "/output.t1.5.bin"
        tran_lookup = {}
        with open(tran_path, "rb") as file:
            byte = file.read(4)
            while byte:
                source_id = int.from_bytes(byte, "big")
                assert(source_id == 0 or source_id in source_voc.keys())
                byte = file.read(4)
                target_id = int.from_bytes(byte, "big")
                assert(target_id in target_voc.keys())
                byte = file.read(4)
                tran_prob = self.intbits_to_float(int.from_bytes(byte, "big"))
                if (target_id in tran_lookup.keys()) and (tran_prob > self.MIN_PROB):
                    tran_lookup[target_id][source_id] = tran_prob
                elif tran_prob > self.MIN_PROB:
                    tran_lookup[target_id] = {}
                    tran_lookup[target_id][source_id] = tran_prob
                byte = file.read(4)
        return self.rescale(
                source_lookup, target_lookup,
                tran_lookup, target_voc, source_voc)

    def get_ibm_score(self, arguments):
        (query_text_lst, test_doc, searcher, source_lookup,
            target_lookup, tran, collect_probs, max_sim) = arguments

        if searcher.doc_raw(test_doc) is None:
            print(f"{test_doc} is not found in searcher")
        contents = json.loads(self.object.doc_raw(test_doc))['contents']
        doc_token_lst = self.bert_tokenizer.tokenize(contents.lower(), truncation=True)
        total_query_prob = 0
        doc_size = len(doc_token_lst)
        query_size = len(query_text_lst)
        for querytoken in query_text_lst:
            target_map = {}
            total_tran_prob = 0
            collect_prob = collect_probs[querytoken]
            max_sim_score = 0
            if querytoken in target_lookup.keys():
                query_word_id = target_lookup[querytoken]
                if query_word_id in tran.keys():
                    target_map = tran[query_word_id]
                    for doctoken in doc_token_lst:
                        tran_prob = 0
                        doc_word_id = 0
                        if doctoken in source_lookup.keys():
                            doc_word_id = source_lookup[doctoken]
                            if doc_word_id in target_map.keys():
                                tran_prob = max(target_map[doc_word_id], tran_prob)
                                max_sim_score = max(tran_prob, max_sim_score)
                                total_tran_prob += (tran_prob/doc_size)
            if max_sim:
                query_word_prob = math.log(
                    (1 - self.LAMBDA_VALUE) * max_sim_score + self.LAMBDA_VALUE * collect_prob)
            else:
                query_word_prob = math.log(
                    (1 - self.LAMBDA_VALUE) * total_tran_prob + self.LAMBDA_VALUE * collect_prob)

            total_query_prob += query_word_prob
        return total_query_prob / query_size

    def search(self, query_text, query_field_text, max_sim, bm25_results):
        origin_scores = [bm25_result.score for bm25_result in bm25_results]
        test_docs = [bm25_result.docid for bm25_result in bm25_results]
        if (test_docs == []):
            print(query_text)

        query_field_text_lst = query_field_text.split(' ')
        total_term_freq = self.termfreq_dic['TOTAL']
        collect_probs = {}
        for querytoken in query_field_text_lst:
            if querytoken in self.termfreq_dic:
                collect_probs[querytoken] = max(self.termfreq_dic[querytoken] / total_term_freq, self.MIN_COLLECT_PROB)
            else:
                collect_probs[querytoken] = self.MIN_COLLECT_PROB
        arguments = [(
            query_field_text_lst, test_doc, self.object,
            self.source_lookup, self.target_lookup,
            self.tran, collect_probs, max_sim)
            for test_doc in test_docs]

        rank_scores = self.pool.map(self.get_ibm_score, arguments)
        return test_docs, rank_scores, origin_scores

    def rerank(self, query_text, query_field_text, baseline, max_sim, tf_table):
        test_docs, origin_scores = baseline
        if (test_docs == []):
            print(query_text)

        query_field_text_lst = query_field_text.split(' ')
        total_term_freq = self.termfreq_dic['TOTAL']
        collect_probs = {}
        for querytoken in query_field_text_lst:
            if querytoken in self.termfreq_dic:
                collect_probs[querytoken] = max(self.termfreq_dic[querytoken] / total_term_freq, self.MIN_COLLECT_PROB)
            else:
                collect_probs[querytoken] = self.MIN_COLLECT_PROB
        arguments = [(
            query_field_text_lst, test_doc, self.object, 
            self.source_lookup, self.target_lookup,
            self.tran, collect_probs, max_sim)
            for test_doc in test_docs]

        rank_scores = self.pool.map(self.get_ibm_score, arguments)
        return test_docs, rank_scores, origin_scores
