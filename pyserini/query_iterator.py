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

import os
import json
from enum import Enum, unique

from pyserini.search import get_topics


@unique
class TopicsFormat(Enum):
    JSON = 'json'
    KILT = 'kilt'


class JsonQueryIterator:

    PREDEFINED_ORDER = {'msmarco-doc-dev',
                        'msmarco_doc_test',
                        'msmarco-passage-dev-subset',
                        'msmarco_passage_test_subset'}

    def __init__(self, topics: dict, order: list = None):
        self.order = order if order else sorted(topics.keys())
        self.topics = topics

    def __iter__(self):
        for id_ in self.order:
            yield id_, self.topics[id_].get('title')

    @classmethod
    def from_topics(cls, topics_path: str):
        if os.path.exists(topics_path):
            f = open(topics_path, 'r')
            topics = json.load(f)
            f.close()
        else:
            topics = get_topics(topics_path)
        if not topics:
            raise FileNotFoundError(f'Topic {topics_path} Not Found')
        order = None
        if topics_path in JsonQueryIterator.PREDEFINED_ORDER:
            print(f'Using pre-defined topic order for {topics_path}')
            # Lazy import:
            from pyserini.query_iterator_order_info import QUERY_IDS
            order = QUERY_IDS[topics_path]
        return cls(topics, order)


class KiltQueryIterator:

    ENT_START_TOKEN = "[START_ENT]"
    ENT_END_TOKEN = "[END_ENT]"

    def __init__(self, topics: dict, order: list):
        self.order = order
        self.topics = topics

    def __iter__(self):
        for id_ in self.order:
            datapoint = self.topics[id_]
            query = (
                datapoint["input"]
                .replace(KiltQueryIterator.ENT_START_TOKEN, "")
                .replace(KiltQueryIterator.ENT_END_TOKEN, "")
                .strip()
            )
            yield id_, query

    @classmethod
    def from_topics(cls, topics_path: str):
        topics = {}
        order = []
        with open(topics_path, 'r') as f:
            for line in f:
                datapoint = json.loads(line)
                topics[datapoint["id"]] = datapoint
                order.append(datapoint["id"])
        return cls(topics, order)


def get_query_iterator(topics_path: str, topics_format: TopicsFormat):
    mapping = {
        TopicsFormat.JSON: JsonQueryIterator,
        TopicsFormat.KILT: KiltQueryIterator,
    }
    return mapping[topics_format].from_topics(topics_path)
