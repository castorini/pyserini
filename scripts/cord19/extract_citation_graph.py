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

import argparse
import os
import csv

import pyserini.collection


def escape_title(title):
    # Neo4j CSV loader is sensitive to double qoutes
    return title.replace("\"", "\\'").replace("\\", "")


def main(path):
    collection = pyserini.collection.Collection('Cord19AbstractCollection', path)
    articles = collection.__next__()

    with open("articles.csv", 'w') as article_csv, open("edges.csv", 'w') as edge_csv:
        article_csv = csv.writer(article_csv)
        edge_csv = csv.writer(edge_csv)
        article_csv.writerow(["cord_uid", "title", "pmcid"])
        edge_csv.writerow(["cord_uid", "target_title", "doi"])

        prev_titles = set()
        prev_cord_uid = set()
        for d in articles:
            article = pyserini.collection.Cord19Article(d.raw)
            title = article.title()
            cord_uid = article.cord_uid()
            if article.is_full_text() and title and title not in prev_titles \
                    and cord_uid not in prev_cord_uid:
                article_data = [article.cord_uid(), escape_title(title),
                                article.json["paper_id"]]
                article_csv.writerow(article_data)
                prev_titles.add(title)
                prev_cord_uid.add(cord_uid)

                bib_entries = article.bib_entries()
                # Create edge between article and each cited title
                for bib_ref in bib_entries:
                    ref = bib_entries[bib_ref]
                    if ref['title']:
                        doi = ref['other_ids'].get('DOI')
                        doi = None if doi == [] or doi is None else doi[0]
                        edge = [article.cord_uid(), escape_title(ref['title']), doi]
                        edge_csv.writerow(edge)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load CORD-19 citation data into Neo4j')
    parser.add_argument('--path', type=str, required=True,
                        help='The path to CORD-19 collection')
    args = parser.parse_args()
    main(args.path)
