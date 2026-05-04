---
name: install-pyserini-dev
description: Use this skill when the user wants to clone Pyserini from GitHub for local development, install Pyserini from source with pip editable mode using `pip install -e .`, create or reuse a development environment, install optional development extras, or debug source-checkout installation issues involving Python, Java, Git, pip, PyPI, or editable installs.
---

# Install Pyserini For Development

## Purpose

Clone Pyserini, install the checkout in editable mode with `python -m pip install -e .`, verify Python/Java prerequisites, and run smoke tests before handing the development environment back to the user.

## Core Workflow

1. Choose the checkout location:
   - If the user named a target directory, use it.
   - If the current directory already looks like a Pyserini checkout, do not clone over it; install from that checkout instead.
   - If no target was specified, create or use a clear project directory such as `pyserini-dev`.
   - Do not overwrite an existing non-empty directory without reading it first.

2. Verify tools and prerequisites:
   ```bash
   git --version
   python3 --version
   java -version
   ```
   Pyserini depends on Anserini/Lucene and may require a specific Java version. Check current Pyserini docs or repository metadata before treating a Java version mismatch as acceptable.

3. Clone Pyserini when needed:
   ```bash
   git clone https://github.com/castorini/pyserini.git pyserini-dev
   cd pyserini-dev
   ```
   If the user needs their fork or a specific branch, clone or check out that requested remote or branch instead. Use normal `git fetch`, `git pull`, or `git checkout`; never force-update a user checkout.

4. Inspect project metadata before installing:
   ```bash
   python3 -m pip --version
   python3 -c "import sys; print(sys.version)"
   ```
   Read `pyproject.toml`, `setup.py`, or installation docs if present before selecting Python versions, extras, or dependency groups.

5. Create or reuse a Python environment:
   - If the user requested an existing environment, target it explicitly.
   - Otherwise prefer a checkout-local virtualenv:
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     python -m pip install --upgrade pip
     ```
   - If the user requested Python 3.12 or project metadata requires it, create the environment with that interpreter:
     ```bash
     python3.12 -m venv .venv
     ```

6. Install Pyserini in editable mode:
   ```bash
   python -m pip install -e .
   ```
   If optional extras are requested, verify the extras names from current project metadata first, then install with:
   ```bash
   python -m pip install -e ".[EXTRA]"
   ```

7. Run smoke tests:
   ```bash
   python -c "import sys, importlib.metadata as m; import pyserini; print(sys.version.split()[0]); print(m.version('pyserini')); print('pyserini editable import ok')"
   python -c "from pyserini.search.lucene import LuceneSearcher; print('LuceneSearcher import ok')"
   ```
   The Lucene import may take tens of seconds while the JVM starts. Warnings about `jdk.incubator.vector` or invalid escape sequences in Pyserini internals are not install failures if the command exits successfully.

8. Report the exact commands run, checkout path, active branch and commit, Python version, Java version, installed Pyserini version, environment path, and any skipped verification.

## Command Choices

Use `python -m pip`, not bare `pip`, so installation targets the intended interpreter.

Use `pip install -e .` when the user wants source edits to be reflected without reinstalling.

Use `pip install -e ".[EXTRA]"` only after verifying that the requested extra exists in current project metadata.

Use a checkout-local `.venv` for a self-contained development setup unless the user asks to reuse another environment.

Use a fork remote when the user plans to contribute from their fork; otherwise clone `https://github.com/castorini/pyserini.git`.

## Troubleshooting

- If Java is missing or too old, install a compatible JDK before retrying Pyserini.
- If Python is too old for current Pyserini metadata, create a fresh environment with a compatible interpreter.
- If editable install dependency resolution fails, inspect current project metadata and retry in a fresh virtualenv before mutating a broken environment in place.
- If imports resolve to a different Pyserini installation, check `python -c "import pyserini; print(pyserini.__file__)"` and reinstall into the intended environment.
- If optional extras fail, install the core editable package first, then add optional packages separately only if the requested workflow needs them.
- If a Conda environment is already active and should be reused, target it explicitly with that environment's Python rather than creating `.venv`.

## Safety Notes

Ask for approval before installing missing system tools, downloading large dependencies, or modifying shell startup files. Do not download large indexes or models unless the user asked for functional retrieval verification or explicitly approved downloads. Do not remove an existing checkout, `.venv`, lockfile, or dependency pin unless the user requested a reset.
