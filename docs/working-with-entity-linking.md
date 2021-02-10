# Pyserini: Working with Entity Linking

In this page, we introduce an entity linking [script](../scripts/entity_linking.py) which links texts to both Wikipedia and Wikidata entities, using [Radboud Entity Linker (REL)](https://github.com/informagi/REL#rel-radboud-entity-linker) and [spaCy NER](https://spacy.io/usage/linguistic-features#named-entities).
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

## Input Prep

Let us take MS MARCO passage dataset as an example.
We need to download the MS MARCO passage dataset and convert the tsv collection into jsonl files by following the detailed instruction [here](https://github.com/castorini/pyserini/blob/master/docs/experiments-msmarco-passage.md#data-prep).
Now we should have 9 jsonl files in `collections/msmarco-passage/collection_jsonl`, and each file path can be considered as `input_path` in our scripts.

## REL

First, we follow the Github [instruction](https://github.com/informagi/REL#installation-from-source) to install REL and download required generic file, appropriate wikipedia corpus as well as the corresponding ED model.
Then we set up variable `base_url` as explained in this [tutorial](https://github.com/informagi/REL/blob/master/tutorials/01_How_to_get_started.md#how-to-get-started).

Note that the `base_url` and ED model path are required as `rel_base_url` and `rel_ed_model_path` in our script respectively.
Another parameter `rel_wiki_version` depends on the version of wikipedia corpus downloaded, e.g. `wiki_2019` for 2019 Wikipedia corpus.

## wikimapper

REL Entity Linker only links texts to Wikipedia entities, but we need their Wikidata information as well.
[Wikimapper](https://pypi.org/project/wikimapper/) is a Python library mapping Wikipedia titles to Wikidata IDs.
In order to use the mapping functionality, we have to download its precomputed indices [here](https://public.ukp.informatik.tu-darmstadt.de/wikimapper/).
Note that the path storing precomputed indices is required as `wikimapper_index` in our script.

## Run Script

Finally, we are ready to run our entity linking script:

```bash
python entity_linking.py --input_path [input_jsonl_file] --rel_base_url [base_url] --rel_ed_model_path [ED_model] \
--rel_wiki_version [wikipedia_corpus_version] --wikimapper_index [precomputed_index] \
--spacy_model [en_core_web_sm, en_core_web_lg, etc.] --output_path [output_jsonl_file]
```

It should take about 5 to 10 minutes to run entity linking on 5,000 MS MARCO passages on Compute Canada.
See [this](https://github.com/castorini/onboarding/blob/master/docs/cc-guide.md#compute-canada) for instructions about running scripts on Compute Canada.
