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

import filecmp
import os
from typing import List

from pyserini.util import get_cache_home
from pyserini.prebuilt_index_info import TF_INDEX_INFO


class LuceneSearcherAnseriniMatchChecker:
    def __init__(self, index: str, topics: str, pyserini_topics: str, qrels: str):
        self.index_path = os.path.join(
            get_cache_home(),
            f'indexes/{TF_INDEX_INFO[index]["filename"].removesuffix(".tar.gz")}.{TF_INDEX_INFO[index]["md5"]}')

        self.topics = topics
        self.qrels = qrels
        self.pyserini_topics = pyserini_topics

        self.anserini_base_cmd = 'java -cp `ls pyserini/resources/jars/*-fatjar.jar` io.anserini.search.SearchCollection -topicReader Trec'
        self.pyserini_base_cmd = 'python -m pyserini.search.lucene'
        self.eval_base_cmd = 'java -cp `ls pyserini/resources/jars/*-fatjar.jar` trec_eval -m map -m P.30'

    @staticmethod
    def _cleanup(files: List[str]):
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def run(self, runtag: str, anserini_extras: str, pyserini_extras: str):
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        anserini_output = f'verify.anserini.{runtag}.txt'
        pyserini_output = f'verify.pyserini.{runtag}.txt'

        anserini_cmd = f'{self.anserini_base_cmd} -index {self.index_path} ' \
                       + f'-topics {self.topics} -output {anserini_output} {anserini_extras}'
        pyserini_cmd = f'{self.pyserini_base_cmd} --index {self.index_path} ' \
                       + f'--topics {self.pyserini_topics} --output {pyserini_output} {pyserini_extras}'

        status = os.system(anserini_cmd)
        if not status == 0:
            self._cleanup([anserini_output, pyserini_output])
            return False
        status = os.system(pyserini_cmd)
        if not status == 0:
            self._cleanup([anserini_output, pyserini_output])
            return False

        res = filecmp.cmp(anserini_output, pyserini_output)
        if res is True:
            eval_cmd = f'{self.eval_base_cmd} {self.qrels} {anserini_output}'
            status = os.system(eval_cmd)
            if not status == 0:
                print(f'[FAIL] {runtag} evaluation failure!')
                self._cleanup([anserini_output, pyserini_output])
                return False
            print(f'[SUCCESS] {runtag} results verified!')
            self._cleanup([anserini_output, pyserini_output])
            return True
        else:
            print(f'[FAIL] {runtag} result do not match!')
            self._cleanup([anserini_output, pyserini_output])
            return False
