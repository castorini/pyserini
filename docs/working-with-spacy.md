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

Build index on TREC Washington Post Corpus (used in TREC 2018 Core Track) with `-storeContents` option:

```bash
python -m pyserini.index -collection WashingtonPostCollection -generator WashingtonPostGenerator \
 -threads 9 -input /path/to/WashingtonPost \
 -index indexes/index-core18-contents -storePositions -storeDocvectors -storeContents
```

Make sure `/path/to/WashingtonPost` is updated with the appropriate path.

Then use Pyserini's `SimpleSearcher` for searching:

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

## Entity Linking

Unfortunately, spaCy does not provide any pre-trained entity linking model currently.
However, we found another great entity linking package called [Radboud Entity Linker (REL)](https://github.com/informagi/REL#rel-radboud-entity-linker).

In this section, we introduce an entity linking [script](../scripts/entity_linking.py) which links texts to both Wikipedia and Wikidata entities, using spaCy NER and REL Entity Linker.
The input should be a JSONL file which has one json object per line, like [this](https://github.com/castorini/pyserini/blob/master/integrations/resources/sample_collection_jsonl/documents.jsonl), while the output is also a JSONL file, where each json object is of format:

```
{
  "id": ...,
  "contents": ...,
  "entities": [
    {"start_pos": ..., "end_pos": ..., "ent_text": ..., "wikipedia_id": ..., "wikidata_id": ..., "ent_type": ...},
    ...
  ]
}
```

For example, given the input file

```json
{"id": "doc1", "contents": "The Manhattan Project and its atomic bomb helped bring an end to World War II. Its legacy of peaceful uses of atomic energy continues to have an impact on history and science."}
```

, the output file would be

```json
{
  "id": "doc1",
  "contents": "The Manhattan Project and its atomic bomb helped bring an end to World War II. Its legacy of peaceful uses of atomic energy continues to have an impact on history and science.",
  "entities": [
    {"start_pos": 0, "end_pos": 21, "ent_text": "The Manhattan Project", "wikipedia_id": "Manhattan_Project", "wikidata_id": "Q127050", "ent_type": "ORG"},
    {"start_pos": 65, "end_pos": 77, "ent_text": "World War II", "wikipedia_id": "World_War_II", "wikidata_id": "Q362", "ent_type": "EVENT"}
  ]
}
```

### Input Prep

Let us take MS MARCO passage dataset as an example.
We need to download the MS MARCO passage dataset and convert the tsv collection into jsonl files by following the detailed instruction [here](https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md#data-prep).
Now we should have 9 jsonl files in `collections/msmarco-passage/collection_jsonl`, and each file path can be considered as `input_path` in our scripts.

### REL

First, we follow the Github [instruction](https://github.com/informagi/REL#installation-from-source) to install REL and download required generic file, appropriate wikipedia corpus as well as the corresponding ED model.
Then we set up variable `base_url` as explained in this [tutorial](https://github.com/informagi/REL/blob/master/tutorials/01_How_to_get_started.md#how-to-get-started).

Note that the `base_url` and ED model path are required as `rel_base_url` and `rel_ed_model_path` in our script respectively.
Another parameter `rel_wiki_version` depends on the version of wikipedia corpus downloaded, e.g. `wiki_2019` for 2019 Wikipedia corpus.

### wikimapper

REL Entity Linker only links texts to Wikipedia entities, but we need their Wikidata information as well.
[Wikimapper](https://pypi.org/project/wikimapper/) is a Python library mapping Wikipedia titles to Wikidata IDs.
In order to use the mapping functionality, we have to download its precomputed indices [here](https://public.ukp.informatik.tu-darmstadt.de/wikimapper/).
Note that the path storing precomputed indices is required as `wikimapper_index` in our script.

### Run Script

Finally, we are ready to run our entity linking script:

```bash
python entity_linking.py --input_path [input_jsonl_file] --rel_base_url [base_url] --rel_ed_model_path [ED_model] \
--rel_wiki_version [wikipedia_corpus_version] --wikimapper_index [precomputed_index] \
--spacy_model [en_core_web_sm, en_core_web_lg, etc.] --output_path [output_jsonl_file]
```

It should take about 5 to 10 minutes to run entity linking on 5,000 MS MARCO passages on Compute Canada.
See [this](https://github.com/castorini/onboarding/blob/master/docs/cc-guide.md#compute-canada) for instructions about running scripts on Compute Canada.
