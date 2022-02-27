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

import cmd
import json
import os
import random

from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher, TctColBertQueryEncoder, AnceQueryEncoder
from pyserini.search.hybrid import HybridSearcher
from pyserini import search


class MsMarcoDemo(cmd.Cmd):
    dev_topics = list(search.get_topics('msmarco-passage-dev-subset').values())

    ssearcher = LuceneSearcher.from_prebuilt_index('msmarco-passage')
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
        print(f'/model [MODEL] : sets encoder to use the model [MODEL] (one of tct, ance)')
        print(f'/mode [MODE] : sets retriever type to [MODE] (one of sparse, dense, hybrid)')
        print(f'/random : returns results for a random question from dev subset')

    def do_k(self, arg):
        print(f'setting k = {int(arg)}')
        self.k = int(arg)

    def do_mode(self, arg):
        if arg == "sparse":
            self.searcher = self.ssearcher
        elif arg == "dense":
            if self.dsearcher is None:
                print(f'Specify model through /model before using dense retrieval.')
                return
            self.searcher = self.dsearcher
        elif arg == "hybrid":
            if self.hsearcher is None:
                print(f'Specify model through /model before using hybrid retrieval.')
                return
            self.searcher = self.hsearcher
        else:
            print(
                f'Mode "{arg}" is invalid. Mode should be one of [sparse, dense, hybrid].')
            return
        print(f'setting retriver = {arg}')

    def do_model(self, arg):
        if arg == "tct":
            encoder = TctColBertQueryEncoder("castorini/tct_colbert-msmarco")
            index = "msmarco-passage-tct_colbert-hnsw"
        elif arg == "ance":
            encoder = AnceQueryEncoder("castorini/ance-msmarco-passage")
            index = "msmarco-passage-ance-bf"
        else:
            print(
                f'Model "{arg}" is invalid. Model should be one of [tct, ance].')
            return

        self.dsearcher = FaissSearcher.from_prebuilt_index(
            index,
            encoder
        )
        self.hsearcher = HybridSearcher(self.dsearcher, self.ssearcher)
        print(f'setting model = {arg}')

    def do_random(self, arg):
        q = random.choice(self.dev_topics)['title']
        print(f'question: {q}')
        self.default(q)

    def do_EOF(self, line):
        return True

    def default(self, q):
        hits = self.searcher.search(q, self.k)

        for i in range(0, len(hits)):
            raw_doc = None
            if isinstance(self.searcher, LuceneSearcher):
                raw_doc = hits[i].raw
            else:
                doc = self.searcher.doc(hits[i].docid)
                if doc:
                    raw_doc = doc.raw()
            jsondoc = json.loads(raw_doc)
            print(f'{i + 1:2} {hits[i].score:.5f} {jsondoc["contents"]}')


if __name__ == '__main__':
    MsMarcoDemo().cmdloop()
