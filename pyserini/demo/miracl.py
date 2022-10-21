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
This script provides an interactive web interface demo for retrieval on the MIRACL dataset.
It requires `flask` (`pip install flask~=2.2.0`).
An example command looks like `python -m pyserini.demo.miracl` that starts up a server on port 8080.
The demo can be accessed via "http://localhost:8080" in a web browser.
Additional arguments include:
    --port [PORT] --hits [Number of hits] --index [BM25 or mdpr-tied-pft-msmarco]
    --k1 [BM25 k1] --b [BM25 b] --device [cpu, cuda]
"""
import json
import logging
from argparse import ArgumentParser
from functools import partial
from typing import Callable, Optional, Tuple, Union

from flask import Flask, render_template, request, flash, jsonify
from pyserini.search import LuceneSearcher, FaissSearcher, AutoQueryEncoder

logging.basicConfig(
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO,
)
logger = logging.getLogger('miracl-demo')

VERSION = '1.0'
LANGUAGES = ('ar', 'bn', 'en', 'es', 'fa', 'fi', 'fr', 'hi', 'id', 'ja', 'ko', 'ru', 'sw', 'te', 'th', 'zh')
Searcher = Union[FaissSearcher, LuceneSearcher]


def create_app(k: int, load_searcher_fn: Callable[[str], Tuple[Searcher, str]]):
    app = Flask(__name__)

    lang = LANGUAGES[0]
    searcher, retriever = load_searcher_fn(lang)

    @app.route('/')
    def index():
        nonlocal lang, searcher, retriever
        return render_template('miracl.html', lang=lang, retriever=retriever)

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        nonlocal lang, searcher, retriever
        query = request.form['q']
        if not query:
            search_results = []
            flash('Question is required')
        else:
            hits = searcher.search(query, k=k)
            docs = [json.loads(searcher.doc(hit.docid).raw()) for hit in hits]
            search_results = [
                {
                    'rank': r + 1,
                    'docid': hit.docid,
                    'doc': docs[r]['text'],
                    'title': docs[r]['title'],
                    'score': hit.score,
                }
                for r, hit in enumerate(hits)
            ]
        return render_template(
            'miracl.html', search_results=search_results, query=query, lang=lang, retriever=retriever
        )

    @app.route('/lang', methods=['GET'])
    def change_language():
        nonlocal lang, searcher, retriever
        new_lang = request.args.get('new_lang', '', type=str)
        if not new_lang or new_lang not in LANGUAGES:
            return

        lang = new_lang
        searcher, retriever = load_searcher_fn(lang)
        return jsonify(lang=lang)

    return app


def _load_sparse_searcher(language: str, k1: Optional[float]=None, b: Optional[float]=None) -> (Searcher, str):
    searcher = LuceneSearcher.from_prebuilt_index(f'miracl-v{VERSION}-{language}')
    searcher.set_language(language)
    if k1 is not None and b is not None:
        searcher.set_bm25(k1, b)
        retriever_name = f'BM25 (k1={k1}, b={b})'
    else:
        retriever_name = 'BM25'

    return searcher, retriever_name


def _load_faiss_searcher(language: str, device:  str) -> (Searcher, str):
    query_encoder = AutoQueryEncoder(encoder_dir='castorini/mdpr-tied-pft-msmarco', device=device)
    searcher = FaissSearcher.from_prebuilt_index(
        f'miracl-v{VERSION}-{language}-mdpr-tied-pft-msmarco', query_encoder
    )
    retriever_name = 'mDPR-pFT-MSMARCO'
    return searcher, retriever_name


def main():
    parser = ArgumentParser()

    parser.add_argument('--index', default='BM25', choices=('BM25', 'mdpr-tied-pft-msmarco'), help='Index type.')
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

    if args.index == 'mdpr-tied-pft-msmarco':
        load_fn = partial(_load_faiss_searcher, device=args.device)
    else:
        load_fn = partial(_load_sparse_searcher, k1=args.k1, b=args.b)

    app = create_app(args.hits, load_fn)
    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
