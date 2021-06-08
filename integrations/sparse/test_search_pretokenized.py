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

import os
import shutil
import unittest

from random import randint
from integrations.simplesearcher_score_checker import SimpleSearcherScoreChecker


class TestSearchIntegration(unittest.TestCase):
    def setUp(self):
        # The current directory depends on if you're running inside an IDE or from command line.
        curdir = os.getcwd()
        if curdir.endswith('sparse'):
            self.pyserini_root = '../..'
        else:
            self.pyserini_root = '.'

        self.tmp = f'{self.pyserini_root}/integrations/tmp{randint(0, 10000)}'

        if os.path.exists(self.tmp):
            shutil.rmtree(self.tmp)
        else:
            os.mkdir(self.tmp)

        #wget cacm jsonl file
        os.system(f'wget https://raw.githubusercontent.com/castorini/anserini-data/master/CACM/corpus/jsonl/cacm.json -P {self.tmp}/cacm_jsonl')

        #pre tokenized jsonl
        os.system(f'python -m pyserini.tokenize_json_collection --input {self.tmp}/cacm_jsonl/ --output {self.tmp}/cacm_bert_jsonl/ --tokenizer bert-base-uncased')

        self.pyserini_index_cmd = 'python -m pyserini.index'
        self.pyserini_search_cmd = 'python -m pyserini.search'

        self.cacm_jsonl_path = os.path.join(self.tmp, 'cacm_jsonl')
        self.cacm_bert_jsonl_path = os.path.join(self.tmp, 'cacm_bert_jsonl')

        self.cacm_index_path = os.path.join(self.tmp, 'cacm_index')
        self.cacm_bert_index_path = os.path.join(self.tmp, 'cacm_bert_index')

        self.cacm_qrels_path = os.path.join(self.pyserini_root, 'tools/topics-and-qrels/qrels.cacm.txt')
        self.cacm_topics_path = os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.cacm.txt')

        os.system(f'{self.pyserini_index_cmd} -collection JsonCollection -generator DefaultLuceneDocumentGenerator -threads 9 -input {self.cacm_jsonl_path} -index {self.cacm_index_path} -storePositions -storeDocvectors -storeRaw' )
        os.system(f'{self.pyserini_index_cmd} -collection JsonCollection -generator DefaultLuceneDocumentGenerator -threads 9 -input {self.cacm_bert_jsonl_path} -index {self.cacm_bert_index_path} -storePositions -storeDocvectors -storeRaw -pretokenized')
        
        self.cacm_checker = SimpleSearcherScoreChecker(
            index=self.cacm_index_path,
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.cacm.txt'),
            pyserini_topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.cacm.txt'),
            qrels=self.cacm_qrels_path,
            eval=f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30')

        self.cacm_bert_checker = SimpleSearcherScoreChecker(
            index=self.cacm_bert_index_path,
            topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.cacm.txt'),
            pyserini_topics=os.path.join(self.pyserini_root, 'tools/topics-and-qrels/topics.cacm.txt'),
            qrels=self.cacm_qrels_path,
            eval=f'{self.pyserini_root}/tools/eval/trec_eval.9.0.4/trec_eval -m map -m P.30')

    def test_without_pretokenized(self):
        self.assertTrue(self.cacm_checker.run('cacm', '--bm25', 0.3114))

    def test_with_pretokenized(self):
        self.assertTrue(self.cacm_bert_checker.run('cacm_bert', '--bm25', 0.2750, 'bert-base-uncased'))

    def tearDown(self):
        shutil.rmtree(f'{self.tmp}')


if __name__ == '__main__':
    unittest.main()