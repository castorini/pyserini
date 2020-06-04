# Pyserini: Usage of the Analyzer API

Pyserini exposes Lucene Analyzers in Python with the `Analyzer` class.
Below is a demonstration of these functionalities:

```python
from pyserini.analysis import Analyzer, get_lucene_analyzer

# Default analyzer for English uses the Porter stemmer:
analyzer = Analyzer(get_lucene_analyzer())
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is ['citi', 'buse', 'run', 'time']

# We can explicitly specify the Porter stemmer as follows:
analyzer = Analyzer(get_lucene_analyzer(stemmer='porter'))
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is same as above.

# We can explicitly specify the Krovetz stemmer as follows:
analyzer = Analyzer(get_lucene_analyzer(stemmer='krovetz'))
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is ['city', 'bus', 'running', 'time']

# Create an analyzer that doesn't stem, simply tokenizes:
analyzer = Analyzer(get_lucene_analyzer(stemming=False))
tokens = analyzer.analyze('City buses are running on time.')
print(tokens)
# Result is ['city', 'buses', 'running', 'time']
```

