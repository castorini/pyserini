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

"""Integration tests for create dense index """

import os
import shutil
import unittest
from pyserini.dsearch import SimpleDenseSearcher
from pyserini.search import ImpactSearcher
from urllib.request import urlretrieve


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('dense'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'
        self.temp_folders = []
        self.corpus_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/corpus/jsonl/cacm.json'
        self.corpus_path = f"{self.pyserini_root}/integrations/dense/temp_cacm/"
        os.makedirs(self.corpus_path, exist_ok=True)
        self.temp_folders.append(self.corpus_path)
        urlretrieve(self.corpus_url, os.path.join(self.corpus_path, 'cacm.json'))

    def test_dpr_encode_as_faiss(self):
        index_dir = f'{self.pyserini_root}/temp_index'
        self.temp_folders.append(index_dir)
        cmd1 = f"python -m pyserini.encode input   --corpus {self.corpus_path} \
                                  --fields text \
                          output  --embeddings {index_dir} --to-faiss \
                          encoder --encoder facebook/dpr-ctx_encoder-multiset-base \
                                  --fields text \
                                  --batch 4 \
                                  --device cpu"
        _ = os.system(cmd1)
        searcher = SimpleDenseSearcher(
            index_dir,
            'facebook/dpr-question_encoder-multiset-base'
        )
        q_emb, hit = searcher.search("What is the solution of separable closed queueing networks?", k=1, return_vector=True)
        self.assertEqual(hit[0].docid, 'CACM-2445')
        self.assertAlmostEqual(hit[0].vectors[0], -6.88267112e-01, places=4)
        self.assertEqual(searcher.num_docs, 3204)

    def test_unicoil_encode_as_jsonl(self):
        embedding_dir = f'{self.pyserini_root}/temp_embeddings'
        self.temp_folders.append(embedding_dir)
        cmd1 = f"python -m pyserini.encode input   --corpus {self.corpus_path} \
                                  --fields text \
                          output  --embeddings {embedding_dir} \
                          encoder --encoder castorini/unicoil-d2q-msmarco-passage \
                                  --fields text \
                                  --batch 4 \
                                  --device cpu"
        _ = os.system(cmd1)
        index_dir = f'{self.pyserini_root}/temp_lucene'
        self.temp_folders.append(index_dir)
        cmd2 = f'python -m pyserini.index -collection JsonVectorCollection \
                                          -input {embedding_dir} \
                                          -index {index_dir} \
                                          -generator DefaultLuceneDocumentGenerator \
                                          -impact -pretokenized -threads 12 -storeRaw'
        _ = os.system(cmd2)
        searcher = ImpactSearcher(index_dir, query_encoder='castorini/unicoil-d2q-msmarco-passage')
        hits = searcher.search("What is the solution of separable closed queueing networks?", k=1)
        hit = hits[0]
        self.assertEqual(hit.docid, 'CACM-2712')
        self.assertAlmostEqual(hit.score, 18.401899337768555, places=4)

    def tearDown(self):
        for f in self.temp_folders:
            shutil.rmtree(f)
