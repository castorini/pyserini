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

from pyserini.encode import TctColBertDocumentEncoder, DprDocumentEncoder, UniCoilDocumentEncoder #, ClipDocumentEncoder
from pyserini.search.lucene import LuceneImpactSearcher


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

    def test_dpr_encoder(self):
        encoder = DprDocumentEncoder('facebook/dpr-ctx_encoder-multiset-base', device='cpu')
        vectors = encoder.encode(self.texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.59793323, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.13036962, places=4)
        self.assertAlmostEqual(vectors[2][0], -0.3044764, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.1516793, places=4)

    def test_tct_colbert_encoder(self):
        encoder = TctColBertDocumentEncoder('castorini/tct_colbert-msmarco', device='cpu')
        vectors = encoder.encode(self.texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.01649557, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.05648308, places=4)
        self.assertAlmostEqual(vectors[2][0], -0.10293338, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.05549275, places=4)

    def test_unicoil_encoder(self):
        encoder = UniCoilDocumentEncoder('castorini/unicoil-msmarco-passage', device='cpu')
        vectors = encoder.encode(self.texts[:3])
        self.assertAlmostEqual(vectors[0]['generation'], 2.2441017627716064, places=4)
        self.assertAlmostEqual(vectors[0]['normal'], 2.4618067741394043, places=4)
        self.assertAlmostEqual(vectors[2]['rounding'], 3.9474332332611084, places=4)
        self.assertAlmostEqual(vectors[2]['commercial'], 3.288801670074463, places=4)

    def test_onnx_encode_unicoil(self):
        temp_object = LuceneImpactSearcher(f'{self.index_dir}lucene9-index.cacm', 'SpladePlusPlusEnsembleDistil', encoder_type='onnx')

        # this function will never be called in _impact_searcher, here to check quantization correctness
        results = temp_object.encode("here is a test")
        self.assertEqual(results.get("here"), 156)
        self.assertEqual(results.get("a"), 31)
        self.assertEqual(results.get("test"), 149)

        temp_object.close()
        del temp_object

        temp_object1 = LuceneImpactSearcher(f'{self.index_dir}lucene9-index.cacm', 'naver/splade-cocondenser-ensembledistil')

        # this function will never be called in _impact_searcher, here to check quantization correctness
        results = temp_object1.encode("here is a test")
        self.assertEqual(results.get("here"), 156)
        self.assertEqual(results.get("a"), 31)
        self.assertEqual(results.get("test"), 149)

        temp_object1.close()
        del temp_object1
    
    @classmethod
    def tearDownClass(cls):
        os.remove(cls.tarball_name)
        shutil.rmtree(cls.index_dir)


if __name__ == '__main__':
    unittest.main()
