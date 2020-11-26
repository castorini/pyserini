import setuptools

with open("project-description.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyserini",
    version="0.10.0.0",
    author="Jimmy Lin",
    author_email="jimmylin@uwaterloo.ca",
    description="Python interface to the Anserini IR toolkit built on Lucene",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"pyserini": [
        "resources/jars/anserini-0.10.0-fatjar.jar",
     ]},
    url="https://github.com/castorini/pyserini",
    install_requires=['Cython', 'pyjnius', 'numpy', 'scipy', 'scikit-learn', 'pandas'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
