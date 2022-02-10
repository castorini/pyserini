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

from pyserini.search.lucene import LuceneImpactSearcher, LuceneSearcher, LuceneFusionSearcher


class SimpleSearcher(LuceneSearcher):
    def __new__(cls, *args, **kwargs):
        print('SimpleSearcher class has been deprecated, '
              'please use LuceneSearcher from pyserini.search.lucene instead')
        return super().__new__(cls)


class ImpactSearcher(LuceneImpactSearcher):
    def __new__(cls, *args, **kwargs):
        print('ImpactSearcher class has been deprecated, '
              'please use LuceneImpactSearcher from pyserini.search.lucene instead')
        return super().__new__(cls)


class SimpleFusionSearcher(LuceneFusionSearcher):
    def __new__(cls, *args, **kwargs):
        print('SimpleFusionSearcher class has been deprecated, '
              'please use LuceneFusionSearcher from pyserini.search.lucene instead')
        return super().__new__(cls)
