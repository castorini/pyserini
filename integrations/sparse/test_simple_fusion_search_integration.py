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

import gzip
import os
import filecmp
import shutil
import unittest
from tqdm import tqdm
from pyserini.fusion import FusionMethod
from pyserini.trectools import TrecRun
from pyserini.search import get_topics, SimpleFusionSearcher
from pyserini.util import download_url, download_and_unpack_index


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        download_and_unpack_index('https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-01/lucene-index-cord19-abstract-2020-05-01.tar.gz')
        download_and_unpack_index('https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-01/lucene-index-cord19-full-text-2020-05-01.tar.gz')
        download_and_unpack_index('https://git.uwaterloo.ca/jimmylin/cord19-indexes/raw/master/2020-05-01/lucene-index-cord19-paragraph-2020-05-01.tar.gz')

        download_url('https://git.uwaterloo.ca/jimmylin/covidex-trec-covid-runs/raw/master/round2/anserini.covid-r2.fusion1.txt.gz', 'runs')
        # from https://stackoverflow.com/questions/31028815/how-to-unzip-gz-file-using-python
        with gzip.open('runs/anserini.covid-r2.fusion1.txt.gz', 'rb') as f_in:
            with open('runs/anserini.covid-r2.fusion1.txt', 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

    def test_simple_fusion_searcher(self):
        index_dirs = ['indexes/lucene-index-cord19-abstract-2020-05-01/',
                      'indexes/lucene-index-cord19-full-text-2020-05-01/',
                      'indexes/lucene-index-cord19-paragraph-2020-05-01/']

        searcher = SimpleFusionSearcher(index_dirs, method=FusionMethod.RRF)

        runs, topics = [], get_topics('covid-round2')
        for topic in tqdm(sorted(topics.keys())):
            query = topics[topic]['question'] + ' ' + topics[topic]['query']
            hits = searcher.search(query, k=10000, query_generator=None, strip_segment_id=True, remove_dups=True)
            docid_score_pair = [(hit.docid, hit.score) for hit in hits]
            run = TrecRun.from_search_results(docid_score_pair, topic=topic)
            runs.append(run)

        all_topics_run = TrecRun.concat(runs)
        all_topics_run.save_to_txt(output_path='runs/fused.txt', tag='reciprocal_rank_fusion_k=60')

        # Only keep topic, docid and rank. Scores have different floating point precisions.
        # TODO: We should probably do this in Python as opposed to calling out to shell for better portability.
        os.system("""awk '{print $1" "$3" "$4}' runs/fused.txt > runs/this.txt""")
        os.system("""awk '{print $1" "$3" "$4}' runs/anserini.covid-r2.fusion1.txt > runs/that.txt""")

        self.assertTrue(filecmp.cmp('runs/this.txt', 'runs/that.txt'))

    def tearDown(self):
        os.remove('runs/anserini.covid-r2.fusion1.txt.gz')
        os.remove('runs/anserini.covid-r2.fusion1.txt')
        os.remove('runs/fused.txt')
        os.remove('runs/this.txt')
        os.remove('runs/that.txt')


if __name__ == '__main__':
    unittest.main()
