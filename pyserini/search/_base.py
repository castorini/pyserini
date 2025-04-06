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
This module serves as the 'root' of Pyserini search capabilities, providing common functionalities across sparse
and dense retrieval.
"""

import logging
import os

from pyserini.pyclass import autoclass

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARNING, format='\n%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# Wrappers around Lucene classes
JPath = autoclass('java.nio.file.Path')

# Wrappers around Anserini classes
JQrels = autoclass('io.anserini.eval.Qrels')
JRelevanceJudgments = autoclass('io.anserini.eval.RelevanceJudgments')
JTopicReader = autoclass('io.anserini.search.topicreader.TopicReader')
JTopics = autoclass('io.anserini.search.topicreader.Topics')


# Function to safely get attributes from a class, returns None if not found
def safe_getattr(cls, attr):
    return getattr(cls, attr, None)


topics_mapping = {
    'trec1-adhoc': 'TREC1_ADHOC',
    'trec2-adhoc': 'TREC2_ADHOC',
    'trec3-adhoc': 'TREC3_ADHOC',
    'robust04': 'ROBUST04',
    'robust05': 'ROBUST05',
    'core17': 'CORE17',
    'core18': 'CORE18',
    'wt10g': 'WT10G',
    'trec2004-terabyte': 'TREC2004_TERABYTE',
    'trec2005-terabyte': 'TREC2005_TERABYTE',
    'trec2006-terabyte': 'TREC2006_TERABYTE',
    'trec2007-million-query': 'TREC2007_MILLION_QUERY',
    'trec2008-million-query': 'TREC2008_MILLION_QUERY',
    'trec2009-million-query': 'TREC2009_MILLION_QUERY',
    'trec2010-web': 'TREC2010_WEB',
    'trec2011-web': 'TREC2011_WEB',
    'trec2012-web': 'TREC2012_WEB',
    'trec2013-web': 'TREC2013_WEB',
    'trec2014-web': 'TREC2014_WEB',
    'mb11': 'MB11',
    'mb12': 'MB12',
    'mb13': 'MB13',
    'mb14': 'MB14',
    'car17v1.5-benchmarkY1test': 'CAR17V15_BENCHMARK_Y1_TEST',
    'car17v2.0-benchmarkY1test': 'CAR17V20_BENCHMARK_Y1_TEST',

    # DL19 doc
    'dl19-doc': 'TREC2019_DL_DOC',
    'dl19-doc-unicoil': 'TREC2019_DL_DOC_UNICOIL',
    'dl19-doc-unicoil-noexp': 'TREC2019_DL_DOC_UNICOIL_NOEXP',

    # DL19 passage
    'dl19-passage': 'TREC2019_DL_PASSAGE',
    'dl19-passage-unicoil': 'TREC2019_DL_PASSAGE_UNICOIL',
    'dl19-passage-unicoil-noexp': 'TREC2019_DL_PASSAGE_UNICOIL_NOEXP',
    'dl19-passage-unicoil': 'TREC2019_DL_PASSAGE_UNICOIL',
    'dl19-passage-splade-distil-cocodenser-medium': 'TREC2019_DL_PASSAGE_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'dl19-passage-splade-pp-ed': 'TREC2019_DL_PASSAGE_SPLADE_PP_ED',
    'dl19-passage-splade-pp-sd': 'TREC2019_DL_PASSAGE_SPLADE_PP_SD',
    'dl19-passage-splade-v3': 'TREC2019_DL_PASSAGE_SPLADE_V3',

    # DL20 (passage and doc are the same)
    'dl20': 'TREC2020_DL',
    'dl20-unicoil': 'TREC2020_DL_UNICOIL',
    'dl20-unicoil-noexp': 'TREC2020_DL_UNICOIL_NOEXP',
    'dl20-splade-distil-cocodenser-medium': 'TREC2020_DL_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'dl20-splade-pp-ed': 'TREC2020_DL_SPLADE_PP_ED',
    'dl20-splade-pp-sd': 'TREC2020_DL_SPLADE_PP_SD',
    'dl20-splade-v3': 'TREC2020_DL_SPLADE_V3',

    # DL20 doc
    'dl20-doc': 'TREC2020_DL',
    'dl20-doc-unicoil': 'TREC2020_DL_UNICOIL',
    'dl20-doc-unicoil-noexp': 'TREC2020_DL_UNICOIL_NOEXP',

    # DL20 passage
    'dl20-passage': 'TREC2020_DL',
    'dl20-passage-unicoil': 'TREC2020_DL_UNICOIL',
    'dl20-passage-unicoil-noexp': 'TREC2020_DL_UNICOIL_NOEXP',
    'dl20-passage-splade-distil-cocodenser-medium': 'TREC2020_DL_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'dl20-passage-splade-pp-ed': 'TREC2020_DL_SPLADE_PP_ED',
    'dl20-passage-splade-pp-sd': 'TREC2020_DL_SPLADE_PP_SD',
    'dl20-passage-splade-v3': 'TREC2020_DL_SPLADE_V3',

    'dl21': 'TREC2021_DL',
    'dl21-doc': 'TREC2021_DL',
    'dl21-unicoil': 'TREC2021_DL_UNICOIL',
    'dl21-unicoil-noexp': 'TREC2021_DL_UNICOIL_NOEXP',
    'dl22': 'TREC2022_DL',
    'dl22-doc': 'TREC2022_DL',
    'dl22-unicoil': 'TREC2022_DL_UNICOIL',
    'dl22-unicoil-noexp': 'TREC2022_DL_UNICOIL_NOEXP',
    'dl23': 'TREC2023_DL',
    'dl23-doc': 'TREC2023_DL',
    'dl23-unicoil': 'TREC2023_DL_UNICOIL',
    'dl23-unicoil-noexp': 'TREC2023_DL_UNICOIL_NOEXP',
    'rag24.raggy-dev': 'TREC2024_RAG_RAGGY_DEV',
    'rag24.researchy-dev': 'TREC2024_RAG_RESEARCHY_DEV',
    'rag24.test': 'TREC2024_RAG_TEST',
    'msmarco-doc-dev': 'MSMARCO_DOC_DEV',
    'msmarco-doc-dev-unicoil': 'MSMARCO_DOC_DEV_UNICOIL',
    'msmarco-doc-dev-unicoil-noexp': 'MSMARCO_DOC_DEV_UNICOIL_NOEXP',
    'msmarco-doc-test': 'MSMARCO_DOC_TEST',

    'msmarco-passage-dev-subset': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-passage-dev': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-passage.dev': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-v1-passage-dev': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-v1-passage.dev': 'MSMARCO_PASSAGE_DEV_SUBSET',

    'msmarco-passage-dev-subset-deepimpact': 'MSMARCO_PASSAGE_DEV_SUBSET_DEEPIMPACT',
    'msmarco-passage-dev-subset-unicoil': 'MSMARCO_PASSAGE_DEV_SUBSET_UNICOIL',
    'msmarco-passage-dev-subset-unicoil-noexp': 'MSMARCO_PASSAGE_DEV_SUBSET_UNICOIL_NOEXP',
    'msmarco-passage-dev-subset-unicoil-tilde': 'MSMARCO_PASSAGE_DEV_SUBSET_UNICOIL_TILDE',
    'msmarco-passage-dev-subset-distill-splade-max': 'MSMARCO_PASSAGE_DEV_SUBSET_DISTILL_SPLADE_MAX',
    'msmarco-passage-dev-subset-splade-distil-cocodenser-medium': 'MSMARCO_PASSAGE_DEV_SUBSET_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'msmarco-passage-dev-subset-splade-pp-ed': 'MSMARCO_PASSAGE_DEV_SUBSET_SPLADE_PP_ED',
    'msmarco-passage-dev-subset-splade-pp-sd': 'MSMARCO_PASSAGE_DEV_SUBSET_SPLADE_PP_SD',
    'msmarco-passage-dev-subset-splade-v3': 'MSMARCO_PASSAGE_DEV_SUBSET_SPLADE_V3',

    'msmarco-passage-test-subset': 'MSMARCO_PASSAGE_TEST_SUBSET',
    'msmarco-v2-doc-dev': 'MSMARCO_V2_DOC_DEV',
    'msmarco-v2-doc.dev': 'MSMARCO_V2_DOC_DEV',
    'msmarco-v2-doc-dev-unicoil': 'MSMARCO_V2_DOC_DEV_UNICOIL',
    'msmarco-v2-doc-dev-unicoil-noexp': 'MSMARCO_V2_DOC_DEV_UNICOIL_NOEXP',
    'msmarco-v2-doc-dev2': 'MSMARCO_V2_DOC_DEV2',
    'msmarco-v2-doc.dev2': 'MSMARCO_V2_DOC_DEV2',
    'msmarco-v2-doc-dev2-unicoil': 'MSMARCO_V2_DOC_DEV2_UNICOIL',
    'msmarco-v2-doc-dev2-unicoil-noexp': 'MSMARCO_V2_DOC_DEV2_UNICOIL_NOEXP',
    'msmarco-v2-passage-dev': 'MSMARCO_V2_PASSAGE_DEV',
    'msmarco-v2-passage-dev-unicoil': 'MSMARCO_V2_PASSAGE_DEV_UNICOIL',
    'msmarco-v2-passage-dev-unicoil-noexp': 'MSMARCO_V2_PASSAGE_DEV_UNICOIL_NOEXP',
    'msmarco-v2-passage-dev2': 'MSMARCO_V2_PASSAGE_DEV2',
    'msmarco-v2-passage-dev2-unicoil': 'MSMARCO_V2_PASSAGE_DEV2_UNICOIL',
    'msmarco-v2-passage-dev2-unicoil-noexp': 'MSMARCO_V2_PASSAGE_DEV2_UNICOIL_NOEXP',
    'ntcir8-zh': 'NTCIR8_ZH',
    'clef2006-fr': 'CLEF2006_FR',
    'trec2002-ar': 'TREC2002_AR',
    'fire2012-bn': 'FIRE2012_BN',
    'fire2012-hi': 'FIRE2012_HI',
    'fire2012-en': 'FIRE2012_EN',
    'covid-round1': 'COVID_ROUND1',
    'covid-round1-udel': 'COVID_ROUND1_UDEL',
    'covid-round2': 'COVID_ROUND2',
    'covid-round2-udel': 'COVID_ROUND2_UDEL',
    'covid-round3': 'COVID_ROUND3',
    'covid-round3-udel': 'COVID_ROUND3_UDEL',
    'covid-round4': 'COVID_ROUND4',
    'covid-round4-udel': 'COVID_ROUND4_UDEL',
    'covid-round5': 'COVID_ROUND5',
    'covid-round5-udel': 'COVID_ROUND5_UDEL',
    'trec2018-bl': 'TREC2018_BL',
    'trec2019-bl': 'TREC2019_BL',
    'trec2020-bl': 'TREC2020_BL',
    'epidemic-qa-expert-prelim': 'EPIDEMIC_QA_EXPERT_PRELIM',
    'epidemic-qa-consumer-prelim': 'EPIDEMIC_QA_CONSUMER_PRELIM',
    'dpr-nq-dev': 'DPR_NQ_DEV',
    'dpr-nq-test': 'DPR_NQ_TEST',
    'dpr-trivia-dev': 'DPR_TRIVIA_DEV',
    'dpr-trivia-test': 'DPR_TRIVIA_TEST',
    'dpr-wq-test': 'DPR_WQ_TEST',
    'dpr-squad-test': 'DPR_SQUAD_TEST',
    'dpr-curated-test': 'DPR_CURATED_TEST',
    'dpr-trivia-test-gar-t5-answers': 'DPR_TRIVIA_TEST_GART5_ANSWERS',
    'dpr-trivia-test-gar-t5-titles': 'DPR_TRIVIA_TEST_GART5_TITLES',
    'dpr-trivia-test-gar-t5-sentences': 'DPR_TRIVIA_TEST_GART5_SENTENCES',
    'dpr-trivia-test-gar-t5-all': 'DPR_TRIVIA_TEST_GART5_ALL',
    'nq-test-gar-t5-answers': 'NQ_TEST_GART5_ANSWERS',
    'nq-test-gar-t5-titles': 'NQ_TEST_GART5_TITLES',
    'nq-test-gar-t5-sentences': 'NQ_TEST_GART5_SENTENCES',
    'nq-test-gar-t5-all': 'NQ_TEST_GART5_ALL',
    'nq-dev': 'NQ_DEV',
    'nq-test': 'NQ_TEST',
    'mrtydi-v1.1-arabic-train': 'MRTYDI_V11_AR_TRAIN',
    'mrtydi-v1.1-arabic-dev': 'MRTYDI_V11_AR_DEV',
    'mrtydi-v1.1-arabic-test': 'MRTYDI_V11_AR_TEST',
    'mrtydi-v1.1-bengali-train': 'MRTYDI_V11_BN_TRAIN',
    'mrtydi-v1.1-bengali-dev': 'MRTYDI_V11_BN_DEV',
    'mrtydi-v1.1-bengali-test': 'MRTYDI_V11_BN_TEST',
    'mrtydi-v1.1-english-train': 'MRTYDI_V11_EN_TRAIN',
    'mrtydi-v1.1-english-dev': 'MRTYDI_V11_EN_DEV',
    'mrtydi-v1.1-english-test': 'MRTYDI_V11_EN_TEST',
    'mrtydi-v1.1-finnish-train': 'MRTYDI_V11_FI_TRAIN',
    'mrtydi-v1.1-finnish-dev': 'MRTYDI_V11_FI_DEV',
    'mrtydi-v1.1-finnish-test': 'MRTYDI_V11_FI_TEST',
    'mrtydi-v1.1-indonesian-train': 'MRTYDI_V11_ID_TRAIN',
    'mrtydi-v1.1-indonesian-dev': 'MRTYDI_V11_ID_DEV',
    'mrtydi-v1.1-indonesian-test': 'MRTYDI_V11_ID_TEST',
    'mrtydi-v1.1-japanese-train': 'MRTYDI_V11_JA_TRAIN',
    'mrtydi-v1.1-japanese-dev': 'MRTYDI_V11_JA_DEV',
    'mrtydi-v1.1-japanese-test': 'MRTYDI_V11_JA_TEST',
    'mrtydi-v1.1-korean-train': 'MRTYDI_V11_KO_TRAIN',
    'mrtydi-v1.1-korean-dev': 'MRTYDI_V11_KO_DEV',
    'mrtydi-v1.1-korean-test': 'MRTYDI_V11_KO_TEST',
    'mrtydi-v1.1-russian-train': 'MRTYDI_V11_RU_TRAIN',
    'mrtydi-v1.1-russian-dev': 'MRTYDI_V11_RU_DEV',
    'mrtydi-v1.1-russian-test': 'MRTYDI_V11_RU_TEST',
    'mrtydi-v1.1-swahili-train': 'MRTYDI_V11_SW_TRAIN',
    'mrtydi-v1.1-swahili-dev': 'MRTYDI_V11_SW_DEV',
    'mrtydi-v1.1-swahili-test': 'MRTYDI_V11_SW_TEST',
    'mrtydi-v1.1-telugu-train': 'MRTYDI_V11_TE_TRAIN',
    'mrtydi-v1.1-telugu-dev': 'MRTYDI_V11_TE_DEV',
    'mrtydi-v1.1-telugu-test': 'MRTYDI_V11_TE_TEST',
    'mrtydi-v1.1-thai-train': 'MRTYDI_V11_TH_TRAIN',
    'mrtydi-v1.1-thai-dev': 'MRTYDI_V11_TH_DEV',
    'mrtydi-v1.1-thai-test': 'MRTYDI_V11_TH_TEST',

    # BEIR topics
    'beir-v1.0.0-trec-covid-test': 'BEIR_V1_0_0_TREC_COVID_TEST',
    'beir-v1.0.0-bioasq-test': 'BEIR_V1_0_0_BIOASQ_TEST',
    'beir-v1.0.0-nfcorpus-test': 'BEIR_V1_0_0_NFCORPUS_TEST',
    'beir-v1.0.0-nq-test': 'BEIR_V1_0_0_NQ_TEST',
    'beir-v1.0.0-hotpotqa-test': 'BEIR_V1_0_0_HOTPOTQA_TEST',
    'beir-v1.0.0-fiqa-test': 'BEIR_V1_0_0_FIQA_TEST',
    'beir-v1.0.0-signal1m-test': 'BEIR_V1_0_0_SIGNAL1M_TEST',
    'beir-v1.0.0-trec-news-test': 'BEIR_V1_0_0_TREC_NEWS_TEST',
    'beir-v1.0.0-robust04-test': 'BEIR_V1_0_0_ROBUST04_TEST',
    'beir-v1.0.0-arguana-test': 'BEIR_V1_0_0_ARGUANA_TEST',
    'beir-v1.0.0-webis-touche2020-test': 'BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST',
    'beir-v1.0.0-cqadupstack-android-test': 'BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST',
    'beir-v1.0.0-cqadupstack-english-test': 'BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST',
    'beir-v1.0.0-cqadupstack-gaming-test': 'BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST',
    'beir-v1.0.0-cqadupstack-gis-test': 'BEIR_V1_0_0_CQADUPSTACK_GIS_TEST',
    'beir-v1.0.0-cqadupstack-mathematica-test': 'BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST',
    'beir-v1.0.0-cqadupstack-physics-test': 'BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST',
    'beir-v1.0.0-cqadupstack-programmers-test': 'BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST',
    'beir-v1.0.0-cqadupstack-stats-test': 'BEIR_V1_0_0_CQADUPSTACK_STATS_TEST',
    'beir-v1.0.0-cqadupstack-tex-test': 'BEIR_V1_0_0_CQADUPSTACK_TEX_TEST',
    'beir-v1.0.0-cqadupstack-unix-test': 'BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST',
    'beir-v1.0.0-cqadupstack-webmasters-test': 'BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST',
    'beir-v1.0.0-cqadupstack-wordpress-test': 'BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST',
    'beir-v1.0.0-quora-test': 'BEIR_V1_0_0_QUORA_TEST',
    'beir-v1.0.0-dbpedia-entity-test': 'BEIR_V1_0_0_DBPEDIA_ENTITY_TEST',
    'beir-v1.0.0-scidocs-test': 'BEIR_V1_0_0_SCIDOCS_TEST',
    'beir-v1.0.0-fever-test': 'BEIR_V1_0_0_FEVER_TEST',
    'beir-v1.0.0-climate-fever-test': 'BEIR_V1_0_0_CLIMATE_FEVER_TEST',
    'beir-v1.0.0-scifact-test': 'BEIR_V1_0_0_SCIFACT_TEST',

    # BEIR topics (aliases, because 'test' is often dropped)
    'beir-v1.0.0-trec-covid': 'BEIR_V1_0_0_TREC_COVID_TEST',
    'beir-v1.0.0-bioasq': 'BEIR_V1_0_0_BIOASQ_TEST',
    'beir-v1.0.0-nfcorpus': 'BEIR_V1_0_0_NFCORPUS_TEST',
    'beir-v1.0.0-nq': 'BEIR_V1_0_0_NQ_TEST',
    'beir-v1.0.0-hotpotqa': 'BEIR_V1_0_0_HOTPOTQA_TEST',
    'beir-v1.0.0-fiqa': 'BEIR_V1_0_0_FIQA_TEST',
    'beir-v1.0.0-signal1m': 'BEIR_V1_0_0_SIGNAL1M_TEST',
    'beir-v1.0.0-trec-news': 'BEIR_V1_0_0_TREC_NEWS_TEST',
    'beir-v1.0.0-robust04': 'BEIR_V1_0_0_ROBUST04_TEST',
    'beir-v1.0.0-arguana': 'BEIR_V1_0_0_ARGUANA_TEST',
    'beir-v1.0.0-webis-touche2020': 'BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST',
    'beir-v1.0.0-cqadupstack-android': 'BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST',
    'beir-v1.0.0-cqadupstack-english': 'BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST',
    'beir-v1.0.0-cqadupstack-gaming': 'BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST',
    'beir-v1.0.0-cqadupstack-gis': 'BEIR_V1_0_0_CQADUPSTACK_GIS_TEST',
    'beir-v1.0.0-cqadupstack-mathematica': 'BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST',
    'beir-v1.0.0-cqadupstack-physics': 'BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST',
    'beir-v1.0.0-cqadupstack-programmers': 'BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST',
    'beir-v1.0.0-cqadupstack-stats': 'BEIR_V1_0_0_CQADUPSTACK_STATS_TEST',
    'beir-v1.0.0-cqadupstack-tex': 'BEIR_V1_0_0_CQADUPSTACK_TEX_TEST',
    'beir-v1.0.0-cqadupstack-unix': 'BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST',
    'beir-v1.0.0-cqadupstack-webmasters': 'BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST',
    'beir-v1.0.0-cqadupstack-wordpress': 'BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST',
    'beir-v1.0.0-quora': 'BEIR_V1_0_0_QUORA_TEST',
    'beir-v1.0.0-dbpedia-entity': 'BEIR_V1_0_0_DBPEDIA_ENTITY_TEST',
    'beir-v1.0.0-scidocs': 'BEIR_V1_0_0_SCIDOCS_TEST',
    'beir-v1.0.0-fever': 'BEIR_V1_0_0_FEVER_TEST',
    'beir-v1.0.0-climate-fever': 'BEIR_V1_0_0_CLIMATE_FEVER_TEST',
    'beir-v1.0.0-scifact': 'BEIR_V1_0_0_SCIFACT_TEST',

    # SPLADE-distil CoCodenser Medium
    'beir-v1.0.0-trec-covid-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_TREC_COVID_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-bioasq-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_BIOASQ_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-nfcorpus-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_NFCORPUS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-nq-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_NQ_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-hotpotqa-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_HOTPOTQA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-fiqa-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_FIQA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-signal1m-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_SIGNAL1M_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-trec-news-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_TREC_NEWS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-robust04-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_ROBUST04_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-arguana-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_ARGUANA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-webis-touche2020-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-android-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-english-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-gaming-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-gis-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_GIS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-mathematica-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-physics-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-programmers-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-stats-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_STATS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-tex-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_TEX_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-unix-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-webmasters-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-cqadupstack-wordpress-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-quora-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_QUORA_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-dbpedia-entity-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_DBPEDIA_ENTITY_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-scidocs-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_SCIDOCS_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-fever-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_FEVER_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-climate-fever-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_CLIMATE_FEVER_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',
    'beir-v1.0.0-scifact-test-splade_distil_cocodenser_medium': 'BEIR_V1_0_0_SCIFACT_TEST_SPLADE_DISTILL_COCODENSER_MEDIUM',

    # SPLADE++ (CoCondenser-EnsembleDistil)
    'beir-v1.0.0-trec-covid.test.splade-pp-ed': 'BEIR_V1_0_0_TREC_COVID_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-bioasq.test.splade-pp-ed': 'BEIR_V1_0_0_BIOASQ_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-nfcorpus.test.splade-pp-ed': 'BEIR_V1_0_0_NFCORPUS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-nq.test.splade-pp-ed': 'BEIR_V1_0_0_NQ_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-hotpotqa.test.splade-pp-ed': 'BEIR_V1_0_0_HOTPOTQA_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-fiqa.test.splade-pp-ed': 'BEIR_V1_0_0_FIQA_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-signal1m.test.splade-pp-ed': 'BEIR_V1_0_0_SIGNAL1M_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-trec-news.test.splade-pp-ed': 'BEIR_V1_0_0_TREC_NEWS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-robust04.test.splade-pp-ed': 'BEIR_V1_0_0_ROBUST04_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-arguana.test.splade-pp-ed': 'BEIR_V1_0_0_ARGUANA_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-webis-touche2020.test.splade-pp-ed': 'BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-android.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-english.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-gaming.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-gis.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_GIS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-mathematica.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-physics.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-programmers.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-stats.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_STATS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-tex.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_TEX_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-unix.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-webmasters.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-cqadupstack-wordpress.test.splade-pp-ed': 'BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-quora.test.splade-pp-ed': 'BEIR_V1_0_0_QUORA_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-dbpedia-entity.test.splade-pp-ed': 'BEIR_V1_0_0_DBPEDIA_ENTITY_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-scidocs.test.splade-pp-ed': 'BEIR_V1_0_0_SCIDOCS_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-fever.test.splade-pp-ed': 'BEIR_V1_0_0_FEVER_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-climate-fever.test.splade-pp-ed': 'BEIR_V1_0_0_CLIMATE_FEVER_TEST_SPLADE_PP_ED',
    'beir-v1.0.0-scifact.test.splade-pp-ed': 'BEIR_V1_0_0_SCIFACT_TEST_SPLADE_PP_ED',
    'hc4-v1.0-fa-dev-title': 'HC4_V1_0_FA_DEV_TITLE',
    'hc4-v1.0-fa-dev-desc': 'HC4_V1_0_FA_DEV_DESC',
    'hc4-v1.0-fa-dev-desc-title': 'HC4_V1_0_FA_DEV_DESC_TITLE',
    'hc4-v1.0-fa-test-title': 'HC4_V1_0_FA_TEST_TITLE',
    'hc4-v1.0-fa-test-desc': 'HC4_V1_0_FA_TEST_DESC',
    'hc4-v1.0-fa-test-desc-title': 'HC4_V1_0_FA_TEST_DESC_TITLE',
    'hc4-v1.0-fa-en-test-title': 'HC4_V1_0_FA_EN_TEST_TITLE',
    'hc4-v1.0-fa-en-test-desc': 'HC4_V1_0_FA_EN_TEST_DESC',
    'hc4-v1.0-fa-en-test-desc-title': 'HC4_V1_0_FA_EN_TEST_DESC_TITLE',
    'hc4-v1.0-ru-dev-title': 'HC4_V1_0_RU_DEV_TITLE',
    'hc4-v1.0-ru-dev-desc': 'HC4_V1_0_RU_DEV_DESC',
    'hc4-v1.0-ru-dev-desc-title': 'HC4_V1_0_RU_DEV_DESC_TITLE',
    'hc4-v1.0-ru-test-title': 'HC4_V1_0_RU_TEST_TITLE',
    'hc4-v1.0-ru-test-desc': 'HC4_V1_0_RU_TEST_DESC',
    'hc4-v1.0-ru-test-desc-title': 'HC4_V1_0_RU_TEST_DESC_TITLE',
    'hc4-v1.0-ru-en-test-title': 'HC4_V1_0_RU_EN_TEST_TITLE',
    'hc4-v1.0-ru-en-test-desc': 'HC4_V1_0_RU_EN_TEST_DESC',
    'hc4-v1.0-ru-en-test-desc-title': 'HC4_V1_0_RU_EN_TEST_DESC_TITLE',
    'hc4-v1.0-zh-dev-title': 'HC4_V1_0_ZH_DEV_TITLE',
    'hc4-v1.0-zh-dev-desc': 'HC4_V1_0_ZH_DEV_DESC',
    'hc4-v1.0-zh-dev-desc-title': 'HC4_V1_0_ZH_DEV_DESC_TITLE',
    'hc4-v1.0-zh-test-title': 'HC4_V1_0_ZH_TEST_TITLE',
    'hc4-v1.0-zh-test-desc': 'HC4_V1_0_ZH_TEST_DESC',
    'hc4-v1.0-zh-test-desc-title': 'HC4_V1_0_ZH_TEST_DESC_TITLE',
    'hc4-v1.0-zh-en-test-title': 'HC4_V1_0_ZH_EN_TEST_TITLE',
    'hc4-v1.0-zh-en-test-desc': 'HC4_V1_0_ZH_EN_TEST_DESC',
    'hc4-v1.0-zh-en-test-desc-title': 'HC4_V1_0_ZH_EN_TEST_DESC_TITLE',

    # NeuCLIR 2022 topics
    'neuclir22-en-title':         'NEUCLIR22_EN_TITLE',
    'neuclir22-en-desc':          'NEUCLIR22_EN_DESC',
    'neuclir22-en-desc-title':    'NEUCLIR22_EN_DESC_TITLE',
    'neuclir22-fa-ht-title':      'NEUCLIR22_FA_HT_TITLE',
    'neuclir22-fa-ht-desc':       'NEUCLIR22_FA_HT_DESC',
    'neuclir22-fa-ht-desc-title': 'NEUCLIR22_FA_HT_DESC_TITLE',
    'neuclir22-fa-mt-title':      'NEUCLIR22_FA_MT_TITLE',
    'neuclir22-fa-mt-desc':       'NEUCLIR22_FA_MT_DESC',
    'neuclir22-fa-mt-desc-title': 'NEUCLIR22_FA_MT_DESC_TITLE',
    'neuclir22-ru-ht-title':      'NEUCLIR22_RU_HT_TITLE',
    'neuclir22-ru-ht-desc':       'NEUCLIR22_RU_HT_DESC',
    'neuclir22-ru-ht-desc-title': 'NEUCLIR22_RU_HT_DESC_TITLE',
    'neuclir22-ru-mt-title':      'NEUCLIR22_RU_MT_TITLE',
    'neuclir22-ru-mt-desc':       'NEUCLIR22_RU_MT_DESC',
    'neuclir22-ru-mt-desc-title': 'NEUCLIR22_RU_MT_DESC_TITLE',
    'neuclir22-zh-ht-title':      'NEUCLIR22_ZH_HT_TITLE',
    'neuclir22-zh-ht-desc':       'NEUCLIR22_ZH_HT_DESC',
    'neuclir22-zh-ht-desc-title': 'NEUCLIR22_ZH_HT_DESC_TITLE',
    'neuclir22-zh-mt-title':      'NEUCLIR22_ZH_MT_TITLE',
    'neuclir22-zh-mt-desc':       'NEUCLIR22_ZH_MT_DESC',
    'neuclir22-zh-mt-desc-title': 'NEUCLIR22_ZH_MT_DESC_TITLE',

    # MIRACL topics
    'miracl-v1.0-ar-dev': 'MIRACL_V10_AR_DEV',
    'miracl-v1.0-bn-dev': 'MIRACL_V10_BN_DEV',
    'miracl-v1.0-en-dev': 'MIRACL_V10_EN_DEV',
    'miracl-v1.0-es-dev': 'MIRACL_V10_ES_DEV',
    'miracl-v1.0-fa-dev': 'MIRACL_V10_FA_DEV',
    'miracl-v1.0-fi-dev': 'MIRACL_V10_FI_DEV',
    'miracl-v1.0-fr-dev': 'MIRACL_V10_FR_DEV',
    'miracl-v1.0-hi-dev': 'MIRACL_V10_HI_DEV',
    'miracl-v1.0-id-dev': 'MIRACL_V10_ID_DEV',
    'miracl-v1.0-ja-dev': 'MIRACL_V10_JA_DEV',
    'miracl-v1.0-ko-dev': 'MIRACL_V10_KO_DEV',
    'miracl-v1.0-ru-dev': 'MIRACL_V10_RU_DEV',
    'miracl-v1.0-sw-dev': 'MIRACL_V10_SW_DEV',
    'miracl-v1.0-te-dev': 'MIRACL_V10_TE_DEV',
    'miracl-v1.0-th-dev': 'MIRACL_V10_TH_DEV',
    'miracl-v1.0-zh-dev': 'MIRACL_V10_ZH_DEV',
    'miracl-v1.0-de-dev': 'MIRACL_V10_DE_DEV',
    'miracl-v1.0-yo-dev': 'MIRACL_V10_YO_DEV',
    
    # AToMiC topics
    'atomic-v0.2.1-ViT-L-14.laion2b_s32b_b82k-text-validation': 'ATOMIC_V021_VIT_L_14_LAION2B_S32B_B82K_TEXT_VAL',
    'atomic-v0.2-ViT-L-14.laion2b_s32b_b82k-image-validation': 'ATOMIC_V021_VIT_L_14_LAION2B_S32B_B82K_IMAGE_VAL',
    'atomic-v0.2.1-ViT-H-14.laion2b_s32b_b79k-text-validation': 'ATOMIC_V021_VIT_H_14_LAION2B_S32B_B79K_TEXT_VAL',
    'atomic-v0.2-ViT-H-14.laion2b_s32b_b79k-image-validation': 'ATOMIC_V021_VIT_H_14_LAION2B_S32B_B79K_IMAGE_VAL',
    'atomic-v0.2.1-ViT-B-32.laion2b_e16-text-validation': 'ATOMIC_V021_VIT_B_32_LAION2B_E16_TEXT_VAL',
    'atomic-v0.2-ViT-B-32.laion2b_e16-image-validation': 'ATOMIC_V021_VIT_B_32_LAION2B_E16_IMAGE_VAL',
    'atomic-v0.2.1-ViT-bigG-14.laion2b_s39b_b160k-text-validation': 'ATOMIC_V021_VIT_BIGG_14_LAION2B_S39B_B160K_TEXT_VAL',
    'atomic-v0.2-ViT-bigG-14.laion2b_s39b_b160k-image-validation': 'ATOMIC_V021_VIT_BIGG_14_LAION2B_S39B_B160K_IMAGE_VAL',
    'atomic-v0.2.1-ViT-B-32.laion400m_e32-text-validation': 'ATOMIC_V021_VIT_B_32_LAION400M_E32_TEXT_VAL',
    'atomic-v0.2-ViT-B-32.laion400m_e32-image-validation': 'ATOMIC_V021_VIT_B_32_LAION400M_E32_IMAGE_VAL',
    'atomic-v0.2.1-Salesforce.blip-itm-large-coco-text-validation': 'ATOMIC_V021_SALESFORCE_BLIP_ITM_LARGE_COCO_TEXT_VAL',
    'atomic-v0.2-Salesforce.blip-itm-large-coco-image-validation': 'ATOMIC_V021_SALESFORCE_BLIP_ITM_LARGE_COCO_IMAGE_VAL',
    'atomic-v0.2.1-Salesforce.blip-itm-base-coco-text-validation': 'ATOMIC_V021_SALESFORCE_BLIP_ITM_BASE_COCO_TEXT_VAL',
    'atomic-v0.2-Salesforce.blip-itm-base-coco-image-validation': 'ATOMIC_V021_SALESFORCE_BLIP_ITM_BASE_COCO_IMAGE_VAL',
    'atomic-v0.2.1-openai.clip-vit-base-patch32-text-validation': 'ATOMIC_V021_OPENAI_CLIP_VIT_BASE_PATCH32_TEXT_VAL',
    'atomic-v0.2-openai.clip-vit-base-patch32-image-validation': 'ATOMIC_V021_OPENAI_CLIP_VIT_BASE_PATCH32_IMAGE_VAL',
    'atomic-v0.2.1-openai.clip-vit-large-patch14-text-validation': 'ATOMIC_V021_OPENAI_CLIP_VIT_LARGE_PATCH14_TEXT_VAL',
    'atomic-v0.2-openai.clip-vit-large-patch14-image-validation': 'ATOMIC_V021_OPENAI_CLIP_VIT_LARGE_PATCH14_IMAGE_VAL',
    'atomic-v0.2.1-facebook.flava-full-text-validation': 'ATOMIC_V021_FACEBOOK_FLAVA_FULL_TEXT_VAL',
    'atomic-v0.2-facebook.flava-full-image-validation': 'ATOMIC_V021_FACEBOOK_FLAVA_FULL_IMAGE_VAL',

    # CIRAL topics
    'ciral-v1.0-ha-test-a': 'CIRAL_V10_HA_TEST_A',
    'ciral-v1.0-so-test-a': 'CIRAL_V10_SO_TEST_A',
    'ciral-v1.0-sw-test-a': 'CIRAL_V10_SW_TEST_A',
    'ciral-v1.0-yo-test-a': 'CIRAL_V10_YO_TEST_A',
    'ciral-v1.0-ha-test-a-native': 'CIRAL_V10_HA_TEST_A_NATIVE',
    'ciral-v1.0-so-test-a-native': 'CIRAL_V10_SO_TEST_A_NATIVE',
    'ciral-v1.0-sw-test-a-native': 'CIRAL_V10_SW_TEST_A_NATIVE',
    'ciral-v1.0-yo-test-a-native': 'CIRAL_V10_YO_TEST_A_NATIVE',
    'ciral-v1.0-ha-test-b': 'CIRAL_V10_HA_TEST_B',
    'ciral-v1.0-so-test-b': 'CIRAL_V10_SO_TEST_B',
    'ciral-v1.0-sw-test-b': 'CIRAL_V10_SW_TEST_B',
    'ciral-v1.0-yo-test-b': 'CIRAL_V10_YO_TEST_B',
    'ciral-v1.0-ha-test-b-native': 'CIRAL_V10_HA_TEST_B_NATIVE',
    'ciral-v1.0-so-test-b-native': 'CIRAL_V10_SO_TEST_B_NATIVE',
    'ciral-v1.0-sw-test-b-native': 'CIRAL_V10_SW_TEST_B_NATIVE',
    'ciral-v1.0-yo-test-b-native': 'CIRAL_V10_YO_TEST_B_NATIVE',
    'ciral-v1.0-ha-dev-native': 'CIRAL_V10_HA_DEV_MONO',
    'ciral-v1.0-so-dev-native': 'CIRAL_V10_SO_DEV_MONO',
    'ciral-v1.0-sw-dev-native': 'CIRAL_V10_SW_DEV_MONO',
    'ciral-v1.0-yo-dev-native': 'CIRAL_V10_YO_DEV_MONO',
}

qrels_mapping = {
    'trec1-adhoc': 'TREC1_ADHOC',
    'trec2-adhoc': 'TREC2_ADHOC',
    'trec3-adhoc': 'TREC3_ADHOC',
    'robust04': 'ROBUST04',
    'robust05': 'ROBUST05',
    'core17': 'CORE17',
    'core18': 'CORE18',
    'wt10g': 'WT10G',
    'trec2004-terabyte': 'TREC2004_TERABYTE',
    'trec2005-terabyte': 'TREC2005_TERABYTE',
    'trec2006-terabyte': 'TREC2006_TERABYTE',
    'trec2011-web': 'TREC2011_WEB',
    'trec2012-web': 'TREC2012_WEB',
    'trec2013-web': 'TREC2013_WEB',
    'trec2014-web': 'TREC2014_WEB',
    'mb11': 'MB11',
    'mb12': 'MB12',
    'mb13': 'MB13',
    'mb14': 'MB14',
    'car17v1.5-benchmarkY1test': 'CAR17V15_BENCHMARK_Y1_TEST',
    'car17v2.0-benchmarkY1test': 'CAR17V20_BENCHMARK_Y1_TEST',
    'dl19-doc': 'TREC2019_DL_DOC',
    'dl19-passage': 'TREC2019_DL_PASSAGE',
    'dl20-doc': 'TREC2020_DL_DOC',
    'dl20-passage': 'TREC2020_DL_PASSAGE',
    'dl21-doc': 'TREC2021_DL_DOC',
    'dl21-passage': 'TREC2021_DL_PASSAGE',
    'dl22-doc': 'TREC2022_DL_DOC',
    'dl22-passage': 'TREC2022_DL_PASSAGE',
    'dl23-doc': 'TREC2023_DL_DOC',
    'dl23-passage': 'TREC2023_DL_PASSAGE',
    'dl21-doc-msmarco-v2.1': 'TREC2021_DL_DOC_MSMARCO_V21',
    'dl22-doc-msmarco-v2.1': 'TREC2022_DL_DOC_MSMARCO_V21',
    'dl23-doc-msmarco-v2.1': 'TREC2023_DL_DOC_MSMARCO_V21',
    'rag24.raggy-dev': 'TREC2024_RAG_RAGGY_DEV',
    'rag24.test-umbrela': 'TREC2024_RAG_UMBRELA',
    'msmarco-doc-dev': 'MSMARCO_DOC_DEV',
    'msmarco-passage-dev-subset': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-passage-dev': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-passage.dev': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-v1-passage-dev': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-v1-passage.dev': 'MSMARCO_PASSAGE_DEV_SUBSET',
    'msmarco-v2-doc-dev': 'MSMARCO_V2_DOC_DEV',
    'msmarco-v2-doc-dev2': 'MSMARCO_V2_DOC_DEV2',
    'msmarco-v2-passage-dev': 'MSMARCO_V2_PASSAGE_DEV',
    'msmarco-v2-passage-dev2': 'MSMARCO_V2_PASSAGE_DEV2',
    'msmarco-v2.1-doc.dev': 'MSMARCO_V21_DOC_DEV',
    'msmarco-v2.1-doc.dev2': 'MSMARCO_V21_DOC_DEV2',
    'ntcir8-zh': 'NTCIR8_ZH',
    'clef2006-fr': 'CLEF2006_FR',
    'trec2002-ar': 'TREC2002_AR',
    'fire2012-bn': 'FIRE2012_BN',
    'fire2012-hi': 'FIRE2012_HI',
    'fire2012-en': 'FIRE2012_EN',
    'covid-complete': 'COVID_COMPLETE',
    'covid-round1': 'COVID_ROUND1',
    'covid-round2': 'COVID_ROUND2',
    'covid-round3': 'COVID_ROUND3',
    'covid-round3-cumulative': 'COVID_ROUND3_CUMULATIVE',
    'covid-round4': 'COVID_ROUND4',
    'covid-round4-cumulative': 'COVID_ROUND4_CUMULATIVE',
    'covid-round5': 'COVID_ROUND5',
    'trec2018-bl': 'TREC2018_BL',
    'trec2019-bl': 'TREC2019_BL',
    'trec2020-bl': 'TREC2020_BL',
    'mrtydi-v1.1-arabic-train': 'MRTYDI_V11_AR_TRAIN',
    'mrtydi-v1.1-arabic-dev': 'MRTYDI_V11_AR_DEV',
    'mrtydi-v1.1-arabic-test': 'MRTYDI_V11_AR_TEST',
    'mrtydi-v1.1-bengali-train': 'MRTYDI_V11_BN_TRAIN',
    'mrtydi-v1.1-bengali-dev': 'MRTYDI_V11_BN_DEV',
    'mrtydi-v1.1-bengali-test': 'MRTYDI_V11_BN_TEST',
    'mrtydi-v1.1-english-train': 'MRTYDI_V11_EN_TRAIN',
    'mrtydi-v1.1-english-dev': 'MRTYDI_V11_EN_DEV',
    'mrtydi-v1.1-english-test': 'MRTYDI_V11_EN_TEST',
    'mrtydi-v1.1-finnish-train': 'MRTYDI_V11_FI_TRAIN',
    'mrtydi-v1.1-finnish-dev': 'MRTYDI_V11_FI_DEV',
    'mrtydi-v1.1-finnish-test': 'MRTYDI_V11_FI_TEST',
    'mrtydi-v1.1-indonesian-train': 'MRTYDI_V11_ID_TRAIN',
    'mrtydi-v1.1-indonesian-dev': 'MRTYDI_V11_ID_DEV',
    'mrtydi-v1.1-indonesian-test': 'MRTYDI_V11_ID_TEST',
    'mrtydi-v1.1-japanese-train': 'MRTYDI_V11_JA_TRAIN',
    'mrtydi-v1.1-japanese-dev': 'MRTYDI_V11_JA_DEV',
    'mrtydi-v1.1-japanese-test': 'MRTYDI_V11_JA_TEST',
    'mrtydi-v1.1-korean-train': 'MRTYDI_V11_KO_TRAIN',
    'mrtydi-v1.1-korean-dev': 'MRTYDI_V11_KO_DEV',
    'mrtydi-v1.1-korean-test': 'MRTYDI_V11_KO_TEST',
    'mrtydi-v1.1-russian-train': 'MRTYDI_V11_RU_TRAIN',
    'mrtydi-v1.1-russian-dev': 'MRTYDI_V11_RU_DEV',
    'mrtydi-v1.1-russian-test': 'MRTYDI_V11_RU_TEST',
    'mrtydi-v1.1-swahili-train': 'MRTYDI_V11_SW_TRAIN',
    'mrtydi-v1.1-swahili-dev': 'MRTYDI_V11_SW_DEV',
    'mrtydi-v1.1-swahili-test': 'MRTYDI_V11_SW_TEST',
    'mrtydi-v1.1-telugu-train': 'MRTYDI_V11_TE_TRAIN',
    'mrtydi-v1.1-telugu-dev': 'MRTYDI_V11_TE_DEV',
    'mrtydi-v1.1-telugu-test': 'MRTYDI_V11_TE_TEST',
    'mrtydi-v1.1-thai-train': 'MRTYDI_V11_TH_TRAIN',
    'mrtydi-v1.1-thai-dev': 'MRTYDI_V11_TH_DEV',
    'mrtydi-v1.1-thai-test': 'MRTYDI_V11_TH_TEST',

    # BEIR qrels
    'beir-v1.0.0-trec-covid-test': 'BEIR_V1_0_0_TREC_COVID_TEST',
    'beir-v1.0.0-bioasq-test': 'BEIR_V1_0_0_BIOASQ_TEST',
    'beir-v1.0.0-nfcorpus-test': 'BEIR_V1_0_0_NFCORPUS_TEST',
    'beir-v1.0.0-nq-test': 'BEIR_V1_0_0_NQ_TEST',
    'beir-v1.0.0-hotpotqa-test': 'BEIR_V1_0_0_HOTPOTQA_TEST',
    'beir-v1.0.0-fiqa-test': 'BEIR_V1_0_0_FIQA_TEST',
    'beir-v1.0.0-signal1m-test': 'BEIR_V1_0_0_SIGNAL1M_TEST',
    'beir-v1.0.0-trec-news-test': 'BEIR_V1_0_0_TREC_NEWS_TEST',
    'beir-v1.0.0-robust04-test': 'BEIR_V1_0_0_ROBUST04_TEST',
    'beir-v1.0.0-arguana-test': 'BEIR_V1_0_0_ARGUANA_TEST',
    'beir-v1.0.0-webis-touche2020-test': 'BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST',
    'beir-v1.0.0-cqadupstack-android-test': 'BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST',
    'beir-v1.0.0-cqadupstack-english-test': 'BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST',
    'beir-v1.0.0-cqadupstack-gaming-test': 'BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST',
    'beir-v1.0.0-cqadupstack-gis-test': 'BEIR_V1_0_0_CQADUPSTACK_GIS_TEST',
    'beir-v1.0.0-cqadupstack-mathematica-test': 'BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST',
    'beir-v1.0.0-cqadupstack-physics-test': 'BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST',
    'beir-v1.0.0-cqadupstack-programmers-test': 'BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST',
    'beir-v1.0.0-cqadupstack-stats-test': 'BEIR_V1_0_0_CQADUPSTACK_STATS_TEST',
    'beir-v1.0.0-cqadupstack-tex-test': 'BEIR_V1_0_0_CQADUPSTACK_TEX_TEST',
    'beir-v1.0.0-cqadupstack-unix-test': 'BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST',
    'beir-v1.0.0-cqadupstack-webmasters-test': 'BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST',
    'beir-v1.0.0-cqadupstack-wordpress-test': 'BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST',
    'beir-v1.0.0-quora-test': 'BEIR_V1_0_0_QUORA_TEST',
    'beir-v1.0.0-dbpedia-entity-test': 'BEIR_V1_0_0_DBPEDIA_ENTITY_TEST',
    'beir-v1.0.0-scidocs-test': 'BEIR_V1_0_0_SCIDOCS_TEST',
    'beir-v1.0.0-fever-test': 'BEIR_V1_0_0_FEVER_TEST',
    'beir-v1.0.0-climate-fever-test': 'BEIR_V1_0_0_CLIMATE_FEVER_TEST',
    'beir-v1.0.0-scifact-test': 'BEIR_V1_0_0_SCIFACT_TEST',

    # BEIR qrels (aliases, because 'test' is often dropped)
    'beir-v1.0.0-trec-covid': 'BEIR_V1_0_0_TREC_COVID_TEST',
    'beir-v1.0.0-bioasq': 'BEIR_V1_0_0_BIOASQ_TEST',
    'beir-v1.0.0-nfcorpus': 'BEIR_V1_0_0_NFCORPUS_TEST',
    'beir-v1.0.0-nq': 'BEIR_V1_0_0_NQ_TEST',
    'beir-v1.0.0-hotpotqa': 'BEIR_V1_0_0_HOTPOTQA_TEST',
    'beir-v1.0.0-fiqa': 'BEIR_V1_0_0_FIQA_TEST',
    'beir-v1.0.0-signal1m': 'BEIR_V1_0_0_SIGNAL1M_TEST',
    'beir-v1.0.0-trec-news': 'BEIR_V1_0_0_TREC_NEWS_TEST',
    'beir-v1.0.0-robust04': 'BEIR_V1_0_0_ROBUST04_TEST',
    'beir-v1.0.0-arguana': 'BEIR_V1_0_0_ARGUANA_TEST',
    'beir-v1.0.0-webis-touche2020': 'BEIR_V1_0_0_WEBIS_TOUCHE2020_TEST',
    'beir-v1.0.0-cqadupstack-android': 'BEIR_V1_0_0_CQADUPSTACK_ANDROID_TEST',
    'beir-v1.0.0-cqadupstack-english': 'BEIR_V1_0_0_CQADUPSTACK_ENGLISH_TEST',
    'beir-v1.0.0-cqadupstack-gaming': 'BEIR_V1_0_0_CQADUPSTACK_GAMING_TEST',
    'beir-v1.0.0-cqadupstack-gis': 'BEIR_V1_0_0_CQADUPSTACK_GIS_TEST',
    'beir-v1.0.0-cqadupstack-mathematica': 'BEIR_V1_0_0_CQADUPSTACK_MATHEMATICA_TEST',
    'beir-v1.0.0-cqadupstack-physics': 'BEIR_V1_0_0_CQADUPSTACK_PHYSICS_TEST',
    'beir-v1.0.0-cqadupstack-programmers': 'BEIR_V1_0_0_CQADUPSTACK_PROGRAMMERS_TEST',
    'beir-v1.0.0-cqadupstack-stats': 'BEIR_V1_0_0_CQADUPSTACK_STATS_TEST',
    'beir-v1.0.0-cqadupstack-tex': 'BEIR_V1_0_0_CQADUPSTACK_TEX_TEST',
    'beir-v1.0.0-cqadupstack-unix': 'BEIR_V1_0_0_CQADUPSTACK_UNIX_TEST',
    'beir-v1.0.0-cqadupstack-webmasters': 'BEIR_V1_0_0_CQADUPSTACK_WEBMASTERS_TEST',
    'beir-v1.0.0-cqadupstack-wordpress': 'BEIR_V1_0_0_CQADUPSTACK_WORDPRESS_TEST',
    'beir-v1.0.0-quora': 'BEIR_V1_0_0_QUORA_TEST',
    'beir-v1.0.0-dbpedia-entity': 'BEIR_V1_0_0_DBPEDIA_ENTITY_TEST',
    'beir-v1.0.0-scidocs': 'BEIR_V1_0_0_SCIDOCS_TEST',
    'beir-v1.0.0-fever': 'BEIR_V1_0_0_FEVER_TEST',
    'beir-v1.0.0-climate-fever': 'BEIR_V1_0_0_CLIMATE_FEVER_TEST',
    'beir-v1.0.0-scifact': 'BEIR_V1_0_0_SCIFACT_TEST',

    'hc4-v1.0-fa-dev': 'HC4_V1_0_FA_DEV',
    'hc4-v1.0-fa-test': 'HC4_V1_0_FA_TEST',
    'hc4-v1.0-ru-dev': 'HC4_V1_0_RU_DEV',
    'hc4-v1.0-ru-test': 'HC4_V1_0_RU_TEST',
    'hc4-v1.0-zh-dev': 'HC4_V1_0_ZH_DEV',
    'hc4-v1.0-zh-test': 'HC4_V1_0_ZH_TEST',
    'hc4-neuclir22-fa-test': 'HC4_NEUCLIR22_FA_TEST',
    'hc4-neuclir22-ru-test': 'HC4_NEUCLIR22_RU_TEST',
    'hc4-neuclir22-zh-test': 'HC4_NEUCLIR22_ZH_TEST',
    'miracl-v1.0-ar-dev': 'MIRACL_V10_AR_DEV',
    'miracl-v1.0-bn-dev': 'MIRACL_V10_BN_DEV',
    'miracl-v1.0-en-dev': 'MIRACL_V10_EN_DEV',
    'miracl-v1.0-es-dev': 'MIRACL_V10_ES_DEV',
    'miracl-v1.0-fa-dev': 'MIRACL_V10_FA_DEV',
    'miracl-v1.0-fi-dev': 'MIRACL_V10_FI_DEV',
    'miracl-v1.0-fr-dev': 'MIRACL_V10_FR_DEV',
    'miracl-v1.0-hi-dev': 'MIRACL_V10_HI_DEV',
    'miracl-v1.0-id-dev': 'MIRACL_V10_ID_DEV',
    'miracl-v1.0-ja-dev': 'MIRACL_V10_JA_DEV',
    'miracl-v1.0-ko-dev': 'MIRACL_V10_KO_DEV',
    'miracl-v1.0-ru-dev': 'MIRACL_V10_RU_DEV',
    'miracl-v1.0-sw-dev': 'MIRACL_V10_SW_DEV',
    'miracl-v1.0-te-dev': 'MIRACL_V10_TE_DEV',
    'miracl-v1.0-th-dev': 'MIRACL_V10_TH_DEV',
    'miracl-v1.0-zh-dev': 'MIRACL_V10_ZH_DEV',
    'miracl-v1.0-de-dev': 'MIRACL_V10_DE_DEV',
    'miracl-v1.0-yo-dev': 'MIRACL_V10_YO_DEV',
    'atomic.validation.t2i': 'ATOMIC_VAL_T2I',
    'atomic.validation.i2t': 'ATOMIC_VAL_I2T',
    'ciral-v1.0-ha-dev': 'CIRAL_V10_HA_DEV',
    'ciral-v1.0-so-dev': 'CIRAL_V10_SO_DEV',
    'ciral-v1.0-sw-dev': 'CIRAL_V10_SW_DEV',
    'ciral-v1.0-yo-dev': 'CIRAL_V10_YO_DEV',
    'ciral-v1.0-ha-test-a': 'CIRAL_V10_HA_TEST_A',
    'ciral-v1.0-so-test-a': 'CIRAL_V10_SO_TEST_A',
    'ciral-v1.0-sw-test-a': 'CIRAL_V10_SW_TEST_A',
    'ciral-v1.0-yo-test-a': 'CIRAL_V10_YO_TEST_A',
    'ciral-v1.0-ha-test-a-pools': 'CIRAL_V10_HA_TEST_A_POOLS',
    'ciral-v1.0-so-test-a-pools': 'CIRAL_V10_SO_TEST_A_POOLS',
    'ciral-v1.0-sw-test-a-pools': 'CIRAL_V10_SW_TEST_A_POOLS',
    'ciral-v1.0-yo-test-a-pools': 'CIRAL_V10_YO_TEST_A_POOLS',
    'ciral-v1.0-ha-test-b': 'CIRAL_V10_HA_TEST_B',
    'ciral-v1.0-so-test-b': 'CIRAL_V10_SO_TEST_B',
    'ciral-v1.0-sw-test-b': 'CIRAL_V10_SW_TEST_B',
    'ciral-v1.0-yo-test-b': 'CIRAL_V10_YO_TEST_B'
}

# Log warnings for missing mappings
for topic in topics_mapping:
    topics_mapping[topic] = safe_getattr(JTopics, topics_mapping[topic])
    if topics_mapping[topic] is None:
        logger.warning(f"Topic '{topic}' is not available in your Anserini binding.")

for qrel in qrels_mapping:
    qrels_mapping[qrel] = safe_getattr(JQrels, qrels_mapping[qrel])
    if qrels_mapping[qrel] is None:
        logger.warning(f"Qrel '{qrel}' is not available in your Anserini binding.")

topics_mapping = {k: v for k, v in topics_mapping.items() if v is not None}
qrels_mapping = {k: v for k, v in qrels_mapping.items() if v is not None}

# Programmatically add aliases, e.g., dl19-passage-splade-v3 and dl19-passage.splade-v3 should both work.
topics_alias = {}
for topic in topics_mapping:
    # Note that startswith can tell you if a str starts with any from a list of prefixes,
    # but doesn't easily tell you *which* one. Easier just to iterate through options.
    if topic.startswith('msmarco-passage-dev-subset-'):
        topics_alias[topic.replace('msmarco-passage-dev-subset-', 'msmarco-passage-dev-subset.')] = topics_mapping[topic]
        topics_alias[topic.replace('msmarco-passage-dev-subset-', 'msmarco-passage-dev.')] = topics_mapping[topic]
        topics_alias[topic.replace('msmarco-passage-dev-subset-', 'msmarco-passage.dev.')] = topics_mapping[topic]
        topics_alias[topic.replace('msmarco-passage-dev-subset-', 'msmarco-v1-passage-dev.')] = topics_mapping[topic]
        topics_alias[topic.replace('msmarco-passage-dev-subset-', 'msmarco-v1-passage.dev.')] = topics_mapping[topic]
    elif topic.startswith('dl19-passage-'):
        topics_alias[topic.replace('dl19-passage-', 'dl19-passage.')] = topics_mapping[topic]
    elif topic.startswith('dl20-passage-'):
        topics_alias[topic.replace('dl20-passage-', 'dl20-passage.')] = topics_mapping[topic]


# Union original mappings and the aliases.
topics_mapping = {**topics_mapping, **topics_alias}


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
        target_path = JRelevanceJudgments.getQrelsPath(JPath.of(qrels.path)).toString()
        if os.path.exists(target_path):
            return target_path
        target_dir = os.path.split(target_path)[0]
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        with open(target_path, 'w') as file:
            qrels_content = JRelevanceJudgments.getQrelsResource(JPath.of(target_path))
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
