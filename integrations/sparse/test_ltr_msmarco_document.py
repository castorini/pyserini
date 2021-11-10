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

import unittest
import subprocess
import os
from shutil import rmtree
from pyserini.search import SimpleSearcher
from random import randint
from urllib.request import urlretrieve
import tarfile
import sys

class TestLtrMsmarcoDocument(unittest.TestCase):
    def test_reranking(self):
        if(os.path.isdir('ltr_test')):
            rmtree('ltr_test')
            os.mkdir('ltr_test')
        inp = 'run.msmarco-pass-doc.bm25.txt'
        outp = 'run.ltr.msmarco-pass-doc.test.trec'
        outp_tsv = 'run.ltr.msmarco-pass-doc.test.tsv'
        #Download candidate
        os.system('wget https://www.dropbox.com/s/sxf16jcjtw1q9z7/run.msmarco-pass-doc.bm25.txt -P ltr_test')
        #Download prebuilt index
        SimpleSearcher.from_prebuilt_index('msmarco-doc-per-passage-ltr')
        #Pre-trained ltr model
        model_url = 'https://www.dropbox.com/s/ffl2bfw4cd5ngyz/msmarco-passage-ltr-mrr-v1.tar.gz'
        model_tar_name = 'msmarco-passage-ltr-mrr-v1.tar.gz'
        os.system(f'wget {model_url} -P ltr_test/')
        os.system(f'tar -xzvf ltr_test/{model_tar_name} -C ltr_test')
        #ibm model
        ibm_model_url = 'https://www.dropbox.com/s/vlrfcz3vmr4nt0q/ibm_model.tar.gz'
        ibm_model_tar_name = 'ibm_model.tar.gz'
        os.system(f'wget {ibm_model_url} -P ltr_test/')
        #queries process
        os.system(f'tar -xzvf ltr_test/{ibm_model_tar_name} -C ltr_test')
        os.system('python scripts/ltr_msmarco/convert_queries.py --input tools/topics-and-qrels/topics.msmarco-doc.dev.txt --output ltr_test/queries.dev.small.json')
        os.system(f'python scripts/ltr_msmarco/ltr_inference.py  --input ltr_test/{inp} --input-format trec --data document --model ltr_test/msmarco-passage-ltr-mrr-v1 --index ~/.cache/pyserini/indexes/index-msmarco-doc-per-passage-ltr-20211031-33e4151 --ibm-model ltr_test/ibm_model/ --queries ltr_test --output ltr_test/{outp}')
        #convert trec to tsv withmaxP
        os.system(f'python scripts/ltr_msmarco/generate_document_score_withmaxP.py --input ltr_test/{outp} --output ltr_test/{outp_tsv}')


        result = subprocess.check_output(f'python tools/scripts/msmarco/msmarco_doc_eval.py --judgments tools/topics-and-qrels/qrels.msmarco-doc.dev.txt --run ltr_test/{outp_tsv}', shell=True).decode(sys.stdout.encoding)
        a,b = result.find('#####################\nMRR @100:'), result.find('\nQueriesRanked: 5193\n#####################\n')
        mrr = result[a+32:b]
        self.assertAlmostEqual(float(mrr),0.3090492928920076, delta=0.000001)
        rmtree('ltr_test')

if __name__ == '__main__':
    unittest.main()