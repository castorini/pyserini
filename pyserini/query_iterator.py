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
from abc import ABC, abstractmethod
from enum import Enum, unique

from pyserini.search import get_topics


@unique
class TopicsFormat(Enum):
    DEFAULT = 'default'
    KILT = 'kilt'


class QueryIterator(ABC):

    PREDEFINED_ORDER = {'msmarco-doc-dev',
                        'msmarco-doc-test',
                        'msmarco-passage-dev-subset',
                        'msmarco-passage-test-subset'}

    def __init__(self, topics: dict, order: list = None):
        self.order = order if order else topics.keys()
        self.topics = topics

    @abstractmethod
    def get_query(self, id_):
        raise NotImplementedError()

    @classmethod
    @abstractmethod
    def from_topics(cls, topics_path: str):
        raise NotImplementedError()

    def __iter__(self):
        for id_ in self.order:
            yield id_, self.get_query(id_)

    @staticmethod
    def get_predefined_order(topics_path: str):
        order = None
        if topics_path in QueryIterator.PREDEFINED_ORDER:
            print(f'Using pre-defined topic order for {topics_path}')
            # Lazy import:
            from pyserini.query_iterator_order_info import QUERY_IDS
            order = QUERY_IDS[topics_path]
        return order


class DefaultQueryIterator(QueryIterator):

    def get_query(self, id_):
        return self.topics[id_].get('title')

    @classmethod
    def from_topics(cls, topics_path: str):
        if os.path.exists(topics_path):
            with open(topics_path, 'r') as f:
                if topics_path.endswith('.json'):
                    topics = json.load(f)
                elif topics_path.endswith('.tsv'):
                    topics = {}
                    for line in f:
                        topic, text = line.rstrip().split('\t')
                        try:
                            topic = int(topic)
                        except ValueError:
                            pass
                        topics[topic] = {'title': text}
                else:
                    raise NotImplementedError(f"Not sure how to parse {topics_path}. Please specify the file extension.")
        else:
            topics = get_topics(topics_path)
        if not topics:
            raise FileNotFoundError(f'Topic {topics_path} Not Found')
        order = QueryIterator.get_predefined_order(topics_path)
        return cls(topics, order)


class KiltQueryIterator(QueryIterator):

    ENT_START_TOKEN = "[START_ENT]"
    ENT_END_TOKEN = "[END_ENT]"

    def get_query(self, id_):
        datapoint = self.topics[id_]
        query = (
            datapoint["input"]
            .replace(KiltQueryIterator.ENT_START_TOKEN, "")
            .replace(KiltQueryIterator.ENT_END_TOKEN, "")
            .strip()
        )
        return query

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
        TopicsFormat.DEFAULT: DefaultQueryIterator,
        TopicsFormat.KILT: KiltQueryIterator,
    }
    return mapping[topics_format].from_topics(topics_path)
