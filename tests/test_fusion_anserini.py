#
# Pyserini: Reproducible IR research with sparse and dense representations
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import unittest
from pyserini.pyclass import autoclass, JArrayList
from pyserini.search.lucene import JScoredDoc
from pyserini.fusion import reciprocal_rank_fusion
from pyserini.trectools import TrecRun
JScoredDocs = autoclass('io.anserini.search.ScoredDocs')
JRunsFuser = autoclass('io.anserini.fusion.RunsFuser')
JStoredField = autoclass('org.apache.lucene.document.StoredField')

def doc_to_docs(hits: list[JScoredDoc]) -> JScoredDocs:
    return JScoredDocs.fromScoredDocs(hits)

# Add fields as they are used in Anserini side
def translate(hits: list[JScoredDoc]) -> list[JScoredDoc]:
    for i in range(len(hits)):
        hits[i].lucene_docid = i + 1
        hits[i].lucene_document.add(JStoredField("TOPIC", "0"))
    return hits

def rrf(all_hits: list[list[JScoredDoc]], k: int) -> JScoredDocs:
    all_docs = [doc_to_docs(translate(hits)) for hits in all_hits]
    arr_list = JArrayList()
    for docs in all_docs:
        arr_list.add(docs)
    return JRunsFuser.reciprocalRankFusion(arr_list, k, 1000, 1000)

def current_fusion(all_hits: list[list[JScoredDoc]]) -> TrecRun:
    trec_runs, docid_to_search_result = list(), dict()
    for hits in all_hits:
        docid_score_pair = list()
        for hit in hits:
            docid_to_search_result[hit.docid] = hit
            docid_score_pair.append((hit.docid, hit.score))

            run = TrecRun.from_search_results(docid_score_pair)
            trec_runs.append(run)
    return reciprocal_rank_fusion(trec_runs, rrf_k=60)

class TestFusion(unittest.TestCase):
    def testFusion(self):
        from pyserini.search.lucene import LuceneSearcher
        searcher = LuceneSearcher.from_prebuilt_index("bright-biology")
        hits = searcher.search("dogs")
        # print("hits 1")
        # for hit in hits:
        #     print(f"{hit.docid} {hit.score}")
        # print()
        from pyserini.search.lucene import LuceneImpactSearcher
        searcher2 = LuceneImpactSearcher.from_prebuilt_index("bright-biology.splade-v3", "naver/splade-v3")
        hits2 = searcher2.search("dogs")
        # print("hits 2")
        # for hit in hits2:
        #     print(f"{hit.docid} {hit.score}")
        # print()
        
        fused = rrf([hits, hits2], 60)
        for i in range(len(fused.docids)):
            print(f"{fused.docids[i]} {fused.scores[i]}")
        print()

        print(current_fusion([hits, hits2]).run_data)