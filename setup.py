import setuptools

with open("project-description.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyserini",
    version="0.10.1.0",
    author="Jimmy Lin",
    author_email="jimmylin@uwaterloo.ca",
    description="Python interface to the Anserini IR toolkit built on Lucene",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"pyserini": [
        "resources/jars/anserini-0.10.1-fatjar.jar",
     ]},
    url="https://github.com/castorini/pyserini",
    install_requires=['Cython>=0.29.21', 'pyjnius>=1.2.1', 'numpy>=1.18.1', 'scipy>=1.4.1', 'scikit-learn>=0.22.1',
                      'pandas>=1.1.5', 'tqdm>=4.56.0', 'tensorflow>=2.3.0', 'faiss-cpu>=1.6.5', 'transformers==4.0.0'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
