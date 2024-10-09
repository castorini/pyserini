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
import shutil
import tarfile
import unittest
from random import randint
from urllib.request import urlretrieve

from pyserini.encode import UniCoilDocumentEncoder
from pyserini.search.lucene import LuceneImpactSearcher


class TestEncodeUniCoil(unittest.TestCase):
    def test_unicoil_encoder(self):
        texts = []
        with open('tests/resources/simple_cacm_corpus.json') as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = UniCoilDocumentEncoder('castorini/unicoil-msmarco-passage', device='cpu')
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0]['generation'], 2.2441017627716064, places=4)
        self.assertAlmostEqual(vectors[0]['normal'], 2.4618067741394043, places=4)
        self.assertAlmostEqual(vectors[2]['rounding'], 3.9474332332611084, places=4)
        self.assertAlmostEqual(vectors[2]['commercial'], 3.288801670074463, places=4)

    def test_onnx_encode_unicoil(self):
        # LuceneImpactSearcher requires a pre-built index to be initialized
        r = randint(0, 10000000)
        collection_url = 'https://github.com/castorini/anserini-data/raw/master/CACM/lucene9-index.cacm.tar.gz'
        tarball_name = f'lucene-index.cacm-{r}.tar.gz'
        index_dir = f'index-{r}/'

        urlretrieve(collection_url, tarball_name)

        tarball = tarfile.open(tarball_name)
        tarball.extractall(index_dir)
        tarball.close()

        searcher1 = LuceneImpactSearcher(f'{index_dir}lucene9-index.cacm',
                                         'SpladePlusPlusEnsembleDistil',
                                         encoder_type='onnx')

        results = searcher1.encode("here is a test")
        self.assertEqual(results.get("here"), 156)
        self.assertEqual(results.get("a"), 31)
        self.assertEqual(results.get("test"), 149)

        searcher1.close()
        del searcher1

        searcher2 = LuceneImpactSearcher(f'{index_dir}lucene9-index.cacm',
                                         'naver/splade-cocondenser-ensembledistil')

        results = searcher2.encode("here is a test")
        self.assertEqual(results.get("here"), 156)
        self.assertEqual(results.get("a"), 31)
        self.assertEqual(results.get("test"), 149)

        searcher2.close()
        del searcher2

        os.remove(tarball_name)
        shutil.rmtree(index_dir)


if __name__ == '__main__':
    unittest.main()
