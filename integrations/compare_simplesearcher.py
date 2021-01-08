#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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


class CompareSimpleSearcher:
    def __init__(self, index: str, topics: str):
        self.index_path = index
        self.topics = topics
        self.pyserini_base_cmd = 'python3 -m pyserini.search'

    @staticmethod
    def _cleanup(files: List[str]):
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def run(self, runtag: str, extras_one: str, extras_two: List[str]):
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        output = []

        output_one = f'verify.pyserini.{runtag}.txt'
        output.append(output_one)
        pyserini_cmd_one = f'{self.pyserini_base_cmd} --index {self.index_path} ' \
            + f'--topics {self.topics} --output {output_one} {extras_one}'
        status = os.system(pyserini_cmd_one)
        if not status == 0:
            self._cleanup(output)
            return False

        for id, extras in enumerate(extras_two):
            output_two = f'verify.pyserini.{runtag}.{id}.txt'
            output.append(output_two)
            pyserini_cmd_two = f'{self.pyserini_base_cmd} --index {self.index_path} ' \
                + f'--topics {self.topics} --output {output_two} {extras}'

            status = os.system(pyserini_cmd_two)
            if not status == 0:
                self._cleanup(output)
                return False

            res = filecmp.cmp(output_one, output_two)
            if res is False:
                print(f'[FAIL] {runtag} result for {extras} does not match!')
                self._cleanup(output)
                return False

        print(f'[SUCCESS] {runtag} results match!')
        self._cleanup(output)
        return True
