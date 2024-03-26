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
from typing import List, Dict

from pyserini.search.faiss import FaissSearcher, ClipQueryEncoder
import pathlib as pl



class TestMultimodalSearch(unittest.TestCase):
    tarball_name = None
    collection_url = None
    searcher = None
    searcher_index_dir = None

    @classmethod
    def setUpClass(cls):
        cls.text_file = 'tests/resources/sample_collection_jsonl/documents.jsonl'
        cls.image_file = 'tests/resources/sample_collection_jsonl_image/images.small.jsonl'

        pretrained_model_name = 'openai/clip-vit-base-patch32'
        dim = 512
        cls.emb_dir = 'temp_embeddings'
        pl.Path(cls.emb_dir).mkdir(exist_ok=True)
        cls.index_dir = 'temp_indexes'
        pl.Path(cls.index_dir).mkdir(exist_ok=True)
        cmd1 = f'python -m pyserini.encode \
                  input   --corpus {cls.text_file} \
                          --fields text \
                  output  --embeddings {cls.emb_dir}/texts --to-faiss \
                  encoder --encoder {pretrained_model_name} \
                          --fields text \
                          --batch 1 \
                          --max-length 77 \
                          --l2-norm --dimension {dim}\
                          --device cpu'
        status = os.system(cmd1)
        cmd2 = f'python -m pyserini.encode \
                  input   --corpus {cls.image_file} \
                          --fields path \
                  output  --embeddings {cls.emb_dir}/images --to-faiss \
                  encoder --encoder {pretrained_model_name} \
                          --fields path \
                          --batch 1 \
                          --multimodal --l2-norm --dimension {dim} \
                          --device cpu'
        status = os.system(cmd2)
        cmd3 = f'python -m pyserini.index.faiss --input {cls.emb_dir}/texts --output {cls.index_dir}/texts --dim {dim}'
        status = os.system(cmd3)
        cmd4 = f'python -m pyserini.index.faiss --input {cls.emb_dir}/images --output {cls.index_dir}/images --dim {dim}'
        status = os.system(cmd4)

        cls.text_encoder = ClipQueryEncoder(pretrained_model_name, l2_norm=True, prefix='A picture of', multimodal=False, device='cpu')
        cls.image_encoder = ClipQueryEncoder(pretrained_model_name, l2_norm=True, prefix=None, multimodal=True, device='cpu')
        
    def test_text2image_search(self):
        searcher = FaissSearcher(f'{self.index_dir}/images', self.text_encoder)
        hits = searcher.search('information retrieval')
        self.assertTrue(isinstance(hits, List))
        self.assertEqual(hits[0].docid, '01c79307-76fb-3b82-a96f-8ba1c1b6fa09')
        self.assertAlmostEqual(hits[0].score, 0.20057034, places=5)
    
    def test_image2text_search(self):
        searcher = FaissSearcher(f'{self.index_dir}/texts', self.image_encoder)
        hits = searcher.search('tests/resources/sample_collection_jsonl_image/images.small/00a3019b-c47c-3a97-8132-81896ab92dfc.webp')
        self.assertTrue(isinstance(hits, List))
        self.assertEqual(hits[0].docid, 'doc1')
        self.assertAlmostEqual(hits[0].score, 0.2340512, places=5)
    
    def test_text2text_search(self):
        searcher = FaissSearcher(f'{self.index_dir}/texts', self.text_encoder)
        hits = searcher.search('information retrieval')
        self.assertTrue(isinstance(hits, List))
        self.assertEqual(hits[0].docid, 'doc3')
        self.assertAlmostEqual(hits[0].score, 0.8558732, places=5)
    
    def test_image2image_search(self):
        searcher = FaissSearcher(f'{self.index_dir}/images', self.image_encoder)
        hits = searcher.search('tests/resources/sample_collection_jsonl_image/images.small/00a3019b-c47c-3a97-8132-81896ab92dfc.webp')
        self.assertTrue(isinstance(hits, List))
        self.assertEqual(hits[0].docid, '00a3019b-c47c-3a97-8132-81896ab92dfc')
        self.assertAlmostEqual(hits[0].score, 0.9999999, places=5)
    
    def test_imageurl2text_search(self):
        searcher = FaissSearcher(f'{self.index_dir}/texts', self.image_encoder)
        hits = searcher.search('https://raw.githubusercontent.com/castorini/pyserini/master/docs/pyserini-logo.png')
        self.assertTrue(isinstance(hits, List))
        self.assertEqual(hits[0].docid, 'doc3')
        self.assertAlmostEqual(hits[0].score, 0.20829172, places=5)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.emb_dir)
        shutil.rmtree(cls.index_dir)


if __name__ == '__main__':
    unittest.main()
