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
        writer = csv.writer(file1)
        writer.writerow(fieldnames)

def edge(edge_file, mode, fieldnames):
    with open(edge_file, mode) as file2:
        writer = csv.writer(file2)
        writer.writerow(fieldnames)

def create_dict(key, value):
    data = {}
    data[key] = value
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-path', type=dir_path)
    parser.add_argument("-node_file", default="node.csv")
    parser.add_argument("-edge_file", default="edge.csv")
    args = parser.parse_args()
    collection = pyserini.collection.Collection('Cord19AbstractCollection', args.path)
    articles = collection.__next__()
    article = None
    mapping = {}
    node(args.node_file, 'w', ["id", "title", "publication_date"])
    edge(args.edge_file, 'w', ["source", "target", "target_title"])
    mapping = {}
    check_replication = {}
    for (i, d) in enumerate(articles):
        article = pyserini.collection.Cord19Article(d.raw)
        if article.title() not in mapping:
            mapping.update(create_dict(article.title(), article.cord_uid()))
            
    count = 1
    collection = pyserini.collection.Collection('Cord19AbstractCollection', args.path)
    articles = collection.__next__()
    article = None

    for (i, d) in enumerate(articles):
        if i == 100:
            break
        article = pyserini.collection.Cord19Article(d.raw)
        if article.is_full_text():
            bib = article.bib_entries()
            if article.title() not in check_replication:
                if 'publish_time' in article.metadata():
                    publish_time = article.metadata()['publish_time']
                else:
                    publish_time = ''
                node(args.node_file, 'a', [mapping[article.title()], article.title(), publish_time])
                check_replication.update(create_dict(article.title(), ''))
            j = 0
            number = 'BIBREF%d' %j
            while True:
                if number in bib:
                    title = bib[number]['title']
                    if title:
                        if 'year' in bib[number]:
                            publish_time = bib[number]['year']
                        else:
                            publish_time = ''
                        if title not in check_replication:
                            if title in mapping:
                                node(args.node_file, 'a', [mapping[title], title, publish_time])
                                edge(args.edge_file, 'a', [mapping[article.title()], mapping[title], title])
                                check_replication.update(create_dict(title, ''))
                            elif 'DOI' in bib[number]['other_ids'] and bib[number]['other_ids']['DOI']:
                                node(args.node_file, 'a', [bib[number]['other_ids']['DOI'], title, publish_time])
                                edge(args.edge_file, 'a', [mapping[article.title()], bib[number]['other_ids']['DOI'], title])
                                check_replication.update(create_dict(title, ''))
                            else:
                                node(args.node_file, 'a', ["not_in_collection_%d" %count, title, publish_time])
                                edge(args.edge_file, 'a', [mapping[article.title()], "not_in_collection_%d" %count, title])
                                check_replication.update(create_dict(title, "not_in_collection_%d" %count))
                                count = count + 1
                        else:
                            if title in mapping:
                                edge(args.edge_file, 'a', [mapping[article.title()], mapping[title], title])
                            elif 'DOI' in bib[number]['other_ids'] and bib[number]['other_ids']['DOI']:
                                edge(args.edge_file, 'a', [mapping[article.title()], bib[number]['other_ids']['DOI'], title])
                            else:
                                edge(args.edge_file, 'a', [mapping[article.title()], check_replication[title], title])
                    j = j + 1
                    number = 'BIBREF%d' % j
                elif j < len(bib):
                    j = j + 1
                    number = 'BIBREF%d' % j
                else:
                    break

