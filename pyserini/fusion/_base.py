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

import pandas as pd
from ..trectools import TrecRun
from typing import List


def reciprocal_rank_fusion(trec_runs: List[TrecRun], k: int = 60, max_docs: int = None):
    """Given a list of TrecRun, return a new fused TrecRun using reciprocal rank fusion.

    Parameters
    ----------
    runs : List[TrecRun]
        List of TrecRun.
    k : int
        Parameters k for recriprocal rank calculation.
    max_docs: int
        Max number of documents per topics.

    Returns
    -------
    fused_run : TrecRun
        The fused TrecRun using reciprocal rank fusion.
    """

    if len(trec_runs) < 2:
        raise Exception('Fusion requires at least 2 runs.')

    fused_run, rows = TrecRun(), []

    for topic in TrecRun.get_all_topics_from_runs(trec_runs):
        doc_scores = dict()
        for run in trec_runs:
            docs = run.get_docs_by_topic(topic, max_docs)

            for _, doc in docs.iterrows():
                doc_scores[doc['docid']] = doc_scores.get(doc['docid'], 0.0) + 1 / (k + doc['rank'])

        for rank, (docid, score) in enumerate(sorted(iter(doc_scores.items()), key=lambda x: (-x[1], x[0]))[:max_docs], start=1):
            rows.append((topic, "Q0", docid, rank, score, "reciprocal_rank_fusion_k=%d" % k))

    df = pd.DataFrame(rows)
    df.columns = ["topic", "q0", "docid", "rank", "score", "tag"]
    fused_run.run_data = df.copy()

    return fused_run
