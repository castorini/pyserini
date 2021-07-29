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
import shutil
import unittest

from pyserini import search


def read_file_lines(path):
    with open(path) as f:
        return f.readlines()


class TestGetQrels(unittest.TestCase):

    def setUp(self):
        os.environ['PYSERINI_CACHE'] = 'temp_dir'

    def test_robust04(self):
        qrels_path = search.get_qrels_file('robust04')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length//2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 311410)
        self.assertEqual(first_line, "301 0 FBIS3-10082 1")
        self.assertEqual(mid_line, "409 0 LA010189-0112 0")
        self.assertEqual(last_line, "700 0 LA123090-0137 0")

    def test_robust05(self):
        qrels_path = search.get_qrels_file('robust05')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 37798)
        self.assertEqual(first_line, "303 0 APW19980609.1531 2")
        self.assertEqual(mid_line, "397 0 XIE19960920.0297 0")
        self.assertEqual(last_line, "689 0 XIE20000925.0055 0")

    def test_core17(self):
        qrels_path = search.get_qrels_file('core17')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 30030)
        self.assertEqual(first_line, "307 0 1001536 1")
        self.assertEqual(mid_line, "393 0 1586039 2")
        self.assertEqual(last_line, "690 0 996059 0")

    def test_core18(self):
        qrels_path = search.get_qrels_file('core18')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 26233)
        self.assertEqual(first_line, "321 0 004c6120d0aa69da29cc045da0562168 0")
        self.assertEqual(mid_line, "646 0 260365e8-eb18-11e2-a301-ea5a8116d211 0")
        self.assertEqual(last_line, "825 0 ff3a25b0-0ba4-11e4-8341-b8072b1e7348 0")

    def test_car15(self):
        qrels_path = search.get_qrels_file('car17v1.5-benchmarkY1test')
        lines = read_file_lines(qrels_path)
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

    def test_car20(self):
        qrels_path = search.get_qrels_file('car17v2.0-benchmarkY1test')
        lines = read_file_lines(qrels_path)
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

    def test_msmarco_doc(self):
        qrels_path = search.get_qrels_file('msmarco-doc-dev')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 5193)
        self.assertEqual(first_line, "2	0	D1650436	1")
        self.assertEqual(mid_line, "855050	0	D2851565	1")
        self.assertEqual(last_line, "1102400	0	D677570	1")

    def test_msmarco_passage(self):
        qrels_path = search.get_qrels_file('msmarco-passage-dev-subset')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 7437)
        self.assertEqual(first_line, "300674 0 7067032 1")
        self.assertEqual(mid_line, "573452 0 3182069 1")
        self.assertEqual(last_line, "195199 0 8009377 1")

    def test_covid_round1(self):
        qrels_path = search.get_qrels_file('covid-round1')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 8691)
        self.assertEqual(first_line, "1 0.5  010vptx3 2")
        self.assertEqual(mid_line, "15 0.5  01rdlf8l 0")
        self.assertEqual(last_line, "30 0.5  zn87f1lk 1")

    def test_covid_round2(self):
        qrels_path = search.get_qrels_file('covid-round2')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 12037)
        self.assertEqual(first_line, "1 1.5  08efpohc 0")
        self.assertEqual(mid_line, "16 2  uj0i2anr 0")
        self.assertEqual(last_line, "35 2  zzmfhr2s 0")

    def test_covid_round3(self):
        qrels_path = search.get_qrels_file('covid-round3')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 12713)
        self.assertEqual(first_line, "1 2.5  0194oljo 1")
        self.assertEqual(mid_line, "19 2.5  s0o0egw8 2")
        self.assertEqual(last_line, "40 3  zsx7wfyj 1")

    def test_covid_round4(self):
        qrels_path = search.get_qrels_file('covid-round4')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 13262)
        self.assertEqual(first_line, "1 4  00fmeepz 1")
        self.assertEqual(mid_line, "27 4  hmh4s3w4 0")
        self.assertEqual(last_line, "45 4  zzrsk1ls 2")

    def test_covid_round5(self):
        qrels_path = search.get_qrels_file('covid-round5')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 23151)
        self.assertEqual(first_line, "1 4.5  005b2j4b 2")
        self.assertEqual(mid_line, "36 4.5  ylgmn69k 0")
        self.assertEqual(last_line, "50 5  zz8wvos9 1")

    def test_covid_round3_cumulative(self):
        qrels_path = search.get_qrels_file('covid-round3-cumulative')
        lines = read_file_lines(qrels_path)
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
        lines = read_file_lines(qrels_path)
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
        lines = read_file_lines(qrels_path)
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
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 8508)
        self.assertEqual(first_line, "321 0 00f57310e5c8ec7833d6756ba637332e 16")
        self.assertEqual(mid_line, "809 0 921073ca-c0a3-11e1-9ce8-ff26651238d0 0")
        self.assertEqual(last_line, "825 0 f66b624ba8689d704872fa776fb52860 0")

    def test_trec2019_bl(self):
        qrels_path = search.get_qrels_file('trec2019-bl')
        lines = read_file_lines(qrels_path)
        length = len(lines)
        first_line = lines[0].rstrip()
        mid_line = lines[length // 2].rstrip()
        last_line = lines[-1].rstrip()
        self.assertEqual(length, 15655)
        self.assertEqual(first_line, "826 0 0154349511cd8c49ab862d6cb0d8f6a8 2")
        self.assertEqual(mid_line, "853 0 2444d88d62539b0b88dc919909cb9701 2")
        self.assertEqual(last_line, "885 0 fde80cb0-b4f0-11e2-bbf2-a6f9e9d79e19 0")

    def tearDown(self):
        if os.path.exists('temp_dir'):
            shutil.rmtree('temp_dir')
            os.environ['PYSERINI_CACHE'] = ''


if __name__ == '__main__':
    unittest.main()
