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
import hashlib
import os
import shlex
import sys
import tempfile

from integrations.utils import parse_score, run_command
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

    def run(self, runtag: str, anserini_extras: str, pyserini_extras: str):
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        os.makedirs('tmp', exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=f'lucenesearcher-{runtag}-', dir='tmp') as temp_dir:
            anserini_output = os.path.join(temp_dir, 'anserini.txt')
            pyserini_output = os.path.join(temp_dir, 'pyserini.txt')

            anserini_cmd = self.anserini_base_cmd + ['-index', self.index_path, '-topics', self.topics, '-output', anserini_output, *shlex.split(anserini_extras)]
            pyserini_cmd = self.pyserini_base_cmd + ['--index', self.index_path, '--topics', self.topics, '--output', pyserini_output, *shlex.split(pyserini_extras)]

            result = run_command(anserini_cmd)
            if result.returncode != 0:
                return False

            result = run_command(pyserini_cmd)
            if result.returncode != 0:
                return False

            res = filecmp.cmp(anserini_output, pyserini_output)
            if res is True:
                eval_cmd = self.eval_base_cmd + [self.qrels, anserini_output]
                result = run_command(eval_cmd)
                if result.returncode != 0:
                    print(f'[FAIL] {runtag} evaluation failure!')
                    return False
                print(f'[SUCCESS] {runtag} results verified!')
                return True
            else:
                print(f'[FAIL] {runtag} result do not match!')
                return False


class LuceneSearcherScoreChecker:
    def __init__(self, index: str, topics: str, qrels: str, eval:str):
        self.index_path = index
        self.topics = topics
        self.qrels = qrels
        self.pyserini_base_cmd = [sys.executable, '-m', 'pyserini.search.lucene']
        self.eval_base_cmd = shlex.split(eval)

    @staticmethod
    def _cleanup(files: list[str]):
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def run(self, runtag: str, pyserini_extras: str, actualscore: float, tokenizer = None):
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        pyserini_output = f'verify.pyserini.{runtag}.txt'

        pyserini_cmd = self.pyserini_base_cmd + [
            '--index', self.index_path,
            '--topics', self.topics,
            '--output', pyserini_output,
            *shlex.split(pyserini_extras),
        ]

        if tokenizer is not None:
            pyserini_cmd += ['--tokenizer', tokenizer]

        result = run_command(pyserini_cmd)
        if result.returncode != 0:
            return False

        eval_cmd = self.eval_base_cmd + [self.qrels, pyserini_output]
        result = run_command(eval_cmd)
        if result.returncode != 0:
            return False

        score = parse_score(result.stdout, 'map')
        self._cleanup([pyserini_output])

        return actualscore == score


class RunLuceneSearcher:
    def __init__(self, index: str, topics: str):
        self.index_path = index
        self.topics = topics
        self.pyserini_base_cmd = [sys.executable, '-m', 'pyserini.search.lucene']

    @staticmethod
    def _cleanup(files: list[str]):
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def run(self, runtag: str, extras: str) -> str:
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        output = f'verify.pyserini.{runtag}.txt'
        pyserini_cmd = self.pyserini_base_cmd + [
            '--index', self.index_path,
            '--topics', self.topics,
            '--output', output,
            *shlex.split(extras),
        ]

        result = run_command(pyserini_cmd)
        if result.returncode != 0:
            self._cleanup([output])
            return ''

        with open(output, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        self._cleanup([output])
        return md5
