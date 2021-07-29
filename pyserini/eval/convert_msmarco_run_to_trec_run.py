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


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert an MS MARCO run file to a TREC run file.')
    parser.add_argument('--input', required=True, default='', help='Input MS MARCO run file.')
    parser.add_argument('--output', required=True, default='', help='Output TREC run file.')

    args = parser.parse_args()

    with open(args.output, 'w') as fout:
        for line in open(args.input):
            query_id, doc_id, rank = line.strip().split('\t')
            score = 1.0 / int(rank)
            fout.write('{} Q0 {} {} {} anserini\n'.format(
                query_id, doc_id, rank, score))

    print('Done!')
