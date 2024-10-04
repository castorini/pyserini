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


class TestLtrMsmarcoDocument(unittest.TestCase):
    def test_reranking(self):
        if(os.path.isdir('ltr_test')):
            rmtree('ltr_test')
            os.mkdir('ltr_test')
        inp = 'run.msmarco-pass-doc.bm25.txt'
        outp = 'run.ltr.msmarco-pass-doc.test.trec'
        outp_tsv = 'run.ltr.msmarco-pass-doc.test.tsv'
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
        os.system(f'python -m pyserini.search.lucene.ltr  \
                    --topic tools/topics-and-qrels/topics.msmarco-doc.dev.txt \
                    --model ltr_test/msmarco-passage-ltr-mrr-v1/   \
                    --qrel tools/topics-and-qrels/qrels.msmarco-doc.dev.txt \
                    --index msmarco-v1-doc-segmented.ltr --ibm-model ltr_test/ibm_model/ \
                    --granularity document --output ltr_test/{outp} --max-passage --hits 10000')

        result = subprocess.check_output(f'python tools/scripts/msmarco/msmarco_doc_eval.py --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt --run ltr_test/{outp}', shell=True).decode(sys.stdout.encoding)
        a,b = result.find('#####################\nMRR @100:'), result.find('\nQueriesRanked: 5193\n#####################\n')
        mrr = result[a+32:b]
        # See:
        #  - https://github.com/castorini/pyserini/issues/951
        #  - https://github.com/castorini/pyserini/issues/1430
        self.assertAlmostEqual(float(mrr), 0.3108, delta=0.0002)
        rmtree('ltr_test')

if __name__ == '__main__':
    unittest.main()
