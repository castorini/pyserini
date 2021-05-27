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


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        curdir = os.getcwd()
        if curdir.endswith('dense'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'
        self.temp_folders = []

    def test_create_index(self):
        index_dir = f'{self.pyserini_root}/temp_index'
        self.temp_folders.append(index_dir)
        cmd1 = f"python -m pyserini.dindex --corpus {self.pyserini_root}/integrations/resources/sample_collection_dense \
                          --encoder facebook/dpr-ctx_encoder-multiset-base \
                          --index {index_dir} \
                          --batch 64 \
                          --device cpu \
                          --title-delimiter '\n'"
        status = os.system(cmd1)
        self.assertEqual(status, 0)
        searcher = SimpleDenseSearcher(
            index_dir,
            'facebook/dpr-question_encoder-multiset-base'
        )
        self.assertEqual(searcher.num_docs, 18)

    def test_create_index_shard(self):
        index_dir = f'{self.pyserini_root}/temp_index-0'
        self.temp_folders.append(index_dir)
        cmd1 = f"python -m pyserini.dindex --corpus {self.pyserini_root}/integrations/resources/sample_collection_dense \
                          --encoder facebook/dpr-ctx_encoder-multiset-base \
                          --index {index_dir} \
                          --batch 64 \
                          --device cpu \
                          --title-delimiter '\n' \
                          --shard-id 0 \
                          --shard-num 2 "

        index_dir = f'{self.pyserini_root}/temp_index-1'
        self.temp_folders.append(index_dir)
        cmd2 = f"python -m pyserini.dindex --corpus {self.pyserini_root}/integrations/resources/sample_collection_dense \
                                  --encoder facebook/dpr-ctx_encoder-multiset-base \
                                  --index {index_dir} \
                                  --batch 64 \
                                  --device cpu \
                                  --title-delimiter '\n' \
                                  --shard-id 1 \
                                  --shard-num 2 "
        status = os.system(cmd1)
        self.assertEqual(status, 0)
        status = os.system(cmd2)
        self.assertEqual(status, 0)
        cmd3 = f"python -m pyserini.dindex.merge_indexes --prefix {self.pyserini_root}/temp_index- --shard-num 2"
        status = os.system(cmd3)
        self.assertEqual(status, 0)
        index_dir = f'{self.pyserini_root}/temp_index-full'
        self.temp_folders.append(index_dir)
        searcher = SimpleDenseSearcher(
            index_dir,
            'facebook/dpr-question_encoder-multiset-base'
        )
        self.assertEqual(searcher.num_docs, 18)

    def tearDown(self):
        for f in self.temp_folders:
            shutil.rmtree(f)
