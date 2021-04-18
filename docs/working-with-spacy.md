# Pyserini: Working with spaCy

This page describes how to take Pyserini output and apply [spaCy](https://spacy.io/) to do some NLP basics on it.


## spaCy Prep

First, download the spaCy package and model:

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

In this guide, we use model `en_core_web_sm`, which is a small English model trained on written web text (blogs, news, comments).
There are many other [models](https://spacy.io/usage/models) supporting different languages, you can download the best one for your application.


## Search

Use Pyserini's `SimpleSearcher` to fetch document from the MS MARCO pre-built index [`msmarco-passage`](https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md):

```python
import json
from pyserini.search import SimpleSearcher

# Initialize a searcher from a pre-built index
searcher = SimpleSearcher.from_prebuilt_index('msmarco-passage')

# Fetch raw text of a document given its docid
raw = searcher.doc('1').raw()
# Get actual content from raw
content = json.loads(raw)['contents']
print(content)
```

`content` should be as follows:

```text
The Manhattan Project and its atomic bomb helped bring an end to World War II. Its legacy of peaceful uses of atomic energy continues to have an impact on history and science.
```


## Linguistic Features

Load spaCy's pre-trained model to a `Language` object called `nlp`, then call the `nlp` on `content` to get a processed [`Doc`](https://spacy.io/api/doc) object:

```python
import spacy

nlp = spacy.load('en_core_web_sm')
doc = nlp(content)
```

From `Doc`, we can apply spaCy's NLP [features](https://spacy.io/usage/spacy-101#features) on our document.
In this guide, we will talk about [Tokenization](#tokenization), [POS Tagging](#part-of-speech-pos-tagging), [NER](#named-entity-recognition-ner) and [Sentence Segmentation](#sentence-segmentation).


### Tokenization

Each `Doc` object contains individual [`Token`](https://spacy.io/api/token) objects, and you can iterate over them:

```python
for token in doc:
    print(token.text)
```

The result should be as follows:

| 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | ... |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| The | Manhattan | Project | and | its | atomic | bomb | helped | bring | an | end | to | World | War | II | . | ... |


### Part-of-speech (POS) Tagging

There are many linguistic annotations contained in `Token`'s [attributes](https://spacy.io/api/token#attributes), such as

TEXT: The original word text.

LEMMA: The base form of the word.

POS: The simple [UPOS](https://universaldependencies.org/docs/u/pos/) part-of-speech tag.

DEP: Syntactic dependency, i.e. the relation between tokens.

SHAPE: The word shape – capitalization, punctuation, digits.

STOP: Is the token part of a stop list, i.e. the most common words of the language?

These attributes can be easily accessed by:

```python
for token in doc:
    print(token.text, token.lemma_, token.pos_, token.dep_, token.shape_, token.is_stop)
```

The output is shown in the following table:

| TEXT | LEMMA | POS | DEP | SHAPE | STOP |
|---|---|---|---|---|---|
| The | the | DET | det | Xxx | True |
| Manhattan | Manhattan | PROPN | compound | Xxxxx | False |
| Project | Project | PROPN | nsubj | Xxxxx | False |
| and | and | CCONJ | cc | xxx | True |
| its | -PRON- | DET | poss | xxx | True |
| atomic | atomic | ADJ | amod | xxxx | False |
| bomb | bomb | NOUN | conj | xxxx | False |
| helped | help | VERB | aux | xxxx | False |
| bring | bring | VERB | ROOT | xxxx | False |
| an | an | DET | det | xx | True |
| end | end | NOUN | dobj | xxx | False |
| to | to | ADP | prep | xx | True |
| World | World | PROPN | compound | Xxxxx | False |
| War | War | PROPN | compound | Xxx | False |
| II | II | PROPN | pobj | XX | False |
| . | . | PUNCT | punct | . | False |
| ... | ... | ... | ... | ... | ... |


### Named Entity Recognition (NER)

spaCy can recognize various [types](https://spacy.io/api/annotation#named-entities) of named entities in a document:

```python
for ent in doc.ents:
    print(ent.text, ent.start_char, ent.end_char, ent.label_)
```

The following table shows recognized entities:

| TEXT | START | END | LABEL | DESCRIPTION |
|---|---|---|---|---|
| The Manhattan Project | 0 | 21 | ORG | Companies, agencies, institutions, etc. |
| World War II | 65 | 77 | EVENT | Named hurricanes, battles, wars, sports events, etc. |


### Sentence Segmentation

`Doc` also contains segmented sentences as [`Span`](https://spacy.io/api/span) objects, we can iterate over them:

```python
for sent in doc.sents:
    print(sent.text)
```

Then we have sentences:

| # | SENTENCE |
|---|---|
| 0 | The Manhattan Project and its atomic bomb helped bring an end to World War II. |
| 1 | Its legacy of peaceful uses of atomic energy continues to have an impact on history and science. |
