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

import faiss

from pyserini.encode import TctColBertDocumentEncoder, DprDocumentEncoder, UniCoilDocumentEncoder, ClipDocumentEncoder
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
    
    def test_clip_encoder(self):
        encoder = ClipDocumentEncoder('openai/clip-vit-base-patch32', device='cpu')
        vectors = encoder.encode(self.texts[:3])
        self.assertAlmostEqual(vectors[0][0], 0.1933609, places=4)
        self.assertAlmostEqual(vectors[0][-1], -0.21501173, places=4)
        self.assertAlmostEqual(vectors[2][0], 0.06461975, places=4)
        self.assertAlmostEqual(vectors[2][-1], 0.35396004, places=4)

    def test_tct_colbert_v2_encoder_cmd(self):
        index_dir = 'temp_index'
        cmd = f'python -m pyserini.encode \
                  input   --corpus {self.test_file} \
                          --fields text \
                  output  --embeddings {index_dir} \
                  encoder --encoder castorini/tct_colbert-v2-hnp-msmarco \
                          --fields text \
                          --batch 1 \
                          --device cpu'
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

    def test_tct_colbert_v2_encoder_cmd_shard(self):
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

    def test_aggretriever_distilbert_encoder_cmd(self):
        index_dir = 'temp_index'
        cmd = f'python -m pyserini.encode \
                  input   --corpus {self.test_file} \
                          --fields text \
                  output  --embeddings {index_dir} \
                  encoder --encoder castorini/aggretriever-distilbert \
                          --fields text \
                          --batch 1 \
                          --device cpu'
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
        self.assertAlmostEqual(embeddings[0]['vector'][0], 0.14203716814517975, places=4)
        self.assertAlmostEqual(embeddings[0]['vector'][-1], -0.011851579882204533, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][0], 0.4780103862285614, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][-1], 0.0017992404755204916, places=4)

        shutil.rmtree(index_dir)
    
    def test_aggretriever_cocondenser_encoder_cmd(self):
        index_dir = 'temp_index'
        cmd = f'python -m pyserini.encode \
                  input   --corpus {self.test_file} \
                          --fields text \
                  output  --embeddings {index_dir} \
                  encoder --encoder castorini/aggretriever-cocondenser \
                          --fields text \
                          --batch 1 \
                          --device cpu'
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
        self.assertAlmostEqual(embeddings[0]['vector'][0], 0.4865410327911377, places=4)
        self.assertAlmostEqual(embeddings[0]['vector'][-1], 0.006781343836337328, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][0], 0.32751473784446716, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][-1], 0.0014184381579980254, places=4)

        shutil.rmtree(index_dir)

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
    
    def test_clip_encoder_cmd_text(self):
        index_dir = 'temp_index'
        cmd = f'python -m pyserini.encode \
                  input   --corpus {self.test_file} \
                          --fields text \
                  output  --embeddings {index_dir} \
                  encoder --encoder openai/clip-vit-base-patch32 \
                          --fields text \
                          --batch 1 --max-length 77 \
                          --device cpu'
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
 
        self.assertAlmostEqual(embeddings[0]['vector'][0], 0.022726990282535553, places=4)
        self.assertAlmostEqual(embeddings[0]['vector'][-1], -0.02527175098657608, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][0], 0.00724585447460413, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][-1], 0.039689723402261734, places=4)

        shutil.rmtree(index_dir)
    
    def test_clip_encoder_cmd_image(self):
        # special case setup for image data
        docids = []
        texts = []
        test_file = 'tests/resources/sample_collection_jsonl_image/images.small.jsonl'
        image_dir = pl.Path(test_file).parent
        
        with open(test_file) as f:
            for line in f:
                line = json.loads(line)
                docids.append(line['id'])
                texts.append(line['path'])
        
        index_dir = 'temp_index'
        cmd = f'python -m pyserini.encode \
                  input   --corpus {test_file} \
                          --fields path \
                  output  --embeddings {index_dir} \
                  encoder --encoder openai/clip-vit-base-patch32 \
                          --fields path \
                          --batch 1 --multimodal --l2-norm \
                          --device cpu'
        status = os.system(cmd)
        self.assertEqual(status, 0)

        embedding_json_fn = os.path.join(index_dir, 'embeddings.jsonl')
        self.assertIsFile(embedding_json_fn)

        with open(embedding_json_fn) as f:
            embeddings = [json.loads(line) for line in f]

        self.assertListEqual([entry["id"] for entry in embeddings], docids)
        self.assertListEqual(
            [entry["contents"] for entry in embeddings], 
            [str(pl.Path(image_dir, entry.strip())) for entry in texts],
        )
 
        self.assertAlmostEqual(embeddings[0]['vector'][0], 0.003283643862232566, places=4)
        self.assertAlmostEqual(embeddings[0]['vector'][-1], -0.055951327085494995, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][0], 0.021012384444475174, places=4)
        self.assertAlmostEqual(embeddings[2]['vector'][-1], -0.0011692788684740663, places=4)

        shutil.rmtree(index_dir)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.tarball_name)
        shutil.rmtree(cls.index_dir)


if __name__ == '__main__':
    unittest.main()
