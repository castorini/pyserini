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

    for field in ['readme', 'total_terms', 'documents', 'unique_terms', 'downloaded', 'note']:
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


class _LazyPrebuiltIndexInfoJson(Mapping):
    def __init__(self, url):
        self._url = url
        self._info = None

    def _load(self):
        if self._info is None:
            resource = importlib.resources.files('pyserini')
            for path_part in self._url.split('/'):
                resource = resource / path_part
            with resource.open(encoding='utf-8') as response:
                self._info = json.load(response)

        return self._info

    def __getitem__(self, key):
        return self._load()[key]

    def __iter__(self):
        return iter(self._load())

    def __len__(self):
        return len(self._load())

    def __contains__(self, key):
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

# Bindings for Lucene HNSW MSMARCO indexes
LUCENE_HNSW_INDEX_INFO_MSMARCO = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/msmarco-v1-passage-hnsw.json'),
    _prebuilt_indexes_url('lucene/msmarco-v2.1-doc-segmented-hnsw.json'),
    key_prefixes=('msmarco-',)
)

# Bindings for Lucene HNSW BEIR indexes
LUCENE_HNSW_INDEX_INFO_BEIR = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/beir-hnsw-bge-base-en-v1.5.json'),
    key_prefixes=('beir-v1.0.0-',)
)

LUCENE_HNSW_INDEX_INFO = _PrebuiltIndexCatalog(LUCENE_HNSW_INDEX_INFO_MSMARCO,
                                               LUCENE_HNSW_INDEX_INFO_BEIR)

# Bindings for Lucene flat indexes
LUCENE_FLAT_INDEX_INFO_BEIR = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/beir-flat-bge-base-en-v1.5.json'),
    key_prefixes=('beir-v1.0.0-',)
)

LUCENE_FLAT_INDEX_INFO_BRIGHT = _LazyLucenePrebuiltInvertedIndexJson(
    _prebuilt_indexes_url('lucene/bright-flat.json'),
    key_prefixes=('bright-',)
)

LUCENE_FLAT_INDEX_INFO = _PrebuiltIndexCatalog(LUCENE_FLAT_INDEX_INFO_BEIR,
                                               LUCENE_FLAT_INDEX_INFO_BRIGHT)


# Bindings for Faiss indexes
FAISS_INDEX_INFO_MSMARCO = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/msmarco-faiss.json'
)

FAISS_INDEX_INFO_BEIR = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/beir-faiss.json'
)

FAISS_INDEX_INFO_BRIGHT = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/bright-faiss.json'
)

FAISS_INDEX_INFO_MRTYDI = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/mrtydi-faiss.json'
)

FAISS_INDEX_INFO_MIRACL = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/miracl-faiss.json'
)

FAISS_INDEX_INFO_CIRAL = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/ciral-faiss.json'
)

FAISS_INDEX_INFO_WIKIPEDIA = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/wikipedia-faiss.json'
)

FAISS_INDEX_INFO_M_BEIR = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/m-beir-faiss.json'
)

FAISS_INDEX_INFO_DSE = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/dse-faiss.json'
)

FAISS_INDEX_INFO_MMEB = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/mmeb-faiss.json'
)

FAISS_INDEX_INFO_OTHER = _LazyPrebuiltIndexInfoJson(
    'resources/prebuilt-indexes/faiss/other-faiss.json'
)

FAISS_INDEX_INFO = _PrebuiltIndexCatalog(FAISS_INDEX_INFO_MSMARCO,
                                         FAISS_INDEX_INFO_BEIR,
                                         FAISS_INDEX_INFO_BRIGHT,
                                         FAISS_INDEX_INFO_MRTYDI,
                                         FAISS_INDEX_INFO_MIRACL,
                                         FAISS_INDEX_INFO_WIKIPEDIA,
                                         FAISS_INDEX_INFO_CIRAL,
                                         FAISS_INDEX_INFO_M_BEIR,
                                         FAISS_INDEX_INFO_DSE,
                                         FAISS_INDEX_INFO_MMEB,
                                         FAISS_INDEX_INFO_OTHER)
