# -*- coding: utf-8 -*-
#
# Anserini: A toolkit for reproducible information retrieval research built on Lucene
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

'''
Module for providing python interface to Anserini searchers
'''

from ..pyclass import JSearcher, JString, JArrayList

import logging
logger = logging.getLogger(__name__)

class SimpleSearcher:
    '''
    Wrapper class for Anserini's SimpleSearcher.
            
    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory
    '''
    
    def __init__(self, index_dir):
        self.object = JSearcher(JString(index_dir))
    
    def search(self, q, k=10, t=-1):
        '''
        Parameters
        ----------
        q : str
            Query string
        k : int
            Number of hits to return
        t : int
            Query tweet time for searching tweets  
            
        Returns
        -------
        results : list of io.anserini.search.SimpleSearcher$Result
            List of document hits returned from search
        '''
        return self.object.search(JString(q), k, t)
        
    def batch_search(self, queries, qids, k=10, t=-1, threads=1):
        '''
        Parameters
        ----------
        queries : list of str
            list of query strings
        qids : list of str
            list of corresponding query ids
        k : int
            Number of hits to return
        t : int
            Query tweet time for searching tweets  
        threads : int
            Maximum number of threads 
            
        Returns
        -------
        result_dict : dict of {str : io.anserini.search.SimpleSearcher$Result}
            Dictionary of {qid : document hits} returned from each query
        '''
        query_strings = JArrayList()
        qid_strings = JArrayList()
        for query in queries:
            jq = JString(query.encode('utf8'))
            query_strings.add(jq)

        for qid in qids:
            jqid = JString(qid)
            qid_strings.add(jqid)

        results = self.object.batchSearch(query_strings, qid_strings, int(k), int(t), int(threads)).entrySet().toArray()
        return {r.getKey() : r.getValue() for r in results}

    def search_fields(self, q, f, boost, k):
        '''
        Parameters
        ----------
        q : str
            Query string
        f : str
            Name of additional field to search over
        boost : float
            Weight boost for additional field
        k : int
            Number of hits to return
            
        Returns
        -------
        results : list of io.anserini.search.SimpleSearcher$Result
            List of document hits returned from search
        '''
        return self.object.searchFields(JString(q), JString(f), float(boost), k)
    
    def set_search_tweets(self, flag):
        '''
        Parameters
        ----------
        flag : bool
            True if searching over tweets
        '''
        self.object.setSearchTweets(flag)
        
    def set_rm3_reranker(self, fb_terms=10, fb_docs=10, 
                         original_query_weight=float(0.5), 
                         rm3_output_query=False):
        '''
        Parameters
        ----------
        fb_terms : int
            RM3 parameter for number of expansion terms
        fb_docs : int
            RM3 parameter for number of documents
        original_query_weight : float
            RM3 parameter for weight to assign to the original query
        rm3_output_query : bool
            True if we want to print original and expanded queries for RM3
        '''
        self.object.setRM3Reranker(fb_terms, fb_docs, 
                                   original_query_weight, rm3_output_query)
        
    def set_default_reranker(self):
        self.object.setDefaultReranker()
        
    def set_lm_dirichlet_similarity(self, mu):
        '''
        Parameters
        ----------
        mu : float
            Dirichlet smoothing parameter
        '''
        self.object.setLMDirichletSimilarity(float(mu))
        
    def set_lm_jelinek_mercer_similarity(self, lam):
        '''
        Parameters
        ----------
        lam : float
            Jelinek Mercer smoothing parameter
        '''
        self.object.set.LMJelinekMercerSimilarity(float(lam))
        
    def set_bm25_similarity(self, k1, b):
        '''
        Parameters
        ----------
        k1 : float
            BM25 k1 parameter
        b : float
            BM25 b parameter
        '''
        self.object.setBM25Similarity(float(k1), float(b))
        
    def set_dfr_similarity(self, c):
        '''
        Parameters
        ----------
        c : float
            DFR c parameter
        '''
        self.object.setDFRSimilarity(float(c))
            
    def set_ib_similarity(self, c):
        '''
        Parameters
        ----------
        c : float
            Information-based c parameter
        '''
        self.object.setIBSimilarity(float(c))

    def set_f2exp_similarity(self, s):
        '''
        Parameters
        ----------
        s : float
            F2Exp s parameter
        '''
        self.object.setF2ExpSimilarity(float(s))
        
    def set_f2log_similarity(self, s):
        '''
        Parameters
        ----------
        s : float
            F2Log s parameter
        '''
        self.object.setF2LogSimilarity(float(s))

    def doc(self, ldocid):
        '''
        Parameters
        ----------
        ldocid : int
            Internal Lucene docid of a document
        
        Returns
        -------
        result : str
            Raw content of the given document
        
        '''
        return self.object.doc(ldocid)
        
    def close(self):
        self.object.close()
