from pyserini.analysis import Analyzer, get_lucene_analyzer

analyzer = Analyzer(get_lucene_analyzer())
query_tokens = analyzer.analyze('what is paula deen\'s brother')
multihot_query_weights = {k: 1 for k in query_tokens}

print(multihot_query_weights)