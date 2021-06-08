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

import argparse
from ._base import FusionMethod
from pyserini.fusion import average, interpolation, reciprocal_rank_fusion
from ..trectools import TrecRun


parser = argparse.ArgumentParser(description='Perform various ways of fusion given a list of trec run files.')
parser.add_argument('--runs', type=str, nargs='+', default=[], required=True,
                    help='List of run files separated by space.')
parser.add_argument('--output', type=str, required=True, help="Path to resulting fused txt.")
parser.add_argument('--runtag', type=str, default="pyserini.fusion", help="Tag name of fused run.")
parser.add_argument('--method', type=FusionMethod, default=FusionMethod.RRF, help="The fusion method to be used.")
parser.add_argument('--rrf.k', dest='rrf_k', type=int, default=60,
                    help="Parameter k needed for reciprocal rank fusion.")
parser.add_argument('--alpha', type=float, default=0.5, required=False, help='Alpha value used for interpolation.')
parser.add_argument('--depth', type=int, default=1000, required=False, help='Pool depth per topic.')
parser.add_argument('--k', type=int, default=1000, required=False, help='Number of documents to output per topic.')
parser.add_argument('--resort', action='store_true', help='We resort the Trec run files or not')
args = parser.parse_args()

trec_runs = [TrecRun(filepath=path,resort=args.resort) for path in args.runs]

fused_run = None
if args.method == FusionMethod.RRF:
    fused_run = reciprocal_rank_fusion(trec_runs, rrf_k=args.rrf_k, depth=args.depth, k=args.k)
elif args.method == FusionMethod.INTERPOLATION:
    fused_run = interpolation(trec_runs, alpha=args.alpha, depth=args.depth, k=args.k)
elif args.method == FusionMethod.AVERAGE:
    fused_run = average(trec_runs, depth=args.depth, k=args.k)
else:
    raise NotImplementedError(f'Fusion method {args.method} not implemented.')

fused_run.save_to_txt(args.output, tag=args.runtag)
