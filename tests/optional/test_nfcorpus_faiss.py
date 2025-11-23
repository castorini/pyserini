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
import subprocess
import tarfile
import unittest

import numpy as np
from random import randint
from urllib.request import urlretrieve


class TestNFCorpus(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        curdir = os.getcwd()
        if curdir.endswith('optional'):
            cls.queries = '../resources/nfcorpus-queries.tsv'
            cls.qrels = '../resources/nfcorpus-qrels.tsv'
        else:
            cls.queries = 'tests/resources/nfcorpus-queries.tsv'
            cls.qrels = 'tests/resources/nfcorpus-qrels.tsv'

        # TODO: Remove the Lucene part, just keep the Faiss part
        r = randint(0, 10000000)
        cls.dense_index_url = 'https://github.com/castorini/anserini-data/raw/master/NFCorpus/faiss.nfcorpus.contriever-msmacro.tar.gz'
        cls.dense_tarball_name = f'faiss.nfcorpus.contriever-msmacro-{r}.tar.gz'
        cls.dense_index_dir = f'faiss.nfcorpus.contriever-msmacro-{r}/'

        urlretrieve(cls.dense_index_url, cls.dense_tarball_name)

        tarball = tarfile.open(cls.dense_tarball_name)
        tarball.extractall(cls.dense_index_dir)
        tarball.close()

        cls.sparse_index_url = 'https://github.com/castorini/anserini-data/raw/master/NFCorpus/lucene.nfcorpus.tar.gz'
        cls.sparse_tarball_name = f'lucene.nfcorpus-{r}.tar.gz'
        cls.sparse_index_dir = f'lucene.nfcorpus-{r}/'

        urlretrieve(cls.sparse_index_url, cls.sparse_tarball_name)

        tarball = tarfile.open(cls.sparse_tarball_name)
        tarball.extractall(cls.sparse_index_dir)
        tarball.close()

    def test_dense_retrieval(self):
        r = randint(0, 10000000)
        run_file = f'run.{r}.txt'
        cmd = f'python -m pyserini.search.faiss \
                  --encoder-class contriever --encoder facebook/contriever-msmarco \
                  --index {self.dense_index_dir}/faiss.nfcorpus.contriever-msmacro \
                  --topics {self.queries} \
                  --output {run_file} \
                  --batch 32 --threads 4 \
                  --hits 10'

        os.system(cmd)
        results = subprocess.check_output(
            f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 {self.qrels} {run_file}', shell=True)
        results = results.decode('utf-8').split('\n')
        ndcg_line = results[-2]
        ndcg_score = float(ndcg_line.split('\t')[-1])
        self.assertAlmostEqual(ndcg_score, 0.3622, places=5)

        os.remove(run_file)

    def test_sparse_retrieval(self):
        r = randint(0, 10000000)
        run_file = f'run.{r}.txt'
        cmd = f'python -m pyserini.search.lucene \
                  --index {self.sparse_index_dir}/lucene.nfcorpus \
                  --topics {self.queries} \
                  --output {run_file} \
                  --batch 32 --threads 4 \
                  --hits 10 --bm25'

        os.system(cmd)
        results = subprocess.check_output(
            f'python -m pyserini.eval.trec_eval -c -m ndcg_cut.10 {self.qrels} {run_file}', shell=True)
        results = results.decode('utf-8').split('\n')
        ndcg_line = results[-2]
        ndcg_score = float(ndcg_line.split('\t')[-1])
        self.assertAlmostEqual(ndcg_score, 0.3405, places=5)

        os.remove(run_file)

    def test_faiss_flat_dense_with_normalized_distances(self):
        expected_top10 = [
            "PLAIN-1008 Q0 MED-2036 1 0.776563 Faiss",
            "PLAIN-1008 Q0 MED-5135 2 0.775253 Faiss",
            "PLAIN-1008 Q0 MED-4694 3 0.774549 Faiss",
            "PLAIN-1008 Q0 MED-3865 4 0.773869 Faiss",
            "PLAIN-1008 Q0 MED-3316 5 0.771661 Faiss",
            "PLAIN-1008 Q0 MED-901 6 0.766057 Faiss",
            "PLAIN-1008 Q0 MED-4668 7 0.765507 Faiss",
            "PLAIN-1008 Q0 MED-3317 8 0.764854 Faiss",
            "PLAIN-1008 Q0 MED-5211 9 0.764642 Faiss",
            "PLAIN-1008 Q0 MED-2476 10 0.763486 Faiss",
        ]
        r = randint(0, 10000000)
        faiss_run_file = f'run.faiss.beir-v1.0.0-nfcorpus.bge-base-en-v1.5.test.{r}.txt'
        self.__class__.faiss_run_file = faiss_run_file
        
        # Run Faiss search
        faiss_cmd = f'python -m pyserini.search.faiss \
            --encoder-class auto \
            --encoder BAAI/bge-base-en-v1.5 \
            --l2-norm \
            --pooling cls \
            --index beir-v1.0.0-nfcorpus.bge-base-en-v1.5 \
            --topics beir-v1.0.0-nfcorpus-test \
            --output {faiss_run_file} \
            --batch 128 \
            --threads 16 \
            --query-prefix "Represent this sentence for searching relevant passages: " \
            --hits 10 \
            --remove-query \
            --normalize-distances'
        
        faiss_result = os.system(faiss_cmd)
        self.assertEqual(faiss_result, 0, "Faiss search failed")
        self.assertTrue(os.path.exists(faiss_run_file), "Faiss run file was not created")
        
        # Compare top-10 results for PLAIN-1008
        with open(faiss_run_file, 'r') as f:
            faiss_results = [line.strip() for line in f if line.startswith('PLAIN-1008')][:10]
        
        self.assertEqual(len(faiss_results), 10, "Faiss results should have 10 lines for PLAIN-1008")
        for i, line in enumerate(faiss_results):
            self.assertEqual(line, expected_top10[i], f"Faiss result {i+1} should match expected")

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.dense_index_dir)
        os.remove(cls.dense_tarball_name)

        shutil.rmtree(cls.sparse_index_dir)
        os.remove(cls.sparse_tarball_name)
        
        if hasattr(cls, 'faiss_run_file') and os.path.exists(cls.faiss_run_file):
            os.remove(cls.faiss_run_file)


if __name__ == '__main__':
    unittest.main()
