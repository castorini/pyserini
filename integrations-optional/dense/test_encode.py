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
from urllib.request import urlretrieve

import faiss

from pyserini.search.faiss import FaissSearcher
from pyserini.search.lucene import LuceneImpactSearcher


class TestEncode(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('dense'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'
        self.temp_folders = []
        self.corpus_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/corpus/jsonl/cacm.json'
        self.corpus_path = f'{self.pyserini_root}/integrations/dense/temp_cacm/'
        os.makedirs(self.corpus_path, exist_ok=True)
        self.temp_folders.append(self.corpus_path)
        urlretrieve(self.corpus_url, os.path.join(self.corpus_path, 'cacm.json'))

    def test_dpr_encode_as_faiss(self):
        index_dir = f'{self.pyserini_root}/temp_index'
        self.temp_folders.append(index_dir)
        cmd1 = f'python -m pyserini.encode input   --corpus {self.corpus_path} \
                                  --fields text \
                          output  --embeddings {index_dir} --to-faiss \
                          encoder --encoder facebook/dpr-ctx_encoder-multiset-base \
                                  --fields text \
                                  --batch 4 \
                                  --device cpu'
        _ = os.system(cmd1)
        searcher = FaissSearcher(
            index_dir,
            'facebook/dpr-question_encoder-multiset-base'
        )
        q_emb, hit = searcher.search('What is the solution of separable closed queueing networks?', k=1, return_vector=True)
        self.assertEqual(hit[0].docid, 'CACM-2445')
        self.assertAlmostEqual(hit[0].vectors[0], -6.88267112e-01, places=4)
        self.assertEqual(searcher.num_docs, 3204)

    def test_dpr_encode_as_faiss_search_with_partitions(self):
        # Create two partitions of the CACM index, search them individually, and merge results to compute top hit
        index_dir = f'{self.pyserini_root}/temp_index'
        os.makedirs(os.path.join(index_dir, 'partition1'), exist_ok=True)
        os.makedirs(os.path.join(index_dir, 'partition2'), exist_ok=True)
        self.temp_folders.append(index_dir)
        cmd1 = f'python -m pyserini.encode input   --corpus {self.corpus_path} \
                                  --fields text \
                          output  --embeddings {index_dir} --to-faiss \
                          encoder --encoder facebook/dpr-ctx_encoder-multiset-base \
                                  --fields text \
                                  --batch 4 \
                                  --device cpu'
        _ = os.system(cmd1)
        index = faiss.read_index(os.path.join(index_dir, 'index'))
        new_index_partition1 = faiss.IndexFlatIP(index.d) 
        new_index_partition2 = faiss.IndexFlatIP(index.d) 
        vectors_partition1 = index.reconstruct_n(0, index.ntotal // 2)
        vectors_partition2 = index.reconstruct_n(index.ntotal // 2, index.ntotal - index.ntotal // 2)
        new_index_partition1.add(vectors_partition1)
        new_index_partition2.add(vectors_partition2)
        
        faiss.write_index(new_index_partition1, os.path.join(index_dir, 'partition1/index'))
        faiss.write_index(new_index_partition2, os.path.join(index_dir, 'partition2/index'))
        
        with open(os.path.join(index_dir, 'partition1/docid'), 'w') as docid1, open(os.path.join(index_dir, 'partition2/docid'), 'w') as docid2:
            with open(os.path.join(index_dir, 'docid'), 'r') as file:
                for i in range(index.ntotal):
                    line = next(file)
                    if i < (index.ntotal // 2):
                        docid1.write(line)
                    else:
                        docid2.write(line)

        searcher_partition1 = FaissSearcher(index_dir + '/partition1','facebook/dpr-question_encoder-multiset-base')
        searcher_partition2 = FaissSearcher(index_dir + '/partition2','facebook/dpr-question_encoder-multiset-base')
        q_emb, hit1 = searcher_partition1.search('What is the solution of separable closed queueing networks?', k=2, return_vector=True)
        q_emb, hit2 = searcher_partition2.search('What is the solution of separable closed queueing networks?', k=2, return_vector=True)
        merged_hits = hit1 + hit2
        merged_hits.sort(key=lambda x: x.score, reverse=True)
        
        self.assertEqual(merged_hits[0].docid, 'CACM-2445')
        self.assertAlmostEqual(merged_hits[0].vectors[0], -6.88267112e-01, places=4)
        self.assertEqual(searcher_partition1.num_docs, 1602)
        self.assertEqual(searcher_partition2.num_docs, 1602)

    def test_unicoil_encode_as_jsonl(self):
        embedding_dir = f'{self.pyserini_root}/temp_embeddings'
        self.temp_folders.append(embedding_dir)
        cmd1 = f'python -m pyserini.encode input   --corpus {self.corpus_path} \
                                  --fields text \
                          output  --embeddings {embedding_dir} \
                          encoder --encoder castorini/unicoil-msmarco-passage \
                                  --fields text \
                                  --batch 4 \
                                  --device cpu'
        _ = os.system(cmd1)
        index_dir = f'{self.pyserini_root}/temp_lucene'
        self.temp_folders.append(index_dir)
        cmd2 = f'python -m pyserini.index -collection JsonVectorCollection \
                                          -input {embedding_dir} \
                                          -index {index_dir} \
                                          -generator DefaultLuceneDocumentGenerator \
                                          -impact -pretokenized -threads 12 -storeRaw'
        _ = os.system(cmd2)
        searcher = LuceneImpactSearcher(index_dir, query_encoder='castorini/unicoil-msmarco-passage')
        hits = searcher.search('What is the solution of separable closed queueing networks?', k=1)
        hit = hits[0]
        self.assertEqual(hit.docid, 'CACM-2712')
        self.assertAlmostEqual(hit.score, 940, places=3)

    def tearDown(self):
        for f in self.temp_folders:
            shutil.rmtree(f)
