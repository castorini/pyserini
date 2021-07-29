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
from typing import List

from integrations.utils import run_command, parse_score


class SimpleSearcherScoreChecker:
    def __init__(self, index: str, topics: str, pyserini_topics: str, qrels: str, eval:str):
        self.index_path = index
        self.topics = topics
        self.qrels = qrels
        self.pyserini_topics = pyserini_topics

        self.pyserini_base_cmd = 'python -m pyserini.search'

        self.eval_base_cmd = eval

    @staticmethod
    def _cleanup(files: List[str]):
        for file in files:
            if os.path.exists(file):
                os.remove(file)

    def run(self, runtag: str, pyserini_extras: str, actualscore: float, tokenizer = None):
        print('-------------------------')
        print(f'Running {runtag}:')
        print('-------------------------')

        pyserini_output = f'verify.pyserini.{runtag}.txt'

        pyserini_cmd = f'{self.pyserini_base_cmd} --index {self.index_path} ' \
                       + f'--topics {self.pyserini_topics} --output {pyserini_output} {pyserini_extras}'

        if tokenizer != None:
            pyserini_cmd = pyserini_cmd + f' --tokenizer {tokenizer}'

        status = os.system(pyserini_cmd)
        if not status == 0:
            return False

        eval_cmd = f'{self.eval_base_cmd} {self.qrels} {pyserini_output}'
        status = os.system(eval_cmd)
        if not status == 0:
            return False
        stdout, stderr = run_command(eval_cmd)
        score = parse_score(stdout, "map")
        if actualscore !=score:
            self._cleanup([pyserini_output])
            return False
        self._cleanup([pyserini_output])
        return True


