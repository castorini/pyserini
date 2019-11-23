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
Module for providing python interface to Anserini index utils
'''
from ..pyclass import JIndexUtils, JDocumentVectorWeight, JString

import logging

logger = logging.getLogger(__name__)


class IndexUtils:
    '''
    Wrapper class for Anserini's IndexUtils.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory
    '''

    def __init__(self, index_dir):
        self.object = JIndexUtils(JString(index_dir))

    class DocumentVectorWeight:
        NONE = JDocumentVectorWeight.NONE
        TF_IDF = JDocumentVectorWeight.TF_IDF

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
