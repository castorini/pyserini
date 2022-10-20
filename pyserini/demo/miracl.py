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
This script provides a web interface demo for retrieval on the MIRACL dataset.
It requires `flask` (`pip install flask~=2.2.0`).
An example command looks like `python -m pyserini.demo.miracl --language en` that starts up a server on port 8080.
The demo can be accessed via "http://localhost:8080" in a web browser.
Additional arguments include:
    `--port [PORT] --hits [Number of hits] --index [BM25 or mdpr-pft] --k1 [BM25 k1] --b [BM25 b] --device [cpu, cuda]`
"""
import json
import logging
from argparse import ArgumentParser

from flask import Flask, render_template, request, flash
from pyserini.search import LuceneSearcher, FaissSearcher, AutoQueryEncoder

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
logger = logging.getLogger("miracl-demo")

VERSION = "1.0"
LANGUAGES = ("ar", "bn", "en", "es", "fa", "fi", "fr", "hi", "id", "ja", "ko", "ru", "sw", "te", "th", "zh")


def create_app(searcher, lang: str, k: int, retriever: str):
    app = Flask(__name__)

    @app.route("/")
    def index():
        return render_template("miracl.html", lang=lang, retriever=retriever)

    @app.route("/search", methods=["GET", "POST"])
    def search():
        query = request.form["q"]
        if not query:
            search_results = []
            flash("Question is required")
        else:
            hits = searcher.search(query, k=k)
            docs = [json.loads(searcher.doc(hit.docid).raw()) for hit in hits]
            search_results = [
                {
                    "rank": r + 1,
                    "docid": hit.docid,
                    "doc": docs[r]["text"],
                    "title": docs[r]["title"],
                    "score": hit.score,
                }
                for r, hit in enumerate(hits)
            ]
        return render_template(
            "miracl.html", search_results=search_results, query=query, lang=lang, retriever=retriever
        )

    return app


def main():
    parser = ArgumentParser()

    parser.add_argument(
        "--language",
        type=str,
        choices=LANGUAGES,
        required=True,
        default=None,
    )
    parser.add_argument("--index", default="BM25", choices=("BM25", "mdpr-pft"), help="Index type.")
    parser.add_argument("--k1", type=float, help="BM25 k1 parameter.")
    parser.add_argument("--b", type=float, help="BM25 b parameter.")
    parser.add_argument("--hits", type=int, default=10, help="Number of hits returned by the retriever")
    parser.add_argument(
        "--device",
        type=str,
        default="cpu",
        help="Device to run query encoder, cpu or [cuda:0, cuda:1, ...] (used only when index is based on FAISS)",
    )
    parser.add_argument(
        "--port",
        default=8080,
        type=int,
        help="Web server port",
    )

    args = parser.parse_args()

    if args.index == "mdpr-pft":
        query_encoder = AutoQueryEncoder(encoder_dir="castorini/mdpr-tied-pft-msmarco", device=args.device)
        searcher = FaissSearcher.from_prebuilt_index(
            f"miracl-v{VERSION}-{args.language}-mdpr-tied-pft-msmarco", query_encoder
        )
        retriever = "mDPR-pFT-MSMARCO"
    else:
        searcher = LuceneSearcher.from_prebuilt_index(f"miracl-v{VERSION}-{args.language}")
        searcher.set_language(args.language)
        if args.k1 is not None and args.b is not None:
            searcher.set_bm25(args.k1, args.b)
            retriever = f"BM25 (k1={args.k1}, b={args.b})"
        else:
            retriever = "BM25"

    app = create_app(searcher, args.language, args.hits, retriever)
    app.run(host="0.0.0.0", port=args.port)


if __name__ == "__main__":
    main()
