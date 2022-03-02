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
        #Download prebuilt index
        #retrieve candidate
        os.system(f'python -m pyserini.search.lucene --topics msmarco-doc-dev  --index msmarco-doc-per-passage-ltr --output ltr_test/{inp} --bm25 --output-format trec --hits 10000')
        #Pre-trained ltr model
        model_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-msmarco-passage-mrr-v1.tar.gz'
        model_tar_name = 'model-ltr-msmarco-passage-mrr-v1.tar.gz'
        os.system(f'wget {model_url} -P ltr_test/')
        os.system(f'tar -xzvf ltr_test/{model_tar_name} -C ltr_test')

        # IBM model
        ibm_model_url = 'https://rgw.cs.uwaterloo.ca/JIMMYLIN-bucket0/pyserini-models/model-ltr-ibm.tar.gz'
        ibm_model_tar_name = 'model-ltr-ibm.tar.gz'
        os.system(f'wget {ibm_model_url} -P ltr_test/')

        # queries process
        os.system(f'tar -xzvf ltr_test/{ibm_model_tar_name} -C ltr_test')
        os.system('python scripts/ltr_msmarco/convert_queries.py --input tools/topics-and-qrels/topics.msmarco-doc.dev.txt --output ltr_test/queries.dev.small.json')
        os.system(f'python -m pyserini.search.lucene.ltr   --input ltr_test/{inp} --input-format trec --data document --model ltr_test/msmarco-passage-ltr-mrr-v1/ --index msmarco-doc-per-passage-ltr --ibm-model ltr_test/ibm_model/ --queries ltr_test --output ltr_test/{outp} --max-passage')

        result = subprocess.check_output(f'python tools/scripts/msmarco/msmarco_doc_eval.py --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt --run ltr_test/{outp}', shell=True).decode(sys.stdout.encoding)
        a,b = result.find('#####################\nMRR @100:'), result.find('\nQueriesRanked: 5193\n#####################\n')
        mrr = result[a+32:b]
        # See https://github.com/castorini/pyserini/issues/951
        self.assertAlmostEqual(float(mrr), 0.3105, delta=0.0001)
        rmtree('ltr_test')


if __name__ == '__main__':
    unittest.main()
