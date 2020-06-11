# Pyserini: Usage of the Query Builder API

The `querybuilder` provides functionality to construct Lucene queries through Pyserini.
These queries can be directly issued through the `SimpleSearcher`.
Instead of issuing the query `hubble space telescope` directly, we can also construct the same exact query manually as follows:

```python
from pyserini.search import querybuilder

# First, create term queries for each individual query term:
term1 = querybuilder.get_term_query('hubble')
term2 = querybuilder.get_term_query('space')
term3 = querybuilder.get_term_query('telescope')

# Then, assemble into a "bag of words" query:
should = querybuilder.JBooleanClauseOccur['should'].value

boolean_query_builder = querybuilder.get_boolean_query_builder()
boolean_query_builder.add(term1, should)
boolean_query_builder.add(term2, should)
boolean_query_builder.add(term3, should)

query = boolean_query_builder.build()
```

Then issue the query:

```python
hits = searcher.search(query)

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

The results should be exactly the same as:

```python
hits = searcher.search('hubble space telescope')
```

By manually constructing queries, it is possible to define the boost for each query term individually.
For example:

```python
boost1 = querybuilder.get_boost_query(term1, 2.)
boost2 = querybuilder.get_boost_query(term2, 1.)
boost3 = querybuilder.get_boost_query(term3, 1.)

should = querybuilder.JBooleanClauseOccur['should'].value

boolean_query_builder = querybuilder.get_boolean_query_builder()
boolean_query_builder.add(boost1, should)
boolean_query_builder.add(boost2, should)
boolean_query_builder.add(boost3, should)

query = boolean_query_builder.build()

hits = searcher.search(query)

for i in range(0, 10):
    print(f'{i+1:2} {hits[i].docid:15} {hits[i].score:.5f}')
```

Note that the results are different, because we've placed more weight on the term `hubble`.
