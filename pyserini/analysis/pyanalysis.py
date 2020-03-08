from ..pyclass import JArabicAnalyzer
from ..pyclass import JBengaliAnalyzer
from ..pyclass import JCJKAnalyzer
from ..pyclass import JDefaultEnglishAnalyzer
from ..pyclass import JFreebaseAnalyzer
from ..pyclass import JFrenchAnalyzer
from ..pyclass import JGermanAnalyzer
from ..pyclass import JHindiAnalyzer
from ..pyclass import JSpanishAnalyzer
from ..pyclass import JTweetAnalyzer
from ..pyclass import JString


def get_analyzer(analyzer, stemmer='porter'):
    """
    Parameters
    ----------
    analyzer : String
        Name of analyzer to get

    stemmer : String
        Name of stemmer that analyzer needs to use (not all analyzers allow for a stemmer to be provided)

    Returns
    -------
    result : org.apache.lucene.document.Analyzer
        Java Analyzer object
    """
    if analyzer == 'arabic':
        return JArabicAnalyzer()
    elif analyzer == 'bengali':
        return JBengaliAnalyzer()
    elif analyzer == 'cjk':
        return JCJKAnalyzer()
    elif analyzer == 'german':
        return JGermanAnalyzer()
    elif analyzer == 'spanish':
        return JSpanishAnalyzer()
    elif analyzer == 'french':
        return JFrenchAnalyzer()
    elif analyzer == 'hindi':
        return JHindiAnalyzer()
    elif analyzer == 'english':
        return JDefaultEnglishAnalyzer.newDefaultInstance()
    elif analyzer == 'freebase':
        return JFreebaseAnalyzer()
    elif analyzer == 'tokenize':
        return JDefaultEnglishAnalyzer.newNonStemmingInstance()
    elif analyzer == 'tweet':
        return JTweetAnalyzer()
    else:
        return JDefaultEnglishAnalyzer.newStemmingInstance(JString('porter'))
