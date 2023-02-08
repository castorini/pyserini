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

"""
This module provides Pyserini's Python search interface to Anserini. The main entry point is the ``LuceneSearcher``
class, which wraps the Java class with the same name in Anserini.
"""

import logging
import os

from pyserini.util import get_cache_home
from pyserini.pyclass import autoclass

logger = logging.getLogger(__name__)

# Wrappers around Lucene classes
JQuery = autoclass('org.apache.lucene.search.Query')

# Wrappers around Anserini classes
JQrels = autoclass('io.anserini.eval.Qrels')
JRelevanceJudgments = autoclass('io.anserini.eval.RelevanceJudgments')
JTopicReader = autoclass('io.anserini.search.topicreader.TopicReader')
JTopics = autoclass('io.anserini.search.topicreader.Topics')
JQueryGenerator = autoclass('io.anserini.search.query.QueryGenerator')
JBagOfWordsQueryGenerator = autoclass('io.anserini.search.query.BagOfWordsQueryGenerator')
JDisjunctionMaxQueryGenerator = autoclass('io.anserini.search.query.DisjunctionMaxQueryGenerator')
JCovid19QueryGenerator = autoclass('io.anserini.search.query.Covid19QueryGenerator')

topics_mapping = {
    'trec1-adhoc': JTopics.TREC1_ADHOC,
    'trec2-adhoc': JTopics.TREC2_ADHOC,
    'trec3-adhoc': JTopics.TREC3_ADHOC,
    'robust04': JTopics.ROBUST04,
    'robust05': JTopics.ROBUST05,
    'core17': JTopics.CORE17,
    'core18': JTopics.CORE18,
    'wt10g': JTopics.WT10G,
    'trec2004-terabyte': JTopics.TREC2004_TERABYTE,
    'trec2005-terabyte': JTopics.TREC2005_TERABYTE,
    'trec2006-terabyte': JTopics.TREC2006_TERABYTE,
    'trec2007-million-query': JTopics.TREC2007_MILLION_QUERY,
    'trec2008-million-query': JTopics.TREC2008_MILLION_QUERY,
    'trec2009-million-query': JTopics.TREC2009_MILLION_QUERY,
    'trec2010-web': JTopics.TREC2010_WEB,
    'trec2011-web': JTopics.TREC2011_WEB,
    'trec2012-web': JTopics.TREC2012_WEB,
    'trec2013-web': JTopics.TREC2013_WEB,
    'trec2014-web': JTopics.TREC2014_WEB,
    'mb11': JTopics.MB11,
    'mb12': JTopics.MB12,
    'mb13': JTopics.MB13,
    'mb14': JTopics.MB14,
    'car17v1.5-benchmarkY1test': JTopics.CAR17V15_BENCHMARK_Y1_TEST,
    'car17v2.0-benchmarkY1test': JTopics.CAR17V20_BENCHMARK_Y1_TEST,
    'dl19-doc': JTopics.TREC2019_DL_DOC,
    'dl19-doc-unicoil': JTopics.TREC2019_DL_DOC_UNICOIL,
    'dl19-doc-unicoil-noexp': JTopics.TREC2019_DL_DOC_UNICOIL_NOEXP,
    'dl19-passage': JTopics.TREC2019_DL_PASSAGE,
    'dl19-passage-unicoil': JTopics.TREC2019_DL_PASSAGE_UNICOIL,
    'dl19-passage-unicoil-noexp': JTopics.TREC2019_DL_PASSAGE_UNICOIL_NOEXP,
    'dl20': JTopics.TREC2020_DL,
    'dl20-unicoil': JTopics.TREC2020_DL_UNICOIL,
    'dl20-unicoil-noexp': JTopics.TREC2020_DL_UNICOIL_NOEXP,
    'dl21': JTopics.TREC2021_DL,
    'dl21-unicoil': JTopics.TREC2021_DL_UNICOIL,
    'dl21-unicoil-noexp': JTopics.TREC2021_DL_UNICOIL_NOEXP,
    'msmarco-doc-dev': JTopics.MSMARCO_DOC_DEV,
    'msmarco-doc-dev-unicoil': JTopics.MSMARCO_DOC_DEV_UNICOIL,
    'msmarco-doc-dev-unicoil-noexp': JTopics.MSMARCO_DOC_DEV_UNICOIL_NOEXP,
    'msmarco-doc-test': JTopics.MSMARCO_DOC_TEST,
    'msmarco-passage-dev-subset': JTopics.MSMARCO_PASSAGE_DEV_SUBSET,
    'msmarco-passage-dev-subset-deepimpact': JTopics.MSMARCO_PASSAGE_DEV_SUBSET_DEEPIMPACT,
    'msmarco-passage-dev-subset-unicoil': JTopics.MSMARCO_PASSAGE_DEV_SUBSET_UNICOIL,
    'msmarco-passage-dev-subset-unicoil-noexp': JTopics.MSMARCO_PASSAGE_DEV_SUBSET_UNICOIL_NOEXP,
    'msmarco-passage-dev-subset-unicoil-tilde': JTopics.MSMARCO_PASSAGE_DEV_SUBSET_UNICOIL_TILDE,
    'msmarco-passage-dev-subset-distill-splade-max': JTopics.MSMARCO_PASSAGE_DEV_SUBSET_DISTILL_SPLADE_MAX,
    'msmarco-passage-test-subset': JTopics.MSMARCO_PASSAGE_TEST_SUBSET,
    'msmarco-v2-doc-dev': JTopics.MSMARCO_V2_DOC_DEV,
    'msmarco-v2-doc-dev-unicoil': JTopics.MSMARCO_V2_DOC_DEV_UNICOIL,
    'msmarco-v2-doc-dev-unicoil-noexp': JTopics.MSMARCO_V2_DOC_DEV_UNICOIL_NOEXP,
    'msmarco-v2-doc-dev2': JTopics.MSMARCO_V2_DOC_DEV2,
    'msmarco-v2-doc-dev2-unicoil': JTopics.MSMARCO_V2_DOC_DEV2_UNICOIL,
    'msmarco-v2-doc-dev2-unicoil-noexp': JTopics.MSMARCO_V2_DOC_DEV2_UNICOIL_NOEXP,
    'msmarco-v2-passage-dev': JTopics.MSMARCO_V2_PASSAGE_DEV,
    'msmarco-v2-passage-dev-unicoil': JTopics.MSMARCO_V2_PASSAGE_DEV_UNICOIL,
    'msmarco-v2-passage-dev-unicoil-noexp': JTopics.MSMARCO_V2_PASSAGE_DEV_UNICOIL_NOEXP,
    'msmarco-v2-passage-dev2': JTopics.MSMARCO_V2_PASSAGE_DEV2,
    'msmarco-v2-passage-dev2-unicoil': JTopics.MSMARCO_V2_PASSAGE_DEV2_UNICOIL,
    'msmarco-v2-passage-dev2-unicoil-noexp': JTopics.MSMARCO_V2_PASSAGE_DEV2_UNICOIL_NOEXP,
    'ntcir8-zh': JTopics.NTCIR8_ZH,
    'clef2006-fr': JTopics.CLEF2006_FR,
    'trec2002-ar': JTopics.TREC2002_AR,
    'fire2012-bn': JTopics.FIRE2012_BN,
    'fire2012-hi': JTopics.FIRE2012_HI,
    'fire2012-en': JTopics.FIRE2012_EN,
    'covid-round1': JTopics.COVID_ROUND1,
    'covid-round1-udel': JTopics.COVID_ROUND1_UDEL,
    'covid-round2': JTopics.COVID_ROUND2,
    'covid-round2-udel': JTopics.COVID_ROUND2_UDEL,
    'covid-round3': JTopics.COVID_ROUND3,
    'covid-round3-udel': JTopics.COVID_ROUND3_UDEL,
    'covid-round4': JTopics.COVID_ROUND4,
    'covid-round4-udel': JTopics.COVID_ROUND4_UDEL,
    'covid-round5': JTopics.COVID_ROUND5,
    'covid-round5-udel': JTopics.COVID_ROUND5_UDEL,
    'trec2018-bl': JTopics.TREC2018_BL,
    'trec2019-bl': JTopics.TREC2019_BL,
    'trec2020-bl': JTopics.TREC2020_BL,
    'epidemic-qa-expert-prelim': JTopics.EPIDEMIC_QA_EXPERT_PRELIM,
    'epidemic-qa-consumer-prelim': JTopics.EPIDEMIC_QA_CONSUMER_PRELIM,
    'dpr-nq-dev': JTopics.DPR_NQ_DEV,
    'dpr-nq-test': JTopics.DPR_NQ_TEST,
    'dpr-trivia-dev': JTopics.DPR_TRIVIA_DEV,
    'dpr-trivia-test': JTopics.DPR_TRIVIA_TEST,
    'dpr-wq-test': JTopics.DPR_WQ_TEST,
    'dpr-squad-test': JTopics.DPR_SQUAD_TEST,
    'dpr-curated-test': JTopics.DPR_CURATED_TEST,
    'dpr-trivia-test-gar-t5-answers': JTopics.DPR_TRIVIA_TEST_GART5_ANSWERS,
    'dpr-trivia-test-gar-t5-titles': JTopics.DPR_TRIVIA_TEST_GART5_TITLES,
    'dpr-trivia-test-gar-t5-sentences': JTopics.DPR_TRIVIA_TEST_GART5_SENTENCES,
    'dpr-trivia-test-gar-t5-all': JTopics.DPR_TRIVIA_TEST_GART5_ALL,
    'nq-test-gar-t5-answers': JTopics.NQ_TEST_GART5_ANSWERS,
    'nq-test-gar-t5-titles': JTopics.NQ_TEST_GART5_TITLES,
    'nq-test-gar-t5-sentences': JTopics.NQ_TEST_GART5_SENTENCES,
    'nq-test-gar-t5-all': JTopics.NQ_TEST_GART5_ALL,
    'nq-dev': JTopics.NQ_DEV,
    'nq-test': JTopics.NQ_TEST,
    'mrtydi-v1.1-arabic-train': JTopics.MRTYDI_V11_AR_TRAIN,
    'mrtydi-v1.1-arabic-dev': JTopics.MRTYDI_V11_AR_DEV,
    'mrtydi-v1.1-arabic-test': JTopics.MRTYDI_V11_AR_TEST,
    'mrtydi-v1.1-bengali-train': JTopics.MRTYDI_V11_BN_TRAIN,
    'mrtydi-v1.1-bengali-dev': JTopics.MRTYDI_V11_BN_DEV,
    'mrtydi-v1.1-bengali-test': JTopics.MRTYDI_V11_BN_TEST,
    'mrtydi-v1.1-english-train': JTopics.MRTYDI_V11_EN_TRAIN,
    'mrtydi-v1.1-english-dev': JTopics.MRTYDI_V11_EN_DEV,
    'mrtydi-v1.1-english-test': JTopics.MRTYDI_V11_EN_TEST,
    'mrtydi-v1.1-finnish-train': JTopics.MRTYDI_V11_FI_TRAIN,
    'mrtydi-v1.1-finnish-dev': JTopics.MRTYDI_V11_FI_DEV,
    'mrtydi-v1.1-finnish-test': JTopics.MRTYDI_V11_FI_TEST,
    'mrtydi-v1.1-indonesian-train': JTopics.MRTYDI_V11_ID_TRAIN,
    'mrtydi-v1.1-indonesian-dev': JTopics.MRTYDI_V11_ID_DEV,
    'mrtydi-v1.1-indonesian-test': JTopics.MRTYDI_V11_ID_TEST,
    'mrtydi-v1.1-japanese-train': JTopics.MRTYDI_V11_JA_TRAIN,
    'mrtydi-v1.1-japanese-dev': JTopics.MRTYDI_V11_JA_DEV,
    'mrtydi-v1.1-japanese-test': JTopics.MRTYDI_V11_JA_TEST,
    'mrtydi-v1.1-korean-train': JTopics.MRTYDI_V11_KO_TRAIN,
    'mrtydi-v1.1-korean-dev': JTopics.MRTYDI_V11_KO_DEV,
    'mrtydi-v1.1-korean-test': JTopics.MRTYDI_V11_KO_TEST,
    'mrtydi-v1.1-russian-train': JTopics.MRTYDI_V11_RU_TRAIN,
    'mrtydi-v1.1-russian-dev': JTopics.MRTYDI_V11_RU_DEV,
    'mrtydi-v1.1-russian-test': JTopics.MRTYDI_V11_RU_TEST,
    'mrtydi-v1.1-swahili-train': JTopics.MRTYDI_V11_SW_TRAIN,
    'mrtydi-v1.1-swahili-dev': JTopics.MRTYDI_V11_SW_DEV,
    'mrtydi-v1.1-swahili-test': JTopics.MRTYDI_V11_SW_TEST,
    'mrtydi-v1.1-telugu-train': JTopics.MRTYDI_V11_TE_TRAIN,
    'mrtydi-v1.1-telugu-dev': JTopics.MRTYDI_V11_TE_DEV,
    'mrtydi-v1.1-telugu-test': JTopics.MRTYDI_V11_TE_TEST,
    'mrtydi-v1.1-thai-train': JTopics.MRTYDI_V11_TH_TRAIN,
    'mrtydi-v1.1-thai-dev': JTopics.MRTYDI_V11_TH_DEV,
    'mrtydi-v1.1-thai-test': JTopics.MRTYDI_V11_TH_TEST,
    'beir-v1.0.0-trec-covid-test': JTopics.BEIR_V1_0_0_TREC_COVID_TEST,
    'beir-v1.0.0-bioasq-test': JTopics.BEIR_V1_0_0_BIOASQ_TEST,
    'beir-v1.0.0-nfcorpus-test': JTopics.BEIR_V1_0_0_NFCORPUS_TEST,
    'beir-v1.0.0-nq-test': JTopics.BEIR_V1_0_0_NQ_TEST,
    'beir-v1.0.0-hotpotqa-test': JTopics.BEIR_V1_0_0_HOTPOTQA_TEST,
    'beir-v1.0.0-fiqa-test': JTopics.BEIR_V1_0_0_FIQA_TEST,
    'beir-v1.0.0-signal1m-test': JTopics.BEIR_V1_0_0_SIGNAL1M_TEST,
    'beir-v1.0.0-trec-news-test': JTopics.BEIR_V1_0_0_TREC_NEWS_TEST,
    'beir-v1.0.0-robust04-test': JTopics.BEIR_V1_0_0_ROBUST04_TEST,
    'beir-v1.0.0-arguana-test': JTopics.BEIR_V1_0_0_ARGUANA_TEST,
    'beir-v1.0.0-webis-touche2020-test': JTopics.BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST,
    'beir-v1.0.0-cqadupstack-android-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST,
    'beir-v1.0.0-cqadupstack-english-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST,
    'beir-v1.0.0-cqadupstack-gaming-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST,
    'beir-v1.0.0-cqadupstack-gis-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_GIS_TEST,
    'beir-v1.0.0-cqadupstack-mathematica-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST,
    'beir-v1.0.0-cqadupstack-physics-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST,
    'beir-v1.0.0-cqadupstack-programmers-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST,
    'beir-v1.0.0-cqadupstack-stats-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_STATS_TEST,
    'beir-v1.0.0-cqadupstack-tex-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_TEX_TEST,
    'beir-v1.0.0-cqadupstack-unix-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST,
    'beir-v1.0.0-cqadupstack-webmasters-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST,
    'beir-v1.0.0-cqadupstack-wordpress-test': JTopics.BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST,
    'beir-v1.0.0-quora-test': JTopics.BEIR_V1_0_0_QUORA_TEST,
    'beir-v1.0.0-dbpedia-entity-test': JTopics.BEIR_V1_0_0_DBPEDIA_ENTITY_TEST,
    'beir-v1.0.0-scidocs-test': JTopics.BEIR_V1_0_0_SCIDOCS_TEST,
    'beir-v1.0.0-fever-test': JTopics.BEIR_V1_0_0_FEVER_TEST,
    'beir-v1.0.0-climate-fever-test': JTopics.BEIR_V1_0_0_CLIMATE_FEVER_TEST,
    'beir-v1.0.0-scifact-test': JTopics.BEIR_V1_0_0_SCIFACT_TEST,
    'beir-v1.0.0-trec-covid-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_TREC_COVID_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-bioasq-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_BIOASQ_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-nfcorpus-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_NFCORPUS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-nq-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_NQ_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-hotpotqa-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_HOTPOTQA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-fiqa-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_FIQA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-signal1m-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_SIGNAL1M_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-trec-news-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_TREC_NEWS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-robust04-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_ROBUST04_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-arguana-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_ARGUANA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-webis-touche2020-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-android-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-english-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-gaming-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-gis-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_GIS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-mathematica-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-physics-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-programmers-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-stats-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_STATS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-tex-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_TEX_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-unix-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-webmasters-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-cqadupstack-wordpress-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-quora-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_QUORA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-dbpedia-entity-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_DBPEDIA_ENTITY_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-scidocs-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_SCIDOCS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-fever-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_FEVER_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-climate-fever-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_CLIMATE_FEVER_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'beir-v1.0.0-scifact-test-splade_distil_cocodenser_medium': JTopics.BEIR_V1_0_0_SCIFACT_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM,
    'hc4-v1.0-fa-dev-title': JTopics.HC4_V1_0_FA_DEV_TITLE,
    'hc4-v1.0-fa-dev-desc': JTopics.HC4_V1_0_FA_DEV_DESC,
    'hc4-v1.0-fa-dev-desc-title': JTopics.HC4_V1_0_FA_DEV_DESC_TITLE,
    'hc4-v1.0-fa-test-title': JTopics.HC4_V1_0_FA_TEST_TITLE,
    'hc4-v1.0-fa-test-desc': JTopics.HC4_V1_0_FA_TEST_DESC,
    'hc4-v1.0-fa-test-desc-title': JTopics.HC4_V1_0_FA_TEST_DESC_TITLE,
    'hc4-v1.0-fa-en-test-title': JTopics.HC4_V1_0_FA_EN_TEST_TITLE,
    'hc4-v1.0-fa-en-test-desc': JTopics.HC4_V1_0_FA_EN_TEST_DESC,
    'hc4-v1.0-fa-en-test-desc-title': JTopics.HC4_V1_0_FA_EN_TEST_DESC_TITLE,
    'hc4-v1.0-ru-dev-title': JTopics.HC4_V1_0_RU_DEV_TITLE,
    'hc4-v1.0-ru-dev-desc': JTopics.HC4_V1_0_RU_DEV_DESC,
    'hc4-v1.0-ru-dev-desc-title': JTopics.HC4_V1_0_RU_DEV_DESC_TITLE,
    'hc4-v1.0-ru-test-title': JTopics.HC4_V1_0_RU_TEST_TITLE,
    'hc4-v1.0-ru-test-desc': JTopics.HC4_V1_0_RU_TEST_DESC,
    'hc4-v1.0-ru-test-desc-title': JTopics.HC4_V1_0_RU_TEST_DESC_TITLE,
    'hc4-v1.0-ru-en-test-title': JTopics.HC4_V1_0_RU_EN_TEST_TITLE,
    'hc4-v1.0-ru-en-test-desc': JTopics.HC4_V1_0_RU_EN_TEST_DESC,
    'hc4-v1.0-ru-en-test-desc-title': JTopics.HC4_V1_0_RU_EN_TEST_DESC_TITLE,
    'hc4-v1.0-zh-dev-title': JTopics.HC4_V1_0_ZH_DEV_TITLE,
    'hc4-v1.0-zh-dev-desc': JTopics.HC4_V1_0_ZH_DEV_DESC,
    'hc4-v1.0-zh-dev-desc-title': JTopics.HC4_V1_0_ZH_DEV_DESC_TITLE,
    'hc4-v1.0-zh-test-title': JTopics.HC4_V1_0_ZH_TEST_TITLE,
    'hc4-v1.0-zh-test-desc': JTopics.HC4_V1_0_ZH_TEST_DESC,
    'hc4-v1.0-zh-test-desc-title': JTopics.HC4_V1_0_ZH_TEST_DESC_TITLE,
    'hc4-v1.0-zh-en-test-title': JTopics.HC4_V1_0_ZH_EN_TEST_TITLE,
    'hc4-v1.0-zh-en-test-desc': JTopics.HC4_V1_0_ZH_EN_TEST_DESC,
    'hc4-v1.0-zh-en-test-desc-title': JTopics.HC4_V1_0_ZH_EN_TEST_DESC_TITLE,
    # NeuCLIR 2022 topics
    'neuclir22-en-title':         JTopics.NEUCLIR22_EN_TITLE,
    'neuclir22-en-desc':          JTopics.NEUCLIR22_EN_DESC,
    'neuclir22-en-desc-title':    JTopics.NEUCLIR22_EN_DESC_TITLE,
    'neuclir22-fa-ht-title':      JTopics.NEUCLIR22_FA_HT_TITLE,
    'neuclir22-fa-ht-desc':       JTopics.NEUCLIR22_FA_HT_DESC,
    'neuclir22-fa-ht-desc-title': JTopics.NEUCLIR22_FA_HT_DESC_TITLE,
    'neuclir22-fa-mt-title':      JTopics.NEUCLIR22_FA_MT_TITLE,
    'neuclir22-fa-mt-desc':       JTopics.NEUCLIR22_FA_MT_DESC,
    'neuclir22-fa-mt-desc-title': JTopics.NEUCLIR22_FA_MT_DESC_TITLE,
    'neuclir22-ru-ht-title':      JTopics.NEUCLIR22_RU_HT_TITLE,
    'neuclir22-ru-ht-desc':       JTopics.NEUCLIR22_RU_HT_DESC,
    'neuclir22-ru-ht-desc-title': JTopics.NEUCLIR22_RU_HT_DESC_TITLE,
    'neuclir22-ru-mt-title':      JTopics.NEUCLIR22_RU_MT_TITLE,
    'neuclir22-ru-mt-desc':       JTopics.NEUCLIR22_RU_MT_DESC,
    'neuclir22-ru-mt-desc-title': JTopics.NEUCLIR22_RU_MT_DESC_TITLE,
    'neuclir22-zh-ht-title':      JTopics.NEUCLIR22_ZH_HT_TITLE,
    'neuclir22-zh-ht-desc':       JTopics.NEUCLIR22_ZH_HT_DESC,
    'neuclir22-zh-ht-desc-title': JTopics.NEUCLIR22_ZH_HT_DESC_TITLE,
    'neuclir22-zh-mt-title':      JTopics.NEUCLIR22_ZH_MT_TITLE,
    'neuclir22-zh-mt-desc':       JTopics.NEUCLIR22_ZH_MT_DESC,
    'neuclir22-zh-mt-desc-title': JTopics.NEUCLIR22_ZH_MT_DESC_TITLE,
    # MIRACL topics
    'miracl-v1.0-ar-dev': JTopics.MIRACL_V10_AR_DEV,
    'miracl-v1.0-bn-dev': JTopics.MIRACL_V10_BN_DEV,
    'miracl-v1.0-en-dev': JTopics.MIRACL_V10_EN_DEV,
    'miracl-v1.0-es-dev': JTopics.MIRACL_V10_ES_DEV,
    'miracl-v1.0-fa-dev': JTopics.MIRACL_V10_FA_DEV,
    'miracl-v1.0-fi-dev': JTopics.MIRACL_V10_FI_DEV,
    'miracl-v1.0-fr-dev': JTopics.MIRACL_V10_FR_DEV,
    'miracl-v1.0-hi-dev': JTopics.MIRACL_V10_HI_DEV,
    'miracl-v1.0-id-dev': JTopics.MIRACL_V10_ID_DEV,
    'miracl-v1.0-ja-dev': JTopics.MIRACL_V10_JA_DEV,
    'miracl-v1.0-ko-dev': JTopics.MIRACL_V10_KO_DEV,
    'miracl-v1.0-ru-dev': JTopics.MIRACL_V10_RU_DEV,
    'miracl-v1.0-sw-dev': JTopics.MIRACL_V10_SW_DEV,
    'miracl-v1.0-te-dev': JTopics.MIRACL_V10_TE_DEV,
    'miracl-v1.0-th-dev': JTopics.MIRACL_V10_TH_DEV,
    'miracl-v1.0-zh-dev': JTopics.MIRACL_V10_ZH_DEV,
    'miracl-v1.0-de-dev': JTopics.MIRACL_V10_DE_DEV,
    'miracl-v1.0-yo-dev': JTopics.MIRACL_V10_YO_DEV,
}

qrels_mapping = {
    'trec1-adhoc': JQrels.TREC1_ADHOC,
    'trec2-adhoc': JQrels.TREC2_ADHOC,
    'trec3-adhoc': JQrels.TREC3_ADHOC,
    'robust04': JQrels.ROBUST04,
    'robust05': JQrels.ROBUST05,
    'core17': JQrels.CORE17,
    'core18': JQrels.CORE18,
    'wt10g': JQrels.WT10G,
    'trec2004-terabyte': JQrels.TREC2004_TERABYTE,
    'trec2005-terabyte': JQrels.TREC2005_TERABYTE,
    'trec2006-terabyte': JQrels.TREC2006_TERABYTE,
    'trec2011-web': JQrels.TREC2011_WEB,
    'trec2012-web': JQrels.TREC2012_WEB,
    'trec2013-web': JQrels.TREC2013_WEB,
    'trec2014-web': JQrels.TREC2014_WEB,
    'mb11': JQrels.MB11,
    'mb12': JQrels.MB12,
    'mb13': JQrels.MB13,
    'mb14': JQrels.MB14,
    'car17v1.5-benchmarkY1test': JQrels.CAR17V15_BENCHMARK_Y1_TEST,
    'car17v2.0-benchmarkY1test': JQrels.CAR17V20_BENCHMARK_Y1_TEST,
    'dl19-doc': JQrels.TREC2019_DL_DOC,
    'dl19-passage': JQrels.TREC2019_DL_PASSAGE,
    'dl20-doc': JQrels.TREC2020_DL_DOC,
    'dl20-passage': JQrels.TREC2020_DL_PASSAGE,
    'dl21-doc': JQrels.TREC2021_DL_DOC,
    'dl21-passage': JQrels.TREC2021_DL_PASSAGE,
    'msmarco-doc-dev': JQrels.MSMARCO_DOC_DEV,
    'msmarco-passage-dev-subset': JQrels.MSMARCO_PASSAGE_DEV_SUBSET,
    'msmarco-v2-doc-dev': JQrels.MSMARCO_V2_DOC_DEV,
    'msmarco-v2-doc-dev2': JQrels.MSMARCO_V2_DOC_DEV2,
    'msmarco-v2-passage-dev': JQrels.MSMARCO_V2_PASSAGE_DEV,
    'msmarco-v2-passage-dev2': JQrels.MSMARCO_V2_PASSAGE_DEV2,
    'ntcir8-zh': JQrels.NTCIR8_ZH,
    'clef2006-fr': JQrels.CLEF2006_FR,
    'trec2002-ar': JQrels.TREC2002_AR,
    'fire2012-bn': JQrels.FIRE2012_BN,
    'fire2012-hi': JQrels.FIRE2012_HI,
    'fire2012-en': JQrels.FIRE2012_EN,
    'covid-complete': JQrels.COVID_COMPLETE,
    'covid-round1': JQrels.COVID_ROUND1,
    'covid-round2': JQrels.COVID_ROUND2,
    'covid-round3': JQrels.COVID_ROUND3,
    'covid-round3-cumulative': JQrels.COVID_ROUND3_CUMULATIVE,
    'covid-round4': JQrels.COVID_ROUND4,
    'covid-round4-cumulative': JQrels.COVID_ROUND4_CUMULATIVE,
    'covid-round5': JQrels.COVID_ROUND5,
    'trec2018-bl': JQrels.TREC2018_BL,
    'trec2019-bl': JQrels.TREC2019_BL,
    'trec2020-bl': JQrels.TREC2020_BL,
    'mrtydi-v1.1-arabic-train': JQrels.MRTYDI_V11_AR_TRAIN,
    'mrtydi-v1.1-arabic-dev': JQrels.MRTYDI_V11_AR_DEV,
    'mrtydi-v1.1-arabic-test': JQrels.MRTYDI_V11_AR_TEST,
    'mrtydi-v1.1-bengali-train': JQrels.MRTYDI_V11_BN_TRAIN,
    'mrtydi-v1.1-bengali-dev': JQrels.MRTYDI_V11_BN_DEV,
    'mrtydi-v1.1-bengali-test': JQrels.MRTYDI_V11_BN_TEST,
    'mrtydi-v1.1-english-train': JQrels.MRTYDI_V11_EN_TRAIN,
    'mrtydi-v1.1-english-dev': JQrels.MRTYDI_V11_EN_DEV,
    'mrtydi-v1.1-english-test': JQrels.MRTYDI_V11_EN_TEST,
    'mrtydi-v1.1-finnish-train': JQrels.MRTYDI_V11_FI_TRAIN,
    'mrtydi-v1.1-finnish-dev': JQrels.MRTYDI_V11_FI_DEV,
    'mrtydi-v1.1-finnish-test': JQrels.MRTYDI_V11_FI_TEST,
    'mrtydi-v1.1-indonesian-train': JQrels.MRTYDI_V11_ID_TRAIN,
    'mrtydi-v1.1-indonesian-dev': JQrels.MRTYDI_V11_ID_DEV,
    'mrtydi-v1.1-indonesian-test': JQrels.MRTYDI_V11_ID_TEST,
    'mrtydi-v1.1-japanese-train': JQrels.MRTYDI_V11_JA_TRAIN,
    'mrtydi-v1.1-japanese-dev': JQrels.MRTYDI_V11_JA_DEV,
    'mrtydi-v1.1-japanese-test': JQrels.MRTYDI_V11_JA_TEST,
    'mrtydi-v1.1-korean-train': JQrels.MRTYDI_V11_KO_TRAIN,
    'mrtydi-v1.1-korean-dev': JQrels.MRTYDI_V11_KO_DEV,
    'mrtydi-v1.1-korean-test': JQrels.MRTYDI_V11_KO_TEST,
    'mrtydi-v1.1-russian-train': JQrels.MRTYDI_V11_RU_TRAIN,
    'mrtydi-v1.1-russian-dev': JQrels.MRTYDI_V11_RU_DEV,
    'mrtydi-v1.1-russian-test': JQrels.MRTYDI_V11_RU_TEST,
    'mrtydi-v1.1-swahili-train': JQrels.MRTYDI_V11_SW_TRAIN,
    'mrtydi-v1.1-swahili-dev': JQrels.MRTYDI_V11_SW_DEV,
    'mrtydi-v1.1-swahili-test': JQrels.MRTYDI_V11_SW_TEST,
    'mrtydi-v1.1-telugu-train': JQrels.MRTYDI_V11_TE_TRAIN,
    'mrtydi-v1.1-telugu-dev': JQrels.MRTYDI_V11_TE_DEV,
    'mrtydi-v1.1-telugu-test': JQrels.MRTYDI_V11_TE_TEST,
    'mrtydi-v1.1-thai-train': JQrels.MRTYDI_V11_TH_TRAIN,
    'mrtydi-v1.1-thai-dev': JQrels.MRTYDI_V11_TH_DEV,
    'mrtydi-v1.1-thai-test': JQrels.MRTYDI_V11_TH_TEST,
    'beir-v1.0.0-trec-covid-test': JQrels.BEIR_V1_0_0_TREC_COVID_TEST,
    'beir-v1.0.0-bioasq-test': JQrels.BEIR_V1_0_0_BIOASQ_TEST,
    'beir-v1.0.0-nfcorpus-test': JQrels.BEIR_V1_0_0_NFCORPUS_TEST,
    'beir-v1.0.0-nq-test': JQrels.BEIR_V1_0_0_NQ_TEST,
    'beir-v1.0.0-hotpotqa-test': JQrels.BEIR_V1_0_0_HOTPOTQA_TEST,
    'beir-v1.0.0-fiqa-test': JQrels.BEIR_V1_0_0_FIQA_TEST,
    'beir-v1.0.0-signal1m-test': JQrels.BEIR_V1_0_0_SIGNAL1M_TEST,
    'beir-v1.0.0-trec-news-test': JQrels.BEIR_V1_0_0_TREC_NEWS_TEST,
    'beir-v1.0.0-robust04-test': JQrels.BEIR_V1_0_0_ROBUST04_TEST,
    'beir-v1.0.0-arguana-test': JQrels.BEIR_V1_0_0_ARGUANA_TEST,
    'beir-v1.0.0-webis-touche2020-test': JQrels.BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST,
    'beir-v1.0.0-cqadupstack-android-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST,
    'beir-v1.0.0-cqadupstack-english-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST,
    'beir-v1.0.0-cqadupstack-gaming-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST,
    'beir-v1.0.0-cqadupstack-gis-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_GIS_TEST,
    'beir-v1.0.0-cqadupstack-mathematica-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST,
    'beir-v1.0.0-cqadupstack-physics-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST,
    'beir-v1.0.0-cqadupstack-programmers-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST,
    'beir-v1.0.0-cqadupstack-stats-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_STATS_TEST,
    'beir-v1.0.0-cqadupstack-tex-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_TEX_TEST,
    'beir-v1.0.0-cqadupstack-unix-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST,
    'beir-v1.0.0-cqadupstack-webmasters-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST,
    'beir-v1.0.0-cqadupstack-wordpress-test': JQrels.BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST,
    'beir-v1.0.0-quora-test': JQrels.BEIR_V1_0_0_QUORA_TEST,
    'beir-v1.0.0-dbpedia-entity-test': JQrels.BEIR_V1_0_0_DBPEDIA_ENTITY_TEST,
    'beir-v1.0.0-scidocs-test': JQrels.BEIR_V1_0_0_SCIDOCS_TEST,
    'beir-v1.0.0-fever-test': JQrels.BEIR_V1_0_0_FEVER_TEST,
    'beir-v1.0.0-climate-fever-test': JQrels.BEIR_V1_0_0_CLIMATE_FEVER_TEST,
    'beir-v1.0.0-scifact-test': JQrels.BEIR_V1_0_0_SCIFACT_TEST,
    'hc4-v1.0-fa-dev': JQrels.HC4_V1_0_FA_DEV,
    'hc4-v1.0-fa-test': JQrels.HC4_V1_0_FA_TEST,
    'hc4-v1.0-ru-dev': JQrels.HC4_V1_0_RU_DEV,
    'hc4-v1.0-ru-test': JQrels.HC4_V1_0_RU_TEST,
    'hc4-v1.0-zh-dev': JQrels.HC4_V1_0_ZH_DEV,
    'hc4-v1.0-zh-test': JQrels.HC4_V1_0_ZH_TEST,
    'hc4-neuclir22-fa-test': JQrels.HC4_NEUCLIR22_FA_TEST,
    'hc4-neuclir22-ru-test': JQrels.HC4_NEUCLIR22_RU_TEST,
    'hc4-neuclir22-zh-test': JQrels.HC4_NEUCLIR22_ZH_TEST,
    'miracl-v1.0-ar-dev': JQrels.MIRACL_V10_AR_DEV,
    'miracl-v1.0-bn-dev': JQrels.MIRACL_V10_BN_DEV,
    'miracl-v1.0-en-dev': JQrels.MIRACL_V10_EN_DEV,
    'miracl-v1.0-es-dev': JQrels.MIRACL_V10_ES_DEV,
    'miracl-v1.0-fa-dev': JQrels.MIRACL_V10_FA_DEV,
    'miracl-v1.0-fi-dev': JQrels.MIRACL_V10_FI_DEV,
    'miracl-v1.0-fr-dev': JQrels.MIRACL_V10_FR_DEV,
    'miracl-v1.0-hi-dev': JQrels.MIRACL_V10_HI_DEV,
    'miracl-v1.0-id-dev': JQrels.MIRACL_V10_ID_DEV,
    'miracl-v1.0-ja-dev': JQrels.MIRACL_V10_JA_DEV,
    'miracl-v1.0-ko-dev': JQrels.MIRACL_V10_KO_DEV,
    'miracl-v1.0-ru-dev': JQrels.MIRACL_V10_RU_DEV,
    'miracl-v1.0-sw-dev': JQrels.MIRACL_V10_SW_DEV,
    'miracl-v1.0-te-dev': JQrels.MIRACL_V10_TE_DEV,
    'miracl-v1.0-th-dev': JQrels.MIRACL_V10_TH_DEV,
    'miracl-v1.0-zh-dev': JQrels.MIRACL_V10_ZH_DEV,
    'miracl-v1.0-de-dev': JQrels.MIRACL_V10_DE_DEV,
    'miracl-v1.0-yo-dev': JQrels.MIRACL_V10_YO_DEV,
}


def get_topics(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        Topics as a dictionary
    """
    if collection_name not in topics_mapping:
        raise ValueError(f'Topic {collection_name} Not Found')

    topics = JTopicReader.getTopicsWithStringIds(topics_mapping[collection_name])

    t = {}
    for topic in topics.keySet().toArray():
        
        if topic.isdigit():
            # parse the keys into integers
            topic_key = int(topic)
        else:
            topic_key = topic
            
        t[topic_key] = {}
        for key in topics.get(topic).keySet().toArray():
            t[topic_key][key] = topics.get(topic).get(key)
    return t


def get_topics_with_reader(reader_class, file):
    # Yes, this is an insanely ridiculous method name.
    topics = JTopicReader.getTopicsWithStringIdsFromFileWithTopicReaderClass(reader_class, file)
    if topics is None:
        raise ValueError(f'Unable to initialize TopicReader {reader_class} with file {file}!')

    t = {}
    for topic in topics.keySet().toArray():
        
        if topic.isdigit():
            # parse the keys into integers
            topic_key = int(topic)
        else:
            topic_key = topic
            
        t[topic_key] = {}
        for key in topics.get(topic).keySet().toArray():
            t[topic_key][key] = topics.get(topic).get(key)
    return t


def get_qrels_file(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    path : str
        path of the qrels file
    """
    if collection_name in qrels_mapping:
        qrels = qrels_mapping[collection_name]
        target_path = os.path.join(get_cache_home(), qrels.path)
        if os.path.exists(target_path):
            return target_path
        target_dir = os.path.split(target_path)[0]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(target_path, 'w') as file:
            qrels_content = JRelevanceJudgments.getQrelsResource(qrels)
            file.write(qrels_content)
        return target_path

    raise FileNotFoundError(f'no qrels file for {collection_name}')


def get_qrels(collection_name):
    """
    Parameters
    ----------
    collection_name : str
        collection_name

    Returns
    -------
    result : dictionary
        qrels as a dictionary
    """
    file_path = get_qrels_file(collection_name)
    qrels = {}
    with open(file_path, 'r') as f:
        for line in f:
            qid, _, docid, judgement = line.rstrip().split()
            
            if qid.isdigit():
                qrels_key = int(qid)
            else:
                qrels_key = qid
                
            if docid.isdigit():
                doc_key = int(docid)
            else:
                doc_key = docid
                
            if qrels_key in qrels:
                qrels[qrels_key][doc_key] = judgement
            else:
                qrels[qrels_key] = {doc_key: judgement}
    return qrels
