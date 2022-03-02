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

import json
import os

from abc import ABC, abstractmethod
from enum import Enum, unique
from typing import List

from pyserini.search import JLuceneSearcherResult


@unique
class OutputFormat(Enum):
    TREC = 'trec'
    MSMARCO = "msmarco"
    KILT = 'kilt'


class OutputWriter(ABC):

    def __init__(self, file_path: str, mode: str = 'w',
                 max_hits: int = 1000, tag: str = None, topics: dict = None,
                 use_max_passage: bool = False, max_passage_delimiter: str = None, max_passage_hits: int = 100):
        self.file_path = file_path
        self.mode = mode
        self.tag = tag
        self.topics = topics
        self.use_max_passage = use_max_passage
        self.max_passage_delimiter = max_passage_delimiter if use_max_passage else None
        self.max_hits = max_passage_hits if use_max_passage else max_hits
        self._file = None

    def __enter__(self):
        dirname = os.path.dirname(self.file_path)
        if dirname:
            os.makedirs(dirname, exist_ok=True)
        self._file = open(self.file_path, self.mode)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self._file.close()

    def hits_iterator(self, hits: List[JLuceneSearcherResult]):
        unique_docs = set()
        rank = 1
        for hit in hits:
            if self.use_max_passage and self.max_passage_delimiter:
                docid = hit.docid.split(self.max_passage_delimiter)[0]
            else:
                docid = hit.docid.strip()

            if self.use_max_passage:
                if docid in unique_docs:
                    continue
                unique_docs.add(docid)

            yield docid, rank, hit.score, hit

            rank = rank + 1
            if rank > self.max_hits:
                break

    @abstractmethod
    def write(self, topic: str, hits: List[JLuceneSearcherResult]):
        raise NotImplementedError()


class TrecWriter(OutputWriter):
    def write(self, topic: str, hits: List[JLuceneSearcherResult]):
        for docid, rank, score, _ in self.hits_iterator(hits):
            self._file.write(f'{topic} Q0 {docid} {rank} {score:.6f} {self.tag}\n')


class MsMarcoWriter(OutputWriter):
    def write(self, topic: str, hits: List[JLuceneSearcherResult]):
        for docid, rank, score, _ in self.hits_iterator(hits):
            self._file.write(f'{topic}\t{docid}\t{rank}\n')


class KiltWriter(OutputWriter):
    def write(self, topic: str, hits: List[JLuceneSearcherResult]):
        datapoint = self.topics[topic]
        provenance = []
        for docid, rank, score, _ in self.hits_iterator(hits):
            provenance.append({"wikipedia_id": docid})
        datapoint["output"] = [{"provenance": provenance}]
        json.dump(datapoint, self._file)
        self._file.write('\n')


def get_output_writer(file_path: str, output_format: OutputFormat, *args, **kwargs) -> OutputWriter:
    mapping = {
        OutputFormat.TREC: TrecWriter,
        OutputFormat.MSMARCO: MsMarcoWriter,
        OutputFormat.KILT: KiltWriter,
    }
    return mapping[output_format](file_path, *args, **kwargs)


def tie_breaker(hits):
    return sorted(hits, key=lambda x: (-x.score, x.docid))
