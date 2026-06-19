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
import subprocess
import sys
import tempfile
import unittest

import pandas as pd
from transformers import DPRQuestionEncoderTokenizer

from pyserini.encode import DprDocumentEncoder, DprQueryEncoder
from pyserini.encode._dpr import _load_dpr_tokenizer
from pyserini.query_iterator import DefaultQueryIterator


EXPECTED_VALUES = [(-0.39652, 0.25375), (0.06198, -0.49947)]


class TestEncodeDpr(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.resource_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'resources'))
        cls.repo_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))

    def test_dpr_doc_encoder(self):
        texts = []
        with open(os.path.join(self.resource_dir, 'simple_cacm_corpus.json')) as f:
            for line in f:
                line = json.loads(line)
                texts.append(line['contents'])

        encoder = DprDocumentEncoder('facebook/dpr-ctx_encoder-multiset-base', device='cpu')
        vectors = encoder.encode(texts[:3])
        self.assertAlmostEqual(vectors[0][0], -0.59793, places=5)
        self.assertAlmostEqual(vectors[0][-1], -0.13037, places=5)
        self.assertAlmostEqual(vectors[2][0], -0.30448, places=5)
        self.assertAlmostEqual(vectors[2][-1], 0.15168, places=5)

    def test_dpr_encode_query_cli(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, 'encoded_queries.pkl')
            subprocess.run(
                [
                    sys.executable, '-m', 'pyserini.encode.query',
                    '--topics', 'dpr-nq-test',
                    '--encoder', 'facebook/dpr-question_encoder-multiset-base',
                    '--output', output_path,
                    '--device', 'cpu',
                    '--max-queries', '2',
                ],
                cwd=self.repo_dir,
                check=True,
            )

            encoded = pd.read_pickle(output_path)
            self.assertEqual(encoded.shape, (2, 3))
            self.assertEqual(encoded.columns.tolist(), ['id', 'text', 'embedding'])
            self.assertEqual(len(encoded.iloc[0]['embedding']), 768)
            for i, (first_value, last_value) in enumerate(EXPECTED_VALUES):
                self.assertAlmostEqual(encoded.iloc[i]['embedding'][0], first_value, places=5)
                self.assertAlmostEqual(encoded.iloc[i]['embedding'][-1], last_value, places=5)

    def test_dpr_query_encoder_direct(self):
        encoder = DprQueryEncoder('facebook/dpr-question_encoder-multiset-base', device='cpu')
        query_iterator = DefaultQueryIterator.from_topics('dpr-nq-test')
        for i, (_, text) in enumerate(query_iterator):
            if i == 2:
                break
            embedding = encoder.encode(text)
            self.assertEqual(len(embedding), 768)
            self.assertAlmostEqual(embedding[0], EXPECTED_VALUES[i][0], places=5)
            self.assertAlmostEqual(embedding[-1], EXPECTED_VALUES[i][1], places=5)

    def test_cased_dpr_tokenizer(self):
        tokenizer = _load_dpr_tokenizer(DPRQuestionEncoderTokenizer, 'castorini/mdpr-question-nq', clean_up_tokenization_spaces=True)
        # Cased mDPR checkpoints must preserve case for reproducible Mr.TyDi retrieval.
        tokens = tokenizer.tokenize('Je,nani alikuwa rais wa kwanza wa Uganda?')
        self.assertEqual(tokens[0], 'Je')
        self.assertEqual(tokens[-2], 'Uganda')

    def test_bengali_dpr_tokenizer(self):
        tokenizer = _load_dpr_tokenizer(DPRQuestionEncoderTokenizer, 'castorini/mdpr-question-nq', clean_up_tokenization_spaces=True)
        # Bengali mDPR tokenization must preserve legacy WordPiece decomposition.
        tokens = tokenizer.tokenize('১৯৮৮ সালে ঘূর্ণিঝড়ের কারণে বাংলাদেশের মোট ক্ষয়ক্ষতির পরিমান কত ?')
        self.assertIn('##ড়ে', tokens)
        self.assertIn('মোট', tokens)
        self.assertNotIn('[UNK]', tokens)


if __name__ == '__main__':
    unittest.main()
