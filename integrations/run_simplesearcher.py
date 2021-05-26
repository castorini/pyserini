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

import hashlib
import os
from typing import List


class RunSimpleSearcher:
    def __init__(self, index: str, topics: str):
        self.index_path = index
        self.topics = topics
        self.pyserini_base_cmd = 'python -m pyserini.search'

    @staticmethod
    def _cleanup(files: List[str]):
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def run(self, runtag: str, extras: str) -> str:
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        output = f'verify.pyserini.{runtag}.txt'
        pyserini_cmd = f'{self.pyserini_base_cmd} --index {self.index_path} ' \
            + f'--topics {self.topics} --output {output} {extras}'

        status = os.system(pyserini_cmd)
        if not status == 0:
            self._cleanup([output])
            return ""

        with open(output, 'rb') as f:
            md5 = hashlib.md5(f.read()).hexdigest()
        self._cleanup([output])
        return md5
