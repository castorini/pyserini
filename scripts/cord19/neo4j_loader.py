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
from py2neo import Graph

db_uri = "bolt://localhost:7687"
graph = Graph(db_uri)
queries = {
    "CORD_UID_CONSTRAINT":
        """
        // Improve lookup time 
        CREATE CONSTRAINT cord_uid ON (n:Article) ASSERT n.cord_uid IS UNIQUE
        CREATE INDEX ON:Article(title)
        """,
    "CREATE_ARTICLE":
        """
        MERGE(article:Article {cord_uid:$CORD_UID,
                                title:$TITLE,
                                publish_time:$PUBLISH_TIME,
                                abstract:$ABSTRACT})
        """,
    "CREATE_CITATIONS":
        """
        // Match source article
        MATCH(article:Article {cord_uid:$ORIGIN_CORD_UID})
        // Find or create the cited article (no cord_uid)
        MERGE(cited:Article {title:$TITLE})
        MERGE (article)-[r:BIB_REF]->(cited)
        """
}

graph.run(queries["CORD_UID_CONSTRAINT"])
collection = pyserini.collection.Collection('Cord19AbstractCollection',
                                            'collections/cord19-2020-05-26')
articles = collection.__next__()

for (i, d) in enumerate(articles):
    article = pyserini.collection.Cord19Article(d.raw)
    if article.is_full_text() and article.title():
        try:
            publish_time = article.metadata()["publish_time"]
        except KeyError:
            publish_time = None
        graph.run(queries["CREATE_ARTICLE"],
                  CORD_UID=article.cord_uid(),
                  TITLE=article.title(),
                  PUBLISH_TIME=publish_time,
                  ABSTRACT=article.abstract())
        bib_entries = article.bib_entries()
        # Create edge between article and each cited title
        for bib_ref in bib_entries:
            ref = bib_entries[bib_ref]
            graph.run(queries["CREATE_CITATIONS"],
                      ORIGIN_CORD_UID=article.cord_uid(),
                      TITLE=ref['title'])
        
        print(f"Number: {i}")
