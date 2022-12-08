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

from typing import List

from ..pyclass import autoclass

# Wrappers around Lucene classes
JAnalyzer = autoclass('org.apache.lucene.analysis.Analyzer')
JArabicAnalyzer = autoclass('org.apache.lucene.analysis.ar.ArabicAnalyzer')
JBengaliAnalyzer = autoclass('org.apache.lucene.analysis.bn.BengaliAnalyzer')
JCJKAnalyzer = autoclass('org.apache.lucene.analysis.cjk.CJKAnalyzer')
JDanishAnalyzer = autoclass('org.apache.lucene.analysis.da.DanishAnalyzer')
JDefaultEnglishAnalyzer = autoclass('io.anserini.analysis.DefaultEnglishAnalyzer')
JDutchAnalyzer = autoclass('org.apache.lucene.analysis.nl.DutchAnalyzer')
JFinnishAnalyzer = autoclass('org.apache.lucene.analysis.fi.FinnishAnalyzer')
JFrenchAnalyzer = autoclass('org.apache.lucene.analysis.fr.FrenchAnalyzer')
JGermanAnalyzer = autoclass('org.apache.lucene.analysis.de.GermanAnalyzer')
JHindiAnalyzer = autoclass('org.apache.lucene.analysis.hi.HindiAnalyzer')
JHungarianAnalyzer = autoclass('org.apache.lucene.analysis.hu.HungarianAnalyzer')
JIndonesianAnalyzer = autoclass('org.apache.lucene.analysis.id.IndonesianAnalyzer')
JItalianAnalyzer = autoclass('org.apache.lucene.analysis.it.ItalianAnalyzer')
JJapaneseAnalyzer = autoclass('org.apache.lucene.analysis.ja.JapaneseAnalyzer')
JNorwegianAnalyzer = autoclass('org.apache.lucene.analysis.no.NorwegianAnalyzer')
JPortugueseAnalyzer = autoclass('org.apache.lucene.analysis.pt.PortugueseAnalyzer')
JRussianAnalyzer = autoclass('org.apache.lucene.analysis.ru.RussianAnalyzer')
JSpanishAnalyzer = autoclass('org.apache.lucene.analysis.es.SpanishAnalyzer')
JSwedishAnalyzer = autoclass('org.apache.lucene.analysis.sv.SwedishAnalyzer')
JTeluguAnalyzer = autoclass('org.apache.lucene.analysis.te.TeluguAnalyzer')
JThaiAnalyzer = autoclass('org.apache.lucene.analysis.th.ThaiAnalyzer')
JTurkishAnalyzer = autoclass('org.apache.lucene.analysis.tr.TurkishAnalyzer')
JWhiteSpaceAnalyzer = autoclass('org.apache.lucene.analysis.core.WhitespaceAnalyzer')
JCharArraySet = autoclass('org.apache.lucene.analysis.CharArraySet')

# Wrappers around Anserini classes
JAnalyzerUtils = autoclass('io.anserini.analysis.AnalyzerUtils')
JDefaultEnglishAnalyzer = autoclass('io.anserini.analysis.DefaultEnglishAnalyzer')
JTweetAnalyzer = autoclass('io.anserini.analysis.TweetAnalyzer')
JHuggingFaceTokenizerAnalyzer = autoclass('io.anserini.analysis.HuggingFaceTokenizerAnalyzer')


def get_lucene_analyzer(language: str='en', stemming: bool=True, stemmer: str='porter', stopwords: bool=True, huggingFaceTokenizer: str=None) -> JAnalyzer:
    """Create a Lucene ``Analyzer`` with specific settings.

    Parameters
    ----------
    language : str
        Name of analyzer.
    stemming : bool
        Set to stem.
    stemmer : str
        Stemmer to use.
    stopwords : bool
        Set to filter stopwords.
    huggingFaceTokenizer: str
        a huggingface model id or path to a tokenizer.json file

    Returns
    -------
    JAnalyzer
        Java ``Analyzer`` with specified settings.
    """
    if language.lower() == 'ar':
        return JArabicAnalyzer()
    elif language.lower() == 'bn':
        return JBengaliAnalyzer()
    elif language.lower() in ['zh', 'ko']:
        return JCJKAnalyzer()
    elif language.lower() == 'da':
        return JDanishAnalyzer()
    elif language.lower() == 'nl':
        return JDutchAnalyzer()
    elif language.lower() == 'fi':
        return JFinnishAnalyzer()
    elif language.lower() == 'fr':
        return JFrenchAnalyzer()
    elif language.lower() == 'de':
        return JGermanAnalyzer()
    elif language.lower() == 'hi':
        return JHindiAnalyzer()
    elif language.lower() == 'hu':
        return JHungarianAnalyzer()
    elif language.lower() == 'id':
        return JIndonesianAnalyzer()
    elif language.lower() == 'it':
        return JItalianAnalyzer()
    elif language.lower() == 'ja':
        return JJapaneseAnalyzer()
    elif language.lower() == 'no':
        return JNorwegianAnalyzer()
    elif language.lower() == 'pt':
        return JPortugueseAnalyzer()
    elif language.lower() == 'ru':
        return JRussianAnalyzer()
    elif language.lower() == 'es':
        return JSpanishAnalyzer()
    elif language.lower() == 'te':
        return JTeluguAnalyzer()
    elif language.lower() == 'th':
        return JThaiAnalyzer()
    elif language.lower() == 'tr':
        return JTurkishAnalyzer()
    elif language.lower() == 'tweet':
        return JTweetAnalyzer()
    elif language.lower() == 'hgf_tokenizer':
        return JHuggingFaceTokenizerAnalyzer(huggingFaceTokenizer)
    elif language.lower() == 'en':
        if stemming:
            if stopwords:
                return JDefaultEnglishAnalyzer.newStemmingInstance(stemmer)
            else:
                return JDefaultEnglishAnalyzer.newStemmingInstance(stemmer, JCharArraySet.EMPTY_SET)
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
        results = JAnalyzerUtils.analyze(self.analyzer, text)
        tokens = []
        for token in results.toArray():
            tokens.append(token)
        return tokens
