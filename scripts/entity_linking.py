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

import argparse
import jsonlines
import spacy
from REL.REL.mention_detection import MentionDetection
from REL.REL.utils import process_results
from REL.REL.entity_disambiguation import EntityDisambiguation
from REL.REL.ner import NERBase, Span
from wikimapper import WikiMapper


# Spacy Mention Detection class which overrides the NERBase class in the REL entity linking process
class NERSpacy(NERBase):
    def __init__(self):
        # we only want to link entities of specific types
        self.ner_labels = ['PERSON', 'NORP', 'FAC', 'ORG', 'GPE', 'LOC', 'PRODUCT', 'EVENT', 'WORK_OF_ART',
                           'LAW', 'LANGUAGE', 'DATE', 'TIME', 'MONEY', 'QUANTITY']

    # mandatory function which overrides NERBase.predict()
    def predict(self, doc):
        mentions = []
        for ent in doc.ents:
            if ent.label_ in self.ner_labels:
                mentions.append(Span(ent.text, ent.start_char, ent.end_char, 0, ent.label_))
        return mentions


# run REL entity linking on processed doc
def rel_entity_linking(spacy_docs, rel_base_url, rel_wiki_version, rel_ed_model_path):
    mention_detection = MentionDetection(rel_base_url, rel_wiki_version)
    tagger_spacy = NERSpacy()
    mentions_dataset, _ = mention_detection.find_mentions(spacy_docs, tagger_spacy)
    config = {
        'mode': 'eval',
        'model_path': rel_ed_model_path,
    }
    ed_model = EntityDisambiguation(rel_base_url, rel_wiki_version, config)
    predictions, _ = ed_model.predict(mentions_dataset)

    linked_entities = process_results(mentions_dataset, predictions, spacy_docs)
    return linked_entities


# apply spaCy nlp processing pipeline on each doc
def apply_spacy_pipeline(input_path, spacy_model):
    nlp = spacy.load(spacy_model)
    spacy_docs = {}
    with jsonlines.open(input_path) as reader:
        for obj in reader:
            spacy_docs[obj['id']] = nlp(obj['contents'])
    return spacy_docs


# enrich REL entity linking results with entities' wikidata ids, and write final results as json objects
def enrich_el_results(rel_linked_entities, spacy_docs, wikimapper_index):
    wikimapper = WikiMapper(wikimapper_index)
    linked_entities_json = []
    for docid, ents in rel_linked_entities.items():
        linked_entities_info = []
        for start_pos, end_pos, ent_text, ent_wikipedia_id, ent_type in ents:
            # find entities' wikidata ids using their REL results (i.e. linked wikipedia ids)
            ent_wikipedia_id = ent_wikipedia_id.replace('&amp;', '&')
            ent_wikidata_id = wikimapper.title_to_id(ent_wikipedia_id)

            # write results as json objects
            linked_entities_info.append({'start_pos': start_pos, 'end_pos': end_pos, 'ent_text': ent_text,
                                         'wikipedia_id': ent_wikipedia_id, 'wikidata_id': ent_wikidata_id,
                                         'ent_type': ent_type})
        linked_entities_json.append({'id': docid, 'contents': spacy_docs[docid].text,
                                     'entities': linked_entities_info})
    return linked_entities_json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--input_path', type=str, help='path to input texts')
    parser.add_argument('-u', '--rel_base_url', type=str, help='directory containing all required REL data folders')
    parser.add_argument('-m', '--rel_ed_model_path', type=str, help='path to the REL entity disambiguation model')
    parser.add_argument('-v', '--rel_wiki_version', type=str, help='wikipedia corpus version used for REL')
    parser.add_argument('-w', '--wikimapper_index', type=str, help='precomputed index used by Wikimapper')
    parser.add_argument('-s', '--spacy_model', type=str, help='spacy model type')
    parser.add_argument('-o', '--output_path', type=str, help='path to output json file')
    args = parser.parse_args()

    spacy_docs = apply_spacy_pipeline(args.input_path, args.spacy_model)
    rel_linked_entities = rel_entity_linking(spacy_docs, args.rel_base_url, args.rel_wiki_version,
                                             args.rel_ed_model_path)
    linked_entities_json = enrich_el_results(rel_linked_entities, spacy_docs, args.wikimapper_index)
    with jsonlines.open(args.output_path, mode='w') as writer:
        writer.write_all(linked_entities_json)


if __name__ == '__main__':
    main()