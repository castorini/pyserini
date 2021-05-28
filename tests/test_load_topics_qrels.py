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

import os
import unittest

from pyserini import search


class TestLoadTopics(unittest.TestCase):

    def test_trec1_adhoc(self):
        topics = search.get_topics('trec1-adhoc')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec1_adhoc_qrels(self):
        qrels = search.get_qrels('trec1-adhoc')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2_adhoc(self):
        topics = search.get_topics('trec2-adhoc')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2_adhoc_qrels(self):
        qrels = search.get_qrels('trec2-adhoc')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec3_adhoc(self):
        topics = search.get_topics('trec3-adhoc')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec3_adhoc_qrels(self):
        qrels = search.get_qrels('trec3-adhoc')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_robust04(self):
        topics = search.get_topics('robust04')
        self.assertEqual(len(topics), 250)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_robust04_qrels(self):
        qrels = search.get_qrels('robust04')
        self.assertEqual(len(qrels), 249)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_robust05(self):
        topics = search.get_topics('robust05')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_robust05_qrels(self):
        qrels = search.get_qrels('robust05')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_core17(self):
        topics = search.get_topics('core17')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_core17_qrels(self):
        qrels = search.get_qrels('core17')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_core18(self):
        topics = search.get_topics('core18')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_core18_qrels(self):
        qrels = search.get_qrels('core18')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_wt10g(self):
        topics = search.get_topics('wt10g')
        self.assertEqual(len(topics), 100)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_wt10g_qrels(self):
        qrels = search.get_qrels('wt10g')
        self.assertEqual(len(qrels), 100)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2004_terabyte(self):
        topics = search.get_topics('trec2004-terabyte')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2004_terabyte_qrels(self):
        qrels = search.get_qrels('trec2004-terabyte')
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2005_terabyte(self):
        topics = search.get_topics('trec2005-terabyte')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2005_terabyte_qrels(self):
        qrels = search.get_qrels('trec2005-terabyte')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2006_terabyte(self):
        topics = search.get_topics('trec2006-terabyte')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2006_terabyte_qrels(self):
        qrels = search.get_qrels('trec2006-terabyte')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2007_million_query(self):
        topics = search.get_topics('trec2007-million-query')
        self.assertEqual(len(topics), 10000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2008_million_query(self):
        topics = search.get_topics('trec2008-million-query')
        self.assertEqual(len(topics), 10000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2009_million_query(self):
        topics = search.get_topics('trec2009-million-query')
        self.assertEqual(len(topics), 40000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2010_web(self):
        topics = search.get_topics('trec2010-web')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2011_web(self):
        topics = search.get_topics('trec2011-web')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2011_web_qrels(self):
        qrels = search.get_qrels('trec2011-web')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2012_web(self):
        topics = search.get_topics('trec2012-web')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2012_web_qrels(self):
        qrels = search.get_qrels('trec2012-web')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2013_web(self):
        topics = search.get_topics('trec2013-web')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2013_web_qrels(self):
        qrels = search.get_topics('trec2013-web')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2014_web(self):
        topics = search.get_topics('trec2014-web')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2014_web_qrels(self):
        qrels = search.get_qrels('trec2014-web')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb11(self):
        topics = search.get_topics('mb11')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb11_qrels(self):
        qrels = search.get_qrels('mb11')
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb12(self):
        topics = search.get_topics('mb12')
        self.assertEqual(len(topics), 60)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb12_qrels(self):
        qrels = search.get_qrels('mb12')
        self.assertEqual(len(qrels), 59)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb13(self):
        topics = search.get_topics('mb13')
        self.assertEqual(len(topics), 60)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb13_qrels(self):
        qrels = search.get_qrels('mb13')
        self.assertEqual(len(qrels), 60)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb14(self):
        topics = search.get_topics('mb14')
        self.assertEqual(len(topics), 55)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb14_qrels(self):
        qrels = search.get_qrels('mb14')
        self.assertEqual(len(qrels), 55)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_car15(self):
        topics = search.get_topics('car17v1.5-benchmarkY1test')
        self.assertEqual(len(topics), 2125)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

    def test_car15_qrels(self):
        qrels = search.get_qrels('car17v1.5-benchmarkY1test')
        self.assertEqual(len(qrels), 2125)
        self.assertFalse(isinstance(next(iter(qrels.keys())), int))

    def test_car20(self):
        topics = search.get_topics('car17v2.0-benchmarkY1test')
        self.assertEqual(len(topics), 2254)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

    def test_car20_qrels(self):
        qrels = search.get_qrels('car17v2.0-benchmarkY1test')
        self.assertEqual(len(qrels), 2254)
        self.assertFalse(isinstance(next(iter(qrels.keys())), int))

    def test_dl19_doc(self):
        topics = search.get_topics('dl19-doc')
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_dl19_doc_qrels(self):
        qrels = search.get_qrels('dl19-doc')
        self.assertEqual(len(qrels), 43)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl19_passage(self):
        topics = search.get_topics('dl19-passage')
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_dl19_passage_qrels(self):
        qrels = search.get_qrels('dl19-passage')
        self.assertEqual(len(qrels), 43)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl20(self):
        topics = search.get_topics('dl20')
        self.assertEqual(len(topics), 200)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_dl20_doc_qrels(self):
        qrels = search.get_qrels('dl20-doc')
        self.assertEqual(len(qrels), 45)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl20_passage_qrels(self):
        qrels = search.get_qrels('dl20-passage')
        self.assertEqual(len(qrels), 54)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_msmarco_doc(self):
        topics = search.get_topics('msmarco-doc-dev')
        self.assertEqual(len(topics), 5193)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_doc_qrels(self):
        qrels = search.get_qrels('msmarco-doc-dev')
        self.assertEqual(len(qrels), 5193)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_doc_test(self):
        topics = search.get_topics('msmarco-doc-test')
        self.assertEqual(len(topics), 5793)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage(self):
        topics = search.get_topics('msmarco-passage-dev-subset')
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_qrels(self):
        qrels = search.get_qrels('msmarco-passage-dev-subset')
        self.assertEqual(len(qrels), 6980)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_passage_test(self):
        topics = search.get_topics('msmarco-passage-test-subset')
        self.assertEqual(len(topics), 6837)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_ntcir8_zh(self):
        topics = search.get_topics('ntcir8-zh')
        self.assertEqual(len(topics), 73)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

    def test_ntcir8_zh_qrels(self):
        qrels = search.get_qrels('ntcir8-zh')
        self.assertEqual(len(qrels), 100)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))

    def test_clef2006_fr(self):
        topics = search.get_topics('clef2006-fr')
        self.assertEqual(len(topics), 49)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

    def test_clef2006_fr_qrels(self):
        qrels = search.get_qrels('clef2006-fr')
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))

    def test_trec2002_ar(self):
        topics = search.get_topics('trec2002-ar')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2002_ar_qrels(self):
        qrels = search.get_qrels('trec2002-ar')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_bn(self):
        topics = search.get_topics('fire2012-bn')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_fire2012_bn_qrels(self):
        qrels = search.get_qrels('fire2012-bn')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_hi(self):
        topics = search.get_topics('fire2012-hi')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_fire2012_hi_qrels(self):
        qrels = search.get_qrels('fire2012-hi')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_en(self):
        topics = search.get_topics('fire2012-en')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_fire2012_en_qrels(self):
        qrels = search.get_qrels('fire2012-en')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2020_bl(self):
        topics = search.get_topics('trec2020-bl')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_epidemic_qa_expert_prelim(self):
        topics = search.get_topics('epidemic-qa-expert-prelim')
        self.assertEqual(len(topics), 45)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_epidemic_qa_consumer_prelim(self):
        topics = search.get_topics('epidemic-qa-consumer-prelim')
        self.assertEqual(len(topics), 42)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_nq_dev(self):
        topics = search.get_topics('dpr-nq-dev')
        self.assertEqual(len(topics), 8757)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_nq_test(self):
        topics = search.get_topics('dpr-nq-test')
        self.assertEqual(len(topics), 3610)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_wq_test(self):
        topics = search.get_topics('dpr-wq-test')
        self.assertEqual(len(topics), 2032)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_squad_test(self):
        topics = search.get_topics('dpr-squad-test')
        self.assertEqual(len(topics), 10570)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_curated_test(self):
        topics = search.get_topics('dpr-curated-test')
        self.assertEqual(len(topics), 694)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_trivia_test(self):
        topics = search.get_topics('dpr-trivia-test')
        self.assertEqual(len(topics), 11313)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_trivia_dev(self):
        topics = search.get_topics('dpr-trivia-dev')
        self.assertEqual(len(topics), 8837)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round1(self):
        topics = search.get_topics('covid-round1')
        self.assertEqual(len(topics), 30)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus remdesivir', topics[30]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round1_qrels(self):
        qrels = search.get_qrels('covid-round1')
        self.assertEqual(len(qrels), 30)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round1_udel(self):
        topics = search.get_topics('covid-round1-udel')
        self.assertEqual(len(topics), 30)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus remdesivir remdesivir effective treatment COVID-19', topics[30]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round2(self):
        topics = search.get_topics('covid-round2')
        self.assertEqual(len(topics), 35)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus public datasets', topics[35]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round2_qrels(self):
        qrels = search.get_qrels('covid-round2')
        self.assertEqual(len(qrels), 35)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round2_udel(self):
        topics = search.get_topics('covid-round2-udel')
        self.assertEqual(len(topics), 35)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus public datasets public datasets COVID-19', topics[35]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round3(self):
        topics = search.get_topics('covid-round3')
        self.assertEqual(len(topics), 40)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus mutations', topics[40]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round3_qrels(self):
        qrels = search.get_qrels('covid-round3')
        self.assertEqual(len(qrels), 40)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round3_udel(self):
        topics = search.get_topics('covid-round3-udel')
        self.assertEqual(len(topics), 40)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus mutations observed mutations SARS-CoV-2 genome mutations', topics[40]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round4(self):
        topics = search.get_topics('covid-round4')
        self.assertEqual(len(topics), 45)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus mental health impact', topics[45]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round4_qrels(self):
        qrels = search.get_qrels('covid-round4')
        self.assertEqual(len(qrels), 45)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round4_udel(self):
        topics = search.get_topics('covid-round4-udel')
        self.assertEqual(len(topics), 45)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus mental health impact COVID-19 pandemic impacted mental health',
                         topics[45]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round5(self):
        topics = search.get_topics('covid-round5')
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round5_qrels(self):
        qrels = search.get_qrels('covid-round5')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2018_bl(self):
        topics = search.get_topics('trec2018-bl')
        self.assertEqual(len(topics), 50)
        self.assertEqual('fef0f232a9bd94bdb96bac48c7705503', topics[393]['title'])
        self.assertEqual('a1c41a70-35c7-11e3-8a0e-4e2cf80831fc', topics[825]['title'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2018_bl_qrels(self):
        qrels = search.get_qrels('trec2018-bl')
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))
    
    def test_trec2019_bl(self):
        topics = search.get_topics('trec2019-bl')
        self.assertEqual(len(topics), 60)
        self.assertEqual('d7d906991e2883889f850de9ae06655e', topics[870]['title'])
        self.assertEqual('0d7f5e24cafc019265d3ee4b9745e7ea', topics[829]['title'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2019_bl_qrels(self):
        qrels = search.get_qrels('trec2019-bl')
        self.assertEqual(len(qrels), 57)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_tsv_int_topicreader(self):
        # Running from command-line, we're in root of repo, but running in IDE, we're in tests/
        path = 'tools/topics-and-qrels/topics.msmarco-doc.dev.txt'
        if not os.path.exists(path):
            path = f'../{path}'

        self.assertTrue(os.path.exists(path))
        topics = search.get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader', path)
        self.assertEqual(len(topics), 5193)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        self.assertEqual(search.get_topics('msmarco-doc-dev'), topics)

    def test_trec_topicreader(self):
        # Running from command-line, we're in root of repo, but running in IDE, we're in tests/
        path = 'tools/topics-and-qrels/topics.robust04.txt'
        if not os.path.exists(path):
            path = f'../{path}'

        self.assertTrue(os.path.exists(path))
        topics = search.get_topics_with_reader('io.anserini.search.topicreader.TrecTopicReader', path)
        self.assertEqual(len(topics), 250)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        self.assertEqual(search.get_topics('robust04'), topics)


if __name__ == '__main__':
    unittest.main()
