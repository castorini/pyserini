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

from typing import List

from ..pyclass import JAnalyzerUtils
from ..pyclass import JArabicAnalyzer
from ..pyclass import JBengaliAnalyzer
from ..pyclass import JCJKAnalyzer
from ..pyclass import JDefaultEnglishAnalyzer
from ..pyclass import JFreebaseAnalyzer
from ..pyclass import JFrenchAnalyzer
from ..pyclass import JGermanAnalyzer
from ..pyclass import JHindiAnalyzer
from ..pyclass import JSpanishAnalyzer
from ..pyclass import JString
from ..pyclass import JTweetAnalyzer
from ..pyclass import JCharArraySet


def get_lucene_analyzer(name='english', stemming=True, stemmer='porter', stopwords=True):
    """
    Parameters
    ----------
    name : Str
        Name of analyzer.
    stemming : Bool
        Whether or not to stem.
    stemmer : Str
        Stemmer to use.
    stopwords : Bool
        Whether or not to filter stopwords.

    Returns
    -------
    result : org.apache.lucene.document.Analyzer
        Java Analyzer object
    """
    if name.lower() == 'arabic':
        return JArabicAnalyzer()
    elif name.lower() == 'bengali':
        return JBengaliAnalyzer()
    elif name.lower() == 'cjk':
        return JCJKAnalyzer()
    elif name.lower() == 'german':
        return JGermanAnalyzer()
    elif name.lower() == 'spanish':
        return JSpanishAnalyzer()
    elif name.lower() == 'french':
        return JFrenchAnalyzer()
    elif name.lower() == 'hindi':
        return JHindiAnalyzer()
    elif name.lower() == 'freebase':
        return JFreebaseAnalyzer()
    elif name.lower() == 'tweet':
        return JTweetAnalyzer()
    elif name.lower() == 'english':
        if stemming == True:
            if stopwords == True:
                return JDefaultEnglishAnalyzer.newStemmingInstance(JString(stemmer))
            else:
                return JDefaultEnglishAnalyzer.newStemmingInstance(JString(stemmer), JCharArraySet.EMPTY_SET)
        else:
            if stopwords == True:
                return JDefaultEnglishAnalyzer.newNonStemmingInstance()
            else:
                return JDefaultEnglishAnalyzer.newNonStemmingInstance(JCharArraySet.EMPTY_SET)
    else:
        raise ValueError('Invalid configuration.')


class Analyzer:
    """
    Python wrapper around a Lucene Analyzer for easy analysis.

    Parameters
    ----------
    analyzer : org.apache.lucene.document.Analyzer
        Lucene Analyzer.
    """

    def __init__(self, analyzer):
        self.analyzer = analyzer

    def analyze(self, text: str) -> List[str]:
        """Analyzes a piece of text.

        Parameters
        ----------
        text : str
            The piece of text to analyze.

        Returns
        -------
        List[str]
            List of tokens corresponding to the output of the analyzer.
        """
        results = JAnalyzerUtils.analyze(self.analyzer, JString(text.encode('utf-8')))
        tokens = []
        for token in results.toArray():
            tokens.append(token)
        return tokens
