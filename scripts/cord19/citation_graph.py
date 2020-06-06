import pyserini.collection
import json
import csv
collection = pyserini.collection.Collection(
    'Cord19AbstractCollection', 'collections/cord19')
articles = collection.__next__()
article = None
with open("node.csv", 'w') as file1:
    writer = csv.writer(file1)
    writer.writerow(['Id'])
with open("edge.csv", 'w') as file2:
    writer = csv.writer(file2)
    writer.writerow(['Source', 'Target'])

for (i, d) in enumerate(articles):
    article = pyserini.collection.Cord19Article(d.raw)
    # if i == 100:     #change this number
    # break
    if article.is_full_text():
        bib = article.bib_entries()
        with open("node.csv", 'a') as file1:
            fieldnames = [article.title()]
            writer = csv.writer(file1)
            writer.writerow(fieldnames)
        j = 0
        number = 'BIBREF%d' % j
        while True:
            if number in bib:
                title = bib[number]['title']
                if title != '':
                    with open("node.csv", "a") as file1:
                        fieldnames = [title]
                        writer = csv.writer(file1)
                        writer.writerow(fieldnames)
                    with open("edge.csv", "a") as file2:
                        fieldnames = [article.title(), title]
                        writer = csv.writer(file2)
                        writer.writerow(fieldnames)
                j = j + 1
                number = 'BIBREF%d' % j
            elif j < len(bib):
                j = j + 1
                number = 'BIBREF%d' % j
            else:
                break
