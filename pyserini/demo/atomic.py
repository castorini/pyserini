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
This script provides an interactive web interface demo for retrieval on the AToMiC dataset.
It requires `flask` (`pip install flask~=2.2.0`).
An example command looks like `python -m pyserini.demo.atomic` that starts up a server on port 8080.
The demo can be accessed via "http://localhost:8080" in a web browser.
Additional arguments include:
    --port [PORT] --hits [Number of hits] --index [BM25 or {dense retrieval flag}]
    --k1 [BM25 k1] --b [BM25 b] --device [cpu, cuda]
"""
import json
from argparse import ArgumentParser
from functools import partial
from typing import Callable, Optional, Tuple, Union

from flask import Flask, render_template, request, flash, jsonify
from pyserini.search import LuceneSearcher, FaissSearcher, QueryEncoder


RETRIEVER_TO_INDEXES = {
    'BM25': [
        'atomic_image_v0.2_small_validation',
        'atomic_image_v0.2_base',
        'atomic_image_v0.2_large',
        'atomic_text_v0.2.1_small_validation',
        'atomic_text_v0.2.1_base',
        'atomic_text_v0.2.1_large',
    ],
    'ViT-L-14.laion2b_s32b_b82k': [
        'atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.validation',
        'atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.base',
        'atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.large',
        'atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.validation',
        'atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.base',
        'atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.large',
    ],
    'ViT-H-14.laion2b_s32b_b79k': [
        'atomic-v0.2.ViT-H-14.laion2b_s32b_b79k.image.large',
        'atomic-v0.2.1.ViT-H-14.laion2b_s32b_b79k.text.large',
    ],
    'ViT-bigG-14.laion2b_s39b_b160k': [
        'atomic-v0.2.ViT-bigG-14.laion2b_s39b_b160k.image.large',
        'atomic-v0.2.1.ViT-bigG-14.laion2b_s39b_b160k.text.large',
    ],
    'ViT-B-32.laion2b_e16': [
        'atomic-v0.2.ViT-B-32.laion2b_e16.image.large',
        'atomic-v0.2.1.ViT-B-32.laion2b_e16.text.large',
    ],
    'ViT-B-32.laion400m_e32': [
        'atomic-v0.2.ViT-B-32.laion400m_e32.image.large',
        'atomic-v0.2.1.ViT-B-32.laion400m_e32.text.large',
    ],
    'openai.clip-vit-base-patch32': [
        'atomic-v0.2.openai.clip-vit-base-patch32.image.large',
        'atomic-v0.2.1.openai.clip-vit-base-patch32.text.large',
    ],
    'openai.clip-vit-large-patch14': [
        'atomic-v0.2.openai.clip-vit-large-patch14.image.large',
        'atomic-v0.2.1.openai.clip-vit-large-patch14.text.large',
    ],
    'Salesforce.blip-itm-base-coco': [
        'atomic-v0.2.Salesforce.blip-itm-base-coco.image.large',
        'atomic-v0.2.1.Salesforce.blip-itm-base-coco.text.large',
    ],
    'Salesforce.blip-itm-large-coco': [
        'atomic-v0.2.Salesforce.blip-itm-large-coco.image.large',
        'atomic-v0.2.1.Salesforce.blip-itm-large-coco.text.large',
    ],
    'facebook.flava-full': [
        'atomic-v0.2.facebook.flava-full.image.large',
        'atomic-v0.2.1.facebook.flava-full.text.large',
    ],
}

INDEX_TO_ENCODED_QUERIES = {
    # 'ViT-L-14.laion2b_s32b_b82k'
    'atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.validation': 'atomic-v0.2-image-ViT-L-14.laion2b_s32b_b82k-validation',
    'atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.validation': 'atomic-v0.2.1-text-ViT-L-14.laion2b_s32b_b82k-validation',
    'atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.base': 'atomic-v0.2-image-ViT-L-14.laion2b_s32b_b82k-validation',
    'atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.base': 'atomic-v0.2.1-text-ViT-L-14.laion2b_s32b_b82k-validation',
    'atomic-v0.2.1.ViT-L-14.laion2b_s32b_b82k.text.large': 'atomic-v0.2-image-ViT-L-14.laion2b_s32b_b82k-validation',
    'atomic-v0.2.ViT-L-14.laion2b_s32b_b82k.image.large': 'atomic-v0.2.1-text-ViT-L-14.laion2b_s32b_b82k-validation',
    # ViT-H-14.laion2b_s32b_b79k
    'atomic-v0.2.ViT-H-14.laion2b_s32b_b79k.image.large': 'atomic-v0.2.1-text-ViT-H-14.laion2b_s32b_b79k-validation',
    'atomic-v0.2.1.ViT-H-14.laion2b_s32b_b79k.text.large': 'atomic-v0.2-image-ViT-H-14.laion2b_s32b_b79k-validation',
    # ViT-bigG-14.laion2b_s39b_b160k
    'atomic-v0.2.ViT-bigG-14.laion2b_s39b_b160k.image.large': 'atomic-v0.2.1-text-ViT-bigG-14.laion2b_s39b_b160k-validation',
    'atomic-v0.2.1.ViT-bigG-14.laion2b_s39b_b160k.text.large': 'atomic-v0.2-image-ViT-bigG-14.laion2b_s39b_b160k-validation',
    # ViT-B-32.laion2b_e16
    'atomic-v0.2.ViT-B-32.laion2b_e16.image.large': 'atomic-v0.2.1-text-ViT-B-32.laion2b_e16-validation',
    'atomic-v0.2.1.ViT-B-32.laion2b_e16.text.large': 'atomic-v0.2-image-ViT-B-32.laion2b_e16-validation',
    # ViT-B-32.laion400m_e32
    'atomic-v0.2.ViT-B-32.laion400m_e32.image.large': 'atomic-v0.2.1-text-ViT-B-32.laion400m_e32-validation',
    'atomic-v0.2.1.ViT-B-32.laion400m_e32.text.large': 'atomic-v0.2-image-ViT-B-32.laion400m_e32-validation',
    # openai.clip-vit-base-patch32
    'atomic-v0.2.openai.clip-vit-base-patch32.image.large': 'atomic-v0.2.1-text-openai.clip-vit-base-patch32-validation',
    'atomic-v0.2.1.openai.clip-vit-base-patch32.text.large': 'atomic-v0.2-image-openai.clip-vit-base-patch32-validation',
    # openai.clip-vit-large-patch14
    'atomic-v0.2.openai.clip-vit-large-patch14.image.large': 'atomic-v0.2.1-text-openai.clip-vit-large-patch14-validation',
    'atomic-v0.2.1.openai.clip-vit-large-patch14.text.large': 'atomic-v0.2-image-openai.clip-vit-large-patch14-validation',
    # Salesforce.blip-itm-base-coco
    'atomic-v0.2.Salesforce.blip-itm-base-coco.image.large': 'atomic-v0.2.1-text-Salesforce.blip-itm-base-coco-validation',
    'atomic-v0.2.1.Salesforce.blip-itm-base-coco.text.large': 'atomic-v0.2-image-Salesforce.blip-itm-base-coco-validation',
    # Salesforce.blip-itm-large-coco
    'atomic-v0.2.Salesforce.blip-itm-large-coco.image.large': 'atomic-v0.2.1-text-Salesforce.blip-itm-large-coco-validation',
    'atomic-v0.2.1.Salesforce.blip-itm-large-coco.text.large': 'atomic-v0.2-image-Salesforce.blip-itm-large-coco-validation',
    # facebook.flava-full
    'atomic-v0.2.facebook.flava-full.image.large': 'atomic-v0.2.1-text-facebook.flava-full-validation',
    'atomic-v0.2.1.facebook.flava-full.text.large': 'atomic-v0.2-image-facebook.flava-full-validation',
}

Searcher = Union[FaissSearcher, LuceneSearcher]


def create_app(k: int, load_searcher_fn: Callable[[str], Searcher]):
    app = Flask(__name__)

    # Use BM25 as default retriever upon page load
    retriever = "BM25"
    index_name = RETRIEVER_TO_INDEXES[retriever][0]
    searcher = load_searcher_fn(index_name=index_name)
    query_options = [] # for dense search only

    @app.route('/')
    def index():
        return render_template(
            'atomic.html', index_name=index_name, retriever=retriever, retriever_to_indexes=RETRIEVER_TO_INDEXES
        )

    @app.route('/search', methods=['GET', 'POST'])
    def search():
        query = request.form['q']
        if retriever != "BM25":
            query = query_options[int(query)]
        if not query:
            search_results = []
            flash('Question is required')
            # NOTE: this throws an exception unless we set a secret session key
        else:
            try:
                hits = searcher.search(query, k=k)
            except KeyError:
                hits = []
                flash('Invalid query given')
            docs = [json.loads(searcher.doc(hit.docid).raw()) for hit in hits]
            search_results = [
                {
                    'rank': r + 1,
                    'docid': hit.docid,
                    'content': docs[r]['contents'],
                    'score': hit.score,
                    'image_url': docs[r].get('image_url')
                }
                for r, hit in enumerate(hits)
            ]
        return render_template(
            'atomic.html', index_name=index_name, retriever=retriever,
            retriever_to_indexes=RETRIEVER_TO_INDEXES, search_results=search_results, query=query,
        )

    def _change_index(new_index_name):
        nonlocal index_name, searcher, query_options
        index_name = new_index_name
        searcher = load_searcher_fn(index_name=index_name)
        if retriever != "BM25":
            query_options = {i: option for i, option in enumerate(searcher.query_encoder.embedding.keys())}

    @app.route('/retriever', methods=['GET'])
    def change_retriever():
        nonlocal retriever
        new_retriever = request.args.get('new_retriever_name', '', type=str)
        if not new_retriever or new_retriever not in list(RETRIEVER_TO_INDEXES.keys()):
            return

        retriever = new_retriever
        _change_index(new_index_name=RETRIEVER_TO_INDEXES[retriever][0])
        return jsonify(index_list=RETRIEVER_TO_INDEXES[retriever])

    @app.route('/index', methods=['GET'])
    def change_index_name():
        new_index_name = request.args.get('new_index_name', '', type=str)
        if not new_index_name or new_index_name not in RETRIEVER_TO_INDEXES[retriever]:
            return
        _change_index(new_index_name)
        return jsonify(index_name=index_name)

    @app.route('/search_options', methods=['GET'])
    def search_options():
        query = request.args.get('query', '')

        matching_options = {
            i: option
            for i, option in query_options.items()
            if option.lower().startswith(query.lower())
        }
        return jsonify(matching_options)

    return app


def _load_searcher(index_name: str, language: str, k1: Optional[float]=None, b: Optional[float]=None):
    if index_name in RETRIEVER_TO_INDEXES['BM25']:
        searcher = LuceneSearcher.from_prebuilt_index(index_name)
        if k1 is not None and b is not None:
            searcher.set_bm25(k1, b)
    else:
        query_encoder = QueryEncoder.load_encoded_queries(INDEX_TO_ENCODED_QUERIES[index_name])
        searcher = FaissSearcher.from_prebuilt_index(
            index_name, query_encoder
        )
    return searcher


def main():
    parser = ArgumentParser()
    parser.add_argument('--k1', type=float, help='BM25 k1 parameter.')
    parser.add_argument('--b', type=float, help='BM25 b parameter.')
    parser.add_argument('--hits', type=int, default=10, help='Number of hits returned by the retriever')
    parser.add_argument(
        '--port', default=8080, type=int, help='Web server port',
    )
    args = parser.parse_args()

    load_fn = partial(_load_searcher, language='en', k1=args.k1, b=args.b)
    app = create_app(args.hits, load_fn)
    app.run(host='0.0.0.0', port=args.port)


if __name__ == '__main__':
    main()
