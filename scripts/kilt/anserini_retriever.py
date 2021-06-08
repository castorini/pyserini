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

import multiprocessing
from multiprocessing.pool import ThreadPool

from tqdm import tqdm
from pyserini.search import SimpleSearcher

import kilt.kilt_utils as utils
from kilt.retrievers.base_retriever import Retriever

import jnius

from nltk import bigrams, word_tokenize, SnowballStemmer
from nltk.corpus import stopwords
import string

ent_start_token = "[START_ENT]"
ent_end_token = "[END_ENT]"
STOPWORDS = set(stopwords.words('english') + list(string.punctuation))
stemmer = SnowballStemmer("english")


def parse_hits(hits):
    doc_ids = []
    doc_scores = []
    for hit in hits:
        wikipedia_id = hit.docid.split('-')[0]
        if wikipedia_id and wikipedia_id not in doc_ids:
            doc_ids.append(wikipedia_id)
            doc_scores.append(hit.score)
    return doc_ids, doc_scores


def _get_predictions_thread(arguments):

    id = arguments["id"]
    queries_data = arguments["queries_data"]
    topk = arguments["topk"]
    ranker = arguments["ranker"]
    logger = arguments["logger"]
    use_bigrams = arguments["use_bigrams"]
    stem_bigrams = arguments["stem_bigrams"]

    if id == 0:
        iter_ = tqdm(queries_data)
    else:
        iter_ = queries_data

    result_doc_ids = []
    result_doc_scores = []
    result_query_id = []

    for query_element in iter_:

        query = (
            query_element["query"]
            .replace(ent_start_token, "")
            .replace(ent_end_token, "")
            .strip()
        )
        result_query_id.append(query_element["id"])

        doc_ids = []
        doc_scores = []

        if use_bigrams:
            tokens = filter(lambda word: word.lower() not in STOPWORDS, word_tokenize(query))
            if stem_bigrams:
                tokens = map(stemmer.stem, tokens)
            bigram_query = bigrams(tokens)
            bigram_query = " ".join(["".join(bigram) for bigram in bigram_query])
            query += " " + bigram_query
        try:
            hits = ranker.search(query, k=topk)
            doc_ids, doc_scores = parse_hits(hits)
            # doc_ids = [hit.docid for hit in hits]
            # doc_scores = [hit.score for hit in hits]

        except RuntimeError as e:
            if logger:
                logger.warning("RuntimeError: {}".format(e))
        except jnius.JavaException as e:
            if logger:
                logger.warning("{query} jnius.JavaException: {}".format(query_element, e))
            if 'maxClauseCount' in str(e):
                query = " ".join(query.split()[:950])
                hits = ranker.search(query, k=topk)
                doc_ids, doc_scores = parse_hits(hits)
            else:
                print(query, str(e))
                raise e
            # doc_ids = [hit.docid for hit in hits]
            # doc_scores = [hit.score for hit in hits]
        except Exception as e:
            print(query, str(e))
            raise e

        result_doc_ids.append(doc_ids)
        result_doc_scores.append(doc_scores)

    return result_doc_ids, result_doc_scores, result_query_id


class Anserini(Retriever):
    def __init__(self, name, num_threads, index_dir=None, k1=0.9, b=0.4, use_bigrams=False, stem_bigrams=False):
        super().__init__(name)

        self.num_threads = min(num_threads, int(multiprocessing.cpu_count()))

        # initialize a ranker per thread
        self.arguments = []
        for id in tqdm(range(self.num_threads)):
            ranker = SimpleSearcher(index_dir)
            ranker.set_bm25(k1, b)
            self.arguments.append(
                {
                    "id": id,
                    "ranker": ranker,
                    "use_bigrams": use_bigrams,
                    "stem_bigrams": stem_bigrams
                }
            )

    def fed_data(self, queries_data, topk, logger=None):

        chunked_queries = utils.chunk_it(queries_data, self.num_threads)

        for idx, arg in enumerate(self.arguments):
            arg["queries_data"] = chunked_queries[idx]
            arg["topk"] = topk
            arg["logger"] = logger

    def run(self):
        pool = ThreadPool(self.num_threads)
        results = pool.map(_get_predictions_thread, self.arguments)

        all_doc_id = []
        all_doc_scores = []
        all_query_id = []
        provenance = {}

        for x in results:
            i, s, q = x
            all_doc_id.extend(i)
            all_doc_scores.extend(s)
            all_query_id.extend(q)
            for query_id, doc_ids in zip(q, i):
                provenance[query_id] = []
                for d_id in doc_ids:
                    provenance[query_id].append({"wikipedia_id": str(d_id).strip()})

        pool.terminate()
        pool.join()

        return all_doc_id, all_doc_scores, all_query_id, provenance

