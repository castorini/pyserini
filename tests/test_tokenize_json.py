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
import unittest
from shutil import rmtree


class TestTokenizeJson(unittest.TestCase):
    def test_bert_single_file(self):
        inj = 'test_bert_single_file.json'
        outj = 'out_test_bert_single_file.json'
        f = open(inj, 'w')
        f.write('{"id": "doc1","contents": "I have a new gpu!"}\n{"id": "doc2","contents": "I do have an old gpu!"}')
        f.close()
        if(os.getcwd().endswith('tests')):
            os.system(f'python ../pyserini/tokenize_json_collection.py --input {inj} --output {outj}')
        else:
            os.system(f'python pyserini/tokenize_json_collection.py --input {inj} --output {outj}')
        with open(outj, 'r') as ret:
            for i, line in enumerate(ret):
                contents = json.loads(line)['contents']
                if (i == 0):
                    self.assertEqual('i have a new gp ##u !', contents)
                else:
                    self.assertEqual('i do have an old gp ##u !', contents)
        ret.close()
        os.remove(inj)
        os.remove(outj)

    def test_bert_dir(self):
        indir = './test_tokenize_json'
        outdir = './test_out_tokenize_json'
        if(os.path.isdir(indir)):
            rmtree(indir)
        os.mkdir(indir)
        f1 = open(indir+'/doc00.json', 'w')
        f1.write('{"id": "doc1","contents": "I have a new gpu!"}\n{"id": "doc2","contents": "I do have an old gpu!"}')
        f1.close()
        f2 = open(indir+'/doc01.json', 'w')
        f2.write('{"id": "doc1","contents": "A new gpu!"}\n{"id": "doc2","contents": "An old gpu!"}')
        f2.close()
        if (os.getcwd().endswith('tests')):
            os.system(f'python ../pyserini/tokenize_json_collection.py --input {indir} --output {outdir}')
        else:
            os.system(f'python pyserini/tokenize_json_collection.py --input {indir} --output {outdir}')
        with open(outdir+'/docs00.json', 'r') as ret:
            for i, line in enumerate(ret):
                contents = json.loads(line)['contents']
                if (i == 0):
                    self.assertEqual('i have a new gp ##u !', contents)
                else:
                    self.assertEqual('i do have an old gp ##u !', contents)
        with open(outdir+'/docs01.json', 'r') as ret:
            for i, line in enumerate(ret):
                contents = json.loads(line)['contents']
                if (i == 0):
                    self.assertEqual('a new gp ##u !', contents)
                else:
                    self.assertEqual('an old gp ##u !', contents)
        rmtree(outdir)
        rmtree(indir)


if __name__ == '__main__':
    unittest.main()
