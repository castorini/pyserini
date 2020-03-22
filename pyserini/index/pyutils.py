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

"""
This module provides Pyserini's Python interface for raw access to Lucene indexes built by Anserini. The main entry
point is the ``IndexReaderUtils`` class, which wraps the Java class with the same name in Anserini. Many of the classes
and methods provided are meant only to provide tools for examining an index and are not optimized for computing over.
"""

import logging
from typing import Dict, Iterator, List, Tuple

from ..pyclass import JIndexReaderUtils, JString, JAnalyzerUtils

logger = logging.getLogger(__name__)


class IndexTerm:
    """Class representing an analyzed term in an index with associated statistics.

    Parameters
    ----------
    term : str
        The analyzed term.
    df : int
        The document frequency, which is the number of documents in the collection that contains the term.
    cf : int
        The collection frequency, which is the number of times that the term occurs in the entire collection.
        This value is equal to the sum of all the term frequencies of the term across all documents in the collection.
    """

    def __init__(self, term, df, cf):
        self.term = term
        self.df = df
        self.cf = cf


class Posting:
    """Class representing a posting in a postings list.

    Parameters
    ----------
    docid : int
        The ``docid`` associated with this posting.
    tf : int
        The term frequency associated with this posting.
    positions : List[int]
        The list of positions associated with this posting.
    """

    def __init__(self, docid, tf, positions):
        self.docid = docid
        self.tf = tf
        self.positions = positions

    def __repr__(self):
        repr = '(' + str(self.docid) + ', ' + str(self.tf) + ')'
        if self.positions:
            repr += ' [' + ','.join([str(p) for p in self.positions]) + ']'
        return repr


class IndexReaderUtils:
    """
    Wrapper class for ``IndexReaderUtils`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir):
        self.object = JIndexReaderUtils()
        self.reader = self.object.getReader(JString(index_dir))

    def analyze(self, text: str, analyzer=None) -> List[str]:
        """Analyzes a piece of text. Applies Anserini's default Lucene analyzer if analyzer not specified.

        Parameters
        ----------
        text : str
            The piece of text to analyze.
        analyzer : analyzer
            The analyzer to apply.
        Returns
        -------
        List[str]
            List of tokens corresponding to the output of the analyzer.
        """
        if analyzer is None:
            results = JAnalyzerUtils.analyze(JString(text.encode('utf-8')))
        else:
            results = JAnalyzerUtils.analyze(analyzer, JString(text.encode('utf-8')))
        tokens = []
        for token in results.toArray():
            tokens.append(token)
        return tokens

    def terms(self) -> Iterator[IndexTerm]:
        """Returns an iterator over (analyzed) terms in the index.

        Returns
        -------
        Iterator[IndexTerm]
            An Iterator over :class:`IndexTerm` objects corresponding to (analyzed) terms in the index.
        """
        term_iterator = self.object.getTerms(self.reader)
        while term_iterator.hasNext():
            cur_term = term_iterator.next()
            yield IndexTerm(cur_term.getTerm(), cur_term.getDF(), cur_term.getTotalTF())

    def get_term_counts(self, term: str, analyzer=None) -> Tuple[int, int]:      
        """Returns the document frequency and collection frequency of a term 
        (applies Anserini's default Lucene analyzer if analyzer is not specified).

        Parameters
        ----------
        term : str
            The raw (unanalyzed) term.
        analyzer : analyzer
            The analyzer to apply.

        Returns
        -------
        Tuple[int, int]
            The document frequency and collection frequency of the term.
        """
        if analyzer is None:
            term_map = self.object.getTermCounts(self.reader, JString(term.encode('utf-8')))
        else:
            term_map = self.object.getTermCountsWithAnalyzer(self.reader, JString(term.encode('utf-8')), analyzer)
        
        return term_map.get(JString('docFreq')), term_map.get(JString('collectionFreq'))

    def get_postings_list(self, term: str, analyze=True) -> List[Posting]:
        """Returns the postings list for a term.

        Parameters
        ----------
        term : str
            The raw term.
        analyze : Bool
            Whether or not analyze the term.

        Returns
        -------
        List[Posting]
            List of :class:`Posting` objects corresponding to the postings list for the term.
        """
        if analyze:
            postings_list = self.object.getPostingsListForUnanalyzedTerm(self.reader, JString(term.encode('utf-8')))
        else:
            postings_list = self.object.getPostingsListForAnalyzedTerm(self.reader, JString(term.encode('utf-8')))
        if postings_list is None:
            return None

        result = []
        for posting in postings_list.toArray():
            result.append(Posting(posting.getDocid(), posting.getTF(), posting.getPositions()))
        return result

    def get_document_vector(self, docid: str) -> Dict[str, int]:
        """Returns the document vector for a ``docid``.

        Parameters
        ----------
        docid : str
            The collection ``docid``.

        Returns
        -------
        Dict[str, int]
            A dictionary with analyzed terms as keys and their term frequencies as values.
        """
        doc_vector_map = self.object.getDocumentVector(self.reader, JString(docid))
        doc_vector_dict = {}
        for term in doc_vector_map.keySet().toArray():
            doc_vector_dict[term] = doc_vector_map.get(JString(term.encode('utf-8')))
        return doc_vector_dict

    def get_raw_document_contents(self, docid: str) -> str:
        """Returns the raw document contents for a collection ``docid``.

        Parameters
        ----------
        docid : str
            The collection ``docid``.

        Returns
        -------
        str
            The raw document contents.
        """
        return self.object.getRawContents(self.reader, JString(docid))

    def get_indexed_document_contents(self, docid: str) -> str:
        """Returns the indexed document contents for a collection ``docid``.

        Parameters
        ----------
        docid : str
            The collection ``docid``.

        Returns
        -------
        str
            The index document contents.
        """
        return self.object.getIndexedContents(self.reader, JString(docid))

    def compute_bm25_term_weight(self, docid: str, term: str) -> float:
        """Computes the BM25 weight of an (analyzed) term in a document. Note that this method takes the analyzed
        (i.e., stemmed) form because the most common use case is to take the term from the output of
        :func:`get_document_vector`.

        Parameters
        ----------
        docid : str
            The collection ``docid``.
        term : str
            The (analyzed) term.

        Returns
        -------
        float
            The BM25 weight of the term in the document, or ``NaN`` if the term does not exist in the document.
        """
        return self.object.getBM25TermWeight(self.reader, JString(docid), JString(term.encode('utf-8')))

    def convert_internal_docid_to_collection_docid(self, docid: int) -> str:
        """Converts Lucene's internal ``docid`` to its external collection ``docid``.

        Parameters
        ----------
        docid : int
            A Lucene internal ``docid``.

        Returns
        -------
        str
            The external collection ``docid`` corresponding to Lucene's internal ``docid``.
        """
        return self.object.convertLuceneDocidToDocid(self.reader, docid)

    def convert_collection_docid_to_internal_docid(self, docid: str) -> int:
        """Converts an external collection ``docid`` to its Lucene's internal ``docid``.

        Parameters
        ----------
        docid : str
            An external collection ``docid``.

        Returns
        -------
        str
            The Lucene internal ``docid`` corresponding to the external collection ``docid``.
        """
        return self.object.convertDocidToLuceneDocid(self.reader, docid)
