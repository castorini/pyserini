import setuptools

with open("project-description.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

pyserini_packages = setuptools.find_packages()
pyserini_packages.remove('tests')
# For some reason, not automatically discovered
pyserini_packages.append('pyserini.2cr')

setuptools.setup(
    name="pyserini",
    version="0.21.0",
    author="Jimmy Lin",
    author_email="jimmylin@uwaterloo.ca",
    description="A Python toolkit for reproducible information retrieval research with sparse and dense representations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/castorini/pyserini",
    install_requires=requirements,
    packages=pyserini_packages,
    package_data={"pyserini": [
        "resources/jars/anserini-*-fatjar.jar",
    ]},
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
