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
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec1-adhoc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2_adhoc(self):
        topics = search.get_topics('trec2-adhoc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2-adhoc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec3_adhoc(self):
        topics = search.get_topics('trec3-adhoc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec3-adhoc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_robust04(self):
        topics = search.get_topics('robust04')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 250)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('robust04')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 249)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_robust05(self):
        topics = search.get_topics('robust05')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('robust05')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_core17(self):
        topics = search.get_topics('core17')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('core17')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_core18(self):
        topics = search.get_topics('core18')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('core18')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_wt10g(self):
        topics = search.get_topics('wt10g')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 100)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('wt10g')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 100)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2004_terabyte(self):
        topics = search.get_topics('trec2004-terabyte')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2004-terabyte')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2005_terabyte(self):
        topics = search.get_topics('trec2005-terabyte')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2005-terabyte')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2006_terabyte(self):
        topics = search.get_topics('trec2006-terabyte')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2006-terabyte')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2007_million_query(self):
        topics = search.get_topics('trec2007-million-query')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2008_million_query(self):
        topics = search.get_topics('trec2008-million-query')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2009_million_query(self):
        topics = search.get_topics('trec2009-million-query')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 40000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2010_web(self):
        topics = search.get_topics('trec2010-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2011_web(self):
        topics = search.get_topics('trec2011-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2011-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2012_web(self):
        topics = search.get_topics('trec2012-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2012-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2013_web(self):
        topics = search.get_topics('trec2013-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_topics('trec2013-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2014_web(self):
        topics = search.get_topics('trec2014-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2014-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb11(self):
        topics = search.get_topics('mb11')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('mb11')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb12(self):
        topics = search.get_topics('mb12')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 60)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('mb12')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 59)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb13(self):
        topics = search.get_topics('mb13')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 60)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('mb13')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 60)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb14(self):
        topics = search.get_topics('mb14')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 55)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('mb14')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 55)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_car15(self):
        topics = search.get_topics('car17v1.5-benchmarkY1test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2125)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('car17v1.5-benchmarkY1test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 2125)
        self.assertFalse(isinstance(next(iter(qrels.keys())), int))

    def test_car20(self):
        topics = search.get_topics('car17v2.0-benchmarkY1test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2254)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('car17v2.0-benchmarkY1test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 2254)
        self.assertFalse(isinstance(next(iter(qrels.keys())), int))

    def test_dl19_doc(self):
        topics = search.get_topics('dl19-doc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        qrels = search.get_qrels('dl19-doc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 43)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl19_passage(self):
        topics = search.get_topics('dl19-passage')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        qrels = search.get_qrels('dl19-passage')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 43)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl20(self):
        topics = search.get_topics('dl20')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 200)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        qrels = search.get_qrels('dl20-doc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 45)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl20-passage')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 54)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    # MS MARCO V1
    def test_msmarco_doc(self):
        topics = search.get_topics('msmarco-doc-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5193)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('msmarco-doc-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 5193)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_doc_test(self):
        topics = search.get_topics('msmarco-doc-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5793)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_dev(self):
        topics = search.get_topics('msmarco-passage-dev-subset')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('msmarco-passage-dev-subset')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 6980)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_passage_test(self):
        topics = search.get_topics('msmarco-passage-test-subset')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6837)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_dev_deepimpact(self):
        topics = search.get_topics('msmarco-passage-dev-subset-deepimpact')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_dev_unicoil_d2q(self):
        topics = search.get_topics('msmarco-passage-dev-subset-unicoil-d2q')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_dev_unicoil_tidle(self):
        topics = search.get_topics('msmarco-passage-dev-subset-unicoil-tilde')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_dev_distill_splade_max(self):
        topics = search.get_topics('msmarco-passage-dev-subset-distill-splade-max')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    # MS MARCO V2
    def test_msmarco_v2_doc_dev(self):
        topics = search.get_topics('msmarco-v2-doc-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4552)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('msmarco-v2-doc-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 4552)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_v2_doc_dev2(self):
        topics = search.get_topics('msmarco-v2-doc-dev2')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('msmarco-v2-doc-dev2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 5000)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_v2_passage_dev(self):
        topics = search.get_topics('msmarco-v2-passage-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3903)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('msmarco-v2-passage-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3903)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_v2_passage_dev2(self):
        topics = search.get_topics('msmarco-v2-passage-dev2')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4281)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('msmarco-v2-passage-dev2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 4281)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    # Various multi-lingual test collections
    def test_ntcir8_zh(self):
        topics = search.get_topics('ntcir8-zh')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 73)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        qrels = search.get_qrels('ntcir8-zh')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 100)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))

    def test_clef2006_fr(self):
        topics = search.get_topics('clef2006-fr')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 49)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        qrels = search.get_qrels('clef2006-fr')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))

    def test_trec2002_ar(self):
        topics = search.get_topics('trec2002-ar')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2002-ar')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_bn(self):
        topics = search.get_topics('fire2012-bn')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('fire2012-bn')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_hi(self):
        topics = search.get_topics('fire2012-hi')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('fire2012-hi')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_en(self):
        topics = search.get_topics('fire2012-en')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('fire2012-en')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    # Epidemic QA
    def test_epidemic_qa_expert_prelim(self):
        topics = search.get_topics('epidemic-qa-expert-prelim')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 45)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_epidemic_qa_consumer_prelim(self):
        topics = search.get_topics('epidemic-qa-consumer-prelim')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 42)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    # DPR datasets
    def test_dpr_nq_dev(self):
        topics = search.get_topics('dpr-nq-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 8757)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_nq_test(self):
        topics = search.get_topics('dpr-nq-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3610)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_wq_test(self):
        topics = search.get_topics('dpr-wq-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2032)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_squad_test(self):
        topics = search.get_topics('dpr-squad-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10570)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_curated_test(self):
        topics = search.get_topics('dpr-curated-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 694)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_trivia_test(self):
        topics = search.get_topics('dpr-trivia-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 11313)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dpr_trivia_dev(self):
        topics = search.get_topics('dpr-trivia-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 8837)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    # TREC-COVID
    def test_covid_round1(self):
        topics = search.get_topics('covid-round1')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 30)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus remdesivir', topics[30]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('covid-round1')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 30)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round1_udel(self):
        topics = search.get_topics('covid-round1-udel')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 30)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus remdesivir remdesivir effective treatment COVID-19', topics[30]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round2(self):
        topics = search.get_topics('covid-round2')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 35)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus public datasets', topics[35]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('covid-round2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 35)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round2_udel(self):
        topics = search.get_topics('covid-round2-udel')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 35)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus public datasets public datasets COVID-19', topics[35]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round3(self):
        topics = search.get_topics('covid-round3')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 40)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus mutations', topics[40]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('covid-round3')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 40)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round3_udel(self):
        topics = search.get_topics('covid-round3-udel')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 40)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus mutations observed mutations SARS-CoV-2 genome mutations', topics[40]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round4(self):
        topics = search.get_topics('covid-round4')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 45)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus mental health impact', topics[45]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('covid-round4')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 45)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round4_udel(self):
        topics = search.get_topics('covid-round4-udel')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 45)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('coronavirus mental health impact COVID-19 pandemic impacted mental health', topics[45]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_covid_round5(self):
        topics = search.get_topics('covid-round5')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('covid-round5')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    # TREC News Tracks
    def test_trec2018_bl(self):
        topics = search.get_topics('trec2018-bl')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertEqual('fef0f232a9bd94bdb96bac48c7705503', topics[393]['title'])
        self.assertEqual('a1c41a70-35c7-11e3-8a0e-4e2cf80831fc', topics[825]['title'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2018-bl')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))
    
    def test_trec2019_bl(self):
        topics = search.get_topics('trec2019-bl')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 60)
        self.assertEqual('d7d906991e2883889f850de9ae06655e', topics[870]['title'])
        self.assertEqual('0d7f5e24cafc019265d3ee4b9745e7ea', topics[829]['title'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2019-bl')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 57)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2020_bl(self):
        topics = search.get_topics('trec2020-bl')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('trec2020-bl')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    # General test cases
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
