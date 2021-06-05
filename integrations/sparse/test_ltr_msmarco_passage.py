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

class TestLtrMsmarcoPassage(unittest.TestCase):
    def test_reranking(self):
        if(os.path.isdir('ltr_test')):
            rmtree('ltr_test')
            os.mkdir('ltr_test')
        inp = 'run.msmarco-passage.bm25tuned.txt'
        outp = 'run.ltr.msmarco-passage.test.tsv'
        #Download candidate
        os.system('wget https://www.dropbox.com/s/bjyzf65uns2is61/run.msmarco-passage.bm25tuned.txt -P ltr_test')
        #Download prebuilt index
        SimpleSearcher.from_prebuilt_index('msmarco-passage-ltr')
        #Pre-trained ltr model
        model_url = 'https://www.dropbox.com/s/ffl2bfw4cd5ngyz/msmarco-passage-ltr-mrr-v1.tar.gz'
        model_tar_name = 'msmarco-passage-ltr-mrr-v1.tar.gz'
        os.system(f'wget {model_url} -P ltr_test/')
        os.system(f'tar -xzvf ltr_test/{model_tar_name} -C ltr_test')
        #ibm model
        ibm_model_url = 'https://www.dropbox.com/s/vlrfcz3vmr4nt0q/ibm_model.tar.gz'
        ibm_model_tar_name = 'ibm_model.tar.gz'
        os.system(f'wget {ibm_model_url} -P ltr_test/')
        os.system(f'tar -xzvf ltr_test/{ibm_model_tar_name} -C ltr_test')
        #queries process
        os.system('python scripts/ltr_msmarco-passage/convert_queries.py --input tools/topics-and-qrels/topics.msmarco-passage.dev-subset.txt --output ltr_test/queries.dev.small.json')
        os.system(f'python -m pyserini.ltr.search_msmarco_passage --input ltr_test/{inp} --input-format tsv --model ltr_test/msmarco-passage-ltr-mrr-v1 --index ~/.cache/pyserini/indexes/index-msmarco-passage-ltr-20210519-e25e33f.a5de642c268ac1ed5892c069bdc29ae3 --ibm-model ltr_test/ibm_model/ --queries ltr_test --output ltr_test/{outp}')
        result = subprocess.check_output(f'python tools/scripts/msmarco/msmarco_passage_eval.py tools/topics-and-qrels/qrels.msmarco-passage.dev-subset.txt ltr_test/{outp}', shell=True).decode(sys.stdout.encoding)
        a,b = result.find('#####################\nMRR @10:'), result.find('\nQueriesRanked: 6980\n#####################\n')
        mrr = result[a+31:b]
        self.assertAlmostEqual(float(mrr),0.24709612498294367, delta=0.000001)
        rmtree('ltr_test')

if __name__ == '__main__':
    unittest.main()
