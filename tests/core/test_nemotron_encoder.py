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

"""Tests for the Nemotron embedding encoders.

The pooling tests run anywhere. The end-to-end test needs the 16 GB checkpoint and a GPU, so it is
skipped unless PYSERINI_TEST_NEMOTRON=1; it reproduces the similarity matrix published on the model
card, which is the only check that covers prefixes, pooling and normalisation together.
"""

import os
import unittest

import numpy as np
import torch

from pyserini.encode._nemotron import (DEFAULT_DOCUMENT_PREFIX, DEFAULT_QUERY_PREFIX, mean_pool)

MODEL = 'nvidia/Nemotron-3-Embed-8B-BF16'

# model card, "Transformers Expected Output": rows are queries, columns documents
CARD_SCORES = np.array([[0.7856, 0.0496, 0.0113, -0.0298],
                        [0.0458, 0.6505, -0.0642, 0.0451]])

QUERIES = [
    'Write a Python function that counts the frequency of each element in a list of lists.',
    "Write a function that orders a dictionary with tuple keys by the product of each key's tuple values.",
]
DOCUMENTS = [
    'def frequency_lists(list1):\n    flattened = [item for sublist in list1 for item in sublist]\n'
    '    counts = {}\n    for item in flattened:\n        if item in counts:\n'
    '            counts[item] += 1\n        else:\n            counts[item] = 1\n    return counts',
    'def sort_dict_item(test_dict):\n    return {key: test_dict[key] for key in sorted(test_dict.keys(), '
    'key=lambda ele: ele[0] * ele[1])}',
    'Eczema commonly causes itchy, dry, inflamed patches of skin. The affected areas may look red, '
    'scaly, cracked, or darker than the surrounding skin depending on skin tone. Symptoms can flare '
    'after exposure to irritants, allergens, stress, or changes in weather.',
    'People with pollen allergy can reduce exposure by staying indoors on dry, windy days, avoiding '
    'early-morning outdoor activity, and going outside after rain when pollen levels are lower.',
]


class TestNemotronPooling(unittest.TestCase):
    def test_prefixes_match_the_model_card(self):
        # config_sentence_transformers.json: {"query": "query: ", "document": "passage: "}
        self.assertEqual(DEFAULT_QUERY_PREFIX, 'query: ')
        self.assertEqual(DEFAULT_DOCUMENT_PREFIX, 'passage: ')

    def test_mean_pool_ignores_padding(self):
        # two sequences of three positions; the second has one padded position whose state is junk
        hidden = torch.tensor([[[1.0, 2.0], [3.0, 4.0], [5.0, 6.0]],
                               [[1.0, 1.0], [3.0, 3.0], [99.0, -99.0]]])
        mask = torch.tensor([[1, 1, 1], [1, 1, 0]])
        pooled = mean_pool(hidden, mask)
        self.assertTrue(np.allclose(pooled[0].numpy(), [3.0, 4.0]))
        # the padded position must not contribute: mean of (1,1) and (3,3)
        self.assertTrue(np.allclose(pooled[1].numpy(), [2.0, 2.0]))

    def test_mean_pool_handles_left_padding(self):
        # the tokenizer pads on the left, so the mask's leading entries are the zeros
        hidden = torch.tensor([[[-50.0, 50.0], [2.0, 4.0], [4.0, 8.0]]])
        mask = torch.tensor([[0, 1, 1]])
        pooled = mean_pool(hidden, mask)
        self.assertTrue(np.allclose(pooled[0].numpy(), [3.0, 6.0]))

    def test_mean_pool_is_not_last_token_pool(self):
        # guards against the copy-paste that would silently turn this into the Qwen3 encoder
        hidden = torch.tensor([[[0.0, 0.0], [10.0, 10.0]]])
        mask = torch.tensor([[1, 1]])
        pooled = mean_pool(hidden, mask)
        self.assertFalse(np.allclose(pooled[0].numpy(), [10.0, 10.0]))


@unittest.skipUnless(os.environ.get('PYSERINI_TEST_NEMOTRON') == '1',
                     'needs the 16 GB checkpoint and a GPU; set PYSERINI_TEST_NEMOTRON=1')
class TestNemotronAgainstModelCard(unittest.TestCase):
    def test_reproduces_card_similarities(self):
        from pyserini.encode._nemotron import NemotronDocumentEncoder, NemotronQueryEncoder
        device = 'cuda:0' if torch.cuda.is_available() else 'cpu'
        doc_encoder = NemotronDocumentEncoder(MODEL, device=device)
        query_encoder = NemotronQueryEncoder(MODEL, device=device)

        doc_embeddings = doc_encoder.encode(DOCUMENTS)
        query_embeddings = np.stack([query_encoder.encode(q) for q in QUERIES])

        # L2-normalised, so the inner product is the cosine the card reports
        self.assertTrue(np.allclose(np.linalg.norm(doc_embeddings, axis=1), 1.0, atol=1e-2))
        self.assertTrue(np.allclose(np.linalg.norm(query_embeddings, axis=1), 1.0, atol=1e-2))
        self.assertEqual(doc_embeddings.shape[1], 4096)

        scores = query_embeddings @ doc_embeddings.T
        # bf16 across runtimes moves these a little; the card itself warns values vary by runtime
        self.assertTrue(np.allclose(scores, CARD_SCORES, atol=2e-2),
                        f'scores\n{scores}\ndiffer from the model card\n{CARD_SCORES}')
        # and the diagonal must win its row, which is the property retrieval depends on
        for row in range(CARD_SCORES.shape[0]):
            self.assertEqual(int(np.argmax(scores[row])), row)


if __name__ == '__main__':
    unittest.main()
