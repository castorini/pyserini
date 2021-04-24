#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

from transformers import BertTokenizer, T5Tokenizer
import unittest


class TestTokenization(unittest.TestCase):
    def setUp(self):
        pass

    def test_bert_base_uncased(self):
        # https://huggingface.co/transformers/tokenizer_summary.html
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        tokens = tokenizer.tokenize('I have a new GPU!')
        self.assertEqual(['i', 'have', 'a', 'new', 'gp', '##u', '!'], tokens)

    def test_bert_base_uncased(self):
        # These are examples used in the ptr4tr book
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        tokens = tokenizer.tokenize('walking talking balking biking hiking rolling scrolling')
        self.assertEqual(['walking', 'talking', 'bal', '##king', 'biking', 'hiking', 'rolling', 'scrolling'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['bio', '##sta', '##tist', '##ics'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['ad', '##vers', '##aria', '##l'], tokens)

        tokenizer = BertTokenizer.from_pretrained('bert-base-cased')
        tokens = tokenizer.tokenize('walking talking balking biking hiking')
        self.assertEqual(['walking', 'talking', 'b', '##alk', '##ing', 'bi', '##king', 'hiking'], tokens)

        tokens = tokenizer.tokenize('rolling scrolling')
        self.assertEqual(['rolling', 'scroll', '##ing'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['bio', '##sta', '##tist', '##ics'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['ad', '##vers', '##aria', '##l'], tokens)

    def test_doc2query(self):
        tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
        tokens = tokenizer.tokenize('I have a new GPU!')
        self.assertEqual(['▁I', '▁have', '▁', 'a', '▁new', '▁GPU', '!'], tokens)

        tokenizer = T5Tokenizer.from_pretrained('castorini/doc2query-t5-base-msmarco')
        tokens = tokenizer.tokenize('walking talking biking scrolling')
        self.assertEqual(['▁walking', '▁talking', '▁biking', '▁scroll', 'ing'], tokens)

        tokens = tokenizer.tokenize('biostatistics')
        self.assertEqual(['▁bio', 'stat', 'istic', 's'], tokens)

        tokens = tokenizer.tokenize('adversarial')
        self.assertEqual(['▁adversar', 'i', 'al'], tokens)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
