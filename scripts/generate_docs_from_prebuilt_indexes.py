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


from pyserini.prebuilt_index_info import *


__boilerplate__ = '''
# Pyserini: Prebuilt Indexes

Pyserini provides a number of prebuilt Lucene indexes.
To list what's available:

```python
from pyserini.search.lucene import LuceneSearcher
LuceneSearcher.list_prebuilt_indexes()

from pyserini.index.lucene import IndexReader
IndexReader.list_prebuilt_indexes()
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
index_reader = IndexReader.from_prebuilt_index('robust04')
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


def generate_prebuilt(index):
    print('<dl>')
    for entry in index:
        # No, this is not an HTML bug. This is intentional to get GitHub formatting to not add italics to the entry.
        print(f'<dt></dt><b><code>{entry}</code></b>')
        if 'readme' in index[entry]:
            print(f'[<a href="../pyserini/resources/index-metadata/{index[entry]["readme"]}">readme</a>]')
        print(f'<dd>{index[entry]["description"]}')
        print(f'</dd>')
    print('</dl>')


if __name__ == '__main__':
    print(__boilerplate__)
    print('\n\n## Standard Lucene Indexes')

    print('<details>')
    print('<summary>MS MARCO</summary>')
    generate_prebuilt(TF_INDEX_INFO_MSMARCO)
    print('</details>')

    print('<details>')
    print('<summary>BEIR</summary>')
    generate_prebuilt(TF_INDEX_INFO_BEIR)
    print('</details>')

    print('<details>')
    print('<summary>Mr.TyDi</summary>')
    generate_prebuilt(TF_INDEX_INFO_MRTYDI)
    print('</details>')

    print('<details>')
    print('<summary>MIRACL</summary>')
    generate_prebuilt(TF_INDEX_INFO_MIRACL)
    print('</details>')

    print('<details>')
    print('<summary>Other</summary>')
    generate_prebuilt(TF_INDEX_INFO_CIRAL)
    generate_prebuilt(TF_INDEX_INFO_OTHER)
    print('</details>')

    print('\n\n## Lucene Impact Indexes')

    print('<details>')
    print('<summary>MS MARCO</summary>')
    generate_prebuilt(IMPACT_INDEX_INFO_MSMARCO)
    print('</details>')

    print('<details>')
    print('<summary>BEIR</summary>')
    generate_prebuilt(IMPACT_INDEX_INFO_BEIR)
    print('</details>')

    print('\n\n## Faiss Indexes')

    print('<details>')
    print('<summary>MS MARCO</summary>')
    generate_prebuilt(FAISS_INDEX_INFO_MSMARCO)
    print('</details>')

    print('<details>')
    print('<summary>BEIR</summary>')
    generate_prebuilt(FAISS_INDEX_INFO_BEIR)
    print('</details>')

    print('<details>')
    print('<summary>Mr.TyDi</summary>')
    generate_prebuilt(FAISS_INDEX_INFO_MRTYDI)
    print('</details>')

    print('<details>')
    print('<summary>MIRACL</summary>')
    generate_prebuilt(FAISS_INDEX_INFO_MIRACL)
    print('</details>')

    print('<details>')
    print('<summary>Other</summary>')
    generate_prebuilt(FAISS_INDEX_INFO_CIRAL)
    generate_prebuilt(FAISS_INDEX_INFO_WIKIPEDIA)
    generate_prebuilt(FAISS_INDEX_INFO_OTHER)
    print('</details>')
