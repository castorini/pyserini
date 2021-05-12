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

import cmd
import json

from pyserini.search import SimpleSearcher
from pyserini.dsearch import SimpleDenseSearcher, TctColBertQueryEncoder, AnceQueryEncoder
from pyserini.hsearch import HybridSearcher


class MsMarcoDemo(cmd.Cmd):
    ssearcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')
    dsearcher = None
    hsearcher = None
    searcher = ssearcher

    k = 10
    prompt = '>>> '

    # https://stackoverflow.com/questions/35213134/command-prefixes-in-python-cli-using-cmd-in-pythons-standard-library
    def precmd(self, line):
        if line[0] == '/':
            line = line[1:]
        return line

    def do_help(self, arg):
        print(f'/help    : returns this message')
        print(f'/k [NUM] : sets k (number of hits to return) to [NUM]')
        print(
            f'/model [MODEL] : sets encoder to use the model [MODEL] (one of tct, ance)')
        print(
            f'/retriever [RETRIEVER] : sets retriver type to [RETRIEVER] (one of sparse, dense, hybrid)')

    def do_k(self, arg):
        print(f'setting k = {int(arg)}')
        self.k = int(arg)

    def do_retriever(self, arg):
        if arg == "sparse":
            self.searcher = self.ssearcher
        elif arg == "dense":
            self.searcher = self.dsearcher
        elif arg == "hybrid":
            self.searcher = self.hsearcher
        print(f'setting retriver = {arg}')

    def do_model(self, arg):
        if arg == "tct":
            encoder = TctColBertQueryEncoder("castorini/tct_colbert-msmarco")
            index = "msmarco-passage-tct_colbert-hnsw"
        elif arg == "ance":
            encoder = AnceQueryEncoder("castorini/ance-msmarco-passage")
            index = "msmarco-passage-ance-bf"
        else:
            print(f"Invalid argument {arg}. model should be one [tct, ance]")
            return

        self.dsearcher = SimpleDenseSearcher.from_prebuilt_index(
            index,
            encoder
        )
        self.hsearcher = HybridSearcher(self.dsearcher, self.ssearcher)
        print(f'setting model = {arg}')

    def do_EOF(self, line):
        return True

    def default(self, q):
        hits = self.searcher.search(q, self.k)

        for i in range(0, len(hits)):
            jsondoc = json.loads(hits[i].raw)
            print(f'{i + 1:2} {hits[i].score:.5f} {jsondoc["contents"]}')


if __name__ == '__main__':
    MsMarcoDemo().cmdloop()
