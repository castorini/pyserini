import setuptools

with open("project-description.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="pyserini",
    version="0.14.0",
    author="Jimmy Lin",
    author_email="jimmylin@uwaterloo.ca",
    description="A Python toolkit for reproducible information retrieval research with sparse and dense representations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    package_data={"pyserini": [
        "resources/jars/anserini-0.13.5-fatjar.jar",
     ]},
    url="https://github.com/castorini/pyserini",
    install_requires=requirements,
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
