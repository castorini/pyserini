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

languages = [
    ['ar', 'arabic'],
    ['bn', 'bengali'],
    ['en', 'english'],
    ['fi', 'finnish'],
    ['id', 'indonesian'],
    ['ja', 'japanese'],
    ['ko', 'korean'],
    ['ru', 'russian'],
    ['sw', 'swahili'],
    ['te', 'telugu'],
    ['th', 'thai']
]

models = ['bm25', 'mdpr-split-pft-nq', 'mdpr-tied-pft-nq', 'mdpr-tied-pft-msmarco', 'mdpr-tied-pft-msmarco-ft-all']

html_display = {
    'bm25': 'BM25',
    'mdpr-split-pft-nq': 'mDPR (split encoders), pre-FT w/ NQ',
    'mdpr-tied-pft-nq': 'mDPR (tied encoders), pre-FT w/ NQ',
    'mdpr-tied-pft-msmarco': 'mDPR (tied encoders), pre-FT w/ MS MARCO',
    'mdpr-tied-pft-msmarco-ft-all': 'mDPR (tied encoders), pre-FT w/ MS MARCO, FT w/ all'
}

trec_eval_metric_definitions = {
    'MRR@100': '-c -M 100 -m recip_rank',
    'R@100': '-c -m recall.100',
}