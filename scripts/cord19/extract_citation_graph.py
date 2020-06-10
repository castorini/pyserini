#
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
#

import pyserini.collection
import argparse
import os
import json
import csv

def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"{path} is not a valid path")

def node(node_file, mode, fieldnames):
    with open(node_file, mode) as file1:
        fieldname = fieldnames
        writer = csv.writer(file1)
        writer.writerow(fieldnames)

def edge(edge_file, mode, fieldnames):
    with open(edge_file, mode) as file2:
        fieldname = fieldnames
        writer = csv.writer(file2)
        writer.writerow(fieldnames)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=dir_path)
    parser.add_argument("-node_file", default="node.csv")
    parser.add_argument("-edge_file", default="edge.csv")
    args = parser.parse_args()
    collection = pyserini.collection.Collection('Cord19AbstractCollection', args.path)
    articles = collection.__next__()
    article = None
    node(args.node_file, 'w', ['Id'])
    edge(args.edge_file, 'w', ['Source', 'Target'])

    for (i, d) in enumerate(articles):
        article = pyserini.collection.Cord19Article(d.raw)
        if article.is_full_text():
            bib = article.bib_entries()
            node(args.node_file, 'a', [article.title()])
            j = 0
            number = 'BIBREF%d' %j
            while True:
                if number in bib:
                    title = bib[number]['title']
                    if title != '':
                        node(args.node_file, 'a', [title])
                        edge(args.edge_file, 'a', [article.title(), title])
                    j = j + 1
                    number = 'BIBREF%d' % j
                elif j < len(bib):
                    j = j + 1
                    number = 'BIBREF%d' % j
                else:
                    break

