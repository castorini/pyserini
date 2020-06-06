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

from typing import List

from ..pyclass import autoclass, JString

# Wrappers around Lucene classes
JAnalyzer = autoclass('org.apache.lucene.analysis.Analyzer')
JArabicAnalyzer = autoclass('org.apache.lucene.analysis.ar.ArabicAnalyzer')
JBengaliAnalyzer = autoclass('org.apache.lucene.analysis.bn.BengaliAnalyzer')
JCJKAnalyzer = autoclass('org.apache.lucene.analysis.cjk.CJKAnalyzer')
JGermanAnalyzer = autoclass('org.apache.lucene.analysis.de.GermanAnalyzer')
JSpanishAnalyzer = autoclass('org.apache.lucene.analysis.es.SpanishAnalyzer')
JFrenchAnalyzer = autoclass('org.apache.lucene.analysis.fr.FrenchAnalyzer')
JHindiAnalyzer = autoclass('org.apache.lucene.analysis.hi.HindiAnalyzer')
JDefaultEnglishAnalyzer = autoclass('io.anserini.analysis.DefaultEnglishAnalyzer')
JCharArraySet = autoclass('org.apache.lucene.analysis.CharArraySet')

# Wrappers around Anserini classes
JAnalyzerUtils = autoclass('io.anserini.analysis.AnalyzerUtils')
JFreebaseAnalyzer = autoclass('io.anserini.analysis.FreebaseAnalyzer')
JTweetAnalyzer = autoclass('io.anserini.analysis.TweetAnalyzer')


def get_lucene_analyzer(name='english', stemming=True, stemmer='porter', stopwords=True) -> JAnalyzer:
    """Create a Lucene ``Analyzer`` with specific settings.

    Parameters
    ----------
    name : str
        Name of analyzer.
    stemming : bool
        Set to stem.
    stemmer : str
        Stemmer to use.
    stopwords : bool
        Set to filter stopwords.

    Returns
    -------
    JAnalyzer
        Java ``Analyzer`` with specified settings.
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
        if stemming:
            if stopwords:
                return JDefaultEnglishAnalyzer.newStemmingInstance(JString(stemmer))
            else:
                return JDefaultEnglishAnalyzer.newStemmingInstance(JString(stemmer), JCharArraySet.EMPTY_SET)
        else:
            if stopwords:
                return JDefaultEnglishAnalyzer.newNonStemmingInstance()
            else:
                return JDefaultEnglishAnalyzer.newNonStemmingInstance(JCharArraySet.EMPTY_SET)
    else:
        raise ValueError('Invalid configuration.')


class Analyzer:
    """Python wrapper around a Lucene ``Analyzer`` to simplify analysis.

    Parameters
    ----------
    analyzer : JAnalyzer
        Lucene ``Analyzer``.
    """

    def __init__(self, analyzer):
        if not isinstance(analyzer, JAnalyzer):
            raise TypeError('Invalid JAnalyzer!')
        self.analyzer = analyzer

    def analyze(self, text: str) -> List[str]:
        """Analyze a piece of text.

        Parameters
        ----------
        text : str
            Text to analyze.

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
