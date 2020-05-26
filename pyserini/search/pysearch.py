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
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``SimpleSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
from typing import Dict, List, Union

from ..pyclass import JSimpleSearcher, JSimpleSearcherResult, JDocument, JString, JArrayList, JTopics, JTopicReader, \
    JQueryGenerator, JSimpleNearestNeighborSearcherResult, JSimpleNearestNeighborSearcher, JQuery, autoclass

logger = logging.getLogger(__name__)


class Document:
    """Wrapper class for a Lucene ``Document``.

    Parameters
    ----------
    document : JDocument
        Underlying Lucene ``Document``.
    """

    def __init__(self, document):
        if document is None:
            raise ValueError('Cannot create a Document with None.')
        self.object = document

    def docid(self: JDocument) -> str:
        return self.object.getField('id').stringValue()

    def id(self: JDocument) -> str:
        # Convenient alias for docid()
        return self.object.getField('id').stringValue()

    def lucene_document(self: JDocument) -> JDocument:
        return self.object

    def contents(self: JDocument) -> str:
        return self.object.get('contents')

    def raw(self: JDocument) -> str:
        return self.object.get('raw')

    def get(self: JDocument, field: str) -> str:
        return self.object.get(field)


class SimpleSearcher:
    """Wrapper class for ``SimpleSearcher`` in Anserini.

    Parameters
    ----------
    index_dir : str
        Path to Lucene index directory.
    """

    def __init__(self, index_dir: str):
        self.object = JSimpleSearcher(JString(index_dir))
        self.num_docs = self.object.getTotalNumDocuments()

    def search(self, q: Union[str, JQuery], k: int = 10,
               query_generator: JQueryGenerator = None) -> List[JSimpleSearcherResult]:
        """Searches the collection.

        Parameters
        ----------
        q : Union[str, JQuery]
            The query string or the ``JQuery`` objected.
        k : int
            The number of hits to return.
        query_generator : JQueryGenerator
            Generator to build queries.

        Returns
        -------
        List[JSimpleSearcherResult]
            List of search results.
        """
        if query_generator:
            return self.object.search(query_generator, JString(q), k)
        elif isinstance(q, JQuery):
            # Note that RM3 requires the notion of a query (string) to estimate the appropriate models. If we're just
            # given a Lucene query, it's unclear what the "query" is for this estimation. One possibility is to extract
            # all the query terms from the Lucene query, although this might yield unexpected behavior from the user's
            # perspective. Until we think through what exactly is the "right thing to do", we'll raise an exception
            # here explicitly.
            if self.is_using_rm3():
                raise NotImplementedError('RM3 incompatible with search using a Lucene query.')
            return self.object.search(q, k)
        else:
            return self.object.search(JString(q.encode('utf8')), k)

    def batch_search(self, queries: List[str], qids: List[str], k: int = 10,
                     threads: int = 1) -> Dict[str, List[JSimpleSearcherResult]]:
        """Searches the collection concurrently for multiple queries, using multiple threads.

        Parameters
        ----------
        queries : List[str]
            A list of query strings.
        qids : List[str]
            A list of corresponding query ids.
        k : int
            The number of hits to return.
        threads : int
            The maximum number of threads to use.

        Returns
        -------
        Dict[str, List[JSimpleSearcherResult]]
            A dictionary holding the search results, with the query ids as keys and the corresponding lists of search
            results as the values.
        """
        query_strings = JArrayList()
        qid_strings = JArrayList()
        for query in queries:
            jq = JString(query.encode('utf8'))
            query_strings.add(jq)

        for qid in qids:
            jqid = JString(qid)
            qid_strings.add(jqid)

        results = self.object.batchSearch(query_strings, qid_strings, int(k), int(threads)).entrySet().toArray()
        return {r.getKey(): r.getValue() for r in results}

    def search_fields(self, q, f, boost, k):
        """Searches the collection, scoring a separate field with a boost weight.

        Parameters
        ----------
        q : str
            Query string.
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
        """
        return self.object.searchFields(JString(q), JString(f), float(boost), k)

    def set_analyzer(self, analyzer):
        """
        Parameters
        ----------
        analyzer : Analyzer
            Java analyzer object
        """
        self.object.setAnalyzer(analyzer)

    def set_rm3(self, fb_terms=10, fb_docs=10, original_query_weight=float(0.5), rm3_output_query=False):
        """Configures RM3 query expansion.

        Parameters
        ----------
        fb_terms : int
            RM3 parameter for number of expansion terms.
        fb_docs : int
            RM3 parameter for number of expansion documents.
        original_query_weight : float
            RM3 parameter for weight to assign to the original query.
        rm3_output_query : bool
            Whether we want to print the original and expanded as debug output.
        """
        self.object.setRM3(fb_terms, fb_docs, original_query_weight, rm3_output_query)

    def unset_rm3(self):
        """Turns off use of RM3 query expansion.
        """
        self.object.unsetRM3()

    def is_using_rm3(self) -> bool:
        """Returns whether or not RM3 query expansion is being performed.
        """
        return self.object.useRM3()

    def set_qld(self, mu=float(1000)):
        """Configures query likelihood with Dirichlet smoothing as the scoring function.

        Parameters
        ----------
        mu : float
            Dirichlet smoothing parameter mu.
        """
        self.object.setQLD(float(mu))

    def set_bm25(self, k1=float(0.9), b=float(0.4)):
        """Configures BM25 as the scoring function.

        Parameters
        ----------
        k1 : float
            BM25 k1 parameter.
        b : float
            BM25 b parameter.
        """
        self.object.setBM25(float(k1), float(b))

    def get_similarity(self):
        """Returns the Lucene ``Similarity`` used as the scoring function.
        """
        return self.object.getSimilarity()

    def doc(self, docid: Union[str, int]) -> Document:
        """Returns the :class:`Document` corresponding to ``docid``. The ``docid`` is overloaded: if it is of type
        ``str``, it is treated as an external collection ``docid``; if it is of type ``int``, it is treated as an
        internal Lucene ``docid``. Returns ``None`` if the ``docid`` does not exist in the index.

        Parameters
        ----------
        docid : Union[str, int]
            Overloaded ``docid``: either an external collection ``docid`` (``str``) or an internal Lucene ``docid``
            (``int``).

        Returns
        -------
        Document
            :class:`Document` corresponding to the ``docid``.
        """
        lucene_document = self.object.document(docid)
        if lucene_document is None:
            return None
        return Document(lucene_document)

    def doc_by_field(self, field: str, q: str) -> str:
        """Returns the :class:`Document` based on a ``field`` with ``id``. For example, this method can be used to fetch
        document based on alternative primary keys that have been indexed, such as an article's DOI. Returns ``None`` if
        no such document exists.

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
        lucene_document = self.object.documentByField(JString(field), JString(q))
        if lucene_document is None:
            return None
        return Document(lucene_document)

    def close(self):
        self.object.close()


def get_topics(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        Topics as a dictionary
    """
    topics = None
    if collection_name == 'robust04':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.ROBUST04)
    elif collection_name == 'robust05':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.ROBUST05)
    elif collection_name == 'core17':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE17)
    elif collection_name == 'core18':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE18)
    elif collection_name == 'car17v1.5_benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V15_BENCHMARK_Y1_TEST)
    elif collection_name == 'car17v2.0_benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V20_BENCHMARK_Y1_TEST)
    elif collection_name == 'msmarco_doc_dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_DOC_DEV)
    elif collection_name == 'msmarco_passage_dev_subset':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_PASSAGE_DEV_SUBSET)
    elif collection_name == 'covid_round1':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND1)
    elif collection_name == 'covid_round1_udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND1_UDEL)
    elif collection_name == 'covid_round2':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND2)
    elif collection_name == 'covid_round2_udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND2_UDEL)
    elif collection_name == 'covid_round3':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND3)
    elif collection_name == 'covid_round3_udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND3_UDEL)
    else:
        return {}
    t = {}
    for topic in topics.keySet().toArray():
        # Try and parse the keys into integers
        try:
            topic_key = int(topic)
        except ValueError:
            topic_key = topic
        t[topic_key] = {}
        for key in topics.get(topic).keySet().toArray():
            t[topic_key][key] = topics.get(topic).get(key)
    return t


class LuceneSimilarities:
    @staticmethod
    def bm25(k1=0.9, b=0.4):
        return autoclass('org.apache.lucene.search.similarities.BM25Similarity')(k1, b)

    @staticmethod
    def qld(mu=1000):
        return autoclass('org.apache.lucene.search.similarities.LMDirichletSimilarity')(mu)


class SimpleNearestNeighborSearcher:

    def __init__(self, index_dir: str):
        self.object = JSimpleNearestNeighborSearcher(JString(index_dir))

    def search(self, q: str, k=10) -> List[JSimpleNearestNeighborSearcherResult]:
        """Searches nearest neighbor of an embedding identified by its id.

        Parameters
        ----------
        q : id
            The input embedding id.
        k : int
            The number of nearest neighbors to return.

        Returns
        -------
        List(JSimpleNearestNeighborSearcherResult]
            List of (nearest neighbor) search results.
        """
        return self.object.search(JString(q), k)

    def multisearch(self, q: str, k=10) -> List[List[JSimpleNearestNeighborSearcherResult]]:
        """Searches nearest neighbors of all the embeddings having the specified id.

        Parameters
        ----------
        q : id
            The input embedding id.
        k : int
            The number of nearest neighbors to return for each found embedding.

        Returns
        -------
        List(List[JSimpleNearestNeighborSearcherResult])
            List of List of (nearest neighbor) search results (one for each matching id).
        """
        return self.object.multisearch(JString(q), k)


