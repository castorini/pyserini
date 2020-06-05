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
from pyserini.fusion import reciprocal_rank_fusion
from ..trectools import TrecRun

parser = argparse.ArgumentParser(description='Perform various ways of fusion given a list of trec run files.')
parser.add_argument('--runs', type=str, nargs='+', default=[], required=True,
                    help='List of run files separated by space.')
parser.add_argument('--output', type=str, required=True, help="Path to resulting fused txt.")
parser.add_argument('--runtag', type=str, default="pyserini.fusion", help="Tag name of fused run.")
parser.add_argument('--rrf.k', dest='k', type=int, default=60, help="Parameter k needed for reciprocal rank fusion.")
parser.add_argument('--rrf.max_docs', dest='max_docs', type=int, default=1000,
                    required=False, help='Max number of documents per topic.')
args = parser.parse_args()

trec_runs = [TrecRun(filepath=path) for path in args.runs]
fused_run = reciprocal_rank_fusion(trec_runs, k=args.k, max_docs=args.max_docs)
fused_run.save_to_txt(args.output, tag=args.runtag)
