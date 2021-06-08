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

EVALUATION_INFO = {
    "trec_eval": {
        "description": "TREC evaluation script",
        "urls": [
            "https://search.maven.org/remotecontent?filepath=uk/ac/gla/dcs/terrierteam/jtreceval/0.0.5/jtreceval-0.0.5-jar-with-dependencies.jar",
        ],
    },
    "msmarco_passage_eval": {
        "description": "MSMARCO-passage evaluation script",
        "urls": [
            "https://raw.githubusercontent.com/castorini/anserini-tools/master/scripts/msmarco/msmarco_passage_eval.py",
        ],
    },
    "msmarco_doc_eval": {
        "description": "MSMARCO-doc evaluation script",
        "urls": [
            "https://raw.githubusercontent.com/castorini/anserini-tools/master/scripts/msmarco/msmarco_doc_eval.py",
        ],
    }

}
