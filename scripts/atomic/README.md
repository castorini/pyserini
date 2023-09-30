# Usage Guide

We can convert the numpy-style AToMiC prebuilt topics to that of pyserini format as below:

```bash
python convert_embeddings.py --encode-type text --inputs ViT-L-14.laion2b_s32b_b82k.text.validation --topics-output output_dir/ --embeddings-output output_dir/
```

The inputs (AToMiC prebuilt topics) can be found in [this repo](https://huggingface.co/datasets/TREC-AToMiC/AToMiC-Baselines/tree/main).