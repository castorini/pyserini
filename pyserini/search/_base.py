#
# Pyserini: Reproducible IR research with sparse and dense representations
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
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``SimpleSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
import os

from pyserini.util import get_cache_home
from ..pyclass import autoclass

logger = logging.getLogger(__name__)

# Wrappers around Lucene classes
JQuery = autoclass('org.apache.lucene.search.Query')
JDocument = autoclass('org.apache.lucene.document.Document')

# Wrappers around Anserini classes
JQrels = autoclass('io.anserini.eval.Qrels')
JRelevanceJudgments = autoclass('io.anserini.eval.RelevanceJudgments')
JTopicReader = autoclass('io.anserini.search.topicreader.TopicReader')
JTopics = autoclass('io.anserini.search.topicreader.Topics')
JQueryGenerator = autoclass('io.anserini.search.query.QueryGenerator')
JBagOfWordsQueryGenerator = autoclass('io.anserini.search.query.BagOfWordsQueryGenerator')
JDisjunctionMaxQueryGenerator = autoclass('io.anserini.search.query.DisjunctionMaxQueryGenerator')
JCovid19QueryGenerator = autoclass('io.anserini.search.query.Covid19QueryGenerator')


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
    if collection_name == 'trec1-adhoc':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC1_ADHOC)
    elif collection_name == 'trec2-adhoc':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2_ADHOC)
    elif collection_name == 'trec3-adhoc':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC3_ADHOC)
    elif collection_name == 'robust04':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.ROBUST04)
    elif collection_name == 'robust05':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.ROBUST05)
    elif collection_name == 'core17':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE17)
    elif collection_name == 'core18':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CORE18)
    elif collection_name == 'wt10g':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.WT10G)
    elif collection_name == 'trec2004-terabyte':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2004_TERABYTE)
    elif collection_name == 'trec2005-terabyte':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2005_TERABYTE)
    elif collection_name == 'trec2006-terabyte':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2006_TERABYTE)
    elif collection_name == 'trec2007-million-query':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2007_MILLION_QUERY)
    elif collection_name == 'trec2008-million-query':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2008_MILLION_QUERY)
    elif collection_name == 'trec2009-million-query':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2009_MILLION_QUERY)
    elif collection_name == 'trec2010-web':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2010_WEB)
    elif collection_name == 'trec2011-web':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2011_WEB)
    elif collection_name == 'trec2012-web':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2012_WEB)
    elif collection_name == 'trec2013-web':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2013_WEB)
    elif collection_name == 'trec2014-web':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2014_WEB)
    elif collection_name == 'mb11':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MB11)
    elif collection_name == 'mb12':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MB12)
    elif collection_name == 'mb13':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MB13)
    elif collection_name == 'mb14':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MB14)
    elif collection_name == 'car17v1.5-benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V15_BENCHMARK_Y1_TEST)
    elif collection_name == 'car17v2.0-benchmarkY1test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CAR17V20_BENCHMARK_Y1_TEST)
    elif collection_name == 'dl19-doc':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2019_DL_DOC)
    elif collection_name == 'dl19-passage':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2019_DL_PASSAGE)
    elif collection_name == 'dl20':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2020_DL)
    elif collection_name == 'msmarco-doc-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_DOC_DEV)
    elif collection_name == 'msmarco-doc-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_DOC_TEST)
    elif collection_name == 'msmarco-doc-v2-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_DOC_V2_DEV)
    elif collection_name == 'msmarco-doc-v2-dev2':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_DOC_V2_DEV2)
    elif collection_name == 'msmarco-passage-v2-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_PASSAGE_V2_DEV)
    elif collection_name == 'msmarco-passage-v2-dev2':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_PASSAGE_V2_DEV2)
    elif collection_name == 'msmarco-passage-dev-subset':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_PASSAGE_DEV_SUBSET)
    elif collection_name == 'msmarco-passage-test-subset':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.MSMARCO_PASSAGE_TEST_SUBSET)
    elif collection_name == 'ntcir8-zh':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.NTCIR8_ZH)
    elif collection_name == 'clef2006-fr':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.CLEF2006_FR)
    elif collection_name == 'trec2002-ar':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2002_AR)
    elif collection_name == 'fire2012-bn':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.FIRE2012_BN)
    elif collection_name == 'fire2012-hi':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.FIRE2012_HI)
    elif collection_name == 'fire2012-en':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.FIRE2012_EN)
    elif collection_name == 'covid-round1':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND1)
    elif collection_name == 'covid-round1-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND1_UDEL)
    elif collection_name == 'covid-round2':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND2)
    elif collection_name == 'covid-round2-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND2_UDEL)
    elif collection_name == 'covid-round3':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND3)
    elif collection_name == 'covid-round3-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND3_UDEL)
    elif collection_name == 'covid-round4':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND4)
    elif collection_name == 'covid-round4-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND4_UDEL)
    elif collection_name == 'covid-round5':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND5)
    elif collection_name == 'covid-round5-udel':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.COVID_ROUND5_UDEL)
    elif collection_name == 'trec2018-bl':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2018_BL)
    elif collection_name == 'trec2019-bl':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2019_BL)
    elif collection_name == 'trec2020-bl':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.TREC2020_BL)
    elif collection_name == 'epidemic-qa-expert-prelim':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.EPIDEMIC_QA_EXPERT_PRELIM)
    elif collection_name == 'epidemic-qa-consumer-prelim':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.EPIDEMIC_QA_CONSUMER_PRELIM)
    elif collection_name == 'dpr-nq-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_NQ_DEV)
    elif collection_name == 'dpr-nq-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_NQ_TEST)
    elif collection_name == 'dpr-trivia-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_TRIVIA_DEV)
    elif collection_name == 'dpr-trivia-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_TRIVIA_TEST)
    elif collection_name == 'dpr-wq-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_WQ_TEST)
    elif collection_name == 'dpr-squad-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_SQUAD_TEST)
    elif collection_name == 'dpr-curated-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.DPR_CURATED_TEST)
    elif collection_name == 'nq-dev':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.NQ_DEV)
    elif collection_name == 'nq-test':
        topics = JTopicReader.getTopicsWithStringIds(JTopics.NQ_TEST)
    else:
        raise ValueError(f'Topic {collection_name} Not Found')
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


def get_topics_with_reader(reader_class, file):
    # Yes, this is an insanely ridiculous method name.
    topics = JTopicReader.getTopicsWithStringIdsFromFileWithTopicReaderClass(reader_class, file)
    if topics is None:
        raise ValueError(f'Unable to initialize TopicReader {reader_class} with file {file}!')

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


def get_qrels_file(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    path : str
        path of the qrels file
    """
    qrels = None
    if collection_name == 'trec1-adhoc':
        qrels = JQrels.TREC1_ADHOC
    elif collection_name == 'trec2-adhoc':
        qrels = JQrels.TREC2_ADHOC
    elif collection_name == 'trec3-adhoc':
        qrels = JQrels.TREC3_ADHOC
    elif collection_name == 'robust04':
        qrels = JQrels.ROBUST04
    elif collection_name == 'robust05':
        qrels = JQrels.ROBUST05
    elif collection_name == 'core17':
        qrels = JQrels.CORE17
    elif collection_name == 'core18':
        qrels = JQrels.CORE18
    elif collection_name == 'wt10g':
        qrels = JQrels.WT10G
    elif collection_name == 'trec2004-terabyte':
        qrels = JQrels.TREC2004_TERABYTE
    elif collection_name == 'trec2005-terabyte':
        qrels = JQrels.TREC2005_TERABYTE
    elif collection_name == 'trec2006-terabyte':
        qrels = JQrels.TREC2006_TERABYTE
    elif collection_name == 'trec2011-web':
        qrels = JQrels.TREC2011_WEB
    elif collection_name == 'trec2012-web':
        qrels = JQrels.TREC2012_WEB
    elif collection_name == 'trec2013-web':
        qrels = JQrels.TREC2013_WEB
    elif collection_name == 'trec2014-web':
        qrels = JQrels.TREC2014_WEB
    elif collection_name == 'mb11':
        qrels = JQrels.MB11
    elif collection_name == 'mb12':
        qrels = JQrels.MB12
    elif collection_name == 'mb13':
        qrels = JQrels.MB13
    elif collection_name == 'mb14':
        qrels = JQrels.MB14
    elif collection_name == 'car17v1.5-benchmarkY1test':
        qrels = JQrels.CAR17V15_BENCHMARK_Y1_TEST
    elif collection_name == 'car17v2.0-benchmarkY1test':
        qrels = JQrels.CAR17V20_BENCHMARK_Y1_TEST
    elif collection_name == 'dl19-doc':
        qrels = JQrels.TREC2019_DL_DOC
    elif collection_name == 'dl19-passage':
        qrels = JQrels.TREC2019_DL_PASSAGE
    elif collection_name == 'dl20-doc':
        qrels = JQrels.TREC2020_DL_DOC
    elif collection_name == 'dl20-passage':
        qrels = JQrels.TREC2020_DL_PASSAGE
    elif collection_name == 'msmarco-doc-dev':
        qrels = JQrels.MSMARCO_DOC_DEV
    elif collection_name == 'msmarco-passage-dev-subset':
        qrels = JQrels.MSMARCO_PASSAGE_DEV_SUBSET
    elif collection_name == 'msmarco-doc-v2-dev':
        qrels = JQrels.MSMARCO_DOC_V2_DEV
    elif collection_name == 'msmarco-doc-v2-dev2':
        qrels = JQrels.MSMARCO_DOC_V2_DEV2
    elif collection_name == 'msmarco-passage-v2-dev':
        qrels = JQrels.MSMARCO_PASSAGE_V2_DEV
    elif collection_name == 'msmarco-passage-v2-dev2':
        qrels = JQrels.MSMARCO_PASSAGE_V2_DEV2
    elif collection_name == 'ntcir8-zh':
        qrels = JQrels.NTCIR8_ZH
    elif collection_name == 'clef2006-fr':
        qrels = JQrels.CLEF2006_FR
    elif collection_name == 'trec2002-ar':
        qrels = JQrels.TREC2002_AR
    elif collection_name == 'fire2012-bn':
        qrels = JQrels.FIRE2012_BN
    elif collection_name == 'fire2012-hi':
        qrels = JQrels.FIRE2012_HI
    elif collection_name == 'fire2012-en':
        qrels = JQrels.FIRE2012_EN
    elif collection_name == 'covid-complete':
        qrels = JQrels.COVID_COMPLETE
    elif collection_name == 'covid-round1':
        qrels = JQrels.COVID_ROUND1
    elif collection_name == 'covid-round2':
        qrels = JQrels.COVID_ROUND2
    elif collection_name == 'covid-round3':
        qrels = JQrels.COVID_ROUND3
    elif collection_name == 'covid-round3-cumulative':
        qrels = JQrels.COVID_ROUND3_CUMULATIVE
    elif collection_name == 'covid-round4':
        qrels = JQrels.COVID_ROUND4
    elif collection_name == 'covid-round4-cumulative':
        qrels = JQrels.COVID_ROUND4_CUMULATIVE
    elif collection_name == 'covid-round5':
        qrels = JQrels.COVID_ROUND5
    elif collection_name == 'trec2018-bl':
        qrels = JQrels.TREC2018_BL
    elif collection_name == 'trec2019-bl':
        qrels = JQrels.TREC2019_BL
    if qrels:
        target_path = os.path.join(get_cache_home(), qrels.path)
        if os.path.exists(target_path):
            return target_path
        target_dir = os.path.split(target_path)[0]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(target_path, 'w') as file:
            qrels_content = JRelevanceJudgments.getQrelsResource(qrels)
            file.write(qrels_content)
        return target_path
    raise FileNotFoundError(f'no qrels file for {collection_name}')


def get_qrels(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        qrels as a dictionary
    """
    file_path = get_qrels_file(collection_name)
    qrels = {}
    with open(file_path, 'r') as f:
        for line in f:
            qid, _, docid, judgement = line.rstrip().split()
            try:
                qrels_key = int(qid)
            except ValueError:
                qrels_key = qid
            try:
                doc_key = int(docid)
            except ValueError:
                doc_key = docid
            if qrels_key in qrels:
                qrels[qrels_key][doc_key] = judgement
            else:
                qrels[qrels_key] = {doc_key: judgement}
    return qrels
