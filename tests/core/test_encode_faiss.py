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
import unittest

import faiss


class TestEncodeFaiss(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docids = []
        cls.texts = []
        curdir = os.getcwd()
        if curdir.endswith('core'):
            cls.test_file = '../resources/simple_cacm_corpus.json'
        else:
            cls.test_file = 'tests/resources/simple_cacm_corpus.json'

        with open(cls.test_file) as f:
            for line in f:
                line = json.loads(line)
                cls.docids.append(line['id'])
                cls.texts.append(line['contents'])

    @staticmethod
    def assertIsFile(path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    def test_tct_colbert_v2_encode_cmd_shard(self):
        cleanup_list = []
        for shard_i in range(2):
            index_dir = f'temp_index-{shard_i}'
            cleanup_list.append(index_dir)
            cmd = f'python -m pyserini.encode \
                    input   --corpus {self.test_file} \
                            --fields text \
                            --shard-id {shard_i} \
                            --shard-num 2 \
                    output  --embeddings {index_dir} \
                            --to-faiss \
                    encoder --encoder castorini/tct_colbert-v2-hnp-msmarco \
                            --fields text \
                            --batch 1 \
                            --device cpu'
            status = os.system(cmd)
            self.assertEqual(status, 0)
            self.assertIsFile(os.path.join(index_dir, 'docid'))
            self.assertIsFile(os.path.join(index_dir, 'index'))

        cmd = f'python -m pyserini.index.merge_faiss_indexes --prefix temp_index- --shard-num 2'
        index_dir = 'temp_index-full'
        cleanup_list.append(index_dir)
        docid_fn = os.path.join(index_dir, 'docid')
        index_fn = os.path.join(index_dir, 'index')

        status = os.system(cmd)
        self.assertEqual(status, 0)
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

        for index_dir in cleanup_list:
            shutil.rmtree(index_dir)


if __name__ == '__main__':
    unittest.main()
