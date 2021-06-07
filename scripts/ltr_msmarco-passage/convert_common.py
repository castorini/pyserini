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

import re
import spacy
"""
This file provides helpers to convert passage and queries
"""
def read_stopwords(fileName='stopwords.txt', lower_case=True):
    """Reads a list of stopwords from a file. By default the words
       are read from a standard repo location and are lower_cased.
      :param fileName a stopword file name
      :param lower_case  a boolean flag indicating if lowercasing is needed.
      :return a list of stopwords
    """
    stopwords = set()
    with open(fileName) as f:
        for w in f:
            w = w.strip()
            if w:
                if lower_case:
                    w = w.lower()
                stopwords.add(w)
    return stopwords

def is_alpha_num(s):
    return s and (re.match("^[a-zA-Z-_.0-9]+$", s) is not None)

class SpacyTextParser:
    def __init__(self, model_name, stopwords,
                 remove_punct=True,
                 sent_split=False,
                 keep_only_alpha_num=False,
                 lower_case=True,
                 enable_POS=True):
        """Constructor.
                :param  model_name    a name of the spacy model to use, e.g., en_core_web_sm
                :param  stopwords    a list of stop words to be excluded (case insensitive);
                                     a token is also excluded when its lemma is in the stop word list.
                :param  remove_punct  a bool flag indicating if the punctuation tokens need to be removed
                :param  sent_split    a bool flag indicating if sentence splitting is necessary
                :param  keep_only_alpha_num a bool flag indicating if we need to keep only alpha-numeric characters
                :param  enable_POS    a bool flag that enables POS tagging (which, e.g., can improve lemmatization)
        """

        disable_list = ['ner', 'parser']
        if not enable_POS:
            disable_list.append('tagger')
        print('Disabled Spacy components: ', disable_list)

        self._nlp = spacy.load(model_name, disable=disable_list)
        if sent_split:
            sentencizer = self._nlp.create_pipe("sentencizer")
            self._nlp.add_pipe(sentencizer)

        self._remove_punct = remove_punct
        self._stopwords = frozenset([w.lower() for w in stopwords])
        self._keep_only_alpha_num = keep_only_alpha_num
        self._lower_case = lower_case

    @staticmethod
    def _basic_clean(text):
        return text.replace("’", "'")

    def __call__(self, text):
        """A thin wrapper that merely calls spacy.
        :param text     input text string
        :return         a spacy Doc object
        """

        return self._nlp(SpacyTextParser._basic_clean(text))

    def proc_text(self, text):
        """Process text, remove stopwords and obtain lemmas, but does not split into sentences.
        This function should not emit newlines!
        :param text     input text string
        :return         a tuple (lemmatized text, original-form text). Text is white-space separated.
        """

        lemmas = []
        tokens = []
        doc = self(text)
        for tokObj in doc:
            if self._remove_punct and tokObj.is_punct:
                continue
            lemma = tokObj.lemma_
            text = tokObj.text
            if self._keep_only_alpha_num and not is_alpha_num(text):
                continue
            tok1 = text.lower()
            tok2 = lemma.lower()
            if tok1 in self._stopwords or tok2 in self._stopwords:
                continue

            if self._lower_case:
                text = text.lower()
                lemma = lemma.lower()

            lemmas.append(lemma)
            tokens.append(text)

        return ' '.join(lemmas), ' '.join(tokens)


def get_retokenized(tokenizer, text):
    """Obtain a space separated re-tokenized text.
    :param tokenizer:  a tokenizer that has the function
                       tokenize that returns an array of tokens.
    :param text:       a text to re-tokenize.
    """
    return ' '.join(tokenizer.tokenize(text))


def add_retokenized_field(data_entry,
                        src_field,
                        dst_field,
                        tokenizer):
    """
    Create a re-tokenized field from an existing one.
    :param data_entry:   a dictionary of entries (keys are field names, values are text items)
    :param src_field:    a source field
    :param dst_field:    a target field
    :param tokenizer:    a tokenizer to use, if None, nothing is done
    """
    if tokenizer is not None:
        dst = ''
        if src_field in data_entry:
            dst = get_retokenized(tokenizer, data_entry[src_field])

        data_entry[dst_field] = dst