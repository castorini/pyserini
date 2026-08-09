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
import glob
import os
import shlex
import subprocess
import sys

from pyserini.prebuilt_index_info import TF_INDEX_INFO
from pyserini.util import get_cache_home


class LuceneSearcherAnseriniMatchChecker:
    def __init__(self, index: str, topics: str, qrels: str):
        self.index_path = os.path.join(
            get_cache_home(),
            f'indexes/{TF_INDEX_INFO[index]["filename"].removesuffix(".tar.gz")}.{TF_INDEX_INFO[index]["md5"]}')

        self.topics = topics
        self.qrels = qrels

        fatjar = glob.glob('pyserini/resources/jars/*-fatjar.jar')[0]
        self.anserini_base_cmd = ['java', '-cp', fatjar, '-Dslf4j.internal.verbosity=WARN', '--add-modules', 'jdk.incubator.vector', '--enable-native-access=ALL-UNNAMED', 'io.anserini.search.SearchCollection', '-topicReader', 'Trec']
        self.pyserini_base_cmd = [sys.executable, '-m', 'pyserini.search.lucene']
        self.eval_base_cmd = ['java', '-cp', fatjar, 'trec_eval', '-m', 'map', '-m', 'P.30']

    @staticmethod
    def _cleanup(files: list[str]):
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    @staticmethod
    def _run(command: list[str]) -> bool:
        print(shlex.join(command))
        return subprocess.run(command, check=False).returncode == 0

    def run(self, runtag: str, anserini_extras: str, pyserini_extras: str):
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        anserini_output = f'verify.anserini.{runtag}.txt'
        pyserini_output = f'verify.pyserini.{runtag}.txt'

        anserini_cmd = self.anserini_base_cmd + ['-index', self.index_path, '-topics', self.topics, '-output', anserini_output, *shlex.split(anserini_extras)]
        pyserini_cmd = self.pyserini_base_cmd + ['--index', self.index_path, '--topics', self.topics, '--output', pyserini_output, *shlex.split(pyserini_extras)]

        if not self._run(anserini_cmd):
            self._cleanup([anserini_output, pyserini_output])
            return False
        if not self._run(pyserini_cmd):
            self._cleanup([anserini_output, pyserini_output])
            return False

        res = filecmp.cmp(anserini_output, pyserini_output)
        if res is True:
            eval_cmd = self.eval_base_cmd + [self.qrels, anserini_output]
            if not self._run(eval_cmd):
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
