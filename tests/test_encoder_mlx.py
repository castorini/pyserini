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
import tarfile
import unittest
from random import randint
from urllib.request import urlretrieve

from pyserini.encode import MlxTctColBertDocumentEncoder


class TestEncode(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.docids = []
        cls.texts = []
        cls.test_file = 'tests/resources/simple_cacm_corpus.json'

        with open(cls.test_file) as f:
            for line in f:
                line = json.loads(line)
                cls.docids.append(line['id'])
                cls.texts.append(line['contents'])
        
        # LuceneImpactSearcher requires a pre-built index to be initialized
        r = randint(0, 10000000)
        cls.collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene9-index.cacm.tar.gz'
        cls.tarball_name = f'lucene-index.cacm-{r}.tar.gz'
        cls.index_dir = f'index-{r}/'

        urlretrieve(cls.collection_url, cls.tarball_name)

        tarball = tarfile.open(cls.tarball_name)
        tarball.extractall(cls.index_dir)
        tarball.close()

        
    @staticmethod
    def assertIsFile(path):
        if not pl.Path(path).resolve().is_file():
            raise AssertionError("File does not exist: %s" % str(path))

    def test_tct_colbert_encoder(self):
        encoder = MlxTctColBertDocumentEncoder(
            'castorini/tct_colbert-msmarco',
            )

        vectors = encoder.encode(self.texts[:3])
        
        self.assertAlmostEqual(vectors[0][0], -0.01649557, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.05648308, places=4)
        self.assertAlmostEqual(vectors[2][0], -0.10293338, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.05549275, places=4)
    
    def test_tct_colbert_v2_encoder_cmd(self):
        index_dir = 'temp_index'
        cmd = f'python -m pyserini.encode \
                  input   --corpus {self.test_file} \
                          --fields text \
                  output  --embeddings {index_dir} \
                  encoder --encoder castorini/tct_colbert-v2-hnp-msmarco \
                          --encoder-class mlx_tct_colbert \
                          --use-mlx \
                          --fields text \
                          --batch 1 '
        status = os.system(cmd)
        self.assertEqual(status, 0)

        embedding_json_fn = os.path.join(index_dir, 'embeddings.jsonl')
        self.assertIsFile(embedding_json_fn)

        with open(embedding_json_fn) as f:
            embeddings = [json.loads(line) for line in f]

        self.assertListEqual([entry["id"] for entry in embeddings], self.docids)
        self.assertListEqual(
            [entry["contents"] for entry in embeddings], 
            [entry.strip() for entry in self.texts],
        )
 
        self.assertAlmostEqual(embeddings[0]['vector'][0], 0.12679848074913025, places=4)
        self.assertAlmostEqual(embeddings[0]['vector'][-1], -0.0037349488120526075, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][0], 0.03678430616855621, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][-1], 0.13209162652492523, places=4)

        shutil.rmtree(index_dir)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.tarball_name)
        shutil.rmtree(cls.index_dir)


if __name__ == '__main__':
    unittest.main()
