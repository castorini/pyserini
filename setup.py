import setuptools

with open("project-description.md", "r") as fh:
    long_description = fh.read()

base_packages = [
    "Cython>=0.29.21",
    "numpy>=1.18.1",
    "pandas>=1.1.5",
    "pyjnius>=1.4.0",
    "scikit-learn>=0.22.1",
    "scipy>=1.4.1",
    "tqdm",
    "spacy>=3.2.1",
]

dense_packages = [
    "transformers>=4.6.0",
    "sentencepiece>=0.1.95",
    "nmslib>=2.1.1",
    "onnxruntime>=1.8.1",
    "lightgbm>=3.3.2",
    "torch"
]

setuptools.setup(
    name="pyserini",
    version="0.19.1",
    author="Jimmy Lin",
    author_email="jimmylin@uwaterloo.ca",
    description="A Python toolkit for reproducible information retrieval research with sparse and dense representations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"pyserini": [
        "resources/jars/anserini-0.16.1-fatjar.jar",
     ]},
    url="https://github.com/castorini/pyserini",
    install_requires=base_packages,
    extras_requires={
        "dense": dense_packages,
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
