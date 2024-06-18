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

import unittest

from pyserini import search


class TestLoadQrels(unittest.TestCase):
    @staticmethod
    def read_file_lines(path):
        with open(path) as f:
            return f.readlines()

    # Note that these test cases download and cache qrels in ~/.cache/anserini/topics-and-qrels,
    # which is hard-coded from the Anserini end. So if the original source is unavailable, these
    # tests will still pass.

    def test_trec1_adhoc(self):
        qrels = search.get_qrels('trec1-adhoc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2_adhoc(self):
        qrels = search.get_qrels('trec2-adhoc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec3_adhoc(self):
        qrels = search.get_qrels('trec3-adhoc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_robust04a(self):
        qrels_path = search.get_qrels_file('robust04')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length//2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 311410)
        self.assertEqual(first_line, "301 0 FBIS3-10082 1")
        self.assertEqual(mid_line, "409 0 LA010189-0112 0")
        self.assertEqual(last_line, "700 0 LA123090-0137 0")

    def test_robust04b(self):
        qrels = search.get_qrels('robust04')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 249)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_robust05a(self):
        qrels_path = search.get_qrels_file('robust05')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 37798)
        self.assertEqual(first_line, "303 0 APW19980609.1531 2")
        self.assertEqual(mid_line, "397 0 XIE19960920.0297 0")
        self.assertEqual(last_line, "689 0 XIE20000925.0055 0")

    def test_robust05b(self):
        qrels = search.get_qrels('robust05')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_core17a(self):
        qrels_path = search.get_qrels_file('core17')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 30030)
        self.assertEqual(first_line, "307 0 1001536 1")
        self.assertEqual(mid_line, "393 0 1586039 2")
        self.assertEqual(last_line, "690 0 996059 0")

    def test_core17b(self):
        qrels = search.get_qrels('core17')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_core18a(self):
        qrels_path = search.get_qrels_file('core18')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 26233)
        self.assertEqual(first_line, "321 0 004c6120d0aa69da29cc045da0562168 0")
        self.assertEqual(mid_line, "646 0 260365e8-eb18-11e2-a301-ea5a8116d211 0")
        self.assertEqual(last_line, "825 0 ff3a25b0-0ba4-11e4-8341-b8072b1e7348 0")

    def test_core18b(self):
        qrels = search.get_qrels('core18')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_wt10g(self):
        qrels = search.get_qrels('wt10g')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 100)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2004_terabyte(self):
        qrels = search.get_qrels('trec2004-terabyte')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2005_terabyte(self):
        qrels = search.get_qrels('trec2005-terabyte')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2006_terabyte(self):
        qrels = search.get_qrels('trec2006-terabyte')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2011_web(self):
        qrels = search.get_qrels('trec2011-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2012_web(self):
        qrels = search.get_qrels('trec2012-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2013_web(self):
        qrels = search.get_topics('trec2013-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2014_web(self):
        qrels = search.get_qrels('trec2014-web')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb11(self):
        qrels = search.get_qrels('mb11')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb12(self):
        qrels = search.get_qrels('mb12')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 59)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb13(self):
        qrels = search.get_qrels('mb13')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 60)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mb14(self):
        qrels = search.get_qrels('mb14')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 55)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_car15a(self):
        qrels_path = search.get_qrels_file('car17v1.5-benchmarkY1test')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 5820)
        self.assertEqual(first_line, "Aftertaste/Aftertaste%20processing%20in%20the%20cerebral%20cortex "
                                     "0 38c1bd25ddca2705164677a3f598c46df85afba7 1")
        self.assertEqual(mid_line, "Insular%20cortex/Function/Interoceptive%20awareness "
                                   "0 f037f925acd4c59e802a58aa74430fc6aa163606 1")
        self.assertEqual(last_line, "Yellowstone%20National%20Park/Recreation"
                                    " 0 e80b5185da1493edde41bea19a389a3f62167369 1")

    def test_car15b(self):
        qrels = search.get_qrels('car17v1.5-benchmarkY1test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 2125)
        self.assertFalse(isinstance(next(iter(qrels.keys())), int))

    def test_car20a(self):
        qrels_path = search.get_qrels_file('car17v2.0-benchmarkY1test')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 6192)
        self.assertEqual(first_line, "enwiki:Aftertaste 0 327cca6c4d38953196fa6789f615546f03287b25 1")
        self.assertEqual(mid_line, "enwiki:Insular%20cortex/Function/Interoceptive%20awareness"
                                   " 0 f037f925acd4c59e802a58aa74430fc6aa163606 1")
        self.assertEqual(last_line, "enwiki:Yellowstone%20National%20Park/Recreation"
                                    " 0 b812fca195f74f8c563db4262260554fe3ff3731 1")

    def test_car20b(self):
        qrels = search.get_qrels('car17v2.0-benchmarkY1test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 2254)
        self.assertFalse(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_doc1(self):
        qrels_path = search.get_qrels_file('msmarco-doc-dev')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 5193)
        self.assertEqual(first_line, "2	0	D1650436	1")
        self.assertEqual(mid_line, "855050	0	D2851565	1")
        self.assertEqual(last_line, "1102400	0	D677570	1")

    def test_msmarco_doc2(self):
        qrels = search.get_qrels('msmarco-doc-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 5193)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_passage1(self):
        qrels_path = search.get_qrels_file('msmarco-passage-dev-subset')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 7437)
        self.assertEqual(first_line, "300674 0 7067032 1")
        self.assertEqual(mid_line, "573452 0 3182069 1")
        self.assertEqual(last_line, "195199 0 8009377 1")

    def test_msmarco_passage2(self):
        qrels = search.get_qrels('msmarco-passage-dev-subset')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 6980)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

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

        qrels = search.get_qrels('dl19-doc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 43)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

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

        qrels = search.get_qrels('dl19-passage')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 43)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl20(self):
        qrels = search.get_qrels('dl20-doc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 45)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl20-passage')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 54)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    # MS MARCO V2
    def test_msmarco_v2_doc(self):
        qrels = search.get_qrels('msmarco-v2-doc-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 4552)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('msmarco-v2-doc-dev2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 5000)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('msmarco-v2.1-doc.dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 4552)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('msmarco-v2.1-doc.dev2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 5000)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_msmarco_v2_passage(self):
        qrels = search.get_qrels('msmarco-v2-passage-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3903)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('msmarco-v2-passage-dev2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 4281)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_dl21(self):
        qrels = search.get_qrels('dl21-doc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 57)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 13058)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl21-doc-msmarco-v2.1')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 57)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 10973)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl21-passage')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 53)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 10828)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl22(self):
        qrels = search.get_qrels('dl22-doc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 76)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 369638)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl22-doc-msmarco-v2.1')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 76)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 349541)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl22-passage')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 76)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 386416)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_dl23(self):
        qrels = search.get_qrels('dl23-doc')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 82)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 18034)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl23-doc-msmarco-v2.1')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 82)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 15995)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

        qrels = search.get_qrels('dl23-passage')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 82)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 22327)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    def test_rag24(self):
        qrels = search.get_qrels('rag24.raggy-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 120)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 147328)
        self.assertFalse(isinstance(next(iter(qrels.keys())), str))

    # Various multi-lingual test collections
    def test_ntcir8_zh(self):
        qrels = search.get_qrels('ntcir8-zh')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 100)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))

    def test_clef2006_fr(self):
        qrels = search.get_qrels('clef2006-fr')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))

    def test_trec2002_ar(self):
        qrels = search.get_qrels('trec2002-ar')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_bn(self):
        qrels = search.get_qrels('fire2012-bn')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_hi(self):
        qrels = search.get_qrels('fire2012-hi')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_fire2012_en(self):
        qrels = search.get_qrels('fire2012-en')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round1(self):
        qrels_path = search.get_qrels_file('covid-round1')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 8691)
        self.assertEqual(first_line, "1 0.5  010vptx3 2")
        self.assertEqual(mid_line, "15 0.5  01rdlf8l 0")
        self.assertEqual(last_line, "30 0.5  zn87f1lk 1")

        qrels = search.get_qrels('covid-round1')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 30)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round2(self):
        qrels_path = search.get_qrels_file('covid-round2')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 12037)
        self.assertEqual(first_line, "1 1.5  08efpohc 0")
        self.assertEqual(mid_line, "16 2  uj0i2anr 0")
        self.assertEqual(last_line, "35 2  zzmfhr2s 0")

        qrels = search.get_qrels('covid-round2')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 35)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round3(self):
        qrels_path = search.get_qrels_file('covid-round3')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 12713)
        self.assertEqual(first_line, "1 2.5  0194oljo 1")
        self.assertEqual(mid_line, "19 2.5  s0o0egw8 2")
        self.assertEqual(last_line, "40 3  zsx7wfyj 1")

        qrels = search.get_qrels('covid-round3')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 40)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round4(self):
        qrels_path = search.get_qrels_file('covid-round4')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 13262)
        self.assertEqual(first_line, "1 4  00fmeepz 1")
        self.assertEqual(mid_line, "27 4  hmh4s3w4 0")
        self.assertEqual(last_line, "45 4  zzrsk1ls 2")

        qrels = search.get_qrels('covid-round4')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 45)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round5(self):
        qrels_path = search.get_qrels_file('covid-round5')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 23151)
        self.assertEqual(first_line, "1 4.5  005b2j4b 2")
        self.assertEqual(mid_line, "36 4.5  ylgmn69k 0")
        self.assertEqual(last_line, "50 5  zz8wvos9 1")

        qrels = search.get_qrels('covid-round5')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_covid_round3_cumulative(self):
        qrels_path = search.get_qrels_file('covid-round3-cumulative')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 33068)
        self.assertEqual(first_line, "1 0.5 010vptx3 2")
        self.assertEqual(mid_line, "17 1.5 4txctk7k 0")
        self.assertEqual(last_line, "40 3 zsx7wfyj 1")

    def test_covid_round4_cumulative(self):
        qrels_path = search.get_qrels_file('covid-round4-cumulative')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 46203)
        self.assertEqual(first_line, "1 4 00fmeepz 1")
        self.assertEqual(mid_line, "19 1 bt5857p3 0")
        self.assertEqual(last_line, "45 4 zzrsk1ls 2")

    def test_covid_complete(self):
        qrels_path = search.get_qrels_file('covid-complete')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 69318)
        self.assertEqual(first_line, "1 4.5 005b2j4b 2")
        self.assertEqual(mid_line, "23 5 71jjbyds 0")
        self.assertEqual(last_line, "50 5 zz8wvos9 1")

    def test_trec2018_bl(self):
        qrels_path = search.get_qrels_file('trec2018-bl')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 8508)
        self.assertEqual(first_line, "321 0 00f57310e5c8ec7833d6756ba637332e 16")
        self.assertEqual(mid_line, "809 0 921073ca-c0a3-11e1-9ce8-ff26651238d0 0")
        self.assertEqual(last_line, "825 0 f66b624ba8689d704872fa776fb52860 0")

        qrels = search.get_qrels('trec2018-bl')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2019_bl(self):
        qrels_path = search.get_qrels_file('trec2019-bl')
        lines = self.read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 15655)
        self.assertEqual(first_line, "826 0 0154349511cd8c49ab862d6cb0d8f6a8 2")
        self.assertEqual(mid_line, "853 0 2444d88d62539b0b88dc919909cb9701 2")
        self.assertEqual(last_line, "885 0 fde80cb0-b4f0-11e2-bbf2-a6f9e9d79e19 0")

        qrels = search.get_qrels('trec2019-bl')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 57)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_trec2020_bl(self):
        qrels = search.get_qrels('trec2020-bl')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_ar(self):
        qrels = search.get_qrels('mrtydi-v1.1-arabic-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 12377)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-arabic-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3115)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-arabic-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1081)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_bn(self):
        qrels = search.get_qrels('mrtydi-v1.1-bengali-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1713)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-bengali-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 440)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-bengali-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 111)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_en(self):
        qrels = search.get_qrels('mrtydi-v1.1-english-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3547)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-english-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 878)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-english-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 744)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_fi(self):
        qrels = search.get_qrels('mrtydi-v1.1-finnish-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 6561)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-finnish-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1738)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-finnish-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1254)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_id(self):
        qrels = search.get_qrels('mrtydi-v1.1-indonesian-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 4902)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-indonesian-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1224)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-indonesian-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 829)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_ja(self):
        qrels = search.get_qrels('mrtydi-v1.1-japanese-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3697)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-japanese-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 928)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-japanese-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 720)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_ko(self):
        qrels = search.get_qrels('mrtydi-v1.1-korean-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1295)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-korean-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 303)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-korean-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 421)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_ru(self):
        qrels = search.get_qrels('mrtydi-v1.1-russian-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 5366)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-russian-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1375)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-russian-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 995)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_sw(self):
        qrels = search.get_qrels('mrtydi-v1.1-swahili-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 2072)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-swahili-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 526)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-swahili-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 670)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_te(self):
        qrels = search.get_qrels('mrtydi-v1.1-telugu-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3880)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-telugu-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 983)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-telugu-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 646)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mrtydi_11_th(self):
        qrels = search.get_qrels('mrtydi-v1.1-thai-train')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3319)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-thai-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 807)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('mrtydi-v1.1-thai-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1190)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_mircal_10(self):
        qrels = search.get_qrels('miracl-v1.0-ar-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 2896)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-bn-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 411)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-en-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 799)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-es-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 648)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))  # note, not int

        qrels = search.get_qrels('miracl-v1.0-fa-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 632)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))  # note, not int

        qrels = search.get_qrels('miracl-v1.0-fi-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1271)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-fr-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 343)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))  # note, not int

        qrels = search.get_qrels('miracl-v1.0-hi-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 350)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))  # note, not int

        qrels = search.get_qrels('miracl-v1.0-id-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 960)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-ja-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 860)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-ko-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 213)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-ru-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1252)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-sw-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 482)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-te-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 828)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-th-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 733)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('miracl-v1.0-zh-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 393)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))  # note, not int

        qrels = search.get_qrels('miracl-v1.0-de-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 305)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))  # note, not int

        qrels = search.get_qrels('miracl-v1.0-yo-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 119)
        self.assertTrue(isinstance(next(iter(qrels.keys())), str))  # note, not int

    def test_beir(self):
        qrels = search.get_qrels('beir-v1.0.0-trec-covid-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 66334)

        qrels = search.get_qrels('beir-v1.0.0-bioasq-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 500)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 2359)

        qrels = search.get_qrels('beir-v1.0.0-nfcorpus-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 323)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 12334)

        qrels = search.get_qrels('beir-v1.0.0-nq-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 3452)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 4201)

        qrels = search.get_qrels('beir-v1.0.0-hotpotqa-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 7405)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 14810)

        qrels = search.get_qrels('beir-v1.0.0-fiqa-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 648)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1706)

        qrels = search.get_qrels('beir-v1.0.0-signal1m-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 97)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1899)

        qrels = search.get_qrels('beir-v1.0.0-trec-news-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 57)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 15655)

        qrels = search.get_qrels('beir-v1.0.0-robust04-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 249)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 311410)

        qrels = search.get_qrels('beir-v1.0.0-arguana-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1406)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1406)

        qrels = search.get_qrels('beir-v1.0.0-webis-touche2020-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 49)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 932)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-android-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 699)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1696)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-english-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1570)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 3765)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-gaming-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1595)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 2263)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-gis-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 885)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1114)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-mathematica-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 804)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1358)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-physics-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1039)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1933)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-programmers-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 876)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1675)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-stats-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 652)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 913)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-tex-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 2906)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 5154)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-unix-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1072)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1693)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-webmasters-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 506)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 1395)

        qrels = search.get_qrels('beir-v1.0.0-cqadupstack-wordpress-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 541)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 744)

        qrels = search.get_qrels('beir-v1.0.0-quora-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 10000)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 15675)

        qrels = search.get_qrels('beir-v1.0.0-dbpedia-entity-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 400)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 43515)

        qrels = search.get_qrels('beir-v1.0.0-scidocs-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1000)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 29928)

        qrels = search.get_qrels('beir-v1.0.0-fever-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 6666)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 7937)

        qrels = search.get_qrels('beir-v1.0.0-climate-fever-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 1535)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 4681)

        qrels = search.get_qrels('beir-v1.0.0-scifact-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 300)
        self.assertEqual(sum([len(qrels[topic_id]) for topic_id in qrels]), 339)
    
    def test_hc4_10_fa(self):
        qrels = search.get_qrels('hc4-v1.0-fa-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 10)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('hc4-v1.0-fa-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_hc4_10_ru(self):
        qrels = search.get_qrels('hc4-v1.0-ru-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 4)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('hc4-v1.0-ru-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_hc4_10_zh(self):
        qrels = search.get_qrels('hc4-v1.0-zh-dev')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 10)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))
        qrels = search.get_qrels('hc4-v1.0-zh-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

    def test_hc4_neuclir22(self):
        qrels = search.get_qrels('hc4-neuclir22-fa-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('hc4-neuclir22-ru-test')
        self.assertIsNotNone(qrels)
        self.assertEqual(len(qrels), 50)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))

        qrels = search.get_qrels('hc4-neuclir22-zh-test')
        self.assertIsNotNone(qrels)
        # For whatever reason, these qrels also have dev topics.
        self.assertEqual(len(qrels), 60)
        self.assertTrue(isinstance(next(iter(qrels.keys())), int))


if __name__ == '__main__':
    unittest.main()
