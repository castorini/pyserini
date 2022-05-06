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

from jnius import autoclass
import sys
import os

print('pyserini.index is deprecated, please use pyserini.index.lucene.')
args = sys.argv[1:]
# argument check
for i in range(len(args)):
    # Convert double hyphen args into single hyphen args for Java: e.g., --input becomes -input
    if args[i].startswith('--'):
        args[i] = args[i][1:]
    if args[i] == '-input':
        collection_dir = args[i+1]
        if os.path.isfile(collection_dir):
            raise ValueError('Argument -input should be a directory.')

JIndexCollection = autoclass('io.anserini.index.IndexCollection')
JIndexCollection.main(args)
