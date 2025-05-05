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

from pyserini.analysis import Analyzer, get_lucene_analyzer
import argparse
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--corpus-file", type=str)
    parser.add_argument("--query-file", type=str)
    parser.add_argument("--output-corpus", type=str)
    parser.add_argument("--output-query", type=str)
    args = parser.parse_args()

    analyzer = Analyzer(get_lucene_analyzer())
    with open(args.output_corpus, 'w') as out:
        with open(args.corpus_file, 'r') as f:
            for line in f:
                l = json.loads(line)
                s = json.dumps({'id': l['_id'], 'contents': ' '.join(analyzer.analyze(l['title'] + ' ' + l['text']))})
                out.write(s + '\n')

    with open(args.output_query, 'w') as out:
        with open(args.query_file, 'r') as f:
            for line in f:
                l = json.loads(line)
                s = json.dumps({'id': l['_id'], 'contents': ' '.join(analyzer.analyze(l['text']))})
                out.write(s + '\n')