import os
os.environ['ANSERINI_CLASSPATH'] = '/home/stefanm/qwen/pyserini/pyserini/resources/jars'


from pyserini.search.faiss import FaissSearcher
from pyserini.search.faiss import ArcticQueryEncoder

# Path to your index directory
index_dir = '/home/stefanm/qwen/pyserini/collections/faiss_index'

# Initialize the Arctic Query Encoder
query_encoder = ArcticQueryEncoder(
    model_id="Snowflake/snowflake-arctic-embed-m-v1.5",  # Use the model ID for Arctic encoder
    device='cuda:0',  # Change to 'cpu' if you're not using a GPU
    encode_dir=1
)

# Initialize the FaissSearcher with the Arctic encoder
searcher = FaissSearcher(index_dir=index_dir, query_encoder=query_encoder)

# Example query
query = "Which is the best University?"

# Search and print results
results = searcher.search(query, k=10)

for result in results:
    print(f'Document ID: {result.docid}, Score: {result.score}')

