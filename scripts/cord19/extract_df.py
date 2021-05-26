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
import pandas as pd

from pyserini.collection import Collection, Cord19Article


def load(old_path, new_path):
    empty_date = dict()
    normal_old_dates = dict()
    normal_new_dates = dict()

    cnt = 0
    collection_old = Collection('Cord19AbstractCollection', old_path)
    collection_new = Collection('Cord19AbstractCollection', new_path)
    articles = collection_old.__next__()

    # iterate through raw old collection
    for (i, d) in enumerate(articles):
        article = Cord19Article(d.raw)
        metadata = article.metadata()
        date = metadata['publish_time']
        if len(date) == 0:
            empty_date.setdefault(article.cord_uid(), [])
            empty_date[article.cord_uid()].append(article.metadata()["doi"])
            empty_date[article.cord_uid()].append(len(article.title()))
        else:
            normal_old_dates.setdefault(article.cord_uid(), [])
            normal_old_dates[article.cord_uid()].append(article.metadata()["doi"])
            normal_old_dates[article.cord_uid()].append(len(article.title()))
            normal_old_dates[article.cord_uid()].append(date)
        cnt = cnt + 1
        if cnt % 1000 == 0:
            print(f'{cnt} articles read... in old data')

    cnt = 0
    articles = collection_new.__next__()
    # iterate through raw new collection
    for (i, d) in enumerate(articles):
        article = Cord19Article(d.raw)
        metadata = article.metadata()
        date = metadata['publish_time']
        if len(date) != 0:
            normal_new_dates.setdefault(article.cord_uid(), [])
            normal_new_dates[article.cord_uid()].append(article.metadata()["doi"])
            normal_new_dates[article.cord_uid()].append(len(article.title()))
            normal_new_dates[article.cord_uid()].append(date)
        cnt = cnt + 1
        if cnt % 1000 == 0:
            print(f'{cnt} articles read... in new data')

    #create df for old and new collection and groupby publish_date column, record the size of each group in column counts
    normal_old_dates_df = pd.DataFrame([([k] + v) for k, v in normal_old_dates.items()])
    normal_old_dates_df = normal_old_dates_df.loc[:, [0, 1, 2, 3]]
    normal_old_dates_df.columns = ['docid', 'DOI', 'title', 'publish_date']
    df1 = pd.DataFrame(normal_old_dates_df)
    date_df = df1.sort_values('publish_date').groupby('publish_date')
    date_df_counts = date_df.size().reset_index(name='counts')

    normal_new_dates_df = pd.DataFrame([([k] + v) for k, v in normal_new_dates.items()])
    normal_new_dates_df = normal_new_dates_df.loc[:, [0, 1, 2, 3]]
    normal_new_dates_df.columns = ['docid', 'DOI', 'title', 'publish_date']
    df2 = pd.DataFrame(normal_new_dates_df)
    date_new_df = df2.sort_values('publish_date').groupby('publish_date')
    # date_df_counts has two columns
    date_new_df_counts = date_new_df.size().reset_index(name='counts')

    return date_df_counts, date_new_df_counts


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract Dataframes of CORD-19')
    parser.add_argument('--old_path', type=str, required=True, help='Path to old collection')
    parser.add_argument('--new_path', type=str, required=True, help='Path to new collection')
    args = parser.parse_args()
    date_df_counts, date_new_df_counts = load(args.old_path, args.new_path)
    date_df_counts.to_csv('date_df_counts.csv', index=False)
    date_new_df_counts.to_csv('date_new_df_counts.csv', index=False)
    print(f'saved dfs to date_df_counts.csv and date_new_df_counts.csv')
