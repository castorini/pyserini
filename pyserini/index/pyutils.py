# -*- coding: utf-8 -*-
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

'''
Module for providing python interface to Anserini index reader utils
'''
from ..pyclass import JIndexReaderUtils, JDocumentVectorWeight, JString

import logging

logger = logging.getLogger(__name__)


class IndexReaderUtils:
    '''
    Wrapper class for Anserini's IndexReaderUtils.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory
    '''

    def __init__(self, index_dir):
        self.object = JIndexReaderUtils()
        self.reader = self.object.getReader(JString(index_dir))

    class DocumentVectorWeight:
        NONE = JDocumentVectorWeight.NONE
        TF_IDF = JDocumentVectorWeight.TF_IDF

    class Posting:
        '''
        Basic Posting class for Postings List
        '''
        def __init__(self, docid, term_freq, positions):
            self.docid = docid
            self.term_freq = term_freq
            self.positions = positions

        def __repr__(self):
            repr = '(' + str(self.docid) + ', ' + str(self.term_freq) + ')'
            if self.positions:
                repr += ' [' + ','.join([str(p) for p in self.positions]) + ']'
            return repr

    class IndexTerm:
        '''
        Basic IndexTerm class to represent each term in index
        '''
        def __init__(self, term, doc_freq, total_term_freq):
            self.term = term
            self.doc_freq = doc_freq
            self.total_term_freq = total_term_freq

    def analyze(self, text):
        '''
        Parameters
        ----------
        term : str
        Returns
        -------
        result : str
            List of stemmed tokens
        '''
        stemmed = self.object.analyze(JString(text))
        token_list = []
        for token in stemmed.toArray():
            token_list.append(token)
        return token_list

    def terms(self):
        '''
        :return: generator over terms
        '''
        term_iterator = self.object.getTerms(self.reader)
        while term_iterator.hasNext():
            cur_term = term_iterator.next()
            yield self.IndexTerm(cur_term.getTerm(), cur_term.getDF(), cur_term.getTotalTF())

    def get_term_counts(self, term):
        '''
        Parameters
        ----------
        term : str
            Raw term
        Returns
        -------
        result : long, long
            Collection frequency and document frequency of term
        '''
        term_map = self.object.getTermCounts(self.reader, JString(term))
        return term_map.get(JString('collectionFreq')), term_map.get(JString('docFreq'))

    def get_postings_list(self, term):
        '''
        Parameters
        ----------
        term : str
        Returns
        -------
        result : list<Posting>
            Postings list for term
        '''
        postings_list = self.object.getPostingsList(self.reader, JString(term))
        result = []
        for posting in postings_list.toArray():
            result.append(self.Posting(posting.getDocid(), posting.getTF(), posting.getPositions()))
        return result

    def get_document_vector(self, docid):
        '''
        Parameters
        ----------
        docid : str
            Collection docid
        Returns
        -------
        result : dict
            Terms and their respective frequencies in document
        '''
        doc_vector_map = self.object.getDocumentVector(self.reader, JString(docid))
        doc_vector_dict = {}
        for term in doc_vector_map.keySet().toArray():
            doc_vector_dict[term] = doc_vector_map.get(JString(term))
        return doc_vector_dict

    def get_raw_document(self, docid):
        '''
        Parameters
        ----------
        docid : str
            Collection docid
        Returns
        -------
        result : raw document given its collection docid
        '''
        return self.object.getRawDocument(self.reader, JString(docid))

    def get_bm25_term_weight(self, docid, term):
        '''
        Parameters
        ----------
        docid : str
            Collection docid
        term : str
        Returns
        -------
        result : float
            BM25 score (NaN if no documents match)
        '''
        return self.object.getBM25TermWeight(self.reader, JString(docid), JString(term))

    def dump_document_vectors(self, reqDocidsPath, weight):
        '''
        Parameters
        ----------
        reqDocidsPath : str
            dumps the document vector for all documents in reqDocidsPath
        weight : DocumentVectorWeight
            the weight for dumped document vector(s)
        '''
        self.object.dumpDocumentVectors(self.reader, reqDocidsPath, weight)