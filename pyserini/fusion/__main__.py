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

parser = argparse.ArgumentParser(description='Create a input schema')
parser.add_argument('--runs', type=str, nargs='+', default=[], required=True, help='A list of run files.')
parser.add_argument('--output', type=str, required=True, help="Path to Lucene index.")
parser.add_argument('--tag', type=str, default="pyserini.fusion", help="Tag name of fused run.")
args = parser.parse_args()

trec_runs = []

for path in args.runs:
    trec_runs.append(TrecRun(filepath=path))

fused_run = reciprocal_rank_fusion(trec_runs)
fused_run.save_to_txt(args.output, tag=args.tag)
