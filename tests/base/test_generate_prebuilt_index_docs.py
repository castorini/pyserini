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

from io import StringIO
from pathlib import Path
from urllib.parse import urlparse
import unittest

from pyserini.prebuilt_index_info import *


__boilerplate__ = '''
# Pyserini: Prebuilt Indexes

Pyserini provides a number of prebuilt Lucene indexes.
To list what's available:

```python
from pyserini.search.lucene import LuceneSearcher
LuceneSearcher.list_prebuilt_indexes()

from pyserini.index.lucene import LuceneIndexReader
LuceneIndexReader.list_prebuilt_indexes()
```

It's easy initialize a searcher from a prebuilt index:

```python
searcher = LuceneSearcher.from_prebuilt_index('robust04')
```

You can use this simple Python one-liner to download the prebuilt index:

```
python -c "from pyserini.search.lucene import LuceneSearcher; LuceneSearcher.from_prebuilt_index('robust04')"
```

The downloaded index will be in `~/.cache/pyserini/indexes/`.

It's similarly easy initialize an index reader from a prebuilt index:

```python
index_reader = LuceneIndexReader.from_prebuilt_index('robust04')
index_reader.stats()
```

The output will be:

```
{'total_terms': 174540872, 'documents': 528030, 'non_empty_documents': 528030, 'unique_terms': 923436}
```

Note that unless the underlying index was built with the `-optimize` option (i.e., merging all index segments into a single segment), `unique_terms` will show -1.
Nope, that's not a bug.

Pyserini also provides a number of prebuilt Faiss indexes.
To list what's available:

```python
from pyserini.search.faiss import FaissSearcher
FaissSearcher.list_prebuilt_indexes()
```

And to initialize a specific Faiss index:

```python
searcher = FaissSearcher.from_prebuilt_index('msmarco-v1-passage.bge-base-en-v1.5', None)
```

Below is a summary of the prebuilt indexes that are currently available.
Detailed configuration information for the prebuilt indexes are stored in [`pyserini/prebuilt_index_info.py`](../pyserini/prebuilt_index_info.py).

'''


def readme_href(readme):
    parsed = urlparse(readme)
    if parsed.scheme and parsed.netloc:
        return readme
    return f'../pyserini/resources/index-metadata/{readme}'


def generate_prebuilt(out, index):
    print('<dl>', file=out)
    for entry in index:
        # No, this is not an HTML bug. This is intentional to get GitHub formatting to not add italics to the entry.
        print(f'<dt></dt><b><code>{entry}</code></b>', file=out)
        if 'readme' in index[entry]:
            print(f'[<a href="{readme_href(index[entry]["readme"])}">readme</a>]', file=out)
        print(f'<dd>{index[entry]["description"]}', file=out)
        print(f'</dd>', file=out)
    print('</dl>', file=out)


def generate_prebuilt_index_docs():
    out = StringIO()

    print(__boilerplate__, file=out)
    print('\n\n## Lucene Standard Inverted Indexes', file=out)

    print('<details>', file=out)
    print('<summary>MS MARCO</summary>', file=out)
    generate_prebuilt(out, TF_INDEX_INFO_MSMARCO)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BEIR</summary>', file=out)
    generate_prebuilt(out, TF_INDEX_INFO_BEIR)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BRIGHT</summary>', file=out)
    generate_prebuilt(out, TF_INDEX_INFO_BRIGHT)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>Mr.TyDi</summary>', file=out)
    generate_prebuilt(out, TF_INDEX_INFO_MRTYDI)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>MIRACL</summary>', file=out)
    generate_prebuilt(out, TF_INDEX_INFO_MIRACL)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>Other</summary>', file=out)
    generate_prebuilt(out, TF_INDEX_INFO_CIRAL)
    generate_prebuilt(out, TF_INDEX_INFO_OTHER)
    print('</details>', file=out)

    print('\n\n## Lucene Impact Indexes', file=out)

    print('<details>', file=out)
    print('<summary>MS MARCO</summary>', file=out)
    generate_prebuilt(out, IMPACT_INDEX_INFO_MSMARCO)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BEIR</summary>', file=out)
    generate_prebuilt(out, IMPACT_INDEX_INFO_BEIR)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BRIGHT</summary>', file=out)
    generate_prebuilt(out, IMPACT_INDEX_INFO_BRIGHT)
    print('</details>', file=out)

    print('\n\n## Lucene HNSW Indexes', file=out)

    print('<details>', file=out)
    print('<summary>MS MARCO</summary>', file=out)
    generate_prebuilt(out, LUCENE_HNSW_INDEX_INFO_MSMARCO)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BEIR</summary>', file=out)
    generate_prebuilt(out, LUCENE_HNSW_INDEX_INFO_BEIR)
    print('</details>', file=out)

    print('\n\n## Lucene Flat Indexes', file=out)

    print('<details>', file=out)
    print('<summary>BEIR</summary>', file=out)
    generate_prebuilt(out, LUCENE_FLAT_INDEX_INFO_BEIR)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BRIGHT</summary>', file=out)
    generate_prebuilt(out, LUCENE_FLAT_INDEX_INFO_BRIGHT)
    print('</details>', file=out)

    print('\n\n## Faiss Indexes', file=out)

    print('<details>', file=out)
    print('<summary>MS MARCO</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_MSMARCO)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BEIR</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_BEIR)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>BRIGHT</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_BRIGHT)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>Mr.TyDi</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_MRTYDI)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>MIRACL</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_MIRACL)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>M-BEIR</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_M_BEIR)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>DSE</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_DSE)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>MMEB</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_MMEB)
    print('</details>', file=out)

    print('<details>', file=out)
    print('<summary>Other</summary>', file=out)
    generate_prebuilt(out, FAISS_INDEX_INFO_CIRAL)
    generate_prebuilt(out, FAISS_INDEX_INFO_WIKIPEDIA)
    generate_prebuilt(out, FAISS_INDEX_INFO_OTHER)
    print('</details>', file=out)

    return out.getvalue()


class TestGeneratePrebuiltIndexDocs(unittest.TestCase):
    def test_generate_prebuilt_index_docs(self):
        root = Path(__file__).resolve().parents[2]
        docs_path = root / 'docs' / 'prebuilt-indexes.md'
        docs_path.write_text(generate_prebuilt_index_docs(), encoding='utf-8')


if __name__ == '__main__':
    unittest.main()
