# Pyserini: Document Screenshot Embedding (DSE) Experiments

This guide provides instructions for reproducing DSE experiments using Pyserini.

DSE (Document Screenshot Embedding) is a novel retrieval paradigm that directly encodes document screenshots into dense representations, bypassing traditional document parsing and content extraction.

> Xueguang Ma, Sheng-Chieh Lin, Minghan Li, Wenhu Chen, Jimmy Lin. [Unifying Multimodal Retrieval via Document Screenshot Embedding](https://arxiv.org/abs/2406.11251). _arXiv:2406.11251_, 2024.

## Setup

First, ensure you have Pyserini installed with optional dependencies:

```bash
pip install pyserini[optional]
```

DSE requires a vision-language model. We use the Phi-3 based DSE model from the paper:

The model will be downloaded automatically on first use when specified via `--encoder`.

## Wiki-SS: Wikipedia Screenshot Retrieval

The Wiki-SS dataset contains ~1.2M Wikipedia page screenshots for answering Natural Questions.

### Data Preparation

1. **Download the Wiki-SS corpus** from HuggingFace:

```bash
python scripts/dse/download_wiki_ss_corpus.py --output-dir collections/wiki-ss
```

2. **Download NQ test queries**:

```bash
python scripts/dse/download_wiki_ss_nq_queries.py --output-dir collections/wiki-ss
```

### Encoding the Corpus

Encode document screenshots into dense vectors:

```bash
python -m pyserini.encode \
  input   --corpus collections/wiki-ss/corpus.jsonl \
          --fields contents \
  output  --embeddings encode/wiki-ss.dse \
  encoder --encoder Tevatron/dse-phi3-docmatix-v2 \
          --encoder-class dse \
          --fields contents \
          --multimodal \
          --batch-size 16 \
          --device cuda:0
```

### Building the Index

Build a Faiss index from the embeddings:

```bash
python -m pyserini.index.faiss \
  --input encode/wiki-ss.dse \
  --output indexes/wiki-ss.dse \
  --dim 3072
```

### Retrieval

Run retrieval on NQ test questions:

```bash
python -m pyserini.search.faiss \
  --encoder-class dse \
  --encoder Tevatron/dse-phi3-docmatix-v2 \
  --topics collections/wiki-ss/wiki-ss-nq-test-queries.tsv \
  --index indexes/wiki-ss.dse \
  --output runs/run.wiki-ss.dse.txt \
  --hits 100 \
  --device cuda:0
```

### Evaluation

Evaluate retrieval accuracy:

```bash
python -m pyserini.eval.trec_eval \
  -c -m recall.1 -m recall.5 -m recall.20 -m recall.100 \
  collections/wiki-ss/nq-test-qrels.txt \
  runs/run.wiki-ss.dse.txt
```

Expected results (from the paper):

| Metric      | DSE    | BM25   | E5     |
|-------------|--------|--------|--------|
| Top-1 Acc   | 46.2   | 29.5   | 47.6   |
| Top-5 Acc   | 68.5   | 50.4   | 68.6   |
| Top-10 Acc  | 73.7   | 57.5   | 73.1   |
| Top-20 Acc  | 77.6   | 63.7   | 76.5   |

## SlideVQA: Slide Retrieval

DSE is particularly effective for slide retrieval where visual layout matters.

### Data Preparation

1. **Download SlideVQA dataset**:

```bash
mkdir -p collections/slidevqa
# Download from the SlideVQA repository
```

2. **Prepare corpus** (slide images in JSONL format):

```json
{"id": "slide_001", "contents": "slides/slide_001.png"}
```

### Encoding and Indexing

```bash
# Encode slides
python -m pyserini.encode \
  input   --corpus collections/slidevqa/corpus.jsonl \
          --fields contents \
  output  --embeddings encode/slidevqa.dse \
  encoder --encoder Tevatron/dse-phi3-docmatix-v2 \
          --encoder-class dse \
          --fields contents \
          --multimodal \
          --batch-size 1 \
          --device cuda:0

# Build index
python -m pyserini.index.faiss \
  --input encode/slidevqa.dse \
  --output indexes/slidevqa.dse \
  --dim 3072
```

### Retrieval and Evaluation

```bash
# Search
python -m pyserini.search.faiss \
  --encoder-class dse \
  --encoder Tevatron/dse-phi3-docmatix-v2 \
  --topics collections/slidevqa/test-queries.tsv \
  --index indexes/slidevqa.dse \
  --output runs/run.slidevqa.dse.txt \
  --hits 100 \
  --device cuda:0

# Evaluate
python -m pyserini.eval.trec_eval \
  -c -m ndcg_cut.10 -m recall.10 \
  collections/slidevqa/qrels.txt \
  runs/run.slidevqa.dse.txt
```

Expected results (from the paper):

| Method      | nDCG@10 | Recall@10 |
|-------------|---------|-----------|
| **DSE**     | **75.3**| **84.6**  |

## Custom Document Screenshots

To use DSE with your own documents:

### 1. Generate Screenshots

For web pages, use a headless browser:

```python
from playwright.sync_api import sync_playwright

def capture_screenshot(url, output_path, width=1344, height=1344):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={'width': width, 'height': height})
        page.goto(url)
        page.screenshot(path=output_path, full_page=False)
        browser.close()
```

For PDFs, use pdf2image:

```python
from pdf2image import convert_from_path

def pdf_to_screenshots(pdf_path, output_dir):
    images = convert_from_path(pdf_path, dpi=150)
    for i, img in enumerate(images):
        img = img.resize((1344, 1344))  # Resize for DSE
        img.save(f'{output_dir}/page_{i}.png', 'PNG')
```

### 2. Prepare Corpus File

Create a JSONL file with document IDs and screenshot paths:

```python
import json

documents = [
    {"id": "doc1", "contents": "screenshots/doc1.png"},
    {"id": "doc2", "contents": "screenshots/doc2.png"},
]

with open('corpus.jsonl', 'w') as f:
    for doc in documents:
        f.write(json.dumps(doc) + '\n')
```

### 3. Run Standard Pipeline

Follow the encoding, indexing, and retrieval steps above with your corpus.

## Tips and Troubleshooting

### Memory Management

DSE uses the Phi-3-vision model (~4B parameters). For limited GPU memory:

- Reduce batch size: `--batch-size 1` (required for Phi-3)
- Use CPU (much slower): `--device cpu`
- Enable fp16: Model uses bfloat16 by default on CUDA

### Screenshot Quality

- **Resolution**: Phi-3-vision handles dynamic resolutions up to 1344×1344. No need to resize images.
- **Format**: PNG recommended for lossless quality
- **Content**: Ensure important content is visible in the viewport

### Flash Attention

For faster inference, install flash attention:

```bash
pip install flash-attn --no-build-isolation
```

This can provide 2-3x speedup for encoding.

### Model Information

- **Model**: [Tevatron/dse-phi3-docmatix-v2](https://huggingface.co/Tevatron/dse-phi3-docmatix-v2)
- **Embedding dimension**: 3072
- **Base model**: Phi-3-vision
- **Training data**: Docmatix-IR dataset

## References

If you use DSE in your research, please cite:

```bibtex
@article{ma2024dse,
  title={Unifying Multimodal Retrieval via Document Screenshot Embedding},
  author={Ma, Xueguang and Lin, Sheng-Chieh and Li, Minghan and Chen, Wenhu and Lin, Jimmy},
  journal={arXiv preprint arXiv:2406.11251},
  year={2024}
}
```

## Reproduction Log[*](reproducibility.md)

