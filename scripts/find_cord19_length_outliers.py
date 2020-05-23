from pyserini.collection import pycollection
import pandas as pd



if __name__ == '__main__':
    titles_withText = []
    abstracts_withText = []
    docids_withText = []
    dois_withText = []
    paragraph_num = []
    abstracts_total = []
    titles_total = []
    titles_withoutText = []
    dois_withoutText = []
    abstracts_withoutText = []
    docids_withoutText = []
    docids_zero_abs = []
    dois_zero_abs = []
    docids_empty_text = []
    dois_empty_text = []

    collection = pycollection.Collection('Cord19AbstractCollection', '../collections/cord19-2020-05-19')
    articles = collection.__next__()
    article = None
    #interate through raw collection
    for (i, d) in enumerate(articles):
        article = pycollection.Cord19Article(d.raw)
        # documents with empty abstract
        if len(article.abstract()) == 0:
            docids_zero_abs.append(article.cord_uid())
            dois_zero_abs.append(article.metadata()["doi"])
        else:
            # documents does not have text
            if not article.is_full_text():
                docids_withoutText.append(article.cord_uid())
                titles_withoutText.append(len(article.title()))
                abstracts_withoutText.append(len(article.abstract()))
                dois_withoutText.append(article.metadata()["doi"])
            #documents whose text body is empty
            elif len(article.body()) == 0:
                docids_empty_text.append(article.cord_uid())
                dois_empty_text.append(article.metadata()["doi"])
            #normal documents and we put analysis on later
            else:
                docids_withText.append(article.cord_uid())
                dois_withText.append(article.metadata()["doi"])
                titles_withText.append(len(article.title()))
                abstracts_withText.append(len(article.abstract()))
                paragraph_num.append(len(article.body()))
                abstracts_total.append(abstracts_withText[-1] * paragraph_num[-1])
                titles_total.append(titles_withText[-1] * paragraph_num[-1])

    documents_withText = {'docid': docids_withText, 'DOI': dois_withText, 'title': titles_total, 'abstract': abstracts_total, 'num_para': paragraph_num}
    documents_withoutText = {'docid': docids_withoutText, 'DOI': dois_withoutText, 'title': titles_withoutText, 'abstract': abstracts_withoutText}
    documents_withText_df = pd.DataFrame(documents_withText)
    # using quantile to find outliers return a df
    q1 = documents_withText_df['abstract'].quantile(0.25)
    q3 = documents_withText_df['abstract'].quantile(0.75)
    iqr = q3 - q1
    # I only consider extreme big value, since small value will not cause file explosion
    filter = documents_withText_df['abstract'] >= q3 + 1.5 * iqr  # could choose other coefficient to find more "extreme" outlier
    # abstract outlier
    outlier = documents_withText_df.loc[filter]
    #temporarily choose 5
    sorted = outlier.sort_values(by=['abstract'], ascending=False)
    top_5 = sorted.head(5)
    top_5.to_csv('length_outlier_top5.csv')