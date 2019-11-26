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
        def __init__(self, docid, term_freq, positions):
            self.docid = docid
            self.term_freq = term_freq
            self.positions = positions

        def __repr__(self):
            repr = '(' + str(self.docid) + ', ' + str(self.term_freq) + ')'
            if self.positions:
                repr += ' [' + ','.join([str(p) for p in self.positions]) + ']'
            return repr

    def analyze_term(self, term):
        return self.object.analyzeTerm(self.reader, JString(term))

    def get_term_counts(self, term):
        term_map = self.object.getTermCounts(self.reader, JString(term))
        return term_map.get(JString('collectionFreq')), term_map.get(JString('docFreq'))

    def get_postings_list(self, term):
        postings_list = self.object.getPostingsList(self.reader, JString(term))
        result = []
        for posting in postings_list.toArray():
            result.append(self.Posting(posting.getDocid(), posting.getTF(), posting.getPositions()))
        return result

    def get_document_vector(self, docid):
        doc_vector_map = self.object.getDocumentVector(self.reader, JString(docid))
        doc_vector_dict = {}
        for term in doc_vector_map.keySet().toArray():
            doc_vector_dict[term] = doc_vector_map.get(JString(term))
        return doc_vector_dict

    def get_bm25_term_weight(self, docid, term):
        return self.object.getBM25TermWeight(self.reader, JString(docid), JString(term))

    def dump_document_vectors(self, reqDocidsPath: str, weight: DocumentVectorWeight):
        '''
        Parameters
        ----------
        reqDocidsPath : str
            dumps the document vector for all documents in reqDocidsPath
        weight : DocumentVectorWeight
            the weight for dumped document vector(s)
        '''
        self.object.dumpDocumentVectors(reqDocidsPath, weight)
