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
import subprocess
import sys
import unittest
from shutil import rmtree


class TestLtrMsmarcoPassage(unittest.TestCase):
    def test_reranking(self):
        if os.path.isdir('ltr_test'):
            rmtree('ltr_test')
            os.mkdir('ltr_test')
        inp = 'run.msmarco-passage.bm25tuned.txt'
        outp = 'run.ltr.msmarco-passage.test.tsv'
        #Pre-trained ltr model
        model_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-msmarco-passage-mrr-v1.tar.gz'
        model_tar_name = 'model-ltr-msmarco-passage-mrr-v1.tar.gz'
        os.system(f'wget {model_url} -P ltr_test/')
        os.system(f'tar -xzvf ltr_test/{model_tar_name} -C ltr_test')
        # IBM model
        ibm_model_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-ibm.tar.gz'
        ibm_model_tar_name = 'model-ltr-ibm.tar.gz'
        os.system(f'wget {ibm_model_url} -P ltr_test/')
        os.system(f'tar -xzvf ltr_test/{ibm_model_tar_name} -C ltr_test')
        #queries process
        os.system(f'python -m pyserini.search.lucene.ltr \
                    --model ltr_test/msmarco-passage-ltr-mrr-v1 \
                    --topic tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt \
                    --qrel tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt \
                    --index msmarco-v1-passage.ltr --ibm-model ltr_test/ibm_model/ \
                    --output-format tsv --output ltr_test/{outp}')
        result = subprocess.check_output(f'python tools/scripts/msmarco/msmarco_passage_eval.py tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt ltr_test/{outp}', shell=True).decode(sys.stdout.encoding)
        a,b = result.find('#####################\nMRR @10:'), result.find('\nQueriesRanked: 6980\n#####################\n')
        mrr = result[a+31:b]
        # See https://github.com/castorini/pyserini/issues/951
        self.assertAlmostEqual(float(mrr), 0.2472, delta=0.0001)
        rmtree('ltr_test')


if __name__ == '__main__':
    unittest.main()
