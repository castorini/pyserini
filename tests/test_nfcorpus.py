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

import json
import os
import pathlib as pl
import shutil
import subprocess
import tarfile
import unittest

import faiss

from pyserini.encode import JsonlCollectionIterator, TctColBertDocumentEncoder, DprDocumentEncoder, \
    UniCoilDocumentEncoder
from pyserini.search.lucene._impact_searcher import LuceneImpactSearcher
from random import randint
from urllib.request import urlretrieve


class TestNFCorpus(unittest.TestCase):
    def setUp(self):
        self.queries = 'tests/resources/nfcorpus-queries.tsv'

        r = randint(0, 10000000)
        self.dense_index_url = 'https://www.dropbox.com/scl/fi/b2rx4e9rr4rxyvw6xneul/faiss.nfcorpus.contriever-msmacro.tar.gz?rlkey=33uakcl2y6cy7akj98y6yyupg&dl=1'
        self.tarball_name = f'faiss.nfcorpus.contriever-msmacro-{r}.tar.gz'
        self.index_dir = f'index-{r}/'

        _, _ = urlretrieve(self.dense_index_url, self.tarball_name)

        tarball = tarfile.open(self.tarball_name)
        tarball.extractall(self.index_dir)
        tarball.close()

    def test_tct_colbert_v2_encoder_cmd(self):
        print(self.index_dir)

        cmd = f'python -m pyserini.search.faiss \
                  --encoder-class contriever --encoder facebook/contriever-msmarco \
                  --index {self.index_dir}/faiss.nfcorpus.contriever-msmacro \
                  --topics {self.queries} \
                  --output tmp.txt \
                  --batch 32 --threads 4 \
                  --hits 10'

        status = os.system(cmd)
        results = subprocess.check_output(
            f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 collections/nfcorpus/qrels/test.qrels tmp.txt', shell=True)
        results = results.decode('utf-8').split('\n')
        print(results)
        print('###' + results[-2])
        ndcg_line = results[-2]
        ndcg_score = float(ndcg_line.split('\t')[-1])
        print(ndcg_score)
        self.assertAlmostEqual(ndcg_score, 0.0056, places=5)
