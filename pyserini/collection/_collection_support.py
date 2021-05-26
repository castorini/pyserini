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

# Implementations of support for specific collections.

import json


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

    def bib_entries(self):
        return self.json['bib_entries']

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
