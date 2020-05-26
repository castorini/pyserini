from pyserini.collection import pycollection
import argparse
import pandas as pd

def main(collection, path, coef, top):
    documents_with_text = dict()
    documents_without_text = dict()
    documents_zero_abs = dict()
    documents_empty_body = dict()

    collection = pycollection.Collection(collection, path)
    articles = collection.__next__()
    # interate through raw collection
    for (i, d) in enumerate(articles):
        article = pycollection.Cord19Article(d.raw)
        # documents with empty abstract
        if len(article.abstract()) == 0:
            documents_zero_abs.setdefault(article.cord_uid(), [])
            documents_zero_abs[article.cord_uid()].append(article.metadata()["doi"])
        else:
            # documents does not have text
            if not article.is_full_text():
                documents_without_text.setdefault(article.cord_uid(), [])
                documents_without_text[article.cord_uid()].append(article.metadata()["doi"])
                documents_without_text[article.cord_uid()].append(len(article.title()))
                documents_without_text[article.cord_uid()].append(len(article.abstract()))
            # documents whose text body is empty
            elif len(article.body()) == 0:
                documents_empty_body.setdefault(article.cord_uid(), [])
                documents_empty_body[article.cord_uid()].append(article.metadata()["doi"])
            # normal documents and we put analysis on later
            else:
                num_paragraph = len(article.body())
                title_len = len(article.title()) * num_paragraph
                abstract_len = len(article.abstract()) * num_paragraph
                documents_with_text.setdefault(article.cord_uid(), [])
                documents_with_text[article.cord_uid()].append(article.metadata()["doi"])
                documents_with_text[article.cord_uid()].append(title_len)
                documents_with_text[article.cord_uid()].append(abstract_len)
                documents_with_text[article.cord_uid()].append(num_paragraph)

    documents_with_text_df = pd.DataFrame([([k] + v) for k, v in documents_with_text.items()])
    documents_with_text_df= documents_with_text_df.loc[:, [0,1,2,3,4]]
    documents_with_text_df.columns=['docid', 'DOI', 'title', 'abstract', 'num_paragraph']
    # using quantile to find outliers return a df
    q1 = documents_with_text_df['abstract'].quantile(0.25)
    q3 = documents_with_text_df['abstract'].quantile(0.75)
    iqr = q3 - q1
    # I only consider extreme big value, since small value will not cause file explosion
    filter = documents_with_text_df[
                 'abstract'] >= q3 + coef * iqr  # could choose other coefficient to find more "extreme" outlier
    # abstract outlier
    outlier = documents_with_text_df.loc[filter]
    sorted = outlier.sort_values(by=['abstract'], ascending=False)
    tops = sorted.head(top)
    tops.to_csv('length_outlier.csv')

    print("Find {} outliers and saved top {} into file 'length_outerlier.csv".format(len(documents_with_text_df.index), top))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Perform documents length outlier analysis on dataset')
    parser.add_argument('-collection', type=str, required=True,
                        help='collection name')
    parser.add_argument('-path', type=str, required=True,
                        help='the path to the data dir')
    parser.add_argument('-coefficient', type=int, default=1.5,
                        help='finding outlier coefficient')
    parser.add_argument('-top', type=int, default=5,
                        help='choose number of top outliers')
    args = parser.parse_args()
    main(args.collection, args.path, args.coefficient, args.top)