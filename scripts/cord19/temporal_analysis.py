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
import matplotlib.pyplot as plt

from pyserini.collection import Collection, Cord19Article


def load(path):
    empty_date = dict()
    normal_dates = dict()

    cnt = 0
    collection = Collection('Cord19AbstractCollection', path)
    articles = collection.__next__()

    #iterate through raw collection
    for (i, d) in enumerate(articles):
        article = Cord19Article(d.raw)
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
    #this df has 4 columns: docid, DOI, title, publish_date
    normal_dates_df = pd.DataFrame([([k] + v) for k, v in normal_dates.items()])
    normal_dates_df = normal_dates_df.loc[:, [0, 1, 2, 3]]
    normal_dates_df.columns = ['docid', 'DOI', 'title', 'publish_date']

    df1 = pd.DataFrame(normal_dates_df)
    date_df = df1.sort_values('publish_date').groupby('publish_date')
    #date_df_counts has two columns: publish_date, counts
    date_df_counts = date_df.size().reset_index(name='counts')
    #all dfs below have two columns: publish_date, counts (they are massaged df based on date_df_counts)
    #two dfs based on year unit
    only_year_filter = date_df_counts['publish_date'].str.len() == 4
    with_date_filter = date_df_counts['publish_date'].str.len() > 4
    only_year = date_df_counts.loc[only_year_filter].loc[date_df_counts['publish_date'] >= '2003'] #before 2003 are all under 2000
    exact_year_total = date_df_counts.groupby(date_df_counts['publish_date'].str[:4])['counts'].agg('sum').reset_index(name='counts')
    exact_year_total = exact_year_total.loc[exact_year_total['publish_date'] >= '2003']
    
    #on monthly basis
    exact_date = date_df_counts.loc[with_date_filter].groupby(date_df_counts['publish_date'].str[:7])['counts'].agg('sum').reset_index(name='counts')
    before_2003 = exact_date.loc[exact_date['publish_date'] <= '2002-12']
    between_03_19 = exact_date.loc[exact_date['publish_date'] > '2002-12'].loc[exact_date['publish_date'] <= '2019-12']
    after_19 = exact_date.loc[exact_date['publish_date'] >= '2019-12']

    #weekly basis after 2019-12
    weekly_update_19 = date_df_counts.loc[with_date_filter].loc[date_df_counts['publish_date'] >= '2019-12'].groupby(date_df_counts['publish_date'])['counts'].agg('sum').reset_index(name='counts')
    weekly_update_19['publish_date'] = pd.to_datetime(weekly_update_19['publish_date'])
    weekly_update_19 = weekly_update_19.groupby(pd.Grouper(key='publish_date', freq='W'))['counts'].agg('sum').reset_index(name='counts')
    return only_year, exact_year_total, before_2003, between_03_19, after_19, weekly_update_19


def plot_bars(only_year, exact_year_total, before_2003, between_03_19, after_19, weekly_update_19):
    only_year.plot.bar(x='publish_date', y='counts', title='number of publishes only has year')
    exact_year_total.plot.bar(x='publish_date', y='counts', title='number of publishes for all in year units')
    before_2003.plot.bar(x='publish_date', y='counts', title='publish_date before 2003', figsize=(30, 10), fontsize=6)
    between_03_19.plot.bar(x='publish_date', y='counts', title='between_03_19', figsize=(30, 10), fontsize=6)
    after_19.plot.bar(x='publish_date', y='counts', title='after_19', figsize=(20, 10), fontsize=8)
    graph_weekly_19 = weekly_update_19.loc[weekly_update_19['publish_date'] < '2020-08-09']  # omit after 2020-08-09 to make graph readable
    graph_weekly_19.plot.bar(x='publish_date', y='counts', title='after 2019-12 weekly growth', figsize=(20, 10))
    plt.savefig('bar_plots.pdf')
    print(f'draw 6 bar plots for documents based on their publish_dates and saved into file bar_plots.pdf')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Return bar charts of temporal analysis on CORD-19')
    parser.add_argument('--path', type=str, required=True, help='Path to input collection')
    args = parser.parse_args()
    only_year, exact_year_total, before_2003, between_03_19, after_19, weekly_update_19 = load(args.path)
    plot_bars(only_year, exact_year_total, before_2003, between_03_19, after_19, weekly_update_19)

