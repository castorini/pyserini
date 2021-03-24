import re
import spacy

def readStopWords(fileName='stopwords.txt', lowerCase=True):
    """Reads a list of stopwords from a file. By default the words
       are read from a standard repo location and are lowercased.
      :param fileName a stopword file name
      :param lowerCase  a boolean flag indicating if lowercasing is needed.
      :return a list of stopwords
    """
    stopWords = set()
    with open(fileName) as f:
        for w in f:
            w = w.strip()
            if w:
                if lowerCase:
                    w = w.lower()
                stopWords.add(w)
    return stopWords

def isAlphaNum(s):
    return s and (re.match("^[a-zA-Z-_.0-9]+$", s) is not None)

class SpacyTextParser:
    def __init__(self, modelName, stopWords,
                 removePunct=True,
                 sentSplit=False,
                 keepOnlyAlphaNum=False,
                 lowerCase=True,
                 enablePOS=True):
        """Constructor.
                :param  modelName    a name of the spacy model to use, e.g., en_core_web_sm
                :param  stopWords    a list of stop words to be excluded (case insensitive);
                                     a token is also excluded when its lemma is in the stop word list.
                :param  removePunct  a bool flag indicating if the punctuation tokens need to be removed
                :param  sentSplit    a bool flag indicating if sentence splitting is necessary
                :param  keepOnlyAlphaNum a bool flag indicating if we need to keep only alpha-numeric characters
                :param  enablePOS    a bool flag that enables POS tagging (which, e.g., can improve lemmatization)
        """

        disableList = ['ner', 'parser']
        if not enablePOS:
            disableList.append('tagger')
        print('Disabled Spacy components: ', disableList)

        self._nlp = spacy.load(modelName, disable=disableList)
        if sentSplit:
            sentencizer = self._nlp.create_pipe("sentencizer")
            self._nlp.add_pipe(sentencizer)

        self._removePunct = removePunct
        self._stopWords = frozenset([w.lower() for w in stopWords])
        self._keepOnlyAlphaNum = keepOnlyAlphaNum
        self._lowerCase = lowerCase

    @staticmethod
    def _basic_clean(text):
        return text.replace("’", "'")

    def __call__(self, text):
        """A thin wrapper that merely calls spacy.
        :param text     input text string
        :return         a spacy Doc object
        """

        return self._nlp(SpacyTextParser._basic_clean(text))

    def procText(self, text):
        """Process text, remove stopwords and obtain lemmas, but does not split into sentences.
        This function should not emit newlines!
        :param text     input text string
        :return         a tuple (lemmatized text, original-form text). Text is white-space separated.
        """

        lemmas = []
        tokens = []
        doc = self(text)
        for tokObj in doc:
            if self._removePunct and tokObj.is_punct:
                continue
            lemma = tokObj.lemma_
            text = tokObj.text
            if self._keepOnlyAlphaNum and not isAlphaNum(text):
                continue
            tok1 = text.lower()
            tok2 = lemma.lower()
            if tok1 in self._stopWords or tok2 in self._stopWords:
                continue

            if self._lowerCase:
                text = text.lower()
                lemma = lemma.lower()

            lemmas.append(lemma)
            tokens.append(text)

        return ' '.join(lemmas), ' '.join(tokens)


def getRetokenized(tokenizer, text):
    """Obtain a space separated re-tokenized text.
    :param tokenizer:  a tokenizer that has the function
                       tokenize that returns an array of tokens.
    :param text:       a text to re-tokenize.
    """
    return ' '.join(tokenizer.tokenize(text))


def addRetokenizedField(dataEntry,
                        srcField,
                        dstField,
                        tokenizer):
    """
    Create a re-tokenized field from an existing one.
    :param dataEntry:   a dictionary of entries (keys are field names, values are text items)
    :param srcField:    a source field
    :param dstField:    a target field
    :param tokenizer:    a tokenizer to use, if None, nothing is done
    """
    if tokenizer is not None:
        dst = ''
        if srcField in dataEntry:
            dst = getRetokenized(tokenizer, dataEntry[srcField])

        dataEntry[dstField] = dst