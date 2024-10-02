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
import random

import faiss
import shutil
import unittest
import pathlib as pl


class TestIndexFaiss(unittest.TestCase):
    @staticmethod
    def assertIsFile(path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    def setUp(self):
        self.docids = []
        self.texts = []
        self.test_file = 'tests/resources/simple_cacm_corpus.json'
        self.tmp_dir = f'tmp_{self.__class__.__name__}_{str(random.randint(0, 1000))}'

        with open(self.test_file) as f:
            for line in f:
                line = json.loads(line)
                self.docids.append(line['id'])
                self.texts.append(line['contents'])

    def prepare_encoded_collection(self):
        encoded_corpus_dir = f'{self.tmp_dir}/temp_index'
        cmd = f'python -m pyserini.encode \
                input   --corpus {self.test_file} \
                        --fields text \
                output  --embeddings {encoded_corpus_dir} \
                        --to-faiss \
                encoder --encoder castorini/tct_colbert-v2-hnp-msmarco \
                        --fields text \
                        --max-length 512 \
                        --batch 1 \
                        --device cpu'
        status = os.system(cmd)
        self.assertEqual(status, 0)
        self.assertIsFile(os.path.join(encoded_corpus_dir, 'docid'))
        self.assertIsFile(os.path.join(encoded_corpus_dir, 'index'))
        return encoded_corpus_dir

    def test_faiss_hnsw(self):
        index_dir = f'{self.tmp_dir}/temp_hnsw'
        encoded_corpus_dir = self.prepare_encoded_collection()
        cmd = f'python -m pyserini.index.faiss \
            --input {encoded_corpus_dir} \
            --output {index_dir} \
            --M 3 \
            --hnsw'

        status = os.system(cmd)
        self.assertEqual(status, 0) 

        docid_fn = os.path.join(index_dir, 'docid')
        index_fn = os.path.join(index_dir, 'index')
        self.assertIsFile(docid_fn)
        self.assertIsFile(index_fn)

        index = faiss.read_index(index_fn)
        vectors = index.reconstruct_n(0, index.ntotal)

        with open(docid_fn) as f:
            self.assertListEqual([docid.strip() for docid in f], self.docids)

        self.assertAlmostEqual(vectors[0][0], 0.12679848074913025, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.0037349488120526075, places=4)
        self.assertAlmostEqual(vectors[2][0], 0.03678430616855621, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.13209162652492523, places=4)

    def test_faiss_pq(self):
        index_dir = f'{self.tmp_dir}/temp_pq'
        encoded_corpus_dir = self.prepare_encoded_collection()
        cmd = f'python -m pyserini.index.faiss \
            --input {encoded_corpus_dir} \
            --output {index_dir} \
            --pq-m 3 \
            --efC 1 \
            --pq-nbits 128 \
            --pq'

        status = os.system(cmd)
        self.assertEqual(status, 0) 

        docid_fn = os.path.join(index_dir, 'docid')
        index_fn = os.path.join(index_dir, 'index')
        self.assertIsFile(docid_fn)
        self.assertIsFile(index_fn)

        index = faiss.read_index(index_fn)
        vectors = index.reconstruct_n(0, index.ntotal)
    
        with open(docid_fn) as f:
            self.assertListEqual([docid.strip() for docid in f], self.docids)

        self.assertAlmostEqual(vectors[0][0], 0.04343192, places=4)
        self.assertAlmostEqual(vectors[0][-1], 0.075478144, places=4)
        self.assertAlmostEqual(vectors[2][0], 0.04343192, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.075478144, places=4)

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)
