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

import sys
import argparse
import pandas as pd

sys.path.insert(0, './')

from pyserini.collection import Collection, Cord19Article


def main(path, coef, top):
    documents_with_text = dict()
    documents_without_text = dict()
    documents_zero_abs = dict()
    documents_empty_body = dict()

    cnt = 0
    collection = Collection('Cord19AbstractCollection', path)
    articles = collection.__next__()

    # iterate through raw collection
    for (i, d) in enumerate(articles):
        article = Cord19Article(d.raw)
        # documents with empty abstract
        if len(article.abstract()) == 0:
            documents_zero_abs.setdefault(article.cord_uid(), [])
            documents_zero_abs[article.cord_uid()].append(article.metadata()["doi"])
        else:
            # document does not have text
            if not article.is_full_text():
                documents_without_text.setdefault(article.cord_uid(), [])
                documents_without_text[article.cord_uid()].append(article.metadata()["doi"])
                documents_without_text[article.cord_uid()].append(len(article.title()))
                documents_without_text[article.cord_uid()].append(len(article.abstract()))
            # document whose text body is empty
            elif len(article.body()) == 0:
                documents_empty_body.setdefault(article.cord_uid(), [])
                documents_empty_body[article.cord_uid()].append(article.metadata()["doi"])
            # normal document and we save for analysis later
            else:
                num_paragraph = len(article.body())
                title_len = len(article.title()) * num_paragraph
                abstract_len = len(article.abstract()) * num_paragraph
                documents_with_text.setdefault(article.cord_uid(), [])
                documents_with_text[article.cord_uid()].append(article.metadata()["doi"])
                documents_with_text[article.cord_uid()].append(title_len)
                documents_with_text[article.cord_uid()].append(abstract_len)
                documents_with_text[article.cord_uid()].append(num_paragraph)

        cnt = cnt + 1
        if cnt % 1000 == 0:
            print(f'{cnt} articles read...')

    documents_with_text_df = pd.DataFrame([([k] + v) for k, v in documents_with_text.items()])
    documents_with_text_df = documents_with_text_df.loc[:, [0, 1, 2, 3, 4]]
    documents_with_text_df.columns = ['docid', 'DOI', 'title', 'abstract', 'num_paragraph']

    # using quantile to find outliers return a df
    q1 = documents_with_text_df['abstract'].quantile(0.25)
    q3 = documents_with_text_df['abstract'].quantile(0.75)
    iqr = q3 - q1

    # We only consider extreme big value, since small value will not cause file explosion;
    # Could choose other coefficient to find more "extreme" outliers.
    filter = documents_with_text_df['abstract'] >= q3 + coef * iqr

    # abstract outlier
    outlier = documents_with_text_df.loc[filter]
    sorted = outlier.sort_values(by=['abstract'], ascending=False)
    tops = sorted.head(top)
    tops.to_csv('length_outlier.csv')

    print(f'found {len(documents_with_text_df.index)} outliers and saved top {top} into file length_outlier.csv')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Identifies outliers in CORD-19')
    parser.add_argument('--path', type=str, required=True, help='the path to collection')
    parser.add_argument('--coefficient', type=int, default=1.5, help='outlier coefficient')
    parser.add_argument('--top', type=int, default=10, help='number of top outliers')
    args = parser.parse_args()
    main(args.path, args.coefficient, args.top)
