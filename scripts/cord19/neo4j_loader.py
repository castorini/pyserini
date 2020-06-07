# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

import pyserini.collection
import csv

collection = pyserini.collection.Collection('Cord19AbstractCollection', 'collections/cord19-2020-05-26')
articles = collection.__next__()

with open("articles.csv", 'w') as article_csv, open("edges.csv", 'w') as edge_csv:
    article_csv = csv.writer(article_csv)
    edge_csv = csv.writer(edge_csv)
    article_csv.writerow(["cord_uid", "title","publish_time"])
    edge_csv.writerow(["cord_uid", "target_title"])

    for (i, d) in enumerate(articles):
        article = pyserini.collection.Cord19Article(d.raw)
        if article.is_full_text() and article.title():
            try:
                publish_time = article.metadata()["publish_time"]
            except KeyError:
                publish_time = None
            article_data = [article.cord_uid(), article.title(), publish_time]
            article_csv.writerow(article_data)

            bib_entries = article.bib_entries()
            # Create edge between article and each cited title
            for bib_ref in bib_entries:
                ref = bib_entries[bib_ref]
                if ref['title']:
                    edge = [article.cord_uid(), ref['title']]
                    edge_csv.writerow(edge)
