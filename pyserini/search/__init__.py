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

from ._base import JQuery, JQueryGenerator, JDisjunctionMaxQueryGenerator, get_topics,\
    get_topics_with_reader, get_qrels_file, get_qrels
from .lucene import JLuceneSearcherResult, LuceneSimilarities, LuceneFusionSearcher, LuceneSearcher
from .lucene import JImpactSearcherResult, LuceneImpactSearcher
from ._deprecated import SimpleSearcher, ImpactSearcher, SimpleFusionSearcher

from .faiss import DenseSearchResult, PRFDenseSearchResult, FaissSearcher, BinaryDenseSearcher, QueryEncoder, \
    DprQueryEncoder, BprQueryEncoder, DkrrDprQueryEncoder, TctColBertQueryEncoder, AnceQueryEncoder, AutoQueryEncoder
from .faiss import AnceEncoder
from .faiss import DenseVectorAveragePrf, DenseVectorRocchioPrf, DenseVectorAncePrf


__all__ = ['JQuery',
           'LuceneSimilarities',
           'LuceneFusionSearcher',
           'LuceneSearcher',
           'JLuceneSearcherResult',
           'LuceneImpactSearcher',
           'JImpactSearcherResult',
           'JDisjunctionMaxQueryGenerator',
           'JQueryGenerator',
           'get_topics',
           'get_topics_with_reader',
           'get_qrels_file',
           'get_qrels',
           'SimpleSearcher',
           'ImpactSearcher',
           'SimpleFusionSearcher',
           'DenseSearchResult',
           'PRFDenseSearchResult',
           'FaissSearcher',
           'BinaryDenseSearcher',
           'QueryEncoder',
           'DprQueryEncoder',
           'BprQueryEncoder',
           'DkrrDprQueryEncoder',
           'TctColBertQueryEncoder',
           'AnceEncoder',
           'AnceQueryEncoder',
           'AutoQueryEncoder',
           'DenseVectorAveragePrf',
           'DenseVectorRocchioPrf',
           'DenseVectorAncePrf']

