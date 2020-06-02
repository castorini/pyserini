#
# Pyserini: Python interface to the Anserini IR toolkit built on Lucene
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

import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt

sys.path.insert(0, './')

from pyserini.collection import pycollection


def main(path):
    empty_date = dict()
    normal_dates = dict()

    cnt = 0
    collection = pycollection.Collection('Cord19AbstractCollection',path)
    articles = collection.__next__()

    #interate through raw collection
    for (i, d) in enumerate(articles):
        article = pycollection.Cord19Article(d.raw)
        # documents with empty abstract
        metadata = article.metadata()
        date = metadata['publish_time']
        if len(date) == 0:
            empty_date.setdefault(article.cord_uid(), [])
            empty_date[article.cord_uid()].append(article.metadata()["doi"])
            empty_date[article.cord_uid()].append(len(article.title()))
        else:
            normal_dates.setdefault(article.cord_uid(), [])
            normal_dates[article.cord_uid()].append(article.metadata()["doi"])
            normal_dates[article.cord_uid()].append(len(article.title()))
            normal_dates[article.cord_uid()].append(date)
        cnt = cnt + 1
        if cnt % 1000 == 0:
            print(f'{cnt} articles read...')
    normal_dates_df = pd.DataFrame([([k] + v) for k, v in normal_dates.items()])
    normal_dates_df = normal_dates_df.loc[:, [0, 1, 2, 3]]
    normal_dates_df.columns = ['docid', 'DOI', 'title', 'publish_date']

    df1 = pd.DataFrame(normal_dates_df)
    date_df = df1.sort_values('publish_date').groupby('publish_date')
    temp = date_df.size().reset_index(name='counts')
    only_year_filter = temp['publish_date'].str.len() == 4
    with_date_filter = temp['publish_date'].str.len() > 4
    only_year = temp.loc[only_year_filter].loc[temp['publish_date'] >= '2003'] #before 2003 are all under 2000
    exact_date = temp.loc[with_date_filter].groupby(temp['publish_date'].str[:7])['counts'].agg('sum').reset_index(name='counts')
    exact_year_total = temp.groupby(temp['publish_date'].str[:4])['counts'].agg('sum').reset_index(name='counts')
    exact_year_total = exact_year_total.loc[exact_year_total['publish_date'] >= '2003']
    before_2003 = exact_date.loc[exact_date['publish_date'] <= '2002-12']
    between_03_19 = exact_date.loc[exact_date['publish_date'] > '2002-12'].loc[exact_date['publish_date'] <= '2018-12']
    after_19 = exact_date.loc[exact_date['publish_date'] > '2018-12']

    only_year.plot.bar(x='publish_date', y='counts', title='number of publishes only has year')
    exact_year_total.plot.bar(x='publish_date', y='counts', title='number of publishes for all in year units')
    before_2003.plot.bar(x='publish_date', y='counts', title='publish_date before 2003', figsize=(30, 10), fontsize=6)
    between_03_19.plot.bar(x='publish_date', y='counts', title='between_03_19', figsize=(30, 10), fontsize=6)
    after_19.plot.bar(x='publish_date', y='counts', title='after_18', figsize=(20, 10), fontsize=8)
    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Temporal Analysis in CORD-19')
    parser.add_argument('--path', type=str, required=True, help='the path to collection')
    args = parser.parse_args()
    main(args.path)

