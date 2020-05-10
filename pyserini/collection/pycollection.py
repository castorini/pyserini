# -*- coding: utf-8 -*-
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

import json
import logging
import re

from ..multithreading import Counters
from ..pyclass import JCollections, JPaths, cast

logger = logging.getLogger(__name__)


class Collection:
    """
    Iterable wrapper class for Anserini's DocumentCollection.

    Parameters
    ----------
    collection_class : str
        Name of collection class to instantiate
    collection_path : str
        Path to directory containing collection
    """

    def __init__(self, collection_class, collection_path):
        self.counters = Counters()
        self.collection_class = collection_class
        self.collection_path = JPaths.get(collection_path)
        self.object = self._get_collection()
        self.collection_iterator = self.object.iterator()

    def _get_collection(self):
        try:
            return JCollections[self.collection_class].value(self.collection_path)
        except:
            raise ValueError(self.collection_class)

    def __iter__(self):
        return self

    def __next__(self):
        if self.collection_iterator.hasNext():
            fs = self.collection_iterator.next()
            return FileSegment(self, fs, fs.getSegmentPath())
        else:
            raise StopIteration


class FileSegment:
    """
    Iterable wrapper class for Anserini's FileSegment.

    Parameters
    ----------
    collection : Collection
        Parent collection of the file segment
    segment : io.anserini.collection.FileSegment
        FileSegment object to create wrapper from
    segment_path : str
        Path to file backing the file segment
    """

    def __init__(self, collection, segment, segment_path):
        self.collection = collection
        try:
            self.object = cast(collection.object.getClass().getName() +
                               '$Segment', segment)
        except:
            logger.exception('Exception from casting FileSegment type...')
            self.object = cast('io.anserini.collection.FileSegment', segment)

        self.segment_iterator = self.object.iterator()
        self.segment_path = segment_path
        self.segment_name = re.sub(r'\\|\/', '-', collection.collection_path.relativize(segment_path).toString())

    def __iter__(self):
        return self

    def __next__(self):
        if self.object.iterator().hasNext():
            d = self.object.iterator().next()
            return SourceDocument(self, d)
        else:
            # log if iteration stopped by error
            if self.object.getErrorStatus():
                logger.error(self.segment_name + ': Error from segment iteration, stopping...')
                self.collection.counters.errors.increment()

            # stop iteration and log skipped documents
            skipped = self.object.getSkippedCount()
            if skipped > 0:
                self.collection.counters.skips.increment(skipped)
                logger.warning(self.segment_name + ': ' + str(skipped) + ' documents skipped')
            self.object.close()
            raise StopIteration


class SourceDocument:
    """
    Wrapper class for Anserini's SourceDocument.

    Parameters
    ----------

    segment : FileSegment
        Parent segment of the source document
    document : io.anserini.collection.SourceDocument
        SourceDocument object to create wrapper from
    """

    def __init__(self, segment, document):
        self.segment = segment
        self.object = document
        self.id = self.object.id()
        self.indexable = self.object.indexable()
        self.contents = self.object.contents()
        self.raw = self.object.raw()


class Cord19Article:
    """Wrapper class for a raw JSON article from AI2's COVID-19 Open Research Dataset (CORD-19).

    Parameters
    ----------
    doc : str
        A JSON string of a CORD-19 article.
    """

    def __init__(self, doc):
        self.json = json.loads(doc)
        # Performs some basic error checking, throws an exception if user tries to instantiate with something
        # that isn't from CORD-19.
        if 'cord_uid' in self.json:
            self.full_text = False
        elif 'paper_id' in self.json:
            self.full_text = True
        else:
            raise TypeError

    def is_full_text(self):
        return self.json['has_full_text']

    def cord_uid(self):
        return self.json['cord_uid']

    def title(self):
        try:
            if self.is_full_text():
                return self.json['metadata']['title']
            else:
                return self.json['csv_metadata']['title']
        except KeyError:
            return ''

    def abstract(self):
        try:
            # For a full-text article, we can grab the abstract from two independent sources, the metadata or the
            # actual full text. Here, we make the decision to use the metadata, even for full text.
            return self.json['csv_metadata']['abstract']
        except KeyError:
            return ''

    def metadata(self):
        return self.json['csv_metadata']

    def body(self):
        try:
            if self.is_full_text():
                return [entry['text'] for entry in self.json['body_text']]
            else:
                return []
        except KeyError:
            return ''
