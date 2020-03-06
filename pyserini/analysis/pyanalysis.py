from ..pyclass import JArabicAnalyzer
from ..pyclass import JBengaliAnalyzer
from ..pyclass import JCJKAnalyzer
from ..pyclass import JEnglishStemmingAnalyzer
from ..pyclass import JFreebaseAnalyzer
from ..pyclass import JFrenchAnalyzer
from ..pyclass import JGermanAnalyzer
from ..pyclass import JHindiAnalyzer
from ..pyclass import JSpanishAnalyzer
from ..pyclass import JTokenizeOnlyAnalyzer
from ..pyclass import JTweetAnalyzer


def get_default_analyzer():
    """

    Returns
    -------
    JEnglishStemmingAnalyzer
    """
    return get_english_stemming_analyzer()


def get_arabic_analyzer():
    """

    Returns
    -------
    JArabicAnalyzer
    """
    return JArabicAnalyzer()


def get_bengali_analyzer():
    """

    Returns
    -------
    JBengaliAnalyzer
    """
    return JBengaliAnalyzer()


def get_cjk_analyzer():
    """

    Returns
    -------
    JCJKAnalyzer
    """
    return JCJKAnalyzer()


def get_german_analyzer():
    """

    Returns
    -------
    JGermanAnalyzer
    """
    return JGermanAnalyzer()


def get_spanish_analyzer():
    """

    Returns
    -------
    JSpanishAnalyzer
    """
    return JSpanishAnalyzer()


def get_french_analyzer():
    """

    Returns
    -------
    JFrenchAnalyzer
    """
    return JFrenchAnalyzer()


def get_hindi_analyzer():
    """

    Returns
    -------
    JHindiAnalyzer
    """
    return JHindiAnalyzer()


def get_english_stemming_analyzer(stemmer='porter'):
    """

    Returns
    -------
    JEnglishStemmingAnalyzer
    """
    return JEnglishStemmingAnalyzer(stemmer)


def get_freebase_analyzer():
    """

    Returns
    -------
    JFreebaseAnalyzer
    """
    return JFreebaseAnalyzer()


def get_tokenize_only_analyzer():
    """

    Returns
    -------
    JTokenizeOnlyAnalyzer
    """
    return JTokenizeOnlyAnalyzer()


def get_tweet_analyzer():
    """

    Returns
    -------
    JTweetAnalyzer
    """
    return JTweetAnalyzer()
