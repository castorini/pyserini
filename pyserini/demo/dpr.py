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
import random

from pyserini.search.lucene import LuceneSearcher
from pyserini.search.faiss import FaissSearcher, DprQueryEncoder
from pyserini.search.hybrid import HybridSearcher
from pyserini import search


class DPRDemo(cmd.Cmd):
    nq_dev_topics = list(search.get_topics('dpr-nq-dev').values())
    trivia_dev_topics = list(search.get_topics('dpr-trivia-dev').values())

    ssearcher = LuceneSearcher.from_prebuilt_index('wikipedia-dpr')
    searcher = ssearcher

    encoder = DprQueryEncoder("facebook/dpr-question_encoder-multiset-base")
    index = 'wikipedia-dpr-multi-bf'
    dsearcher = FaissSearcher.from_prebuilt_index(
        index,
        encoder
    )
    hsearcher = HybridSearcher(dsearcher, ssearcher)

    k = 10
    prompt = '>>> '

    def precmd(self, line):
        if line[0] == '/':
            line = line[1:]
        return line

    def do_help(self, arg):
        print(f'/help    : returns this message')
        print(f'/k [NUM] : sets k (number of hits to return) to [NUM]')
        print(f'/mode [MODE] : sets retriever type to [MODE] (one of sparse, dense, hybrid)')
        print(f'/random [COLLECTION]: returns results for a random question from the dev subset [COLLECTION] (one of nq, trivia).')

    def do_k(self, arg):
        print(f'setting k = {int(arg)}')
        self.k = int(arg)

    def do_mode(self, arg):
        if arg == "sparse":
            self.searcher = self.ssearcher
        elif arg == "dense":
            self.searcher = self.dsearcher
        elif arg == "hybrid":
            self.searcher = self.hsearcher
        else:
            print(
                f'Mode "{arg}" is invalid. Mode should be one of [sparse, dense, hybrid].')
            return
        print(f'setting retriver = {arg}')

    def do_random(self, arg):
        if arg == "nq":
            topics = self.nq_dev_topics
        elif arg == "trivia":
            topics = self.trivia_dev_topics
        else:
            print(
                f'Collection "{arg}" is invalid. Collection should be one of [nq, trivia].')
            return
        q = random.choice(topics)['title']
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
    DPRDemo().cmdloop()
