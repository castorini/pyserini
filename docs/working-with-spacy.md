# Working with the spaCy

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

Here's a sample pre-built index on TREC Washington Post to play with (used in the TREC 2018 Core Track):

```bash
# TODO: upload pre-built index storing contents
wget index-core18-contents.tar.gz
tar xvfz index-core18-contents.tar.gz -C indexes
rm index-core18-contents.tar.gz
```

Use Pyserini's `SimpleSearcher` for searching:

```python
from pyserini.search import SimpleSearcher

searcher = SimpleSearcher('indexes/index-core18-contents/')
hits = searcher.search('Women in Parliaments')

# Grab contents of the top hit
content = hits[0].contents
print(content)
```

`content` should be as follows, which contains the document's title, kicker and article:

```text
Despite a big year for women in politics, national legislatures are still dominated by men
WorldViews

It's a big year for women in politics.
In a historic first, Hillary Clinton was named the Democratic Party’s presidential nominee in the upcoming U.S. elections. If she wins, she will join Theresa May of Britain and Angela Merkel of Germany in the ranks of women who lead prominent Western democracies.
...
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
| Despite | a | big | year | for | women | in | politics | , | national | legislatures | are | still | dominated | by | men | ... |


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
| Despite | despite | SCONJ | prep | Xxxxx | False |
| a | a | DET | det | x | True |
| big | big | ADJ | amod | xxx | False |
| year | year | NOUN | pobj | xxxx | False |
| for | for | ADP | prep | xxx | True |
| women | woman | NOUN | pobj | xxxx | False |
| in | in | ADP | prep | xx | True |
| politics | politic | NOUN | pobj | xxxx | False |
| , | , | PUNCT | punct | , | False |
| national | national | ADJ | amod | xxxx | False |
| legislatures | legislature | NOUN | nsubjpass | xxxx | False |
| are | be | AUX | auxpass | xxx | True |
| still | still | ADV | advmod | xxxx | True |
| dominated | dominate | VERB | ROOT | xxxx | False |
| by | by | ADP | agent | xx | True |
| men | man | NOUN | pobj | xxx | False |
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
| a big year | 8 | 18 | DATE | Absolute or relative dates or periods. |
| WorldViews | 91 | 101 | ORG | Companies, agencies, institutions, etc. |
| Hillary Clinton | 163 | 178 | PERSON | People, including fictional. |
| the Democratic Party | 189 | 209 | ORG | Companies, agencies, institutions, etc. |
| U.S. | 249 | 253 | GPE | Geopolitical entity, i.e. countries, cities, states. |
| ... | ... | ... | ... | ... |


### Sentence Segmentation

`Doc` also contains segmented sentences as [`Span`](https://spacy.io/api/span) objects, we can iterate over them:

```python
for sent in doc.sents:
    print(sent.text)
```

Then we have sentences:

| # | SENTENCE |
|---|---|
| 0 | Despite a big year for women in politics, national legislatures are still dominated by men |
| 1 | WorldViews |
| 2 | It's a big year for women in politics. |
| 3 | In a historic first, Hillary Clinton was named the Democratic Party’s presidential nominee in the upcoming U.S. elections. |
| 4 | If she wins, she will join Theresa May of Britain and Angela Merkel of Germany in the ranks of women who lead prominent Western democracies. |
| ... | ... |

