from pyserini.search import JASSv2Searcher
import jass



searcher = JASSv2Searcher('msmarco-passage')
hits = searcher.search('what is a lobster roll?')

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:7} {hits[i].score:.5f}')