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

from collections.abc import Mapping
import importlib.resources
import json
from urllib.request import urlopen

from pyserini.pyclass import autoclass


PREBUILT_INDEXES_COMMIT = 'eb2a94de2029b3e9234ffd7445ab74991b6b0137'


def _prebuilt_indexes_url(path):
    return f'https://raw.githubusercontent.com/castorini/prebuilt-indexes/{PREBUILT_INDEXES_COMMIT}/{path}'


def _import_from_lucene_prebuilt_inverted_index_json(index_metadata):
    info = {
        'description': index_metadata['description'],
        'filename': index_metadata['filename'],
        'urls': index_metadata['urls'],
        'md5': index_metadata['md5'],
        'size': index_metadata['size'],
    }

    for field in ['readme', 'total_terms', 'documents', 'unique_terms', 'downloaded']:
        if field in index_metadata:
            info[field] = index_metadata[field]

    if 'corpus_index' in index_metadata:
        info['texts'] = index_metadata['corpus_index']

    return info


class _LazyLucenePrebuiltInvertedIndexJson(Mapping):
    def __init__(self, *urls, key_prefixes=()):
        self._urls = urls
        self._key_prefixes = key_prefixes
        self._info = None

    def _load(self):
        if self._info is None:
            info = {}
            for url in self._urls:
                if url.startswith('http://') or url.startswith('https://'):
                    with urlopen(url, timeout=10) as response:
                        records = json.load(response)
                else:
                    resource = importlib.resources.files('pyserini')
                    for path_part in url.split('/'):
                        resource = resource / path_part
                    with resource.open(encoding='utf-8') as response:
                        records = json.load(response)
                info.update({record['name']: _import_from_lucene_prebuilt_inverted_index_json(record) for record in records})
            self._info = info

        return self._info

    def __getitem__(self, key):
        return self._load()[key]

    def __iter__(self):
        return iter(self._load())

    def __len__(self):
        return len(self._load())

    def __contains__(self, key):
        if not isinstance(key, str):
            return False
        if self._key_prefixes and not any(key.startswith(prefix) for prefix in self._key_prefixes):
            return False
        return key in self._load()


class _PrebuiltIndexCatalog(Mapping):
    def __init__(self, *sources, aliases=None):
        self._sources = sources
        self._aliases = aliases or {}

    def _resolve_alias(self, key):
        seen = set()
        while key in self._aliases:
            if key in seen:
                raise KeyError(key)
            seen.add(key)
            key = self._aliases[key]
        return key

    def __getitem__(self, key):
        resolved_key = self._resolve_alias(key)
        for source in self._sources:
            if resolved_key in source:
                return source[resolved_key]
        raise KeyError(key)

    def __iter__(self):
        seen = set()
        for source in self._sources:
            for key in source:
                if key not in seen:
                    seen.add(key)
                    yield key
        for key in self._aliases:
            if key not in seen:
                yield key

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, key):
        if key in self._aliases:
            return True
        for source in self._sources:
            if key in source:
                return True
        return False


# Bindings for Lucene (standard) inverted indexes
TF_INDEX_INFO_MSMARCO = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/msmarco-v1-doc-inverted.json'),
    _prebuilt_indexes_url('lucene/msmarco-v1-passage-inverted.json'),
    _prebuilt_indexes_url('lucene/msmarco-v2-doc-inverted.json'),
    _prebuilt_indexes_url('lucene/msmarco-v2-doc-segmented-inverted.json'),
    _prebuilt_indexes_url('lucene/msmarco-v2-passage-inverted.json'),
    _prebuilt_indexes_url('lucene/msmarco-v2.1-doc-inverted.json'),
    _prebuilt_indexes_url('lucene/msmarco-v2.1-doc-segmented-inverted.json'),
    key_prefixes=('msmarco-',)
)

TF_INDEX_INFO_MSMARCO_ALIASES = {
    # To preserve working commands in published papers: integrations/core/papers/test_sigir2021.py testcase test_section3_3
    "msmarco-passage": "msmarco-v1-passage",
    # To preserve working commands in published papers: integrations/core/papers/test_sigir2022.py testcase test_Ma_etal_section4_1a
    "msmarco-v1-passage-d2q-t5": "msmarco-v1-passage.d2q-t5",
}

TF_INDEX_INFO_BEIR = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/beir-inverted-flat.json'),
    _prebuilt_indexes_url('lucene/beir-inverted-multifield.json'),
    key_prefixes=('beir-v1.0.0-',)
)

TF_INDEX_INFO_BRIGHT = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/bright-inverted.json'),
    key_prefixes=('bright-',)
)

TF_INDEX_INFO_MRTYDI = _LazyLucenePrebuiltInvertedIndexJson(
    'resources/prebuilt-indexes/lucene/mrtydi-inverted.json',
    key_prefixes=('mrtydi-v1.1-',)
)

TF_INDEX_INFO_MRTYDI_ALIASES = {
    "mrtydi-v1.1-arabic": "mrtydi-v1.1-ar",
    "mrtydi-v1.1-bengali": "mrtydi-v1.1-bn",
    "mrtydi-v1.1-english": "mrtydi-v1.1-en",
    "mrtydi-v1.1-finnish": "mrtydi-v1.1-fi",
    "mrtydi-v1.1-indonesian": "mrtydi-v1.1-id",
    "mrtydi-v1.1-japanese": "mrtydi-v1.1-ja",
    "mrtydi-v1.1-korean": "mrtydi-v1.1-ko",
    "mrtydi-v1.1-russian": "mrtydi-v1.1-ru",
    "mrtydi-v1.1-swahili": "mrtydi-v1.1-sw",
    "mrtydi-v1.1-telugu": "mrtydi-v1.1-te",
    "mrtydi-v1.1-thai": "mrtydi-v1.1-th"
}

TF_INDEX_INFO_MIRACL = _LazyLucenePrebuiltInvertedIndexJson(
    'resources/prebuilt-indexes/lucene/miracl-inverted.json',
    key_prefixes=('miracl-v1.0-',)
)

TF_INDEX_INFO_CIRAL = _LazyLucenePrebuiltInvertedIndexJson(
    'resources/prebuilt-indexes/lucene/ciral-inverted.json',
    key_prefixes=('ciral-v1.0-',)
)

TF_INDEX_INFO_M_BEIR = _LazyLucenePrebuiltInvertedIndexJson(
    'resources/prebuilt-indexes/lucene/m-beir-inverted.json',
    key_prefixes=('m-beir-',)
)

TF_INDEX_INFO_OTHER = _LazyLucenePrebuiltInvertedIndexJson(
    'resources/prebuilt-indexes/lucene/other-inverted.json'
)

TF_INDEX_INFO_OTHER_ALIASES = {
    # To preserve working commands in published papers: integrations/core/papers/test_sigir2021.py
    "wikipedia-dpr": "wikipedia-dpr-100w",

    # Common names mapping to corpora
    "robust04": "disk45",
    "robust05": "aquaint",
    "core17": "nyt",
    "core18": "wapo.v2",
}

TF_INDEX_INFO = _PrebuiltIndexCatalog(TF_INDEX_INFO_MSMARCO,
                                      TF_INDEX_INFO_BEIR,
                                      TF_INDEX_INFO_BRIGHT,
                                      TF_INDEX_INFO_MRTYDI,
                                      TF_INDEX_INFO_MIRACL,
                                      TF_INDEX_INFO_CIRAL,
                                      TF_INDEX_INFO_M_BEIR,
                                      TF_INDEX_INFO_OTHER,
                                      aliases={
                                          **TF_INDEX_INFO_MSMARCO_ALIASES,
                                          **TF_INDEX_INFO_MRTYDI_ALIASES,
                                          **TF_INDEX_INFO_OTHER_ALIASES,
                                      })


# Bindings for Lucene impact indexes
IMPACT_INDEX_INFO_MSMARCO = _LazyLucenePrebuiltInvertedIndexJson(
    'resources/prebuilt-indexes/lucene/msmarco-impact.json',
    key_prefixes=('msmarco-',)
)

IMPACT_INDEX_INFO_MSMARCO_ALIASES = {
    # To preserve working commands in published papers: integrations/core/papers/test_sigir2022.py testcase test_Trotman_etal
    "msmarco-passage-unicoil-d2q": IMPACT_INDEX_INFO_MSMARCO["msmarco-v1-passage.unicoil"],
    # To preserve working commands in published papers: integrations/core/papers/test_sigir2022.py testcase test_Ma_etal_section4_1b
    "msmarco-v2-passage-unicoil-0shot": IMPACT_INDEX_INFO_MSMARCO["msmarco-v2-passage.unicoil-0shot"]
}

IMPACT_INDEX_INFO_BEIR = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/beir-impact-splade-pp-ed.json'),
    _prebuilt_indexes_url('lucene/beir-impact-splade-v3.json'),
    key_prefixes=('beir-v1.0.0-',)
)

IMPACT_INDEX_INFO_BRIGHT = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/bright-impact.json'),
    key_prefixes=('bright-',)
)

IMPACT_INDEX_INFO = _PrebuiltIndexCatalog(IMPACT_INDEX_INFO_MSMARCO,
                                          IMPACT_INDEX_INFO_MSMARCO_ALIASES,
                                          IMPACT_INDEX_INFO_BEIR,
                                          IMPACT_INDEX_INFO_BRIGHT)

JPrebuiltHnswIndex = autoclass('io.anserini.index.prebuilt.PrebuiltHnswIndex')

def import_from_hnsw_lucene(index_metadata):
    info = {
        'description': index_metadata.description,
        'filename': index_metadata.filename,
        'readme': index_metadata.readme,
        'urls': [
            index_metadata.urls[0]
        ],
        'md5': index_metadata.md5,
        'size': index_metadata.size,
        'texts': index_metadata.corpusIndex
    }

    return info

# Bindings for Lucene HNSW MSMARCO indexes
LUCENE_HNSW_INDEX_INFO_MSMARCO = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/msmarco-v1-passage-hnsw.json'),
    _prebuilt_indexes_url('lucene/msmarco-v2.1-doc-segmented-hnsw.json'),
    key_prefixes=('msmarco-',)
)

# Bindings for Lucene HNSW BEIR indexes
LUCENE_HNSW_INDEX_INFO_BEIR = {
    "beir-v1.0.0-trec-covid.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-trec-covid.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-bioasq.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-bioasq.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-nfcorpus.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-nfcorpus.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-nq.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-nq.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-hotpotqa.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-hotpotqa.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-fiqa.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-fiqa.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-signal1m.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-signal1m.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-trec-news.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-trec-news.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-robust04.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-robust04.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-arguana.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-arguana.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-quora.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-quora.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-scidocs.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-scidocs.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-fever.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-fever.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-climate-fever.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-climate-fever.bge-base-en-v1.5.hnsw')),
    "beir-v1.0.0-scifact.bge-base-en-v1.5.hnsw": import_from_hnsw_lucene(JPrebuiltHnswIndex.get('beir-v1.0.0-scifact.bge-base-en-v1.5.hnsw')),
}

LUCENE_HNSW_INDEX_INFO = _PrebuiltIndexCatalog(LUCENE_HNSW_INDEX_INFO_MSMARCO,
                                               LUCENE_HNSW_INDEX_INFO_BEIR)


JPrebuiltFlatIndex = autoclass('io.anserini.index.prebuilt.PrebuiltFlatIndex')

def import_from_flat_lucene(index_metadata):
    info = {
        'description': index_metadata.description,
        'filename': index_metadata.filename,
        'readme': index_metadata.readme,
        'urls': [
            index_metadata.urls[0]
        ],
        'md5': index_metadata.md5,
        'size': index_metadata.size,
        'texts': index_metadata.corpusIndex
    }

    return info

# Bindings for Lucene flat indexes
LUCENE_FLAT_INDEX_INFO_BEIR = {
    "beir-v1.0.0-trec-covid.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-trec-covid.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-bioasq.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-bioasq.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-nfcorpus.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-nfcorpus.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-nq.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-nq.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-hotpotqa.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-hotpotqa.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-fiqa.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-fiqa.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-signal1m.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-signal1m.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-trec-news.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-trec-news.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-robust04.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-robust04.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-arguana.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-arguana.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-quora.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-quora.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-scidocs.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-scidocs.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-fever.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-fever.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-climate-fever.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-climate-fever.bge-base-en-v1.5.flat')),
    "beir-v1.0.0-scifact.bge-base-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('beir-v1.0.0-scifact.bge-base-en-v1.5.flat')),
}

LUCENE_FLAT_INDEX_INFO_BRIGHT = {
    "bright-biology.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-biology.bge-large-en-v1.5.flat')),
    "bright-earth-science.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-earth-science.bge-large-en-v1.5.flat')),
    "bright-economics.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-economics.bge-large-en-v1.5.flat')),
    "bright-psychology.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-psychology.bge-large-en-v1.5.flat')),
    "bright-robotics.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-robotics.bge-large-en-v1.5.flat')),
    "bright-stackoverflow.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-stackoverflow.bge-large-en-v1.5.flat')),
    "bright-sustainable-living.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-sustainable-living.bge-large-en-v1.5.flat')),
    "bright-pony.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-pony.bge-large-en-v1.5.flat')),
    "bright-leetcode.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-leetcode.bge-large-en-v1.5.flat')),
    "bright-aops.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-aops.bge-large-en-v1.5.flat')),
    "bright-theoremqa-theorems.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-theoremqa-theorems.bge-large-en-v1.5.flat')),
    "bright-theoremqa-questions.bge-large-en-v1.5.flat": import_from_flat_lucene(JPrebuiltFlatIndex.get('bright-theoremqa-questions.bge-large-en-v1.5.flat'))
}

LUCENE_FLAT_INDEX_INFO = {**LUCENE_FLAT_INDEX_INFO_BEIR, **LUCENE_FLAT_INDEX_INFO_BRIGHT}


# Bindings for Faiss indexes
FAISS_INDEX_INFO_MSMARCO = {
    "msmarco-v1-passage.cosdpr-distil": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by cosDPR-distil.",
        "filename": "faiss-flat.msmarco-v1-passage.cosdpr-distil.20221023.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.cosdpr-distil.20221023.tar.gz"
        ],
        "md5": "83565019175c79fcc5f8d99fb1bd43ca",
        "size": 23843194320,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.aggretriever-cocondenser": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by aggretriever-cocondenser.",
        "filename": "faiss-flat.msmarco-v1-passage.aggretriever-cocondenser.20230407.f627ef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.aggretriever-cocondenser.20230407.f627ef.tar.gz"
        ],
        "md5": "c55472025808eeca736c7123f0033726",
        "size": 26053474818,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.aggretriever-distilbert": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by aggretriever-distilbert.",
        "filename": "faiss-flat.msmarco-v1-passage.aggretriever-distilbert.20230407.f627ef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.aggretriever-distilbert.20230407.f627ef.tar.gz"
        ],
        "md5": "d8fd51bfe974752cf770856623e39668",
        "size": 25963140631,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },

    "msmarco-v1-passage.ance": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the ANCE MS MARCO passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.ance.20210224.060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.ance.20210224.060cef.tar.gz"
        ],
        "md5": "e6cf0c1011200af81fd53aa7c5ce9414",
        "size": 25102344926,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.distilbert-dot-margin-mse-t2": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the distilbert-dot-margin_mse-T2-msmarco encoder",
        "filename": "faiss-flat.msmarco-v1-passage.distilbert-dot-margin_mse-t2.20210316.d44c3a.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.distilbert-dot-margin_mse-t2.20210316.d44c3a.tar.gz"
        ],
        "md5": "bb8a3c3cf48fcd8c2e66f974fb449336",
        "size": 25162771335,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.distilbert-dot-tas_b-b256": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by distilbert-dot-tas_b-b256-msmarco encoder",
        "filename": "faiss-flat.msmarco-v1-passage.distilbert-dot-tas_b-b256.20210527.63276f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.distilbert-dot-tas_b-b256.20210527.63276f.tar.gz"
        ],
        "md5": "538546d5818527a51d87ce482e7a197e",
        "size": 25162329450,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.sbert": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the SBERT MS MARCO passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.sbert.20210313.a0fbb3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.sbert.20210313.a0fbb3.tar.gz"
        ],
        "md5": "b1649ea89b48cc89b3027399d09873dd",
        "size": 25214193348,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.bge-base-en-v1.5": {
        "description": "Faiss index of the MS MARCO passage corpus encoded by BGE-base-en-v1.5 encoder",
        "filename": "faiss-flat.msmarco-v1-passage.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b21fb6abee3be6da3b6f39c9f6d9f280",
        "size": 25217210007,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by TCT-ColBERT",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz"
        ],
        "md5": "6c544e9dcd87b3b6acac0f8a69d741dd",
        "size": 25204502424,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert.hnsw": {
        "description": "Faiss HNSW index of the MS MARCO passage corpus encoded by TCT-ColBERT",
        "filename": "faiss-hnsw.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-hnsw.msmarco-v1-passage.tct_colbert.20210112.be7119.tar.gz"
        ],
        "md5": "6b7285a7f0163d1a547214396be20488",
        "size": 33359120779,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert-v2": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2 passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert-v2.20210608.5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert-v2.20210608.5f341b.tar.gz"
        ],
        "md5": "768b897ec4ac62f5cea05ece12e5b284",
        "size": 25211079424,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert-v2-hn": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hn passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert-v2-hn.20210608.5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert-v2-hn.20210608.5f341b.tar.gz"
        ],
        "md5": "583210e5e8c8cddd4f34dbdf75bb4c21",
        "size": 25205730186,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.tct_colbert-v2-hnp": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by the tct_colbert-v2-hnp passage encoder",
        "filename": "faiss-flat.msmarco-v1-passage.tct_colbert-v2-hnp.20210608.5f341b.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.tct_colbert-v2-hnp.20210608.5f341b.tar.gz"
        ],
        "md5": "d22d0b6b32f156088a10b0d54ecc1da2",
        "size": 25225526400,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.openai-ada2": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by OpenAI ada2",
        "filename": "faiss-flat.msmarco-v1-passage.openai-ada2.20230530.e3a58f.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.openai-ada2.20230530.e3a58f.tar.gz"
        ],
        "md5": "5bad28d6ab7e28b834c3b3dd7be0fbc7",
        "size": 45649935995,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.cohere-embed-english-v3.0": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by Cohere Embed English v3.0",
        "filename": "faiss-flat.msmarco-v1-passage.cohere-embed-english-v3.0.20240216.2154e79.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.cohere-embed-english-v3.0.20240216.2154e79.tar.gz"
        ],
        "md5": "be2b8975161e1327fc852e01287dff48",
        "size": 21341576860,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },
    "msmarco-v1-passage.openai-text-embedding-3-large": {
        "description": "Faiss flat index of the MS MARCO passage corpus encoded by OpenAI text-embedding-3-large",
        "filename": "faiss-flat.msmarco-v1-passage.openai-text-embedding-3-large.20240410.c13cd6.tar.gz",
        "readme": "faiss-flat.msmarco-v1-passage.openai-text-embedding-3-large.20240410.c13cd6.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-passage.openai-text-embedding-3-large.20240410.c13cd6.tar.gz"
        ],
        "md5": "e52f046b1decc9bf3a55ac0ff70780d0",
        "size": 87658796879,
        "documents": 8841823,
        "downloaded": False,
        "texts": "msmarco-v1-passage"
    },

    "msmarco-v1-doc.ance-maxp": {
        "description": "Faiss flat index of the MS MARCO document corpus encoded by the ANCE MaxP encoder",
        "filename": "faiss-flat.msmarco-v1-doc.ance_maxp.20210304.b2a1b0.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-doc.ance_maxp.20210304.b2a1b0.tar.gz"
        ],
        "md5": "f956d8c718c77717fa9611c471e336da",
        "size": 58312804630,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-doc"
    },
    "msmarco-v1-doc.tct_colbert": {
        "description": "Faiss flat index of the MS MARCO document corpus encoded by TCT-ColBERT",
        "filename": "faiss-flat.msmarco-v1-doc.tct_colbert.20210112.be7119.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-doc.tct_colbert.20210112.be7119.tar.gz"
        ],
        "md5": "be7ff45b369803c10cc90fbab8642e60",
        "size": 58514326319,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-doc"
    },
    "msmarco-v1-doc-segmented.tct_colbert-v2-hnp": {
        "description": "Faiss flat index of the MS MARCO document corpus encoded by TCT-ColBERT-V2-HNP",
        "filename": "faiss-flat.msmarco-v1-doc-segmented.tct_colbert-v2-hnp.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v1-doc-segmented.tct_colbert-v2-hnp.tar.gz"
        ],
        "md5": "51b1309a0afac090aafbf96f84002ec0",
        "size": 58586765630,
        "documents": 20544550,
        "downloaded": False,
        "texts": "msmarco-v1-doc-segmented"
    },
    "msmarco-v2.1-doc-segmented-shard01.arctic-embed-l": {
        "description": "Faiss flat index of the MS MARCO 2.1 document corpus (shard 1) encoded by Snowflake's arctic-l",
        "filename": "faiss-flat.msmarco-v2.1-doc-segmented-shard01.arctic-embed-l.20241111.tar.gz",
        "readme": "faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v2.1-doc-segmented-shard01.arctic-embed-l.20241111.tar.gz"
        ],
        "md5": "66323cd3eb23aaf073e506a3c30e3622",
        "size": 226032429430,
        "documents": 59345785,
        "downloaded": False,
        "texts": "msmarco-v2.1-doc-segmented"
    },
    "msmarco-v2.1-doc-segmented-shard02.arctic-embed-l": {
        "description": "Faiss flat index of the MS MARCO 2.1 document corpus (shard 2) encoded by Snowflake's arctic-l",
        "filename": "faiss-flat.msmarco-v2.1-doc-segmented-shard02.arctic-embed-l.20241111.tar.gz",
        "readme": "faiss-flat.msmarco-v2.1-doc.arctic-embed-l.20240824.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v2.1-doc-segmented-shard02.arctic-embed-l.20241111.tar.gz"
        ],
        "md5": "a23d0a69df520dda9ac2d913f9d30e96",
        "size": 206300692646,
        "documents": 54174965,
        "downloaded": False,
        "texts": "msmarco-v2.1-doc-segmented"
    },
    "msmarco-v2.1-doc-segmented-shard01.arctic-embed-m-v1.5": {
        "description": "Faiss flat index of the MS MARCO 2.1 document corpus (shard 1) encoded by Snowflake's arctic-m-v1.5",
        "filename": "faiss-flat.msmarco-v2.1-doc-segmented-shard01.arctic-embed-m-v1.5.20241111.tar.gz",
        "readme": "faiss-flat.msmarco-v2.1-doc.arctic-embed-m-v1.5.20240824.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v2.1-doc-segmented-shard01.arctic-embed-m-v1.5.20241111.tar.gz"
        ],
        "md5": "d4c9beda52047204137851b8aeb4b41b",
        "size": 174698080459,
        "documents": 61104707,
        "downloaded": False,
        "texts": "msmarco-v2.1-doc-segmented"
    },
    "msmarco-v2.1-doc-segmented-shard02.arctic-embed-m-v1.5": {
        "description": "Faiss flat index of the MS MARCO 2.1 document corpus (shard 2) encoded by Snowflake's arctic-m-v1.5",
        "filename": "faiss-flat.msmarco-v2.1-doc-segmented-shard02.arctic-embed-m-v1.5.20241111.tar.gz",
        "readme": "faiss-flat.msmarco-v2.1-doc.arctic-embed-m-v1.5.20240824.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.msmarco-v2.1-doc-segmented-shard02.arctic-embed-m-v1.5.20241111.tar.gz"
        ],
        "md5": "f885cab8af4a281fde7a33d9d20c5774",
        "size": 149827891716,
        "documents": 52416043,
        "downloaded": False,
        "texts": "msmarco-v2.1-doc-segmented"
    }
}

FAISS_INDEX_INFO_BEIR = {
    # BEIR (v1.0.0) contriever indexes
    "beir-v1.0.0-trec-covid.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.contriever.20230124.tar.gz"
        ],
        "md5": "3f178cadc4a2d31bb1087e344f99ab4c",
        "size": 488100337,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat"
    },
    "beir-v1.0.0-bioasq.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.contriever.20230124.tar.gz"
        ],
        "md5": "a29261de8d5d3e473f66ed255b65ba96",
        "size": 42417202575,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat"
    },
    "beir-v1.0.0-nfcorpus.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.contriever.20230124.tar.gz"
        ],
        "md5": "30008d78302ee205f704bae116523efa",
        "size": 10322413,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat"
    },
    "beir-v1.0.0-nq.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): NQ, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-nq.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.contriever.20230124.tar.gz"
        ],
        "md5": "0bcfc534e6ef614e0f1b9ab6da57e481",
        "size": 7617697773,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat"
    },
    "beir-v1.0.0-hotpotqa.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.contriever.20230124.tar.gz"
        ],
        "md5": "b0813bc6c07b972419385e5f7f9aefe4",
        "size": 14874722012,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat"
    },
    "beir-v1.0.0-fiqa.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.contriever.20230124.tar.gz"
        ],
        "md5": "dd7812b413b2bb6d1168937402b2ac6c",
        "size": 164024743,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat"
    },
    "beir-v1.0.0-signal1m.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.contriever.20230124.tar.gz"
        ],
        "md5": "cb7e12e441584094a996139f16831b71",
        "size": 8142534260,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat"
    },
    "beir-v1.0.0-trec-news.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.contriever.20230124.tar.gz"
        ],
        "md5": "d3c5d0b7c3611805bec59b382f373857",
        "size": 1629958666,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat"
    },
    "beir-v1.0.0-robust04.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Robust04, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.contriever.20230124.tar.gz"
        ],
        "md5": "cbc30e163097ec1269e2b355d40ef373",
        "size": 1501110513,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat"
    },
    "beir-v1.0.0-arguana.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.contriever.20230124.tar.gz"
        ],
        "md5": "d75510f440ba12c645de1a1aa1d2cbc9",
        "size": 24710574,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat"
    },
    "beir-v1.0.0-webis-touche2020.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.contriever.20230124.tar.gz"
        ],
        "md5": "d26a488863f44023580deefc309f4d13",
        "size": 1091320687,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat"
    },
    "beir-v1.0.0-cqadupstack-android.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.contriever.20230124.tar.gz"
        ],
        "md5": "e360f313228e914808bc90721bd39784",
        "size": 65447253,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat"
    },
    "beir-v1.0.0-cqadupstack-english.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.contriever.20230124.tar.gz"
        ],
        "md5": "edb867d9bc0744fefc3024ecd38f83ee",
        "size": 114460503,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat"
    },
    "beir-v1.0.0-cqadupstack-gaming.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever.20230124.tar.gz"
        ],
        "md5": "8778ea1b56d506449eea05a510935500",
        "size": 128906101,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat"
    },
    "beir-v1.0.0-cqadupstack-gis.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever.20230124.tar.gz"
        ],
        "md5": "0b6224dc15c8c5211f8d16189e3c7fac",
        "size": 107128998,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat"
    },
    "beir-v1.0.0-cqadupstack-mathematica.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever.20230124.tar.gz"
        ],
        "md5": "7db3aa811104f7b34464cadcd3084176",
        "size": 47544599,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat"
    },
    "beir-v1.0.0-cqadupstack-physics.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever.20230124.tar.gz"
        ],
        "md5": "26126f4e8896d054cec11d8f4b840c1a",
        "size": 109048292,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat"
    },
    "beir-v1.0.0-cqadupstack-programmers.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever.20230124.tar.gz"
        ],
        "md5": "bb5fec14f14caf08d7338b7d1ff86d6b",
        "size": 91583163,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat"
    },
    "beir-v1.0.0-cqadupstack-stats.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever.20230124.tar.gz"
        ],
        "md5": "249b0a88775ab130e30efd3b6e07ebb8",
        "size": 120288678,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat"
    },
    "beir-v1.0.0-cqadupstack-tex.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever.20230124.tar.gz"
        ],
        "md5": "47d87a4dba07dc2cd651582b0388ccf1",
        "size": 194080722,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat"
    },
    "beir-v1.0.0-cqadupstack-unix.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever.20230124.tar.gz"
        ],
        "md5": "e8e09adcd207653792b5f5c430f355db",
        "size": 134860136,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat"
    },
    "beir-v1.0.0-cqadupstack-webmasters.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever.20230124.tar.gz"
        ],
        "md5": "9c0d468e18b137d8c7123c7ece5deafd",
        "size": 49531606,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat"
    },
    "beir-v1.0.0-cqadupstack-wordpress.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever.20230124.tar.gz"
        ],
        "md5": "c4100815492270db1519f644260a3b5a",
        "size": 138348174,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat"
    },
    "beir-v1.0.0-quora.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Quora, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-quora.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.contriever.20230124.tar.gz"
        ],
        "md5": "65cebdab871e2065fdacf0977f32a2bd",
        "size": 1485866155,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat"
    },
    "beir-v1.0.0-dbpedia-entity.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.contriever.20230124.tar.gz"
        ],
        "md5": "6098fd3dc9b2cae202d56f20b961291f",
        "size": 13214316276,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat"
    },
    "beir-v1.0.0-scidocs.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.contriever.20230124.tar.gz"
        ],
        "md5": "c565903e4eacf637173df096c6306e45",
        "size": 73532582,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat"
    },
    "beir-v1.0.0-fever.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): FEVER, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-fever.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.contriever.20230124.tar.gz"
        ],
        "md5": "01808e4f7ddcd31b391091c441de4bac",
        "size": 15437918697,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat"
    },
    "beir-v1.0.0-climate-fever.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.contriever.20230124.tar.gz"
        ],
        "md5": "b6ed4fe268281cd6cde8a2e0be361485",
        "size": 15437988872,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat"
    },
    "beir-v1.0.0-scifact.contriever": {
        "description": "Faiss flat index for BEIR (v1.0.0): SciFact, encoded by Contriever.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.contriever.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.contriever.20230124.tar.gz"
        ],
        "md5": "b0fe70f77488b3f296ccc98ffce65b49",
        "size": 14753571,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat"
    },

    # BEIR (v1.0.0) contriever ft MSMARCO indexes
    "beir-v1.0.0-trec-covid.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "607174fdc964760a1d491af294fb1b91",
        "size": 487986914,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat",
    },
    "beir-v1.0.0-bioasq.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "280c03564ea10a2bf1dcc01f9107b11c",
        "size": 42438279824,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat",
    },
    "beir-v1.0.0-nfcorpus.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "bfbec2a543a719e4085b2f67911ce965",
        "size": 10327251,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat",
    },
    "beir-v1.0.0-nq.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): NQ, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-nq.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "5eb685f5c2de1978de5b43604560fb01",
        "size": 7619790062,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat",
    },
    "beir-v1.0.0-hotpotqa.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "38c37708f9927501ca2f7563aa43f407",
        "size": 14889518959,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat",
    },
    "beir-v1.0.0-fiqa.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "540216665f5611df5ef968c66a068150",
        "size": 163998686,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat",
    },
    "beir-v1.0.0-signal1m.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "a71e5a2ada31a540817acdc1a2f7b2de",
        "size": 8146484810,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat",
    },
    "beir-v1.0.0-trec-news.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "fe560c02030bf212e4a4f3c1f205560d",
        "size": 1629437390,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat",
    },
    "beir-v1.0.0-robust04.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Robust04, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "de5531902df243521e006fbaa82ca1f9",
        "size": 1501089090,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat",
    },
    "beir-v1.0.0-arguana.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "2e32725a55a0db47953f481de393f1e4",
        "size": 24705839,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat",
    },
    "beir-v1.0.0-webis-touche2020.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c33ec5918c1afc435c5fa5ca2bfe61f1",
        "size": 1090748336,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat",
    },
    "beir-v1.0.0-cqadupstack-android.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "797b950b084d394f491fd84a0e7b8ef1",
        "size": 65438909,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat",
    },
    "beir-v1.0.0-cqadupstack-english.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "47f1408415a30ef448e516331d8c6131",
        "size": 114462176,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat",
    },
    "beir-v1.0.0-cqadupstack-gaming.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c293a3bca328183609c09d910094862a",
        "size": 128896849,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat",
    },
    "beir-v1.0.0-cqadupstack-gis.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "524162e606cc785a9f5e30b369d6334d",
        "size": 107086866,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat",
    },
    "beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "a224440d580614ec8dc5d00f052aaa41",
        "size": 47527017,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat",
    },
    "beir-v1.0.0-cqadupstack-physics.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "ed92c35d50f462cf29b09369a15c0b94",
        "size": 109024718,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat",
    },
    "beir-v1.0.0-cqadupstack-programmers.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "b0f925036d7a7b1b7529fbee840befa1",
        "size": 91567849,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat",
    },
    "beir-v1.0.0-cqadupstack-stats.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "a9db7f37526ee392ba762bf52e29f981",
        "size": 120271278,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat",
    },
    "beir-v1.0.0-cqadupstack-tex.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "f7e4f9da65d21bfc471e72c155791326",
        "size": 194009281,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat",
    },
    "beir-v1.0.0-cqadupstack-unix.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "d866f3c8d21ccfffecd400bda40dd823",
        "size": 134821507,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat",
    },
    "beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "84631850c0a127382e10ebb871b056a6",
        "size": 49530843,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat",
    },
    "beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "2e171633d09f3ac069fbafd7c1b81af3",
        "size": 138328538,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat",
    },
    "beir-v1.0.0-quora.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Quora, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-quora.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "1a58388eca4591390c439c7bf3a10dcc",
        "size": 1487402618,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat",
    },
    "beir-v1.0.0-dbpedia-entity.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "c9dd2022c77ce99a381346b5e550f438",
        "size": 13226845554,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat",
    },
    "beir-v1.0.0-scidocs.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "11181c5fa0c75521cbac1417236a0a95",
        "size": 73530345,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat",
    },
    "beir-v1.0.0-fever.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): FEVER, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-fever.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "736b179578fe3798111bda2b2e00aced",
        "size": 15444001345,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat",
    },
    "beir-v1.0.0-climate-fever.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "fd1bfde8fd2bccc0be98edec8eb3bf20",
        "size": 15444073241,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat",
    },
    "beir-v1.0.0-scifact.contriever-msmarco": {
        "description": "Faiss flat index for BEIR (v1.0.0): SciFact, encoded by Contriever w/ MS MARCO FTing.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.contriever-msmarco.20230124.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.contriever-msmarco.20230124.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.contriever-msmarco.20230124.tar.gz"
        ],
        "md5": "0caa1724d9e6e3324bfd2a875b7218df",
        "size": 14758752,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat",
    },

    # BEIR (v1.0.0) bge-base-en-v1.5 indexes
    "beir-v1.0.0-trec-covid.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-COVID, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "da2d227d8ddbb97109b469f8e1473b3b",
        "size": 489619642,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat"
    },
    "beir-v1.0.0-bioasq.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): BioASQ, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "13261d776f4f27aec1abf4431eedcb42",
        "size": 42566761620,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat"
    },
    "beir-v1.0.0-nfcorpus.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): NFCorpus, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "40da814f50fadf5f5ac1feb06ed3903b",
        "size": 10355291,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat"
    },
    "beir-v1.0.0-nq.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): NQ, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-nq.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b738bbbe7ca36532f25189b776d4e153",
        "size": 7630355859,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat"
    },
    "beir-v1.0.0-hotpotqa.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): HotpotQA, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "d2c08665e8cd750bd06ceb7d23897c94",
        "size": 14932298529,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat"
    },
    "beir-v1.0.0-fiqa.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): FiQA-2018, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b57027c48f0b31c53fca034a1f773541",
        "size": 164430948,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat"
    },
    "beir-v1.0.0-signal1m.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Signal-1M, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "3286c1fa5496e3d5de97eee1e621ad3b",
        "size": 8162604163,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat"
    },
    "beir-v1.0.0-trec-news.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): TREC-NEWS, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "2032399345f13ea0d1f15d7ae22427d1",
        "size": 1580911769,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat"
    },
    "beir-v1.0.0-robust04.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Robust04, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "e136ef8528027b9085161b5a4f3dc046",
        "size": 1503712018,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat"
    },
    "beir-v1.0.0-arguana.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): ArguAna, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "269047a536f856117a6a34048f49c030",
        "size": 24759653,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat"
    },
    "beir-v1.0.0-webis-touche2020.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Webis-Touche2020, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "00b68d1ef1c677715ca1ac10c676f99d",
        "size": 1090354182,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat"
    },
    "beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-android, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "f77217f345ec8e26e8f4b45c1a81dba2",
        "size": 65620193,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat"
    },
    "beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-english, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "0c57a49936831e31f8aec4d893dc2e36",
        "size": 114768549,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat"
    },
    "beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gaming, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "51d5a6a8157a27b2a919890d7760fb01",
        "size": 129249921,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat"
    },
    "beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-gis, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "0d4a65cecf8fb51be5f3fc89bbc0910d",
        "size": 107394286,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat"
    },
    "beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-mathematica, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "bbae6dfe9ad38215143bf04c1d70e210",
        "size": 47672368,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat"
    },
    "beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-physics, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "8a28f699c6c93cf3847b2c7c0e38916d",
        "size": 109354431,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat"
    },
    "beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-programmers, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "87786e84825276f2edddf282dbed87c5",
        "size": 91818236,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat"
    },
    "beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-stats, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "44d178e9780083dc5eb6dafdc7871e69",
        "size": 120632552,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat"
    },
    "beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-tex, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "94eae392bef6c8d78a3e8a086f867478",
        "size": 194551985,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat"
    },
    "beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-unix, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "cc0c4ec48266f3064661f7e2cfd3aa97",
        "size": 135195477,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat"
    },
    "beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-webmasters, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "6e9ccef54902fa6740e0ff37cf187215",
        "size": 49670415,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat"
    },
    "beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): CQADupStack-wordpress, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b0d124624680cc3c833f348b4f9a1396",
        "size": 138678474,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat"
    },
    "beir-v1.0.0-quora.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Quora, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-quora.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "cab4a6c847331986cf62490238aec4a5",
        "size": 1491755601,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat"
    },
    "beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): DBPedia, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "d3ba32cc2c185ef9585a91b6083ad78e",
        "size": 13265129127,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat"
    },
    "beir-v1.0.0-scidocs.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): SCIDOCS, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "cb41d6930f699514c70b23e99506954c",
        "size": 73776098,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat"
    },
    "beir-v1.0.0-fever.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): FEVER, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-fever.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "b9ccc330c46645e7819b73315dab8d29",
        "size": 15489138892,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat"
    },
    "beir-v1.0.0-climate-fever.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): Climate-FEVER, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "13515703cfa4032a0ae3a94ac2a3b76f",
        "size": 15489213928,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat"
    },
    "beir-v1.0.0-scifact.bge-base-en-v1.5": {
        "description": "Faiss flat index for BEIR (v1.0.0): SciFact, encoded by BGE-base-en-v1.5.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.bge-base-en-v1.5.20240107.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.bge-base-en-v1.5.20240107.tar.gz"
        ],
        "md5": "248b6db6e61d18f17674219aecd8b41d",
        "size": 14807082,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat"
    },
    # BEIR (v1.0.0) cohere-embed-english-v3.0 indexes
    "beir-v1.0.0-trec-covid.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-COVID) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-trec-covid.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-covid.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "bd81f8e76434bac6757a177038752868",
        "size": 414024650,
        "documents": 171332,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-covid.flat"
    },
    "beir-v1.0.0-bioasq.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (BioASQ) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-bioasq.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-bioasq.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "d25220fa2405737c41dfec35b67afaa5",
        "size": 36008754089,
        "documents": 14914603,
        "downloaded": False,
        "texts": "beir-v1.0.0-bioasq.flat"
    },
    "beir-v1.0.0-nfcorpus.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (NFCorpus) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-nfcorpus.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nfcorpus.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "8c0d2577f8cc1b29eff99b92bfb11d7c",
        "size": 8769499,
        "documents": 3633,
        "downloaded": False,
        "texts": "beir-v1.0.0-nfcorpus.flat"
    },
    "beir-v1.0.0-nq.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (NQ) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-nq.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-nq.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "33998961282a3dc5230093d058a39cda",
        "size": 6456624636,
        "documents": 2681468,
        "downloaded": False,
        "texts": "beir-v1.0.0-nq.flat"
    },
    "beir-v1.0.0-hotpotqa.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (HotpotQA) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-hotpotqa.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-hotpotqa.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "11631f3ea36c39d50a6a1c695449b630",
        "size": 12618101059,
        "documents": 5233329,
        "downloaded": False,
        "texts": "beir-v1.0.0-hotpotqa.flat"
    },
    "beir-v1.0.0-fiqa.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (FiQA-2018) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-fiqa.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fiqa.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "e5692c7f8ff5d042eba9fe8674d309de",
        "size": 139105165,
        "documents": 57638,
        "downloaded": False,
        "texts": "beir-v1.0.0-fiqa.flat"
    },
    "beir-v1.0.0-signal1m.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Signal-1M) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-signal1m.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-signal1m.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "baef67767588ef7d6a0eac19b3f3ef3c",
        "size": 6910588927,
        "documents": 2866316,
        "downloaded": False,
        "texts": "beir-v1.0.0-signal1m.flat"
    },
    "beir-v1.0.0-trec-news.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (TREC-NEWS) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-trec-news.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-trec-news.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "2de9f2d422d953b71106f8edfbc23e0a",
        "size": 1292117296,
        "documents": 594977,
        "downloaded": False,
        "texts": "beir-v1.0.0-trec-news.flat"
    },
    "beir-v1.0.0-robust04.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Robust04) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-robust04.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-robust04.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "b36948744ed2400343e4bce432c7bb1f",
        "size": 1271873099,
        "documents": 528155,
        "downloaded": False,
        "texts": "beir-v1.0.0-robust04.flat"
    },
    "beir-v1.0.0-arguana.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (ArguAna) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-arguana.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-arguana.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "3206b775623067252027dee67f28d530",
        "size": 20943333,
        "documents": 8674,
        "downloaded": False,
        "texts": "beir-v1.0.0-arguana.flat"
    },
    "beir-v1.0.0-webis-touche2020.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Webis-Touche2020) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-webis-touche2020.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-webis-touche2020.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "216ba2c47b4d0562a4eec7b5e34b9408",
        "size": 920313712,
        "documents": 382545,
        "downloaded": False,
        "texts": "beir-v1.0.0-webis-touche2020.flat"
    },
    "beir-v1.0.0-cqadupstack-android.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-android) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-android.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-android.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "c39b8fa0d7fc013e80f8cca7ac5b6217",
        "size": 55520218,
        "documents": 22998,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-android.flat"
    },
    "beir-v1.0.0-cqadupstack-english.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-english) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-english.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-english.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "f7180a07b8de17a16edc7c47cd4c7cab",
        "size": 97094242,
        "documents": 40221,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-english.flat"
    },
    "beir-v1.0.0-cqadupstack-gaming.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gaming) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gaming.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gaming.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "a85599afabaf741b38cbf0749142709f",
        "size": 109357647,
        "documents": 45301,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gaming.flat"
    },
    "beir-v1.0.0-cqadupstack-gis.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-gis) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-gis.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-gis.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "17c1db9371d645fa2f28d17cdfe2b6f4",
        "size": 90813980,
        "documents": 37637,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-gis.flat"
    },
    "beir-v1.0.0-cqadupstack-mathematica.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-mathematica) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-mathematica.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-mathematica.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "6b357fd66d750cf8ab81687cfd76cc35",
        "size": 40290360,
        "documents": 16705,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-mathematica.flat"
    },
    "beir-v1.0.0-cqadupstack-physics.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-physics) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-physics.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-physics.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "2bc31bf3b46d152c489dde73e986dfef",
        "size": 92506040,
        "documents": 38316,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-physics.flat"
    },
    "beir-v1.0.0-cqadupstack-programmers.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-programmers) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-programmers.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-programmers.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "f3e418d7401b5e317e15cc23ed4468cd",
        "size": 77659213,
        "documents": 32176,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-programmers.flat"
    },
    "beir-v1.0.0-cqadupstack-stats.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-stats) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-stats.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-stats.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "c706454f4c953d1023b427447f9df82b",
        "size": 101984055,
        "documents": 42269,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-stats.flat"
    },
    "beir-v1.0.0-cqadupstack-tex.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-tex) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-tex.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-tex.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "4ae95cca232d0ce62c8fc3cdcbb10dce",
        "size": 164385000,
        "documents": 68184,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-tex.flat"
    },
    "beir-v1.0.0-cqadupstack-unix.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-unix) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-unix.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-unix.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "fcb03ccdf02632a5e038279ed288ef52",
        "size": 114349002,
        "documents": 47382,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-unix.flat"
    },
    "beir-v1.0.0-cqadupstack-webmasters.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-webmasters) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-webmasters.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-webmasters.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "aa255ad1f89050003f32b7dca7b065a9",
        "size": 42021462,
        "documents": 17405,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-webmasters.flat"
    },
    "beir-v1.0.0-cqadupstack-wordpress.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (CQADupStack-wordpress) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-cqadupstack-wordpress.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-cqadupstack-wordpress.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "20d24ee757a09eb1c371c47156d5a121",
        "size": 117282936,
        "documents": 48605,
        "downloaded": False,
        "texts": "beir-v1.0.0-cqadupstack-wordpress.flat"
    },
    "beir-v1.0.0-quora.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Quora) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-quora.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-quora.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "8f7944b52e740cde07093d8eedf59919",
        "size": 1261685446,
        "documents": 522931,
        "downloaded": False,
        "texts": "beir-v1.0.0-quora.flat"
    },
    "beir-v1.0.0-dbpedia-entity.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (DBPedia) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-dbpedia-entity.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-dbpedia-entity.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "03b04926a9ff25b62afc63a04fbdb248",
        "size": 11215257018,
        "documents": 4635922,
        "downloaded": False,
        "texts": "beir-v1.0.0-dbpedia-entity.flat"
    },
    "beir-v1.0.0-scidocs.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (SCIDOCS) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-scidocs.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scidocs.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "e6e5367aef57e9102b54b2216f6be659",
        "size": 62465542,
        "documents": 25657,
        "downloaded": False,
        "texts": "beir-v1.0.0-scidocs.flat"
    },
    "beir-v1.0.0-fever.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (FEVER) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-fever.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-fever.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "4d4124a61acff68acd63dba0c5e1bfb0",
        "size": 13095399713,
        "documents": 5416568,
        "downloaded": False,
        "texts": "beir-v1.0.0-fever.flat"
    },
    "beir-v1.0.0-climate-fever.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (Climate-FEVER) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-climate-fever.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-climate-fever.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "d3f0e6fbe8485406c65d01f6370f3a29",
        "size": 13095456071,
        "documents": 5416593,
        "downloaded": False,
        "texts": "beir-v1.0.0-climate-fever.flat"
    },
    "beir-v1.0.0-scifact.cohere-embed-english-v3.0": {
        "description": "Faiss index for BEIR v1.0.0 (SciFact) corpus encoded by cohere-embed-english-v3.0 encoder.",
        "filename": "faiss-flat.beir-v1.0.0-scifact.cohere-embed-english-v3.0.20240302.tar.gz",
        "readme": "faiss-flat.beir-v1.0.0.cohere-embed-english-v3.0.20240302.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss/faiss-flat.beir-v1.0.0-scifact.cohere-embed-english-v3.0.20240302.tar.gz"
        ],
        "md5": "a6cb53c484e4c44588814e5d22f3e22f",
        "size": 12522128,
        "documents": 5183,
        "downloaded": False,
        "texts": "beir-v1.0.0-scifact.flat"
    },
}

FAISS_INDEX_INFO_BRIGHT = {
    "bright-biology.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: biology corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-biology.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-biology.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "6a9490325549d13e59969cef6d8b5d7c",
        "size": 217330251,
        "documents": 57359,
        "downloaded": False,
        "texts": "bright-biology"
    },
    "bright-earth-science.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: earth-science corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-earth-science.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-earth-science.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "6bf6f0ef39a5d7483dff701373483882",
        "size": 459972791,
        "documents": 121249,
        "downloaded": False,
        "texts": "bright-earth-science"
    },
    "bright-economics.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: economics corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-economics.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-economics.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "6fbdfde1f2926024619b6e775bd008dd",
        "size": 189737637,
        "documents": 50220,
        "downloaded": False,
        "texts": "bright-economics"
    },
    "bright-psychology.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: psychology corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-psychology.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-psychology.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "509b90e64e6364e7385781f4f02c4599",
        "size": 200013778,
        "documents": 52835,
        "downloaded": False,
        "texts": "bright-psychology"
    },
    "bright-robotics.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: robotics corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-robotics.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-robotics.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "c0074c762ceac8172d57d1a7612fd4c3",
        "size": 228859778,
        "documents": 61961,
        "downloaded": False,
        "texts": "bright-robotics"
    },
    "bright-stackoverflow.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: stackoverflow corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-stackoverflow.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-stackoverflow.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "63b6bae7e76a26127cd61be20c6c2d41",
        "size": 393734344,
        "documents": 107081,
        "downloaded": False,
        "texts": "bright-stackoverflow"
    },
    "bright-sustainable-living.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: sustainable-living corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-sustainable-living.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-sustainable-living.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "0635388660ecb68fe1309a98a693fe47",
        "size": 229219246,
        "documents": 60792,
        "downloaded": False,
        "texts": "bright-sustainable-living"
    },
    "bright-pony.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: pony corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-pony.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-pony.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "b3de06631f110e51a717d59b56e085ab",
        "size": 29839662,
        "documents": 7894,
        "downloaded": False,
        "texts": "bright-pony"
    },
    "bright-leetcode.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: leetcode corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-leetcode.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-leetcode.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "3cc820d00ddb92203b0121ac7b26ad51",
        "size": 1575964042,
        "documents": 413932,
        "downloaded": False,
        "texts": "bright-leetcode"
    },
    "bright-aops.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: aops corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-aops.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-aops.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "6f742b4e9f8def4b3b1ca052335a17ac",
        "size": 715133646,
        "documents": 188002,
        "downloaded": False,
        "texts": "bright-aops"
    },
    "bright-theoremqa-theorems.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: theoremqa-theorems corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-theoremqa-theorems.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-theoremqa-theorems.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "b5248a39c78824bfb041ae6f870fc993",
        "size": 90727136,
        "documents": 23839,
        "downloaded": False,
        "texts": "bright-theoremqa-theorems"
    },
    "bright-theoremqa-questions.bge-large-en-v1.5": {
        "description": "Faiss flat index for BRIGHT: theoremqa-questions corpus encoded by BGE-large-en-v1.5.",
        "filename": "faiss-flat.bright-theoremqa-questions.bge-large-en-v1.5.20250808.44889d.tar.gz",
        "readme": "faiss-flat.bright.bge-large-en-v1.5.20250808.44889d.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/bge-large-en-v1.5/faiss-flat.bright-theoremqa-questions.bge-large-en-v1.5.20250808.44889d.tar.gz"
        ],
        "md5": "ec5c6223b284509b6fba48658cd9f58f",
        "size": 715133652,
        "documents": 188002,
        "downloaded": False,
        "texts": "bright-theoremqa-questions"
    },
    "bright-aops.diver-retriever-4b": {
        "description": "Faiss index of the aops corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-aops.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-aops.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "f24a104cc686e87c037b5557381d12e4",
        "size": 896829813,
        "documents": 188002,
        "downloaded": False,
        "texts": "bright-aops"
    },
    "bright-biology.diver-retriever-4b": {
        "description": "Faiss index of the biology corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-biology.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-biology.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "e71949be07d506da8e626aaa6b0b446b",
        "size": 273798661,
        "documents": 57359,
        "downloaded": False,
        "texts": "bright-biology"
    },
    "bright-earth-science.diver-retriever-4b": {
        "description": "Faiss index of the earth-science corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-earth-science.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-earth-science.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "81e0507d98bce70f9d2458aaf6593199",
        "size": 579532629,
        "documents": 121249,
        "downloaded": False,
        "texts": "bright-earth-science"
    },
    "bright-economics.diver-retriever-4b": {
        "description": "Faiss index of the economics corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-economics.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-economics.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "d77ba223e474a426a0bda26d2e941c08",
        "size": 239278385,
        "documents": 50220,
        "downloaded": False,
        "texts": "bright-economics"
    },
    "bright-leetcode.diver-retriever-4b": {
        "description": "Faiss index of the leetcode corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-leetcode.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-leetcode.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "4b4ba409add65925c4486979d1a9123c",
        "size": 1976072736,
        "documents": 413932,
        "downloaded": False,
        "texts": "bright-leetcode"
    },
    "bright-pony.diver-retriever-4b": {
        "description": "Faiss index of the pony corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-pony.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-pony.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "16976eb2bc8a7837d04e421c057049cd",
        "size": 37595406,
        "documents": 7894,
        "downloaded": False,
        "texts": "bright-pony"
    },
    "bright-psychology.diver-retriever-4b": {
        "description": "Faiss index of the psychology corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-psychology.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-psychology.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "30c7ffc975ee9197d8521edfa71ea55f",
        "size": 252033353,
        "documents": 52835,
        "downloaded": False,
        "texts": "bright-psychology"
    },
    "bright-robotics.diver-retriever-4b": {
        "description": "Faiss index of the robotics corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-robotics.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-robotics.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "21338a1542c6efc2bac358cd105cf3f1",
        "size": 292835573,
        "documents": 61961,
        "downloaded": False,
        "texts": "bright-robotics"
    },
    "bright-stackoverflow.diver-retriever-4b": {
        "description": "Faiss index of the stackoverflow corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-stackoverflow.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-stackoverflow.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "159dbb15ef3954e9915b0019789258f5",
        "size": 506187162,
        "documents": 107081,
        "downloaded": False,
        "texts": "bright-stackoverflow"
    },
    "bright-sustainable-living.diver-retriever-4b": {
        "description": "Faiss index of the sustainable-living corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-sustainable-living.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-sustainable-living.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "fa13ea9c83956c6305033fa0ccb11711",
        "size": 289525259,
        "documents": 60792,
        "downloaded": False,
        "texts": "bright-sustainable-living"
    },
    "bright-theoremqa-questions.diver-retriever-4b": {
        "description": "Faiss index of the theoremqa-questions corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-theoremqa-questions.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-theoremqa-questions.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "919193a41b11f39fd33a6b7bd26774e6",
        "size": 896822922,
        "documents": 188002,
        "downloaded": False,
        "texts": "bright-theoremqa-questions"
    },
    "bright-theoremqa-theorems.diver-retriever-4b": {
        "description": "Faiss index of the theoremqa-theorems corpus encoded by diver-retriever-4b",
        "filename": "faiss-flat.bright-theoremqa-theorems.diver-retriever-4b.20260227.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.diver-retriever-4b.20260227.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/diver-retriever-4b/faiss-flat.bright-theoremqa-theorems.diver-retriever-4b.20260227.2f9328f.tar.gz"
        ],
        "md5": "14c4a0c3aa6f4325688ecfc4f40efaf8",
        "size": 113670945,
        "documents": 23839,
        "downloaded": False,
        "texts": "bright-theoremqa-theorems"
    },
    "bright-aops.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the aops corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-aops.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-aops.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "76989f371ea044ea2df2336ec3b310a1",
        "size": 897863808,
        "documents": 188002,
        "downloaded": False,
        "texts": "bright-aops"
    },
    "bright-biology.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the biology corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-biology.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-biology.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "141ee65ed539013096a9ba07a8a19365",
        "size": 273894699,
        "documents": 57359,
        "downloaded": False,
        "texts": "bright-biology"
    },
    "bright-earth-science.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the earth-science corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-earth-science.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-earth-science.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "c0176d3d7bd68aaba44b13b31cc339d6",
        "size": 579701998,
        "documents": 121249,
        "downloaded": False,
        "texts": "bright-earth-science"
    },
    "bright-economics.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the economics corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-economics.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-economics.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "b818160492813c7822be5303d506def8",
        "size": 239426214,
        "documents": 50220,
        "downloaded": False,
        "texts": "bright-economics"
    },
    "bright-leetcode.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the leetcode corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-leetcode.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-leetcode.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "71c835683b84cf764bb4c7b0780e40a9",
        "size": 1978373681,
        "documents": 413932,
        "downloaded": False,
        "texts": "bright-leetcode"
    },
    "bright-pony.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the pony corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-pony.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-pony.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "9ba31e11ba4b87b0685e11453d00ad16",
        "size": 37605121,
        "documents": 7894,
        "downloaded": False,
        "texts": "bright-pony"
    },
    "bright-psychology.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the psychology corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-psychology.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-psychology.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "801632d677dd725c115959a3dc4f4a89",
        "size": 252124461,
        "documents": 52835,
        "downloaded": False,
        "texts": "bright-psychology"
    },
    "bright-robotics.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the robotics corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-robotics.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-robotics.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "6c0b2ffc294ab44c68718c45e7ca06eb",
        "size": 293018660,
        "documents": 61961,
        "downloaded": False,
        "texts": "bright-robotics"
    },
    "bright-stackoverflow.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the stackoverflow corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-stackoverflow.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-stackoverflow.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "c1bef66533ee8df89bf145f2bf94b820",
        "size": 506544282,
        "documents": 107081,
        "downloaded": False,
        "texts": "bright-stackoverflow"
    },
    "bright-sustainable-living.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the sustainable-living corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-sustainable-living.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-sustainable-living.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "8eb33615cad468c79dfbd05ff305e96b",
        "size": 289587208,
        "documents": 60792,
        "downloaded": False,
        "texts": "bright-sustainable-living"
    },
    "bright-theoremqa-questions.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the theoremqa-questions corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-theoremqa-questions.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-theoremqa-questions.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "5e68ee39688e13e484c3118657513489",
        "size": 897852243,
        "documents": 188002,
        "downloaded": False,
        "texts": "bright-theoremqa-questions"
    },
    "bright-theoremqa-theorems.reason-embed-qwen3-4b-0928": {
        "description": "Faiss index of the theoremqa-theorems corpus encoded by reason-embed-qwen3-4b-0928",
        "filename": "faiss-flat.bright-theoremqa-theorems.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz",
        "readme": "faiss-flat.bright.reason-embed-qwen3-4b-0928.20260226.2f9328f.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-bright/resolve/main/faiss-flat/reason-embed-qwen3-4b-0928/faiss-flat.bright-theoremqa-theorems.reason-embed-qwen3-4b-0928.20260226.2f9328f.tar.gz"
        ],
        "md5": "090cf3019dc98a09141a49da8b5f48fd",
        "size": 113826179,
        "documents": 23839,
        "downloaded": False,
        "texts": "bright-theoremqa-theorems"
    }
}

FAISS_INDEX_INFO_MRTYDI = {
    "mrtydi-v1.1-arabic-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-arabic.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220207.5df364.tar.gz"
        ],
        "md5": "de86c1ce43854bbeea4e3af5d95d6ffb",
        "size": 5997718937,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic"
    },
    "mrtydi-v1.1-bengali-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-bengali.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220207.5df364.tar.gz"
        ],
        "md5": "e60cb6f1f7139cf0551f0ba4e4e83bf6",
        "size": 865716848,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali"
    },
    "mrtydi-v1.1-english-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-english.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-english.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220207.5df364.tar.gz"
        ],
        "md5": "a0a8cc39e8af782ec82188a18c4c97c3",
        "size": 93585951488,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-finnish.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220207.5df364.tar.gz"
        ],
        "md5": "3e4e18aacf07ca551b474315f267ead6",
        "size": 5435516778,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-indonesian.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220207.5df364.tar.gz"
        ],
        "md5": "0bf693e4046d9a565ae18b9f5939d193",
        "size": 4179177829,
        "documents": 4179177829,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-japanese.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220207.5df364.tar.gz"
        ],
        "md5": "4ba566e27bc0158108259b18a153e2fc",
        "size": 19920816424,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-korean.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-korean.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220207.5df364.tar.gz"
        ],
        "md5": "44212e5722632d5bcb14f0680741638c",
        "size": 4257414237,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-russian.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-russian.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220207.5df364.tar.gz"
        ],
        "md5": "e7634093f2a3362928e9699441ce8a3b",
        "size": 27317759143,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-swahili.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220207.5df364.tar.gz"
        ],
        "md5": "5061bdd1d81bc32490bbb3682096acdd",
        "size": 389658394,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-telugu.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220207.5df364.tar.gz"
        ],
        "md5": "4952dacaeae89185d3757f9f26af4e88",
        "size": 1561173721,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-thai.20220207.5df364.tar.gz",
        "readme": "faiss.mrtydi-v1.1-thai.20220207.5df364.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220207.5df364.tar.gz"
        ],
        "md5": "2458f704b277fa8ffe2509b6296892a0",
        "size": 1616059846,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    },

    "mrtydi-v1.1-arabic-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "bafb6fb2c530567dec26aa4597c6ee25",
        "size": 5997944387,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic",
    },
    "mrtydi-v1.1-bengali-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "d04bb6e634fb4f7df23dbff7481a8f9b",
        "size": 865733182,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali",
    },
    "mrtydi-v1.1-english-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-english.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "4a93a2211199f7359cc99486a9f93d02",
        "size": 93594560123,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "6cbe2d52225fb15a494857b9df593113",
        "size": 5436419128,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "26108a7ee1fc5ac15e0b7fcecf4d39ad",
        "size": 4178791340,
        "documents": 1469399,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "2ef2b5e3f5778d99e65aafc48450508a",
        "size": 19918319659,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-korean.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "26ed9be031603019304b66f985ce154c",
        "size": 4256863020,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-russian.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "b1be7a45a702be4021f38425c0001f39",
        "size": 27318554290,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "14edb5f677820b5a5a3858555e900591",
        "size": 389600489,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "25b37f5d7a035a17b447f1732e241b85",
        "size": 1561420074,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.mrtydi-v1.1-thai.20220413.aa1c0e9.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220413.aa1c0e9.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220413.aa1c0e9.tar.gz",
        ],
        "md5": "0544ce677fa31b633a29a079c0cdfc82",
        "size": 1616716171,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    },

    "mrtydi-v1.1-arabic-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220523.7b099d5.tar.gz",
        ],
        "md5": "3d764e7936bb6beb5308ccfd6717b38e",
        "size": 5988743258,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic"
    },
    "mrtydi-v1.1-bengali-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220523.7b099d5.tar.gz",
        ],
        "md5": "2ee8e550245f7eb5184c27fe3369d818",
        "size": 864358280,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali"
    },
    "mrtydi-v1.1-english-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-english.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220523.7b099d5.tar.gz",
        ],
        "md5": "a1be61486c209bf2545d63f950274a99",
        "size": 93435965796,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220523.7b099d5.tar.gz",
        ],
        "md5": "0dbd873fa8bf8c87052940bdf4097ba2",
        "size": 5427976705,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220523.7b099d5.tar.gz",
        ],
        "md5": "937f7c03e2386166e34ef81b25d7959f",
        "size": 4172976570,
        "documents": 4179177829,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220523.7b099d5.tar.gz",
        ],
        "md5": "21a64d1a012a854d4bf42fa24c8712fd",
        "size": 19890571158,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-korean.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220523.7b099d5.tar.gz",
        ],
        "md5": "ed3216fb5bc431ac52931b58cc4c4d0f",
        "size": 4250320804,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-russian.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220523.7b099d5.tar.gz",
        ],
        "md5": "c3c4db1397c7125f8e411cf637054148",
        "size": 27278520787,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220523.7b099d5.tar.gz",
        ],
        "md5": "20235115c0a877e11c91cb662d5a6fdb",
        "size": 389244265,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220523.7b099d5.tar.gz",
        ],
        "md5": "86cae6fe8f8c08489e49b6e6c28a09b0",
        "size": 1558691592,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-tied-pft-nq": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-thai.20220523.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220523.7b099d5.mdpr-tied-pft-nq.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220523.7b099d5.tar.gz",
        ],
        "md5": "3ba9c64a9f7479bd2e3a84a816ee0f6f",
        "size": 1613563144,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    },

    "mrtydi-v1.1-arabic-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-arabic.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-arabic.20220524.7b099d5.tar.gz"
        ],
        "md5": "9ea47ae7425fd3376f015ca7c6ba5134",
        "size": 5993958479,
        "documents": 2106586,
        "downloaded": False,
        "texts": "mrtydi-v1.1-arabic"
    },
    "mrtydi-v1.1-bengali-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-bengali.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-bengali.20220524.7b099d5.tar.gz"
        ],
        "md5": "d1e75f4960a723b068bb778a972ffb54",
        "size": 865412932,
        "documents": 304059,
        "downloaded": False,
        "texts": "mrtydi-v1.1-bengali"
    },
    "mrtydi-v1.1-english-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-english.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-english.20220524.7b099d5.tar.gz"
        ],
        "md5": "1fce43e549ff57bbac432a579961f34b",
        "size": 93697654837,
        "documents": 32907100,
        "downloaded": False,
        "texts": "mrtydi-v1.1-english"
    },
    "mrtydi-v1.1-finnish-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-finnish.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-finnish.20220524.7b099d5.tar.gz"
        ],
        "md5": "6faa7b2fe8ad4b9ca284bd7e8f69b727",
        "size": 5433647583,
        "documents": 1908757,
        "downloaded": False,
        "texts": "mrtydi-v1.1-finnish"
    },
    "mrtydi-v1.1-indonesian-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-indonesian.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-indonesian.20220524.7b099d5.tar.gz"
        ],
        "md5": "659b1e0a1bea46f62a842b55385085b7",
        "size": 4177273338,
        "documents": 4179177829,
        "downloaded": False,
        "texts": "mrtydi-v1.1-indonesian"
    },
    "mrtydi-v1.1-japanese-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-japanese.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-japanese.20220524.7b099d5.tar.gz"
        ],
        "md5": "126c82da9e0e0e1fd290cf62d7fe4dfa",
        "size": 19917667830,
        "documents": 7000027,
        "downloaded": False,
        "texts": "mrtydi-v1.1-japanese"
    },
    "mrtydi-v1.1-korean-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-korean.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-korean.20220524.7b099d5.tar.gz"
        ],
        "md5": "cf07b71aaefba58bbe150265f6696503",
        "size": 4256039967,
        "documents": 1496126,
        "downloaded": False,
        "texts": "mrtydi-v1.1-korean"
    },
    "mrtydi-v1.1-russian-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-russian.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-russian.20220524.7b099d5.tar.gz"
        ],
        "md5": "c0a53fa6428cb9b1399a90e3a9a805d5",
        "size": 27315435288,
        "documents": 9597504,
        "downloaded": False,
        "texts": "mrtydi-v1.1-russian"
    },
    "mrtydi-v1.1-swahili-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-swahili.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-swahili.20220524.7b099d5.tar.gz"
        ],
        "md5": "93dc3f3453815c92f3bccf4f41c5f2d4",
        "size": 389336970,
        "documents": 136689,
        "downloaded": False,
        "texts": "mrtydi-v1.1-swahili"
    },
    "mrtydi-v1.1-telugu-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-telugu.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-telugu.20220524.7b099d5.tar.gz"
        ],
        "md5": "7aba1b7ee36e572bd982b3f62f41c380",
        "size": 1560353621,
        "documents": 548224,
        "downloaded": False,
        "texts": "mrtydi-v1.1-telugu"
    },
    "mrtydi-v1.1-thai-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for Mr.TyDi v1.1 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on NQ.",
        "filename": "faiss.mrtydi-v1.1-thai.20220524.7b099d5.tar.gz",
        "readme": "faiss.mrtydi-v1.1.20220524.7b099d5.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.mrtydi-v1.1-thai.20220524.7b099d5.tar.gz"
        ],
        "md5": "57151073a4c0d90b64242e4536a3af75",
        "size": 1615313134,
        "documents": 568855,
        "downloaded": False,
        "texts": "mrtydi-v1.1-thai"
    }
}

FAISS_INDEX_INFO_MIRACL = {
    "miracl-v1.0-ar-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "177d47e9a802c87abca52380ad1ce83b",
        "size": 5870688114,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar",
    },
    "miracl-v1.0-bn-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "156e8ba8cd369b1c4a606e28ea025b2e",
        "size": 846825797,
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn",
    },
    "miracl-v1.0-en-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "ce00518f54b130a157112c2a1b2d0980",
        "size": 93554329940,
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "d7a9627bb60e901386f455ba6c9063ac",
        "size": 29553300438,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "e8b59e3eb2e08f61f81569c6d4c85350",
        "size": 6286832343,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "a82d6e6cf964d2e4cfac99cf14cbcc35",
        "size": 5366191108,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "a952d944aa63dcee604c8357f1be18db",
        "size": 41648462352,
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "9d1dc4b948edf3df263977d82c9fcc3f",
        "size": 1440625237,
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "19815233f5cc3a198b88cdb990459637",
        "size": 4115281733,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "6e9b6e304b2b1a192a3d81e55880f971",
        "size": 19791966022,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "ea1fa34341fc5d5ea88e5b633025d2d5",
        "size": 4231563143,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-ko"
    },
    "miracl-v1.0-ru-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "4325e716ee6af5ea2b73d4b25f1ad76c",
        "size": 27173380025,
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "2b879dac6823077ae497ba8ebfce523b",
        "size": 376181743,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "a3dfb8ba31f316c93d1fd147f88fbbfd",
        "size": 1476021093,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "cb0c9b84a80ff338372b32857c58368d",
        "size": 1541590102,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "2743dfaa794b7abbef1d3c912c5cc4b5",
        "size": 14046912278,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh",
    },
    "miracl-v1.0-de-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (German) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "1abcf3aac78e30ebe7a75163412f1c84",
        "size": 45154018897,
        "documents": 15866222,
        "downloaded": False,
        "texts": "miracl-v1.0-de",
    },
    "miracl-v1.0-yo-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Yoruba) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco.20221004.2b2856.tar.gz"
        ],
        "md5": "2ad15ea0576ae3284082ae661e001faa",
        "size": 139412730,
        "documents": 49043,
        "downloaded": False,
        "texts": "miracl-v1.0-yo",
    },

    "miracl-v1.0-ar-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "428fbde84d2c18e48f0821298947a9d1",
        "size": 5866199790,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar",
    },
    "miracl-v1.0-bn-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "4394a09e043be9be5b820814a82fc8ac",
        "size": 846476050,
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn",
    },
    "miracl-v1.0-en-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "5bd57f5e4daf93294fd2cbd969c05bb3",
        "size": 93527497283,
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "b6db16c1ab0ae95fec0465299c660d2a",
        "size": 29544413180,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "2a2825706211eb96bd3dbb616463c661",
        "size": 6283957262,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "65719de730cda3fa5f6a8a75611db6eb",
        "size": 5363289277,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "24eb2f63f78aa1e39b1ea61e20661424",
        "size": 41635104326,
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "d08aad08a8592aa40355fb7d50afd170",
        "size": 1439798033,
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "b02c20d4fc27e390ec5b1e9ca732dc5a",
        "size": 4113737773,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a5f219c7f46a36c5c7a2555fbdaa0479",
        "size": 19790154560,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "67b2a803eab3491a057d4ac6b81974f1",
        "size": 4230830690,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-ko"
    },
    "miracl-v1.0-ru-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "edad6d5cb508de61ba84173d0ad2aa31",
        "size": 27169921407,
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "0b039d766b55f678102a59a6e050d0bc",
        "size": 375865677,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "ea21915c69f70f41acadee4b6b83d129",
        "size": 1474866678,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a5875b473109310789710e2f3df91b0f",
        "size": 1540180247,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "a2d233e792d46c20c912d10afff033f5",
        "size": 14043150097,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh",
    },
    "miracl-v1.0-de-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-de.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "d53da12ae6119ed54ef968e968f8520a",
        "size": 45139752128,
        "documents": 15866222,
        "downloaded": False,
        "texts": "miracl-v1.0-de",
    },
    "miracl-v1.0-yo-mdpr-tied-pft-msmarco-ft-all": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz",
        "readme": "faiss.miracl-v1.0.20221004.2b2856.mdpr-tied-pft-msmarco-ft-all.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-yo.mdpr-tied-pft-msmarco-ft-all.20221004.2b2856.tar.gz"
        ],
        "md5": "0a1b0f48108508724a3892dfc04eb756",
        "size": 139286213,
        "documents": 49043,
        "downloaded": False,
        "texts": "miracl-v1.0-yo",
    },

    "miracl-v1.0-ar-mdpr-tied-pft-msmarco-ft-miracl-ar": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-miracl-ar.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mdpr-tied-pft-msmarco-ft-miracl-ar.20230329.e40d4a.tar.gz",
        ],
        "md5": "29cdb7fa7cc52cabc32791d57be3bd42",
        "size": 5871030506,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar"
    },
    "miracl-v1.0-bn-mdpr-tied-pft-msmarco-ft-miracl-bn": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-miracl-bn.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mdpr-tied-pft-msmarco-ft-miracl-bn.20230329.e40d4a.tar.gz",
        ],
        "md5": "8972166564a9c13e102ae83ea062c166",
        "size": 846236944,
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn"
    },
    "miracl-v1.0-en-mdpr-tied-pft-msmarco-ft-miracl-en": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-miracl-en.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mdpr-tied-pft-msmarco-ft-miracl-en.20230329.e40d4a.tar.gz",
        ],
        "md5": "cd43e6c93879a107b94396a42aa7c987",
        "size": 93502848095,
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mdpr-tied-pft-msmarco-ft-miracl-es": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-miracl-es.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mdpr-tied-pft-msmarco-ft-miracl-es.20230329.e40d4a.tar.gz",
        ],
        "md5": "4f45c3171690dd691afcfc9e45b89494",
        "size": 29552466540,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mdpr-tied-pft-msmarco-ft-miracl-fa": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-miracl-fa.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mdpr-tied-pft-msmarco-ft-miracl-fa.20230329.e40d4a.tar.gz",
        ],
        "md5": "ae262fea849f6903c93e1f3269e07804",
        "size": 6287728719,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mdpr-tied-pft-msmarco-ft-miracl-fi": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-miracl-fi.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mdpr-tied-pft-msmarco-ft-miracl-fi.20230329.e40d4a.tar.gz",
        ],
        "md5": "12c5c5c4dd8df37ad8ae90039851fbec",
        "size": 5367069541,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mdpr-tied-pft-msmarco-ft-miracl-fr": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-miracl-fr.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mdpr-tied-pft-msmarco-ft-miracl-fr.20230329.e40d4a.tar.gz",
        ],
        "md5": "8cf28f8df0805a848cb5c54d5f5d8bfb",
        "size": 41654288474,
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mdpr-tied-pft-msmarco-ft-miracl-hi": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-miracl-hi.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mdpr-tied-pft-msmarco-ft-miracl-hi.20230329.e40d4a.tar.gz",
        ],
        "md5": "f579dfa45a5f14c48f97ba9980f7dec8",
        "size": 1440859085,
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mdpr-tied-pft-msmarco-ft-miracl-id": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-miracl-id.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mdpr-tied-pft-msmarco-ft-miracl-id.20230329.e40d4a.tar.gz",
        ],
        "md5": "d5b540fb82fe21c1fd2b56e248184af6",
        "size": 4111428848,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mdpr-tied-pft-msmarco-ft-miracl-ja": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-miracl-ja.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mdpr-tied-pft-msmarco-ft-miracl-ja.20230329.e40d4a.tar.gz",
        ],
        "md5": "e7ad21b12a7d5e937c55d49184d68814",
        "size": 19790420501,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mdpr-tied-pft-msmarco-ft-miracl-ko": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-miracl-ko.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mdpr-tied-pft-msmarco-ft-miracl-ko.20230329.e40d4a.tar.gz",
        ],
        "md5": "c31290dfae5429549500759279af3a8d",
        "size": 4230154713,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-ko"
    },
    "miracl-v1.0-ru-mdpr-tied-pft-msmarco-ft-miracl-ru": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-miracl-ru.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mdpr-tied-pft-msmarco-ft-miracl-ru.20230329.e40d4a.tar.gz",
        ],
        "md5": "b9460efd096292a1012ab1d27082498e",
        "size": 27177739148,
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mdpr-tied-pft-msmarco-ft-miracl-sw": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-miracl-sw.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mdpr-tied-pft-msmarco-ft-miracl-sw.20230329.e40d4a.tar.gz",
        ],
        "md5": "526a930a27353462e11cc7e1b794dcc7",
        "size": 375865597,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mdpr-tied-pft-msmarco-ft-miracl-te": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-miracl-te.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mdpr-tied-pft-msmarco-ft-miracl-te.20230329.e40d4a.tar.gz",
        ],
        "md5": "f64b28542afdd15b2fe3831972bcd91e",
        "size": 1475895517,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mdpr-tied-pft-msmarco-ft-miracl-th": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-miracl-th.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mdpr-tied-pft-msmarco-ft-miracl-th.20230329.e40d4a.tar.gz",
        ],
        "md5": "b6ba6d5363bf07a5dc8e1cd35fe11e93",
        "size": 1540581013,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mdpr-tied-pft-msmarco-ft-miracl-zh": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO, then fine-tuned in-language with MIRACL.",
        "filename": "faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-miracl-zh.20230329.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.mdpr-tied-pft-msmarco-ft-miracl.20230329.e40d4a.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mdpr-tied-pft-msmarco-ft-miracl-zh.20230329.e40d4a.tar.gz",
        ],
        "md5": "feba34e41cb8234988f7fb99bd8998f3",
        "size": 14049243202,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh"
    },

    "miracl-v1.0-ar-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Arabic) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ar.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ar.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "80c18ac84922ae27bfbee881485816c6",
        "size": 5861079368,
        "documents": 2061414,
        "downloaded": False,
        "texts": "miracl-v1.0-ar",
    },
    "miracl-v1.0-bn-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Bengali) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-bn.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-bn.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "08191b7749151a7bc70e54b92988dd25",
        "size": 845828394, 
        "documents": 297265,
        "downloaded": False,
        "texts": "miracl-v1.0-bn",
    },
    "miracl-v1.0-en-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (English) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-en.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-en.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "a460d0eb95cf8a278686531e13141d00",
        "size": 93426889457, 
        "documents": 32893221,
        "downloaded": False,
        "texts": "miracl-v1.0-en"
    },
    "miracl-v1.0-es-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Spanish) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-es.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-es.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "936e9188c4dcf57f8f116b9e25790372",
        "size": 29499200527,
        "documents": 10373953,
        "downloaded": False,
        "texts": "miracl-v1.0-es"
    },
    "miracl-v1.0-fa-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Persian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fa.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fa.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "58f83135ecafae6993e49f5f08e471ff",
        "size": 6278766617,
        "documents": 2207172,
        "downloaded": False,
        "texts": "miracl-v1.0-fa"
    },
    "miracl-v1.0-fi-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Finnish) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "b10bc504213199fe0c0972678ab4fdd6",
        "size": 5358004166,
        "documents": 1883509,
        "downloaded": False,
        "texts": "miracl-v1.0-fi"
    },
    "miracl-v1.0-fr-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (French) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-fr.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-fr.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "b0d5543824b456d9008d05d7dcef5272",
        "size": 41578767020, 
        "documents": 14636953,
        "downloaded": False,
        "texts": "miracl-v1.0-fr"
    },
    "miracl-v1.0-hi-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Hindi) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-hi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-hi.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "ba66e98169b22244c7a7a89ae9bfe549", 
        "size": 1439122724, 
        "documents": 506264,
        "downloaded": False,
        "texts": "miracl-v1.0-hi"
    },
    "miracl-v1.0-id-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Indonesian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-id.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-id.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "700466ab62bfd4b0ceddff7aa9b7a5f8",
        "size": 4113610061,
        "documents": 1446315,
        "downloaded": False,
        "texts": "miracl-v1.0-id"
    },
    "miracl-v1.0-ja-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Japanese) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ja.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ja.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "f0358ae58b32456c3cef5f71e83a0143",
        "size": 19772957772,
        "documents": 6953614,
        "downloaded": False,
        "texts": "miracl-v1.0-ja"
    },
    "miracl-v1.0-ko-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Korean) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ko.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ko.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "fa00afb61fa4332c408069cb6eb2e8f2",
        "size": 4229330667,
        "documents": 1486752,
        "downloaded": False,
        "texts": "miracl-v1.0-ko"
    },
    "miracl-v1.0-ru-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Russian) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-ru.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-ru.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "118835c214f7b24997ab9f1744b3f5ee",
        "size": 27155045095, 
        "documents": 9543918,
        "downloaded": False,
        "texts": "miracl-v1.0-ru"
    },
    "miracl-v1.0-sw-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Swahili) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-sw.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-sw.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "ae45812eadb685c672f7b19c084ae3bc",
        "size": 375416284,
        "documents": 131924,
        "downloaded": False,
        "texts": "miracl-v1.0-sw"
    },
    "miracl-v1.0-te-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Telugu) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-te.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-te.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "8cbea3c141002dd477a15b387350ea37",
        "size": 1474250608,
        "documents": 518079,
        "downloaded": False,
        "texts": "miracl-v1.0-te"
    },
    "miracl-v1.0-th-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Thai) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-th.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-th.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "58cd7d862f202ece45dbd4cb6b6d12f4",
        "size": 1540980581,
        "documents": 542166,
        "downloaded": False,
        "texts": "miracl-v1.0-th"
    },
    "miracl-v1.0-zh-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Chinese) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-zh.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-zh.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "d8800abe1ac22b4161704f2b6d4fe575",
        "size": 14034991692,
        "documents": 4934368,
        "downloaded": False,
        "texts": "miracl-v1.0-zh",
    },
    "miracl-v1.0-de-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (German) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-de.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-de.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "218cb42441af355285fbf219e9d2d7c7",
        "size": 45085913144,
        "documents": 15866222,
        "downloaded": False,
        "texts": "miracl-v1.0-de",
    },
    "miracl-v1.0-yo-mcontriever-pft-msmarco": {
        "description": "Faiss index for MIRACL v1.0 (Yoruba) corpus encoded by mContriever passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.miracl-v1.0-yo.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz",
        "readme": "faiss.miracl-v1.0.20230313.e40d4a.mcontriever-tied-pft-msmarco.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.miracl-v1.0-yo.mcontriever-tied-pft-msmarco.20230313.e40d4a.tar.gz"
        ],
        "md5": "f8aee10055a31914c4c214819a7c1890",
        "size": 139276690,
        "documents": 49043,
        "downloaded": False,
        "texts": "miracl-v1.0-yo",
    }

}

FAISS_INDEX_INFO_CIRAL = {
    "ciral-v1.0-ha-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Hausa) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-ha.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-ha.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "1feb2fb70d16117bd588f7d2168758c8",
        "size": 2023010636,
        "documents": 715355,
        "downloaded": False,
        "texts": "ciral-v1.0-ha"
    },

    "ciral-v1.0-so-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Somali) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-so.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-so.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "eb5a9ab2c0aea0939768980f93bd28a2",
        "size": 2356035207,
        "documents": 827552,
        "downloaded": False,
        "texts": "ciral-v1.0-so"
    },

    "ciral-v1.0-sw-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Swahili) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-sw.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-sw.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "0a0412eadf7fb8895bbc6d7090019352",
        "size": 2689038831,
        "documents": 949013,
        "downloaded": False,
        "texts": "ciral-v1.0-sw"
    },

    "ciral-v1.0-yo-mdpr-tied-pft-msmarco": {
        "description": "Faiss index for CIRAL v1.0 (Yoruba) corpus encoded by mDPR passage encoder pre-fine-tuned on MS MARCO.",
        "filename": "faiss.ciral-v1.0-yo.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz",
        "readme": "faiss.ciral-v1.0.mdpr-tied-pft-msmarco.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-yo.mdpr-tied-pft-msmarco.20240212.2154e7.tar.gz"
        ],
        "md5": "0f84c7f8594b6352aa26970565877668",
        "size": 233478586,
        "documents": 82095,
        "downloaded": False,
        "texts": "ciral-v1.0-yo"
    },

    "ciral-v1.0-ha-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Hausa) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-ha.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-ha.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "809f7c3c211c019a345e7bc8a716ff7b",
        "size": 2023992713,
        "documents": 715355,
        "downloaded": False,
        "texts": "ciral-v1.0-ha"
    },

    "ciral-v1.0-so-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Somali) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-so.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-so.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "0ef7404ef10f3135f6a11addcf723504",
        "size": 2356542027,
        "documents": 827552,
        "downloaded": False,
        "texts": "ciral-v1.0-so"
    },

    "ciral-v1.0-sw-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Swahili) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-sw.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-sw.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "1951d3f61eef760407c66c426e5047c6",
        "size": 2688836925,
        "documents": 949013,
        "downloaded": False,
        "texts": "ciral-v1.0-sw"
    },

    "ciral-v1.0-yo-afriberta-dpr-ptf-msmarco-ft-latin-mrtydi": {
        "description": "Faiss index for CIRAL v1.0 (Yoruba) corpus encoded by Afriberta-DPR passage encoder pre-fine-tuned on MS MARCO and fine-tuned on Latin languages in Mr. TyDi.",
        "filename": "faiss.ciral-v1.0-yo.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz",
        "readme": "faiss.ciral-v1.0.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20240212.2154e7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.ciral-v1.0-yo.afriberta-dpr-ptf-msmarco-ft-latin-mrtydi.20230814.b56d04.tar.gz"
        ],
        "md5": "f433299809c659cfc4dede6c42d4a3fd",
        "size": 233490804,
        "documents": 82095,
        "downloaded": False,
        "texts": "ciral-v1.0-yo"
    },
}

FAISS_INDEX_INFO_WIKIPEDIA = {
    "wikipedia-dpr-100w.dpr-multi": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on multiple QA datasets",
        "filename": "faiss.wikipedia-dpr-100w.dpr_multi.20200127.f403c3.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dpr_multi.20200127.f403c3.tar.gz"
        ],
        "md5": "fe307ef2e60ab6e6f3ad66e24a4144ae",
        "size": 59836766732,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.dpr-single-nq": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the DPR doc encoder trained on NQ",
        "filename": "faiss.wikipedia-dpr-100w.dpr_single-nq.20200115.cd5034.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dpr_single-nq.20200115.cd5034.tar.gz"
        ],
        "md5": "01fb6bcaa047df254663d0a3d854b7cc",
        "size": 59836863979,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.bpr-single-nq": {
        "description": "Faiss binary index of Wikipedia encoded by the BPR doc encoder trained on NQ",
        "filename": "faiss.wikipedia-dpr-100w.bpr_single-nq.20210827.8a8f75.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.bpr_single-nq.20210827.8a8f75.tar.gz"
        ],
        "md5": "b022580ab2fc66f6eaa54af241dba690",
        "size": 1886380629,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.ance-multi": {
        "description": "Faiss FlatIP index of Wikipedia encoded by the ANCE-multi encoder",
        "filename": "faiss.wikipedia-dpr-100w.ance_multi.20210224.060cef.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.ance_multi.20210224.060cef.tar.gz"
        ],
        "md5": "eb00e096460c8e6296a39732f1676dd7",
        "size": 59890491335,
        "documents": 21015320,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.dkrr-nq": {
        "description": "Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on NQ",
        "filename": "faiss.wikipedia-dpr-100w.dkrr-dpr-nq-retriever.20220217.25ed1f.cc91b2.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dkrr-dpr-nq-retriever.20220217.25ed1f.cc91b2.tar.gz",
        ],
        "md5": "36a658e08dafb3e3313b05f88e001557",
        "size": 37812137732,
        "documents": 21015324,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wikipedia-dpr-100w.dkrr-tqa": {
        "description": "Faiss FlatIP index of Wikipedia DPR encoded by the retriever model from 'Distilling Knowledge from Reader to Retriever for Question Answering' trained on TriviaQA",
        "filename": "faiss.wikipedia-dpr-100w.dkrr-dpr-tqa-retriever.20220217.25ed1f.cc91b2.tar.gz",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wikipedia-dpr-100w.dkrr-dpr-tqa-retriever.20220217.25ed1f.cc91b2.tar.gz",
        ],
        "md5": "072a514ca3ff7717339038d024019e3d",
        "size": 37802648577,
        "documents": 21015324,
        "downloaded": False,
        "texts": "wikipedia-dpr-100w"
    },
    "wiki-all-6-3.dpr2-multi-retriever": {
        "description": "Faiss FlatIP index of wiki-all-6-3-tamber encoded by a 2nd iteration DPR model trained on multiple QA datasets",
        "filename": "faiss.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.tar.gz",
        "readme": "faiss-flat.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.README.md",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/faiss.wiki-all-6-3.dpr2-multi-retriever.20230103.186fa7.tar.gz",
        ],
        "md5": "823b6297d6fd8011598e7618742ac7f8",
        "size": 218257913366,
        "documents": 76680040,
        "downloaded": False,
        "texts": "wiki-all-6-3-tamber"
    }
}

FAISS_INDEX_INFO_M_BEIR = {
    "m-beir-cirr_task7.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR CIRR task 7 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-cirr-task7.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-cirr-task7.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "2df0ed1aa8d405148977a74218748db6",
        "size": 38817422,
        "documents": 21551,
        "downloaded": False,
        "texts": "m-beir-cirr_task7"
    },
    "m-beir-edis_task2.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR EDIS task 2 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-edis-task2.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-edis-task2.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "f507b70f48facec1de962fd7b2ce617d",
        "size": 1889309291,
        "documents": 1047067,
        "downloaded": False,
        "texts": "m-beir-edis_task2"
    },
    "m-beir-fashion200k_task0.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR Fashion200k task 0 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-fashion200k-task0.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-fashion200k-task0.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "e5fe87d779545ef493ee5740e2b075c8",
        "size": 362431088,
        "documents": 201824,
        "downloaded": False,
        "texts": "m-beir-fashion200k_task0"
    },
    "m-beir-fashion200k_task3.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR Fashion200k task 3 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-fashion200k-task3.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-fashion200k-task3.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "f1d419f3b711b3614300e136e391e63e",
        "size": 111419375,
        "documents": 61707,
        "downloaded": False,
        "texts": "m-beir-fashion200k_task3"
    },
    "m-beir-fashioniq_task7.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR FashionIQ task 7 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-fashioniq-task7.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-fashioniq-task7.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "77504ab31f03bcf397a5ec3c20864eaf",
        "size": 134235025,
        "documents": 74381,
        "downloaded": False,
        "texts": "m-beir-fashioniq_task7"
    },
    "m-beir-infoseek_task6.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR InfoSeek task 6 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-infoseek-task6.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-infoseek-task6.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "e471f7cf13c3ba4cdf0233d9e74f9ee8",
        "size": 1106428847,
        "documents": 611651,
        "downloaded": False,
        "texts": "m-beir-infoseek_task6"
    },
    "m-beir-infoseek_task8.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR InfoSeek task 8 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-infoseek-task8.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-infoseek-task8.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "ba5b02f2e97086ddced32d9af730d841",
        "size": 870321158,
        "documents": 481782,
        "downloaded": False,
        "texts": "m-beir-infoseek_task8"
    },
    "m-beir-mscoco_task0.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR MSCOCO task 0 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-mscoco-task0.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-mscoco-task0.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "d015ea6b4b2014722e81bd500999b12b",
        "size": 9018762,
        "documents": 5000,
        "downloaded": False,
        "texts": "m-beir-mscoco_task0"
    },
    "m-beir-mscoco_task3.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR MSCOCO task 3 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-mscoco-task3.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-mscoco-task3.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "ba172cbbca9903561a4fe522d2349fb5",
        "size": 44898554,
        "documents": 24809,
        "downloaded": False,
        "texts": "m-beir-mscoco_task3"
    },
    "m-beir-nights_task4.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR NIGHTS task 4 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-nights-task4.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-nights-task4.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "f4dbd632d15efd7eb5abfb0ffc5484af",
        "size": 72057798,
        "documents": 40038,
        "downloaded": False,
        "texts": "m-beir-nights_task4"
    },
    "m-beir-oven_task6.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR OVEN task 6 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-oven-task6.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-oven-task6.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "589ebd6326ab1de2329d70840470e5ab",
        "size": 1224166256,
        "documents": 676667,
        "downloaded": False,
        "texts": "m-beir-oven_task6"
    },
    "m-beir-oven_task8.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR OVEN task 8 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-oven-task8.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-oven-task8.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "ecf91e65de23aa90971a7c2c395cc485",
        "size": 605524879,
        "documents": 335135,
        "downloaded": False,
        "texts": "m-beir-oven_task8"
    },
    "m-beir-visualnews_task0.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR VisualNews task 0 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-visualnews-task0.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-visualnews-task0.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "73742e95859b11ac1d3d8692d06e73b2",
        "size": 978318460,
        "documents": 542246,
        "downloaded": False,
        "texts": "m-beir-visualnews_task0"
    },
    "m-beir-visualnews_task3.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR VisualNews task 3 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-visualnews-task3.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-visualnews-task3.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "73f3245e40c1684bb4d74c532a65cb45",
        "size": 972353309,
        "documents": 537568,
        "downloaded": False,
        "texts": "m-beir-visualnews_task3"
    },
    "m-beir-webqa_task1.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR WebQA task 1 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-webqa-task1.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-webqa-task1.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "0cda2d38ce2218607c31a129997a79f1",
        "size": 983308425,
        "documents": 544457,
        "downloaded": False,
        "texts": "m-beir-webqa_task1"
    },
    "m-beir-webqa_task2.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR WebQA task 2 corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-webqa-task2.clip-sf-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-webqa-task2.clip-sf-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "1b138a7749e4f1272f39eb9c2ae0f18a",
        "size": 726335240,
        "documents": 403196,
        "downloaded": False,
        "texts": "m-beir-webqa_task2"
    },
    "m-beir-union.clip-sf-large": {
        "description": "Faiss FlatIP index of the MBEIR global (union) corpus encoded by UniIR's clip-sf-large model",
        "filename": "faiss-flat.m-beir-union.clip-sf-large.20260302.tar.gz",
        "readme": "faiss-flat.m-beir.clip-sf-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/CLIP_SF/faiss-flat.m-beir-union.clip-sf-large.20260302.tar.gz"
        ],
        "md5": "2bbd6bf0bb3f08c95542b46b26a43612",
        "size": 10131881426,
        "documents": 5609079,
        "downloaded": False,
        "texts": "m-beir-union"
    },
    "m-beir-cirr_task7.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR CIRR task 7 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-cirr-task7.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-cirr-task7.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "9cc2cbc853ed3f40faeb1625883dd787",
        "size": 38778158,
        "documents": 21551,
        "downloaded": False,
        "texts": "m-beir-cirr_task7"
    },
    "m-beir-edis_task2.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR EDIS task 2 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-edis-task2.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-edis-task2.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "8e6c689bd963c3ba98a12bb09722e6ff",
        "size": 1882886595,
        "documents": 1047067,
        "downloaded": False,
        "texts": "m-beir-edis_task2"
    },
    "m-beir-fashion200k_task0.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR Fashion200k task 0 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-fashion200k-task0.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-fashion200k-task0.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "9a994c44fd9cde8950975bae85dc8ce4",
        "size": 361951451,
        "documents": 201824,
        "downloaded": False,
        "texts": "m-beir-fashion200k_task0"
    },
    "m-beir-fashion200k_task3.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR Fashion200k task 3 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-fashion200k-task3.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-fashion200k-task3.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "49a93245fc3dc254e93db4ef55d88e93",
        "size": 111000347,
        "documents": 61707,
        "downloaded": False,
        "texts": "m-beir-fashion200k_task3"
    },
    "m-beir-fashioniq_task7.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR FashionIQ task 7 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-fashioniq-task7.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-fashioniq-task7.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "afc68db8916ddfeef0ab4b7c4fcd7c9a",
        "size": 133814528,
        "documents": 74381,
        "downloaded": False,
        "texts": "m-beir-fashioniq_task7"
    },
    "m-beir-infoseek_task6.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR InfoSeek task 6 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-infoseek-task6.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-infoseek-task6.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "81a3d728a0e2d73e5fba7bc1c6c04c8d",
        "size": 1101028282,
        "documents": 611651,
        "downloaded": False,
        "texts": "m-beir-infoseek_task6"
    },
    "m-beir-infoseek_task8.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR InfoSeek task 8 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-infoseek-task8.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-infoseek-task8.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "c1b1e9f3301acfc8da19797d2f805a3e",
        "size": 867079294,
        "documents": 481782,
        "downloaded": False,
        "texts": "m-beir-infoseek_task8"
    },
    "m-beir-mscoco_task0.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR MSCOCO task 0 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-mscoco-task0.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-mscoco-task0.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "423c4994b238cdcc38c9516606207236",
        "size": 8997191,
        "documents": 5000,
        "downloaded": False,
        "texts": "m-beir-mscoco_task0"
    },
    "m-beir-mscoco_task3.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR MSCOCO task 3 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-mscoco-task3.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-mscoco-task3.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "2b7ec1d919a579b9d8c1f40c875a6897",
        "size": 44642915,
        "documents": 24809,
        "downloaded": False,
        "texts": "m-beir-mscoco_task3"
    },
    "m-beir-nights_task4.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR NIGHTS task 4 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-nights-task4.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-nights-task4.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "f356bb29294510bdace4523fa888d8ba",
        "size": 72063162,
        "documents": 40038,
        "downloaded": False,
        "texts": "m-beir-nights_task4"
    },
    "m-beir-oven_task6.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR OVEN task 6 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-oven-task6.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-oven-task6.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "42c11b37cb51fc3b3358fa887702d61b",
        "size": 1217888354,
        "documents": 676667,
        "downloaded": False,
        "texts": "m-beir-oven_task6"
    },
    "m-beir-oven_task8.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR OVEN task 8 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-oven-task8.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-oven-task8.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "35ab385ac5e83d829b2d40d048e9c576",
        "size": 603292386,
        "documents": 335135,
        "downloaded": False,
        "texts": "m-beir-oven_task8"
    },
    "m-beir-visualnews_task0.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR VisualNews task 0 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-visualnews-task0.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-visualnews-task0.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "17945848e8425f2c83c671b6f5ab8f8b",
        "size": 975312678,
        "documents": 542246,
        "downloaded": False,
        "texts": "m-beir-visualnews_task0"
    },
    "m-beir-visualnews_task3.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR VisualNews task 3 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-visualnews-task3.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-visualnews-task3.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "75eeedee852dcbeed968e45a3bb585f7",
        "size": 967522065,
        "documents": 537568,
        "downloaded": False,
        "texts": "m-beir-visualnews_task3"
    },
    "m-beir-webqa_task1.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR WebQA task 1 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-webqa-task1.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-webqa-task1.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "b861ea5754d2e6a3c7194818a6521ad9",
        "size": 979823458,
        "documents": 544457,
        "downloaded": False,
        "texts": "m-beir-webqa_task1"
    },
    "m-beir-webqa_task2.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR WebQA task 2 corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-webqa-task2.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-webqa-task2.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "2e37ddecd2cd7175056cfb7a743f251c",
        "size": 724742262,
        "documents": 403196,
        "downloaded": False,
        "texts": "m-beir-webqa_task2"
    },
    "m-beir-union.blip-ff-large": {
        "description": "Faiss FlatIP index of the MBEIR global (union) corpus encoded by UniIR's blip-ff-large model",
        "filename": "faiss-flat.m-beir-union.blip-ff-large.20260302.fa77cbd.tar.gz",
        "readme": "faiss-flat.m-beir.blip-ff-large.20260302.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-m-beir/resolve/main/UniIR/BLIP_FF/faiss-flat.m-beir-union.blip-ff-large.20260302.fa77cbd.tar.gz"
        ],
        "md5": "76c614a504333ea6b3e28e11ef6656a2",
        "size": 10090371795,
        "documents": 5609079,
        "downloaded": False,
        "texts": "m-beir-union"
    }
}

FAISS_INDEX_INFO_DSE = {
    "slidevqa.dse": {
        "description": "Faiss index of the SlideVQA corpus encoded by DSE (Tevatron/dse-phi3-v1.0)",
        "filename": "slidevqa.dse.tar.gz",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-dse/resolve/main/slidevqa/slidevqa.dse.tar.gz"
        ],
        "md5": "920bcdbae5cd2730dbf961c7d72778e6",
        "size": 340388515,
        "documents": 52480,
        "downloaded": False,
        "texts": None
    },
    "wiki-ss.dse": {
        "description": "Faiss index of the Wiki-SS corpus encoded by DSE (Tevatron/dse-phi3-v1.0)",
        "filename": "wiki-ss.dse.tar.gz",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-dse/resolve/main/wiki-ss/wiki-ss.dse.tar.gz"
        ],
        "md5": "b80f7a05049d76be18497e3489e91066",
        "size": 8231110478,
        "documents": 1267874,
        "downloaded": False,
        "texts": None
    },
}

FAISS_INDEX_INFO_MMEB = {
    "mmeb-visdoc-MMLongBench-page.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the MMLongBench-page corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-MMLongBench-page.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-MMLongBench-page.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "bc76564734166016e1b3b91b50cb6c4f",
        "size": 22231867,
        "documents": 6492,
        "downloaded": False,
        "texts": "mmeb-visdoc-MMLongBench-page"
    },
    "mmeb-visdoc-ViDoRe_arxivqa.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_arxivqa corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_arxivqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_arxivqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "3e990bb6d563b1221d31fc770cb3585a",
        "size": 1712816,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_arxivqa"
    },
    "mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_biomedical_lectures_v2_multilingual corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "bba14aa67334ea0885c440d13ad15710",
        "size": 3476911,
        "documents": 1016,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual"
    },
    "mmeb-visdoc-ViDoRe_docvqa.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_docvqa corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_docvqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_docvqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "9c95c4e2df355eedcfaf0047851b6eb9",
        "size": 1711921,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_docvqa"
    },
    "mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_economics_reports_v2_multilingual corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "5d2f01361a4709d7d2581513c1788271",
        "size": 1515827,
        "documents": 452,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual"
    },
    "mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_esg_reports_human_labeled_v2 corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "8b1b83e5591c1857164ad29b2ed6cae8",
        "size": 5272565,
        "documents": 1538,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2"
    },
    "mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_esg_reports_v2_multilingual corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "32bf50e35bc8a766eeda75f5fd06ae5a",
        "size": 5271794,
        "documents": 1538,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual"
    },
    "mmeb-visdoc-ViDoRe_infovqa.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_infovqa corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_infovqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_infovqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "ac393b43b7375f174e30db6ea3cfbaa7",
        "size": 1715092,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_infovqa"
    },
    "mmeb-visdoc-ViDoRe_shiftproject.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_shiftproject corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_shiftproject.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_shiftproject.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "e08f1292ddc85461d25996243a3b68cc",
        "size": 3425058,
        "documents": 999,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_shiftproject"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_artificial_intelligence corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "02f75b35beec881ed7e7b2d3b6bc3565",
        "size": 3316096,
        "documents": 968,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_energy.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_energy corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_energy.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_energy.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "df05dcebb29719324411e95ab45e3094",
        "size": 3338175,
        "documents": 975,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_energy"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_government_reports corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "426b717c4c36dc45b3d6ea9483805fbc",
        "size": 3329254,
        "documents": 972,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_healthcare_industry corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "4b8a8f7718430f09d2e5903faeeabd04",
        "size": 3297932,
        "documents": 963,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry"
    },
    "mmeb-visdoc-ViDoRe_tabfquad.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_tabfquad corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_tabfquad.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_tabfquad.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "1446fe9b9a9bb2d09285fe939a394357",
        "size": 241172,
        "documents": 70,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_tabfquad"
    },
    "mmeb-visdoc-ViDoRe_tatdqa.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoRe_tatdqa corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_tatdqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoRe_tatdqa.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "39977e4f476ef04036452951a6dd3aee",
        "size": 926788,
        "documents": 271,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_tatdqa"
    },
    "mmeb-visdoc-ViDoSeek-page.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the ViDoSeek-page corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-ViDoSeek-page.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-ViDoSeek-page.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "134ee2bb9c9bff84f798c3a42709c191",
        "size": 18332388,
        "documents": 5349,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoSeek-page"
    },
    "mmeb-visdoc-VisRAG_ArxivQA.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the VisRAG_ArxivQA corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_ArxivQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-VisRAG_ArxivQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "d44fe8b4eed3fabb4e17b4519d1f94a7",
        "size": 27623153,
        "documents": 8066,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_ArxivQA"
    },
    "mmeb-visdoc-VisRAG_ChartQA.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the VisRAG_ChartQA corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_ChartQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-VisRAG_ChartQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "a8a69bb167fec98e62bc6c96fa11754b",
        "size": 1715864,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_ChartQA"
    },
    "mmeb-visdoc-VisRAG_InfoVQA.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the VisRAG_InfoVQA corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_InfoVQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-VisRAG_InfoVQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "9826a0c798bc364afd3c1e45389ce620",
        "size": 1575019,
        "documents": 459,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_InfoVQA"
    },
    "mmeb-visdoc-VisRAG_MP-DocVQA.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the VisRAG_MP-DocVQA corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_MP-DocVQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-VisRAG_MP-DocVQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "55a44170e9677ea9e293818cb79c12bb",
        "size": 2537728,
        "documents": 741,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_MP-DocVQA"
    },
    "mmeb-visdoc-VisRAG_PlotQA.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the VisRAG_PlotQA corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_PlotQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-VisRAG_PlotQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "fdb1aed9649f98018221682a830ca84d",
        "size": 32863763,
        "documents": 9593,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_PlotQA"
    },
    "mmeb-visdoc-VisRAG_SlideVQA.gme-Qwen2-VL-2B-Instruct": {
        "description": "Faiss index of the VisRAG_SlideVQA corpus encoded by gme-Qwen2-VL-2B-Instruct",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_SlideVQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/gme-Qwen2-VL-2B-Instruct/faiss-flat.mmeb-visdoc-VisRAG_SlideVQA.gme-Qwen2-VL-2B-Instruct.20260303.fa77cbd.tar.gz"
        ],
        "md5": "357f7eea450c72dcacdeabcb13ac4109",
        "size": 4420763,
        "documents": 1284,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_SlideVQA"
    },
    "mmeb-visdoc-MMLongBench-page.VLM2Vec-V2.0": {
        "description": "Faiss index of the MMLongBench-page corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-MMLongBench-page.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-MMLongBench-page.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "6d43c203b2510167655b68c676637b6c",
        "size": 22178560,
        "documents": 6492,
        "downloaded": False,
        "texts": "mmeb-visdoc-MMLongBench-page"
    },
    "mmeb-visdoc-ViDoRe_arxivqa.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_arxivqa corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_arxivqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_arxivqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "837900a41433f8f7087d4c32b2383d54",
        "size": 1712097,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_arxivqa"
    },
    "mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_biomedical_lectures_v2_multilingual corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "109a1752ecad596caa28575fdf614cbd",
        "size": 3469056,
        "documents": 1016,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_biomedical_lectures_v2_multilingual"
    },
    "mmeb-visdoc-ViDoRe_docvqa.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_docvqa corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_docvqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_docvqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "cffa22452328059db00589524f882d57",
        "size": 1709732,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_docvqa"
    },
    "mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_economics_reports_v2_multilingual corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "9b65603f98ca7dc9bc6082c98cfe8862",
        "size": 1512562,
        "documents": 452,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_economics_reports_v2_multilingual"
    },
    "mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_esg_reports_human_labeled_v2 corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "8fefe05fedc73a8bc21def74a89648bd",
        "size": 5255906,
        "documents": 1538,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_esg_reports_human_labeled_v2"
    },
    "mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_esg_reports_v2_multilingual corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "b6a7b5c3807159537cd4764686b274e7",
        "size": 5256175,
        "documents": 1538,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_esg_reports_v2_multilingual"
    },
    "mmeb-visdoc-ViDoRe_infovqa.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_infovqa corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_infovqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_infovqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "b477a1649f8c0e2ea2d48c53e59645be",
        "size": 1710805,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_infovqa"
    },
    "mmeb-visdoc-ViDoRe_shiftproject.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_shiftproject corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_shiftproject.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_shiftproject.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "a9980cea71cd9f07d474f6f9eeb29015",
        "size": 3414665,
        "documents": 999,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_shiftproject"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_artificial_intelligence corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "e9bf9534b1274dc553e3157519b0ad32",
        "size": 3309513,
        "documents": 968,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_artificial_intelligence"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_energy.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_energy corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_energy.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_energy.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "40494bbcf2c2badf963eaa3da33076f8",
        "size": 3332470,
        "documents": 975,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_energy"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_government_reports corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "0b674e4a8d752d9499b93fffaddcb82f",
        "size": 3322883,
        "documents": 972,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_government_reports"
    },
    "mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_syntheticDocQA_healthcare_industry corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "7c84f00b2337b4ccbff7c0d14287e6f6",
        "size": 3292728,
        "documents": 963,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_syntheticDocQA_healthcare_industry"
    },
    "mmeb-visdoc-ViDoRe_tabfquad.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_tabfquad corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_tabfquad.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_tabfquad.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "019668a306e85f92bf507b176ef2a8bd",
        "size": 241001,
        "documents": 70,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_tabfquad"
    },
    "mmeb-visdoc-ViDoRe_tatdqa.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoRe_tatdqa corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoRe_tatdqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoRe_tatdqa.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "6a22f1fee5fd3b251e4debbc75917f31",
        "size": 928230,
        "documents": 271,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoRe_tatdqa"
    },
    "mmeb-visdoc-ViDoSeek-page.VLM2Vec-V2.0": {
        "description": "Faiss index of the ViDoSeek-page corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-ViDoSeek-page.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-ViDoSeek-page.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "c203a9d820c0320d8564dfb5d937403e",
        "size": 18286911,
        "documents": 5349,
        "downloaded": False,
        "texts": "mmeb-visdoc-ViDoSeek-page"
    },
    "mmeb-visdoc-VisRAG_ArxivQA.VLM2Vec-V2.0": {
        "description": "Faiss index of the VisRAG_ArxivQA corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_ArxivQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-VisRAG_ArxivQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "48d5d1d54a379f3b8e9c28fd40c87777",
        "size": 27624787,
        "documents": 8066,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_ArxivQA"
    },
    "mmeb-visdoc-VisRAG_ChartQA.VLM2Vec-V2.0": {
        "description": "Faiss index of the VisRAG_ChartQA corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_ChartQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-VisRAG_ChartQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "c7e7db93f708031a9348cdca98b286c8",
        "size": 1713915,
        "documents": 500,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_ChartQA"
    },
    "mmeb-visdoc-VisRAG_InfoVQA.VLM2Vec-V2.0": {
        "description": "Faiss index of the VisRAG_InfoVQA corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_InfoVQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-VisRAG_InfoVQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "6ee853bd33007d5cb42610dd20d30608",
        "size": 1571434,
        "documents": 459,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_InfoVQA"
    },
    "mmeb-visdoc-VisRAG_MP-DocVQA.VLM2Vec-V2.0": {
        "description": "Faiss index of the VisRAG_MP-DocVQA corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_MP-DocVQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-VisRAG_MP-DocVQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "e413821565def456be77cb45581d5627",
        "size": 2535412,
        "documents": 741,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_MP-DocVQA"
    },
    "mmeb-visdoc-VisRAG_PlotQA.VLM2Vec-V2.0": {
        "description": "Faiss index of the VisRAG_PlotQA corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_PlotQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-VisRAG_PlotQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "7e0e261fd082f02b7cc8112161ec4b62",
        "size": 32818893,
        "documents": 9593,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_PlotQA"
    },
    "mmeb-visdoc-VisRAG_SlideVQA.VLM2Vec-V2.0": {
        "description": "Faiss index of the VisRAG_SlideVQA corpus encoded by VLM2Vec-V2.0",
        "filename": "faiss-flat.mmeb-visdoc-VisRAG_SlideVQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz",
        "readme": "faiss-flat.mmeb-visdoc.VLM2Vec-V2.20260303.fa77cbd.README.md",
        "urls": [
            "https://huggingface.co/datasets/castorini/prebuilt-indexes-mmeb/resolve/main/faiss-flat/VLM2Vec-V2.0/faiss-flat.mmeb-visdoc-VisRAG_SlideVQA.VLM2Vec-V2.0.20260303.fa77cbd.tar.gz"
        ],
        "md5": "c4027618ca83a791da38948372a7f7b1",
        "size": 4411898,
        "documents": 1284,
        "downloaded": False,
        "texts": "mmeb-visdoc-VisRAG_SlideVQA"
    }
}

FAISS_INDEX_INFO_OTHER = {
    "cast2019-tct_colbert-v2.hnsw": {
        "description": "Faiss HNSW index of the CAsT2019 passage corpus encoded by the tct_colbert-v2 passage encoder",
        "filename": "faiss-hnsw.cast2019.tct_colbert-v2.tar.gz",
        "readme": "faiss-hnsw.cast2019.tct_colbert-v2-readme.txt",
        "urls": [
            "https://rgw.cs.uwaterloo.ca/pyserini/indexes/hnsw-faiss.cast2019.tct_colbert-v2.tar.gz"
        ],
        "md5": "2ce7ce8064ed235a9b6aad08571340d4",
        "size": 112121368296,
        "documents": 38429835,
        "downloaded": False,
        "texts": "cast2019"
    },
    # TODO: update urls to rgw.cs.uwaterloo.ca/....
    "atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.base": {
        "description": "Faiss index for AToMiC Images v0.2 on base corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.image.base.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.image.base.faiss.flat.tar.gz"
        ],
        "md5": "7e7abf80e99b81c444281405db19c579",
        "size": 9284282630,
        "documents": 3410779,
        "downloaded": False,
        "texts": "atomic_image_v0.2_base"
    },
    "atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.image.faiss.flat.tar.gz"
        ],
        "md5": "501b7477a8e1eea9e10904a2ea307906",
        "size": 29984366146,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.validation": {
        "description": "Faiss index for AToMiC Images v0.2 on validation corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.image.small.validation.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.image.small.validation.faiss.flat.tar.gz"
        ],
        "md5": "798d601cfc505a4b290bb708290a38fc",
        "size": 43875634,
        "documents": 16126,
        "downloaded": False,
        "texts": "atomic_image_v0.2_small_validation"
    },
    "atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.base": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on base corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.text.base.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.text.base.faiss.flat.tar.gz"
        ],
        "md5": "1d90ecfb703b96f003a9d6dc054c057b",
        "size": 8187618352,
        "documents": 3029504,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_base"
    },
    "atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.text.faiss.flat.tar.gz"
        ],
        "md5": "9f5962e0b29bb341cba88041107b693e",
        "size": 27373277238,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.validation": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on validation corpus encoded by laion/CLIP-ViT-L-14-laion2B-s32B-b82K",
        "filename": "ViT-L-14.laion2b_s32b_b82k.text.small.validation.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-L-14.laion2b_s32b_b82k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-L-14.laion2b_s32b_b82k.text.small.validation.faiss.flat.tar.gz"
        ],
        "md5": "2dd9d0c805bbef6a6a23ece3c2b221a3",
        "size": 46421016,
        "documents": 17173,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_small_validation"
    },
    "atomic-v0.2.ViT-H-14.laion2b_s32b_b79k.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-H-14.laion2b_s32b_b79k",
        "filename": "ViT-H-14.laion2b_s32b_b79k.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-H-14.laion2b_s32b_b79k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-H-14.laion2b_s32b_b79k.image.faiss.flat.tar.gz"
        ],
        "md5": "3cacbc8af251dd59177140b83de61024",
        "size": 39192329951,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-H-14.laion2b_s32b_b79k.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-H-14.laion2b_s32b_b79k",
        "filename": "ViT-H-14.laion2b_s32b_b79k.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-H-14.laion2b_s32b_b79k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-H-14.laion2b_s32b_b79k.text.faiss.flat.tar.gz"
        ],
        "md5": "7866b6b2c38cd46eea5fc28254cf17bc",
        "size": 35824621106,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.ViT-bigG-14.laion2b_s39b_b160k.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-bigG-14.laion2b_s39b_b160k",
        "filename": "ViT-bigG-14.laion2b_s39b_b160k.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-bigG-14.laion2b_s39b_b160k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-bigG-14.laion2b_s39b_b160k.image.faiss.flat.tar.gz"
        ],
        "md5": "1837c886187bb6ecc60fdc02c6056a21",
        "size": 48274458058,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-bigG-14.laion2b_s39b_b160k.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-bigG-14.laion2b_s39b_b160k",
        "filename": "ViT-bigG-14.laion2b_s39b_b160k.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-bigG-14.laion2b_s39b_b160k.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-bigG-14.laion2b_s39b_b160k.text.faiss.flat.tar.gz"
        ],
        "md5": "5cc288862b73772b466916a79ec311b0",
        "size": 44195349889,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.ViT-B-32.laion2b_e16.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-B-32.laion2b_e16",
        "filename": "ViT-B-32.laion2b_e16.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion2b_e16.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion2b_e16.image.faiss.flat.tar.gz"
        ],
        "md5": "1b35007a5b066179180edd2fb2d56448",
        "size": 20408227482,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-B-32.laion2b_e16.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-B-32.laion2b_e16",
        "filename": "ViT-B-32.laion2b_e16.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion2b_e16.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion2b_e16.text.faiss.flat.tar.gz"
        ],
        "md5": "6182fc18d112dea4dcfd91546ddf0747",
        "size": 18574571493,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.ViT-B-32.laion400m_e32.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-ViT-B-32.laion400m_e32",
        "filename": "ViT-B-32.laion400m_e32.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion400m_e32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion400m_e32.image.faiss.flat.tar.gz"
        ],
        "md5": "c08ea30351953b6c91c9b15ad87749e4",
        "size": 20402486061,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.ViT-B-32.laion400m_e32.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-ViT-B-32.laion400m_e32",
        "filename": "ViT-B-32.laion400m_e32.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.ViT-B-32.laion400m_e32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/ViT-B-32.laion400m_e32.text.faiss.flat.tar.gz"
        ],
        "md5": "a68e71ed301870a9be82003f0246183b",
        "size": 18566367182,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.openai.clip-vit-large-patch14.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-openai.clip-vit-large-patch14",
        "filename": "openai.clip-vit-large-patch14.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-large-patch14.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-large-patch14.image.faiss.flat.tar.gz"
        ],
        "md5": "6bb4b5169ca864328ab03ecdd484437d",
        "size": 29989412901,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.openai.clip-vit-large-patch14.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-openai.clip-vit-large-patch14",
        "filename": "openai.clip-vit-large-patch14.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-large-patch14.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-large-patch14.text.faiss.flat.tar.gz"
        ],
        "md5": "c6303d01cac83be6902df2967782d2cb",
        "size": 27399921354,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.openai.clip-vit-base-patch32.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-openai.clip-vit-base-patch32",
        "filename": "openai.clip-vit-base-patch32.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-base-patch32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-base-patch32.image.faiss.flat.tar.gz"
        ],
        "md5": "2af24862dd2a37b92cc03edc465d3705",
        "size": 20434283763,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.openai.clip-vit-base-patch32.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-openai.clip-vit-base-patch32",
        "filename": "openai.clip-vit-base-patch32.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.openai.clip-vit-base-patch32.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/openai.clip-vit-base-patch32.text.faiss.flat.tar.gz"
        ],
        "md5": "15c643b65b990aaf5fe3ec1012a710e0",
        "size": 18586684424,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.facebook.flava-full.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-facebook.flava-full",
        "filename": "facebook.flava-full.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.facebook.flava-full.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/facebook.flava-full.image.faiss.flat.tar.gz"
        ],
        "md5": "0c5d4e938627dc902cbde9a47a179d41",
        "size": 29963221412,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.facebook.flava-full.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-facebook.flava-full",
        "filename": "facebook.flava-full.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.facebook.flava-full.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/facebook.flava-full.text.faiss.flat.tar.gz"
        ],
        "md5": "763e574a749a16b6bf56d7b622131c12",
        "size": 27414008560,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.Salesforce.blip-itm-base-coco.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-base-coco",
        "filename": "Salesforce.blip-itm-base-coco.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-base-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-base-coco.image.faiss.flat.tar.gz"
        ],
        "md5": "9d924b64860ae26857e57591c621b811",
        "size": 10466804855,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.Salesforce.blip-itm-base-coco.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-base-coco",
        "filename": "Salesforce.blip-itm-base-coco.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-base-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-base-coco.text.faiss.flat.tar.gz"
        ],
        "md5": "a52770a28ce877e271544de3298b1e53",
        "size": 9439317784,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
    "atomic-v0.2.Salesforce.blip-itm-large-coco.image.large": {
        "description": "Faiss index for AToMiC Images v0.2 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-large-coco",
        "filename": "Salesforce.blip-itm-large-coco.image.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-large-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-large-coco.image.faiss.flat.tar.gz"
        ],
        "md5": "550b318e53f18604b2b919a3c22cfa39",
        "size": 10463191370,
        "documents": 3803656,
        "downloaded": False,
        "texts": "atomic_image_v0.2_large"
    },
    "atomic-v0.2.1.Salesforce.blip-itm-large-coco.text.large": {
        "description": "Faiss index for AToMiC Texts v0.2.1 on large corpus encoded by laion/CLIP-Salesforce.blip-itm-large-coco",
        "filename": "Salesforce.blip-itm-large-coco.text.faiss.flat.tar.gz",
        "readme": "faiss.atomic.Salesforce.blip-itm-large-coco.20230621.83e97fc.README.md",
        "urls": [
            "https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/resolve/main/indexes/Salesforce.blip-itm-large-coco.text.faiss.flat.tar.gz"
        ],
        "md5": "a09bb2b0b2ae3eb5099061a7cddfe949",
        "size": 9440231672,
        "documents": 10134744,
        "downloaded": False,
        "texts": "atomic_text_v0.2.1_large"
    },
}

FAISS_INDEX_INFO = {**FAISS_INDEX_INFO_MSMARCO,
                    **FAISS_INDEX_INFO_BEIR,
                    **FAISS_INDEX_INFO_BRIGHT,
                    **FAISS_INDEX_INFO_MRTYDI,
                    **FAISS_INDEX_INFO_MIRACL,
                    **FAISS_INDEX_INFO_WIKIPEDIA,
                    **FAISS_INDEX_INFO_CIRAL,
                    **FAISS_INDEX_INFO_M_BEIR,
                    **FAISS_INDEX_INFO_DSE,
                    **FAISS_INDEX_INFO_MMEB,
                    **FAISS_INDEX_INFO_OTHER}
