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
#

import os
import filecmp
import unittest
from tqdm import tqdm
from pyserini.fusion import FusionMethod
from pyserini.trectools import TrecRun
from pyserini.search import get_topics, SimpleFusionSearcher, SimpleSearcher


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        if not os.path.exists('indexes/lucene-index-cord19-abstract-2020-05-01/'):
            os.system('wget -nc https://www.dropbox.com/s/wxjoe4g71zt5za2/lucene-index-cord19-abstract-2020-05-01.tar.gz')
            os.system('tar -xvzf lucene-index-cord19-abstract-2020-05-01.tar.gz -C indexes')
            os.system('rm lucene-index-cord19-abstract-2020-05-01.tar.gz')

        if not os.path.exists('indexes/lucene-index-cord19-full-text-2020-05-01/'):
            os.system('wget -nc https://www.dropbox.com/s/di27r5o2g5kat5k/lucene-index-cord19-full-text-2020-05-01.tar.gz')
            os.system('tar -xvzf lucene-index-cord19-full-text-2020-05-01.tar.gz -C indexes')
            os.system('rm lucene-index-cord19-full-text-2020-05-01.tar.gz')

        if not os.path.exists('indexes/lucene-index-cord19-paragraph-2020-05-01/'):
            os.system('wget -nc https://www.dropbox.com/s/6ib71scm925mclk/lucene-index-cord19-paragraph-2020-05-01.tar.gz')
            os.system('tar -xvzf lucene-index-cord19-paragraph-2020-05-01.tar.gz -C indexes')
            os.system('rm lucene-index-cord19-paragraph-2020-05-01.tar.gz')

        if not os.path.exists('anserini.covid-r2.fusion1.txt'):
            os.system('wget -q -nc https://www.dropbox.com/s/wqb0vhxp98g7dxh/anserini.covid-r2.fusion1.txt.gz')
            os.system('gunzip -f anserini.covid-r2.fusion1.txt.gz')

    def test_simple_fusion_searcher(self):
        index_dirs = ['indexes/lucene-index-cord19-abstract-2020-05-01/',
                      'indexes/lucene-index-cord19-full-text-2020-05-01/',
                      'indexes/lucene-index-cord19-paragraph-2020-05-01/']

        searcher = SimpleFusionSearcher(index_dirs, method=FusionMethod.RRF)

        runs, topics = [], get_topics('covid_round2')
        for topic in tqdm(sorted(topics.keys())):
            query = topics[topic]['question'] + ' ' + topics[topic]['query']
            hits = searcher.search(query, k=10000, query_generator=None, strip_segment_id=True, remove_dups=True)
            docid_score_pair = [(hit.docid, hit.score) for hit in hits]
            run = TrecRun.from_search_results(docid_score_pair, topic=topic)
            runs.append(run)

        all_topics_run = TrecRun.concat(runs)
        all_topics_run.save_to_txt(output_path='fused.txt', tag='reciprocal_rank_fusion_k=60')

        # Only keep topic, docid and rank. Scores have different floating point precisions.
        os.system("""awk '{print $1" "$3" "$4}' fused.txt > this.txt""")
        os.system("""awk '{print $1" "$3" "$4}' anserini.covid-r2.fusion1.txt > that.txt""")

        self.assertTrue(filecmp.cmp('this.txt', 'that.txt'))

    def tearDown(self):
        os.system('rm anserini.covid-r2.fusion1.txt fused.txt this.txt that.txt')


if __name__ == '__main__':
    unittest.main()
