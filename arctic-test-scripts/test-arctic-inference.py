import torch
from torch.nn.functional import normalize
from transformers import AutoModel, AutoTokenizer

# Model constants.
MODEL_ID = "Snowflake/snowflake-arctic-embed-m-v1.5"
QUERY_PREFIX = 'Represent this sentence for searching relevant passages: '

# Your queries and docs.
queries  = ['what is snowflake?', 'Where can I get the best tacos?']
documents = ['The Data Cloud!', 'Mexico City of Course!']

# Load the model and tokenizer.
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
model = AutoModel.from_pretrained(MODEL_ID, add_pooling_layer=False)
model.eval()

# Add query prefix and tokenize queries and docs.
queries_with_prefix = [f"{QUERY_PREFIX}{q}" for q in queries]
query_tokens = tokenizer(queries_with_prefix, padding=True, truncation=True, return_tensors='pt', max_length=512)
document_tokens =  tokenizer(documents, padding=True, truncation=True, return_tensors='pt', max_length=512)

# Use the model to generate text embeddings.
with torch.inference_mode():
    query_embeddings = model(**query_tokens)[0][:, 0]
    document_embeddings = model(**document_tokens)[0][:, 0]

# Remember to normalize embeddings.
query_embeddings = normalize(query_embeddings)
document_embeddings = normalize(document_embeddings)

# Scores via dotproduct.
scores = query_embeddings @ document_embeddings.T

# Pretty-print the results.
for query, query_scores in zip(queries, scores):
    doc_score_pairs = list(zip(documents, query_scores))
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)
    print(f'Query: "{query}"')
    for document, score in doc_score_pairs:
        print(f'Score: {score:.4f} | Document: "{document}"')
    print()

#### OUTPUT ####
# Query: "what is snowflake?"
# Score: 0.3521 | Document: "The Data Cloud!"
# Score: 0.2358 | Document: "Mexico City of Course!"

# Query: "Where can I get the best tacos?"
# Score: 0.3884 | Document: "Mexico City of Course!"
# Score: 0.2389 | Document: "The Data Cloud!"
#

#### Variation: Truncated Embeddings ####
query_embeddings_256 = normalize(query_embeddings[:, :256])
document_embeddings_256 = normalize(document_embeddings[:, :256])
scores_256 = query_embeddings_256 @ document_embeddings_256.T

# Pretty-print the results.
for query, query_scores in zip(queries, scores_256):
    doc_score_pairs = sorted(zip(documents, query_scores), key=lambda x: x[1], reverse=True)
    print(f'Query: "{query}"')
    for document, score in doc_score_pairs:
        print(f'Score: {score:.4f} | Document: "{document}"')
    print()

#### OUTPUT ####
# Query: "what is snowflake?"
# Score: 0.3852 | Document: "The Data Cloud!"
# Score: 0.2721 | Document: "Mexico City of Course!"

# Query: "Where can I get the best tacos?"
# Score: 0.4337 | Document: "Mexico City of Course!"
# Score: 0.2886 | Document: "The Data Cloud!"
#
