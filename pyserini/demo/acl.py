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
This script provides an interactive web interface demo for retrieval on the ACL dataset.
It requires `flask` (`pip install flask~=2.2.0`).
An example command looks like `python -m pyserini.demo.acl` that starts up a server on port 8080.
The demo can be accessed via "http://localhost:8080" in a web browser.
Additional arguments include:
    --port [PORT] --hits [Number of hits]
    --k1 [BM25 k1] --b [BM25 b] --device [cpu, cuda]
"""

import logging
from argparse import ArgumentParser
from functools import partial
from typing import Callable, Optional, Tuple, Union

from flask import Flask, render_template, request, flash

from pyserini.search.faiss import FaissSearcher
from pyserini.search.lucene import LuceneSearcher

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)
logger = logging.getLogger('acl-demo')

VERSION = '1.0'
Searcher = Union[FaissSearcher, LuceneSearcher]


def create_app(k: int, load_searcher_fn: Callable[[str], Tuple[Searcher, str]]):
    app = Flask(__name__)

    lang = 'en'
    searcher, retriever = load_searcher_fn(lang)

    @app.route('/')
    def index():
        nonlocal lang, searcher, retriever
        return render_template('acl.html', lang=lang, retriever=retriever)

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        nonlocal lang, searcher, retriever
        query = request.form['q']
        if not query:
            search_results = []
            flash('Question is required')
        else:
            hits = searcher.search(query, k=k)
            docs = [searcher.doc(hit.docid) for hit in hits]
            search_results = [
                {
                    'rank': r + 1,
                    'docid': hit.docid,
                    'doc': docs[r].contents(),
                    'score': hit.score,
                }
                for r, hit in enumerate(hits)
            ]
        return render_template(
            'acl.html', search_results=search_results, query=query, lang=lang, retriever=retriever
        )


    return app


def _load_sparse_searcher(language: str, k1: Optional[float]=None, b: Optional[float]=None) -> (Searcher, str):
    searcher = LuceneSearcher('indexes/lucene-index-acl-paragraph')
    searcher.set_language(language)
    if k1 is not None and b is not None:
        searcher.set_bm25(k1, b)
        retriever_name = f'BM25 (k1={k1}, b={b})'
    else:
        retriever_name = 'BM25'

    return searcher, retriever_name


def main():
    parser = ArgumentParser()

    parser.add_argument('--k1', type=float, help='BM25 k1 parameter.')
    parser.add_argument('--b', type=float, help='BM25 b parameter.')
    parser.add_argument('--hits', type=int, default=10, help='Number of hits returned by the retriever')
    parser.add_argument(
        '--device',
        type=str,
        default='cpu',
        help='Device to run query encoder, cpu or [cuda:0, cuda:1, ...] (used only when index is based on FAISS)',
    )
    parser.add_argument(
        '--port',
        default=8080,
        type=int,
        help='Web server port',
    )

    args = parser.parse_args()

    load_fn = partial(_load_sparse_searcher, k1=args.k1, b=args.b)

    app = create_app(args.hits, load_fn)
    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
