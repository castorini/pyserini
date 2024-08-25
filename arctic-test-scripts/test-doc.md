# Arctic Model Testing Log

## Overview
This document tracks all commands, scripts, and steps used during the testing of the Arctic model.

---

## Environment Setup
- **Python version:** `3.10+`
- **Pyserini version:** `0.36.0`


```bash
# Activate the environment
conda activate [env_name]
```

## Inference Model
```bash
python arctic-test-scripts/test-arctic-inference.py
```

## Test corpus and embedding
There is a test corpus located in ```collections``` folder. Paired with its corresponding embedding in ```collections/test_embeddings_arctic```.

One could freely generate emebdding of other corpus with script ```arctic-test-scripts/test-embedding-gen.py```

## Indexing
There is an index available in ```indexes/faiss_index``` which is a hnsw faiss index of the test corpus mentioned above. One could generate index on other embeddings with command 
```bash
python -m pyserini.index.faiss   \
--input [path-to-embedding-DIRECTORY]   \
--output [path-to-output-directory] \
--hnsw
```

## Search test
There is a script for testing the search classes here
```arctic-test-scripts/test-arctic-search.py```

## TODOs
Still need to work on figuring out how to keep a default model-id for arctic models
Current implementation ignores the user input (encode argument) and determines the model-id as a parameter of the artic question encoder class in ```search/faiss/_search.py```