from pyserini.collection import pycollection
import pandas as pd
import matplotlib.pyplot as plt

if __name__ == '__main__':
    empty_date_docids=[]
    empty_date_dois=[]
    empty_date_titles=[]

    date_docids = []
    date_titles = []
    date_dois = []
    dates =[]

    collection = pycollection.Collection('Cord19AbstractCollection', '/Users/stephaniewhoo/URA/pyserini/collections/cord19-2020-05-19')
    articles = collection.__next__()
    article = None
    #interate through raw collection
    for (i, d) in enumerate(articles):
        article = pycollection.Cord19Article(d.raw)
        # documents with empty abstract
        metadata = article.metadata()
        date = metadata['publish_time']
        if (len(date) == 0):
            empty_date_docids.append(article.cord_uid())
            empty_date_dois.append(metadata['doi'])
            empty_date_titles.append(article.title())
        else:
            date_docids.append(article.cord_uid())
            date_dois.append(metadata['doi'])
            date_titles.append(article.title())
            dates.append(date)

    data1 = {'docid': date_docids, 'title': date_titles, 'doi':date_dois,'publish_date': dates}
    df1 = pd.DataFrame(data1)
    date_df = df1.sort_values('publish_date').groupby('publish_date')
    temp = date_df.size().reset_index(name='counts')
    before_2003 = temp.loc[temp['publish_date'] <= '2002-12-31']
    between_03_19 = temp.loc[temp['publish_date'] > '2002-12-31'].loc[temp['publish_date'] <= '2019-12-19']
    after_19 = temp.loc[temp['publish_date'] > '2019-12-19']
    temp.plot(x='publish_date', y='counts')
    before_2003.plot(x='publish_date', y='counts')
    between_03_19.plot(x='publish_date', y='counts')
    after_19.plot(x='publish_date', y='counts')
    plt.show()

    print('hey')
