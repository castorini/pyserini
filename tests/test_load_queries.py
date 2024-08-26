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

    def test_trec2_adhoc(self):
        topics = search.get_topics('trec2-adhoc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec3_adhoc(self):
        topics = search.get_topics('trec3-adhoc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_robust04(self):
        topics = search.get_topics('robust04')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 250)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_robust05(self):
        topics = search.get_topics('robust05')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_core17(self):
        topics = search.get_topics('core17')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_core18(self):
        topics = search.get_topics('core18')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_wt10g(self):
        topics = search.get_topics('wt10g')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 100)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2004_terabyte(self):
        topics = search.get_topics('trec2004-terabyte')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2005_terabyte(self):
        topics = search.get_topics('trec2005-terabyte')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2006_terabyte(self):
        topics = search.get_topics('trec2006-terabyte')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

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

    def test_trec2012_web(self):
        topics = search.get_topics('trec2012-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2013_web(self):
        topics = search.get_topics('trec2013-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2014_web(self):
        topics = search.get_topics('trec2014-web')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb11(self):
        topics = search.get_topics('mb11')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb12(self):
        topics = search.get_topics('mb12')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 60)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb13(self):
        topics = search.get_topics('mb13')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 60)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mb14(self):
        topics = search.get_topics('mb14')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 55)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_car15(self):
        topics = search.get_topics('car17v1.5-benchmarkY1test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2125)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

    def test_car20(self):
        topics = search.get_topics('car17v2.0-benchmarkY1test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2254)
        self.assertFalse(isinstance(next(iter(topics.keys())), int))

    # MS MARCO V1
    def test_msmarco_doc(self):
        topics = search.get_topics('msmarco-doc-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5193)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-doc-dev-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5193)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-doc-dev-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5193)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-doc-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5793)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage(self):
        topics = search.get_topics('msmarco-passage-dev-subset')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-passage-dev-subset-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-passage-dev-subset-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-passage-test-subset')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6837)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_deepimpact(self):
        topics = search.get_topics('msmarco-passage-dev-subset-deepimpact')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_unicoil_tidle(self):
        topics = search.get_topics('msmarco-passage-dev-subset-unicoil-tilde')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_msmarco_passage_distill_splade_max(self):
        topics = search.get_topics('msmarco-passage-dev-subset-distill-splade-max')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6980)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dl19_doc(self):
        topics = search.get_topics('dl19-doc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl19-doc-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl19-doc-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_dl19_passage(self):
        topics = search.get_topics('dl19-passage')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl19-passage-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl19-passage-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 43)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_dl20(self):
        topics = search.get_topics('dl20')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 200)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl20-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 200)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl20-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 200)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    # MS MARCO V2
    def test_msmarco_v2_doc(self):
        topics = search.get_topics('msmarco-v2-doc-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4552)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        # This is an alias used by Anserini fatjar regressions, making sure it works in Pyserini also.
        topics = search.get_topics('msmarco-v2-doc.dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4552)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-doc-dev-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4552)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-doc-dev-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4552)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-doc-dev2')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        # This is an alias used by Anserini fatjar regressions, making sure it works in Pyserini also.
        topics = search.get_topics('msmarco-v2-doc.dev2')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-doc-dev2-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-doc-dev2-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5000)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        qrels = search.get_qrels('msmarco-v2-doc-dev2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 5000)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_v2_passage(self):
        topics = search.get_topics('msmarco-v2-passage-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3903)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-passage-dev-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3903)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-passage-dev-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3903)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-passage-dev2')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4281)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-passage-dev2-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4281)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('msmarco-v2-passage-dev2-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4281)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_dl21(self):
        topics = search.get_topics('dl21')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 477)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        # This is an alias used by Anserini fatjar regressions, making sure it works in Pyserini also.
        topics = search.get_topics('dl21-doc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 477)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl21-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 477)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl21-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 477)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_dl22(self):
        topics = search.get_topics('dl22')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 500)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        # This is an alias used by Anserini fatjar regressions, making sure it works in Pyserini also.
        topics = search.get_topics('dl22-doc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 500)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl22-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 500)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl22-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 500)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_dl23(self):
        topics = search.get_topics('dl23')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 700)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        # This is an alias used by Anserini fatjar regressions, making sure it works in Pyserini also.
        topics = search.get_topics('dl23-doc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 700)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl23-unicoil')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 700)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('dl23-unicoil-noexp')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 700)
        self.assertFalse(isinstance(next(iter(topics.keys())), str))

    def test_rag24(self):
        topics = search.get_topics('rag24.raggy-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 120)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('rag24.researchy-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 600)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('rag24.test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 301)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

    # Various multi-lingual test collections
    def test_ntcir8_zh(self):
        topics = search.get_topics('ntcir8-zh')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 73)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

    def test_clef2006_fr(self):
        topics = search.get_topics('clef2006-fr')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 49)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

    def test_trec2002_ar(self):
        topics = search.get_topics('trec2002-ar')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_fire2012_bn(self):
        topics = search.get_topics('fire2012-bn')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_fire2012_hi(self):
        topics = search.get_topics('fire2012-hi')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_fire2012_en(self):
        topics = search.get_topics('fire2012-en')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

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

    # GarT5 topics
    def test_gart5_nq_test(self):
        topics = search.get_topics('nq-test-gar-t5-answers')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3610)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('nq-test-gar-t5-titles')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3610)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('nq-test-gar-t5-sentences')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3610)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('nq-test-gar-t5-all')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3610)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_gart5_trivia_test(self):
        topics = search.get_topics('dpr-trivia-test-gar-t5-answers')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 11313)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('dpr-trivia-test-gar-t5-titles')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 11313)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('dpr-trivia-test-gar-t5-sentences')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 11313)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('dpr-trivia-test-gar-t5-all')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 11313)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    # TREC-COVID    
    def test_covid_round1(self):
        topics = search.get_topics('covid-round1')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 30)
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('coronavirus remdesivir', topics[30]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

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
        self.assertEqual('coronavirus origin', topics[1]['query'])
        self.assertEqual('mRNA vaccine coronavirus', topics[50]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('covid-round5-udel')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertEqual('coronavirus origin origin COVID-19', topics[1]['query'])
        self.assertEqual('mRNA vaccine coronavirus mRNA vaccine SARS-CoV-2 virus', topics[50]['query'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    # TREC News Tracks
    def test_trec2018_bl(self):
        topics = search.get_topics('trec2018-bl')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertEqual('fef0f232a9bd94bdb96bac48c7705503', topics[393]['title'])
        self.assertEqual('a1c41a70-35c7-11e3-8a0e-4e2cf80831fc', topics[825]['title'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2019_bl(self):
        topics = search.get_topics('trec2019-bl')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 60)
        self.assertEqual('d7d906991e2883889f850de9ae06655e', topics[870]['title'])
        self.assertEqual('0d7f5e24cafc019265d3ee4b9745e7ea', topics[829]['title'])
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_trec2020_bl(self):
        topics = search.get_topics('trec2020-bl')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_ar(self):
        topics = search.get_topics('mrtydi-v1.1-arabic-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 12377)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-arabic-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3115)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-arabic-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1081)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_bn(self):
        topics = search.get_topics('mrtydi-v1.1-bengali-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1713)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-bengali-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 440)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-bengali-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 111)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_en(self):
        topics = search.get_topics('mrtydi-v1.1-english-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3547)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-english-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 878)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-english-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 744)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_fi(self):
        topics = search.get_topics('mrtydi-v1.1-finnish-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6561)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-finnish-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1738)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-finnish-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1254)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_id(self):
        topics = search.get_topics('mrtydi-v1.1-indonesian-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4902)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-indonesian-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1224)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-indonesian-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 829)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_ja(self):
        topics = search.get_topics('mrtydi-v1.1-japanese-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3697)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-japanese-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 928)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-japanese-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 720)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_ko(self):
        topics = search.get_topics('mrtydi-v1.1-korean-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1295)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-korean-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 303)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-korean-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 421)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_ru(self):
        topics = search.get_topics('mrtydi-v1.1-russian-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 5366)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-russian-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1375)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-russian-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 995)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_sw(self):
        topics = search.get_topics('mrtydi-v1.1-swahili-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2072)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-swahili-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 526)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-swahili-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 670)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_te(self):
        topics = search.get_topics('mrtydi-v1.1-telugu-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3880)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-telugu-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 983)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-telugu-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 646)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_mrtydi_11_th(self):
        topics = search.get_topics('mrtydi-v1.1-thai-train')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3319)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-thai-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 807)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('mrtydi-v1.1-thai-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1190)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_beir(self):
        topics = search.get_topics('beir-v1.0.0-trec-covid-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)

        topics = search.get_topics('beir-v1.0.0-bioasq-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 500)

        topics = search.get_topics('beir-v1.0.0-nfcorpus-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 323)

        topics = search.get_topics('beir-v1.0.0-nq-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 3452)

        topics = search.get_topics('beir-v1.0.0-hotpotqa-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 7405)

        topics = search.get_topics('beir-v1.0.0-fiqa-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 648)

        topics = search.get_topics('beir-v1.0.0-signal1m-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 97)

        topics = search.get_topics('beir-v1.0.0-trec-news-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 57)

        topics = search.get_topics('beir-v1.0.0-robust04-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 249)

        topics = search.get_topics('beir-v1.0.0-arguana-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1406)

        topics = search.get_topics('beir-v1.0.0-webis-touche2020-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 49)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-android-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 699)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-english-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1570)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-gaming-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1595)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-gis-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 885)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-mathematica-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 804)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-physics-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1039)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-programmers-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 876)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-stats-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 652)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-tex-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2906)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-unix-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1072)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-webmasters-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 506)

        topics = search.get_topics('beir-v1.0.0-cqadupstack-wordpress-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 541)

        topics = search.get_topics('beir-v1.0.0-quora-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10000)

        topics = search.get_topics('beir-v1.0.0-dbpedia-entity-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 400)

        topics = search.get_topics('beir-v1.0.0-scidocs-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1000)

        topics = search.get_topics('beir-v1.0.0-fever-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 6666)

        topics = search.get_topics('beir-v1.0.0-climate-fever-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1535)

        topics = search.get_topics('beir-v1.0.0-scifact-test')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 300)
    
    def test_hc4_1_0_fa(self):
        topics = search.get_topics('hc4-v1.0-fa-dev-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-dev-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-dev-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-test-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-test-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-test-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-en-test-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-en-test-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-fa-en-test-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_hc4_1_0_ru(self):
        topics = search.get_topics('hc4-v1.0-ru-dev-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-dev-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-dev-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 4)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-test-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-test-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-test-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-en-test-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-en-test-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-ru-en-test-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_hc4_1_0_zh(self):
        topics = search.get_topics('hc4-v1.0-zh-dev-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-zh-dev-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-zh-dev-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 10)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-zh-en-test-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-zh-en-test-desc')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('hc4-v1.0-zh-en-test-desc-title')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 50)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_neurclir22(self):
        for key in ['neuclir22-en-title', 'neuclir22-en-title', 'neuclir22-en-desc-title']:
            topics = search.get_topics(key)
            self.assertIsNotNone(topics)
            self.assertEqual(len(topics), 114)
            self.assertTrue(isinstance(next(iter(topics.keys())), int))

        for key in ['neuclir22-fa-ht-title', 'neuclir22-fa-ht-desc', 'neuclir22-fa-ht-desc-title',
                    'neuclir22-fa-mt-title', 'neuclir22-fa-mt-desc', 'neuclir22-fa-mt-desc-title']:
            topics = search.get_topics(key)
            self.assertIsNotNone(topics)
            self.assertEqual(len(topics), 114)
            self.assertTrue(isinstance(next(iter(topics.keys())), int))

        for key in ['neuclir22-ru-ht-title', 'neuclir22-ru-ht-desc', 'neuclir22-ru-ht-desc-title',
                    'neuclir22-ru-mt-title', 'neuclir22-ru-mt-desc', 'neuclir22-ru-mt-desc-title']:
            topics = search.get_topics(key)
            self.assertIsNotNone(topics)
            self.assertEqual(len(topics), 114)
            self.assertTrue(isinstance(next(iter(topics.keys())), int))

        for key in ['neuclir22-zh-ht-title', 'neuclir22-zh-ht-desc', 'neuclir22-zh-ht-desc-title',
                    'neuclir22-zh-mt-title', 'neuclir22-zh-mt-desc', 'neuclir22-zh-mt-desc-title']:
            topics = search.get_topics(key)
            self.assertIsNotNone(topics)
            self.assertEqual(len(topics), 114)
            self.assertTrue(isinstance(next(iter(topics.keys())), int))

    def test_miracl_10(self):
        topics = search.get_topics('miracl-v1.0-ar-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 2896)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-bn-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 411)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-en-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 799)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-es-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 648)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('miracl-v1.0-fa-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 632)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('miracl-v1.0-fi-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1271)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-fr-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 343)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('miracl-v1.0-hi-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 350)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('miracl-v1.0-id-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 960)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-ja-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 860)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-ko-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 213)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-ru-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 1252)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-sw-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 482)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-te-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 828)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-th-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 733)
        self.assertTrue(isinstance(next(iter(topics.keys())), int))

        topics = search.get_topics('miracl-v1.0-zh-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 393)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('miracl-v1.0-de-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 305)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

        topics = search.get_topics('miracl-v1.0-yo-dev')
        self.assertIsNotNone(topics)
        self.assertEqual(len(topics), 119)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))

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

    def test_trec_topicreader_nonint_qid(self):
        # Running from command-line, we're in root of repo, but running in IDE, we're in tests/
        path = 'tests/resources/sample_queries_nonint_qid.tsv'
        if not os.path.exists(path):
            path = f'../{path}'

        self.assertTrue(os.path.exists(path))
        topics = search.get_topics_with_reader('io.anserini.search.topicreader.TsvStringTopicReader', path)
        self.assertEqual(len(topics), 3)
        self.assertTrue(isinstance(next(iter(topics.keys())), str))
        self.assertEqual({'30_1', '30_2', '30_3'}, set(topics))


if __name__ == '__main__':
    unittest.main()
