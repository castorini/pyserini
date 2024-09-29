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

# from ._geo_searcher import LuceneGeoSearcher
# from ._impact_searcher import JScoredDoc, LuceneImpactSearcher, SlimSearcher
#from ._searcher import JScoredDoc
# from ._hnsw_searcher import LuceneHnswDenseSearcher, LuceneFlatDenseSearcher
#
# __all__ = ['JScoredDoc',
#            'LuceneFusionSearcher',
#            'LuceneGeoSearcher',
#            'LuceneImpactSearcher',
#            'LuceneSearcher',
#            'LuceneHnswDenseSearcher',
#            'LuceneFlatDenseSearcher',
#            'SlimSearcher',
#            'LuceneSimilarities']

from pyserini.pyclass import autoclass

JQuery = autoclass('org.apache.lucene.search.Query')
JScoredDoc = autoclass('io.anserini.search.ScoredDoc')
JQueryGenerator = autoclass('io.anserini.search.query.QueryGenerator')
JBagOfWordsQueryGenerator = autoclass('io.anserini.search.query.BagOfWordsQueryGenerator')
JDisjunctionMaxQueryGenerator = autoclass('io.anserini.search.query.DisjunctionMaxQueryGenerator')
JCovid19QueryGenerator = autoclass('io.anserini.search.query.Covid19QueryGenerator')
