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

import argparse
import os

import numpy as np
from tqdm import tqdm

from pyserini.dsearch import QueryEncoder, SimpleDenseSearcher
from pyserini.search import SimpleSearcher, get_topics
from pyserini.hsearch import HybridSearcher

# Fixes this error: "OMP: Error #15: Initializing libomp.a, but found libomp.dylib already initialized."
# https://stackoverflow.com/questions/53014306/error-15-initializing-libiomp5-dylib-but-found-libiomp5-dylib-already-initial
os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

parser = argparse.ArgumentParser(description='Conduct a hybrid search on dense+sparse indexes.')
parser.add_argument('--dindex', type=str, metavar='path to dense index or index name', required=True,
                    help="Path to Faiss index or name of prebuilt index.")
parser.add_argument('--sindex', type=str, metavar='path to sparse index or index name', required=True,
                    help="Path to Anserini index or name of prebuilt index.")
parser.add_argument('--topics', type=str, metavar='topic_name', required=True,
                    help="Name of topics. Available: msmarco_passage_dev_subset.")
parser.add_argument('--encoded-queries', type=str, metavar='path to query embedding or query name', required=True,
                    help="Path to query embedding or name of pre encoded queries")
parser.add_argument('--hits', type=int, metavar='num', required=False, default=1000, help="Number of hits.")
parser.add_argument('--alpha', type=float, metavar='num', required=False, default=0.1, help="alpha for hybrid search")
parser.add_argument('--msmarco',  action='store_true', default=False, help="Output in MS MARCO format.")
parser.add_argument('--output', type=str, metavar='path', required=True, help="Path to output file.")
args = parser.parse_args()

topics = get_topics(args.topics)

if os.path.exists(args.encoded_queries):
    # create query encoder from query embedding directory
    query_encoder = QueryEncoder(args.encoded_queries)
else:
    # create query encoder from pre encoded query name
    query_encoder = QueryEncoder.load_encoded_queries(args.encoded_queries)

if not query_encoder:
    exit()

if os.path.exists(args.dindex):
    # create searcher from index directory
    dsearcher = SimpleDenseSearcher(args.dindex)
else:
    # create searcher from prebuilt index name
    dsearcher = SimpleDenseSearcher.from_prebuilt_index(args.dindex)

if not dsearcher:
    exit()

if os.path.exists(args.sindex):
    # create searcher from index directory
    ssearcher = SimpleSearcher(args.sindex)
else:
    # create searcher from prebuilt index name
    ssearcher = SimpleSearcher.from_prebuilt_index(args.sindex)

if not ssearcher:
    exit()

hsearcher = HybridSearcher(dsearcher, query_encoder, ssearcher)
if not hsearcher:
    exit()

# invalid topics name
if topics == {}:
    print(f'Topic {args.topics} Not Found')
    exit()

# build output path
output_path = args.output

print(f'Running {args.topics} topics, saving to {output_path}...')
tag = 'hybrid'

with open(output_path, 'w') as target_file:
    for topic in tqdm(sorted(topics.keys())):
        search = topics[topic].get('title').strip()
        hits = hsearcher.search(search, k=args.hits, alpha=args.alpha)
        docids = [hit.docid.strip() for hit in hits]
        scores = [hit.score for hit in hits]

        if args.msmarco:
            for i, docid in enumerate(docids):
                if i < args.hits:
                    target_file.write(f'{topic}\t{docid}\t{i + 1}\n')
        else:
            for i, (docid, score) in enumerate(zip(docids, scores)):
                if i < args.hits:
                    target_file.write(f'{topic} Q0 {docid} {i + 1} {score:.6f} {tag}\n')
