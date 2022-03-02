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
import struct
from multiprocessing.pool import ThreadPool
from pyserini.search.lucene import LuceneSearcher
from pyserini.pyclass import autoclass
from pyserini.util import download_prebuilt_index
from typing import Dict

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

    def __init__(self, ibm_model: str, index: str, field_name: str):
        self.ibm_model = ibm_model
        self.object = JLuceneSearcher(index)
        self.index_reader = JIndexReader().getReader(index)
        self.field_name = field_name
        self.source_lookup, self.target_lookup, self.tran = self.load_tranprobs_table()
        self.pool = ThreadPool(24)
        self.bm25search = LuceneSearcher.from_prebuilt_index("msmarco-passage")


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
        dir_path = self.ibm_model
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
        (query_text_lst, test_doc, searcher, field_name, source_lookup,
            target_lookup, tran, collect_probs, max_sim) = arguments

        if searcher.documentRaw(test_doc) is None:
            print(f'{test_doc} is not found in searcher')
        document_text = json.loads(searcher.documentRaw(test_doc))[field_name]
        doc_token_lst = document_text.split(" ")
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

    def search(self, query_text, query_field_text, hits, max_sim):
        self.bm25search.set_bm25(0.82, 0.68)

        bm25_results = self.bm25search.search(query_text, hits)
        origin_scores = [bm25_result.score for bm25_result in bm25_results]
        test_docs = [bm25_result.docid for bm25_result in bm25_results]
        if (test_docs == []):
            print(query_text)

        query_text_lst = query_field_text.split(' ')
        total_term_freq = self.index_reader.getSumTotalTermFreq(self.field_name)
        collect_probs = {}
        for querytoken in query_text_lst:
            collect_probs[querytoken] = max(self.index_reader.totalTermFreq(
                JTerm(self.field_name, querytoken)) / total_term_freq,
                self.MIN_COLLECT_PROB)

        arguments = [(
            query_text_lst, test_doc, self.object, self.field_name,
            self.source_lookup, self.target_lookup,
            self.tran, collect_probs, max_sim)
            for test_doc in test_docs]

        rank_scores = self.pool.map(self.get_ibm_score, arguments)
        return test_docs, rank_scores, origin_scores

    def rerank(self, query_text, query_field_text, baseline, max_sim):
        test_docs, origin_scores = baseline
        if (test_docs == []):
            print(query_text)

        query_text_lst = query_field_text.split(' ')
        total_term_freq = self.index_reader.getSumTotalTermFreq(self.field_name)
        collect_probs = {}
        for querytoken in query_text_lst:
            collect_probs[querytoken] = max(self.index_reader.totalTermFreq(
                JTerm(self.field_name, querytoken)) / total_term_freq,
                self.MIN_COLLECT_PROB)

        arguments = [(
            query_text_lst, test_doc, self.object, self.field_name,
            self.source_lookup, self.target_lookup,
            self.tran, collect_probs, max_sim)
            for test_doc in test_docs]

        rank_scores = self.pool.map(self.get_ibm_score, arguments)
        return test_docs, rank_scores, origin_scores
