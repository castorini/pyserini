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
from ..search.pysearch import Document
from ..analysis.pyanalysis import get_lucene_analyzer

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

    def get_term_counts(self, term: str, analyzer=get_lucene_analyzer()) -> Tuple[int, int]:      
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
            analyzer = get_lucene_analyzer(stemming=False, stopwords=False)
        
        term_map = self.object.getTermCountsWithAnalyzer(self.reader, JString(term.encode('utf-8')), analyzer)
        
        return term_map.get(JString('docFreq')), term_map.get(JString('collectionFreq'))

    def get_postings_list(self, term: str, analyzer=get_lucene_analyzer()) -> List[Posting]:
        """Returns the postings list for a term.

        Parameters
        ----------
        term : str
            The raw term.
        analyzer : analyzer
            The analyzer to apply.

        Returns
        -------
        List[Posting]
            List of :class:`Posting` objects corresponding to the postings list for the term.
        """
        if analyzer is None:
            postings_list = self.object.getPostingsListForAnalyzedTerm(self.reader, JString(term.encode('utf-8')))
        else:
            postings_list = self.object.getPostingsListWithAnalyzer(self.reader, JString(term.encode('utf-8')), analyzer)

        if postings_list is None:
            return None

        result = []
        for posting in postings_list.toArray():
            result.append(Posting(posting.getDocid(), posting.getTF(), posting.getPositions()))
        return result

    def get_document_vector(self, docid: str) -> Dict[str, int]:
        """Returns the document vector for a ``docid``. Note that requesting the document vector of a ``docid`` that
        does not exist in the index will return ``None`` (as opposed to an empty dictionary); this forces the caller
        to handle ``None`` explicitly and guards against silent errors.

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
        if doc_vector_map is None:
            return None
        doc_vector_dict = {}
        for term in doc_vector_map.keySet().toArray():
            doc_vector_dict[term] = doc_vector_map.get(JString(term.encode('utf-8')))
        return doc_vector_dict

    def doc(self, docid: str) -> str:
        """Returns the :class:`Document` corresponding to ``docid``. Returns ``None`` if the ``docid`` does not exist
        in the index.

        Parameters
        ----------
        docid : str
            The collection ``docid``.

        Returns
        -------
        Document
            :class:`Document` corresponding to the ``docid``.
        """
        lucene_document = self.object.document(self.reader, JString(docid))
        if lucene_document is None:
            return None
        return Document(lucene_document)

    def doc_by_field(self, field: str, q: str) -> str:
        """Returns the :class:`Document` based on a ``field`` with ``id``. For example, this method can be used to fetch
        document based on alternative primary keys that have been indexed, such as an article's DOI.

        Parameters
        ----------
        field : str
            The field to look up.
        q : str
            The document's unique id.

        Returns
        -------
        Document
            :class:`Document` whose ``field`` is ``id``.
        """
        lucene_document = self.object.documentByField(self.reader, JString(field), JString(q))
        if lucene_document is None:
            return None
        return Document(lucene_document)

    def doc_raw(self, docid: str) -> str:
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
        return self.object.documentRaw(self.reader, JString(docid))

    def doc_contents(self, docid: str) -> str:
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
        return self.object.documentContents(self.reader, JString(docid))

    def compute_bm25_term_weight(self, docid: str, term: str, analyzer=get_lucene_analyzer(), k1=0.9, b=0.4) -> float:
        """Computes the BM25 weight of an (analyzed) term in a document. Note that this method takes the analyzed
        (i.e., stemmed) form because the most common use case is to take the term from the output of
        :func:`get_document_vector`.

        Parameters
        ----------
        docid : str
            The collection ``docid``.
        term : str
            The (analyzed) term.
        analyzer : analyzer
            Lucene analyzer to use.
        k1 : float
            BM25 k1 parameter.
        b : float
            BM25 b parameter.

        Returns
        -------
        float
            The BM25 weight of the term in the document, or 0 if the term does not exist in the document.
        """
        if analyzer is None:
            return self.object.getBM25AnalyzedTermWeightWithParameters(self.reader, JString(docid),
                                                                       JString(term.encode('utf-8')),
                                                                       float(k1), float(b))
        else:
            return self.object.getBM25UnanalyzedTermWeightWithParameters(self.reader, JString(docid),
                                                                         JString(term.encode('utf-8')), analyzer,
                                                                         float(k1), float(b))

    def compute_query_document_score(self, docid: str, query: str, similarity=None):
        if similarity is None:
            return self.object.computeQueryDocumentScore(self.reader, docid, query)
        else:
            return self.object.computeQueryDocumentScoreWithSimilarity(self.reader, docid, query, similarity)

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

    def stats(self) -> Dict[str, int]:
        """Returns dictionary with index statistics.

        Returns
        -------
        Dict[str, int]
            Index statistics as a dictionary of statistic's name to statistic.
            - documents: number of documents
            - non_empty_documents: number of non-empty documents
            - unique_terms: number of unique terms
            - total_terms: number of total terms
        """        
        index_stats_map = self.object.getIndexStats(self.reader)

        if index_stats_map is None:
            return None

        index_stats_dict = {}
        for term in index_stats_map.keySet().toArray():
            index_stats_dict[term] = index_stats_map.get(JString(term.encode('utf-8')))
            
        return index_stats_dict
