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

import os
import json
from abc import ABC, abstractmethod
from enum import Enum, unique
from pathlib import Path

from pyserini.search import get_topics, get_topics_with_reader
from pyserini.util import download_url, get_cache_home
from pyserini.external_query_info import KILT_QUERY_INFO
from urllib.error import HTTPError, URLError


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
        self.order = order if order else sorted(topics.keys())
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

    def __len__(self):
        return len(self.topics.keys())

    @staticmethod
    def get_predefined_order(topics_path: str):
        order = None
        normalized_path = Path(topics_path).stem  # get filename w/o extension
        normalized_path = normalized_path.replace('_', '-')

        if normalized_path in QueryIterator.PREDEFINED_ORDER:
            print(f'Using pre-defined topic order for {normalized_path}')
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
            if topics_path.endswith('.json'):
                with open(topics_path, 'r') as f:
                    topics = json.load(f)
            elif "beir" in topics_path:
                topics = get_topics_with_reader('io.anserini.search.topicreader.TsvStringTopicReader', topics_path)
            elif topics_path.endswith('.tsv') or topics_path.endswith('.tsv.gz'):
                try:
                    topics = get_topics_with_reader('io.anserini.search.topicreader.TsvIntTopicReader', topics_path)
                except ValueError as e:
                    topics = get_topics_with_reader('io.anserini.search.topicreader.TsvStringTopicReader', topics_path)
            elif topics_path.endswith('.trec'):
                topics = get_topics_with_reader('io.anserini.search.topicreader.TrecTopicReader', topics_path)
            elif 'cacm' in topics_path:
                topics = get_topics_with_reader('io.anserini.search.topicreader.CacmTopicReader', topics_path)
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
        if not os.path.exists(topics_path):
            # Download if necessary:
            topics_path = cls.download_kilt_topics(topics_path)
        with open(topics_path, 'r') as f:
            for line in f:
                datapoint = json.loads(line)
                topics[datapoint["id"]] = datapoint
                order.append(datapoint["id"])
        return cls(topics, order)

    @classmethod
    def download_kilt_topics(cls, task: str, force=False):
        if task not in KILT_QUERY_INFO:
            raise ValueError(f'Unrecognized query name {task}')
        task = KILT_QUERY_INFO[task]
        md5 = task['md5']
        save_dir = os.path.join(get_cache_home(), 'queries')
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        for url in task['urls']:
            try:
                return download_url(url, save_dir, force=force, md5=md5)
            except (HTTPError, URLError) as e:
                print(f'Unable to download encoded query at {url}, trying next URL...')
        raise ValueError(f'Unable to download encoded query at any known URLs.')


def get_query_iterator(topics_path: str, topics_format: TopicsFormat):
    mapping = {
        TopicsFormat.DEFAULT: DefaultQueryIterator,
        TopicsFormat.KILT: KiltQueryIterator,
    }
    return mapping[topics_format].from_topics(topics_path)
