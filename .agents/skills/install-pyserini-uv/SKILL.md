---
name: install-pyserini-uv
description: Use this skill when the user wants to install Pyserini with uv, create a uv-managed environment for Pyserini, add Pyserini to an existing uv project, install optional Pyserini extras, or debug uv/Pyserini installation issues involving Python, Java, PyPI, or dependency resolution.
---

# Install Pyserini With uv

## Purpose

Install Pyserini in a uv-managed Python environment, verify Java/Python prerequisites, and run smoke tests before handing the environment back to the user.

## Core Workflow

1. Inspect the current directory:
   - If `pyproject.toml` exists, treat it as an existing uv project.
   - If no project exists, create one with `uv init` or create only a virtualenv with `uv venv`, depending on the user's goal.
   - Do not overwrite project metadata without reading it first.

2. Verify tools and prerequisites:
   ```bash
   uv --version
   java -version
   ```
   If the `uv` binary is not on `PATH`, check `python -c "import uv"` before trying `python -m uv --version`. If `uv` is not installed, ask for approval before installing it. If the user does not want uv installed, use the pip fallback below. Prefer the `uv` binary when it is available; use `python -m uv` only after confirming the `uv` Python module is importable and the binary is not on `PATH`. Pyserini depends on Anserini/Lucene and currently expects Java 21.

3. Check current PyPI metadata before choosing versions:
   ```bash
   curl -sS https://pypi.org/pypi/pyserini/json
   ```
   As of Pyserini 2.0.0, `requires_python` is `>=3.12`, and project docs say it is built on Python 3.12 and Java 21. Use current metadata if it differs.

4. Create a uv environment. Prefer a simple project-local `.venv`:
   ```bash
   uv venv .venv --python 3.12
   ```
   For sandboxed or workspace-local installs, keep uv state under the workspace:
   ```bash
   uv python install 3.12 --install-dir .uv-python --cache-dir .uv-cache
   uv venv .venv --python 3.12 --cache-dir .uv-cache
   ```
   If `uv venv --python 3.12` cannot discover the workspace-local interpreter, find it and pass the explicit path:
   ```bash
   find .uv-python -name 'python3.12' -print
   uv venv .venv --python PATH_FROM_FIND --cache-dir .uv-cache
   ```

5. Install Pyserini:
   - Existing uv project:
     ```bash
     uv add pyserini
     ```
   - Existing environment without project metadata, or workspace-local `.venv`:
     ```bash
     uv pip install pyserini --python .venv --cache-dir .uv-cache
     ```
   - If the user asked for reproducibility or a specific version, pin the verified version explicitly:
     ```bash
     uv pip install pyserini==VERSION --python .venv --cache-dir .uv-cache
     ```
   - Optional dependencies when requested:
     ```bash
     uv add "pyserini[optional]"
     ```
     or:
     ```bash
     uv pip install "pyserini[optional]" --python .venv --cache-dir .uv-cache
     ```

6. Run smoke tests:
   ```bash
   uv run --no-project --python .venv/bin/python --cache-dir .uv-cache python -c "import sys, importlib.metadata as m; import pyserini; print(sys.version.split()[0]); print(m.version('pyserini')); print('pyserini import ok')"
   uv run --no-project --python .venv/bin/python --cache-dir .uv-cache python -c "from pyserini.search.lucene import LuceneSearcher; print('LuceneSearcher import ok')"
   ```
   The Lucene import may take tens of seconds while the JVM starts. Warnings about `jdk.incubator.vector` or invalid escape sequences in Pyserini internals are not install failures if the command exits successfully.

7. Report the exact commands run, Python version, Java version, installed Pyserini version, environment path, and any skipped verification.

## pip Fallback

Use this only when uv is unavailable and the user does not want it installed:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install pyserini
python -c "import sys, importlib.metadata as m; import pyserini; print(sys.version.split()[0]); print(m.version('pyserini')); print('pyserini import ok')"
python -c "from pyserini.search.lucene import LuceneSearcher; print('LuceneSearcher import ok')"
```

Keep using `python -m pip`, not bare `pip`, so installation targets the intended interpreter.

## Command Choices

Use `uv add` when the install should become part of a project and update `pyproject.toml` / `uv.lock`.

Use `uv pip install` when the user only wants to populate the active `.venv` or avoid changing project files.

Use `python -m uv` only when `uv` was installed into a user site, its script directory is not on `PATH`, and `python -c "import uv"` succeeds.

Use `--cache-dir .uv-cache` when the default uv cache under the user's home directory is not writable or when the user wants workspace-local state.

Use `uv sync` after editing dependencies manually or when the repo already has a lockfile.

Use `uv run ...` for verification so commands execute inside the uv-managed environment.

Do not require Conda or Mamba for the default install. Mention Conda/Mamba only when the user needs a binary stack that is better managed through Conda channels, such as CUDA-specific PyTorch, Faiss variants, or cluster-standard environments. In those cases, Conda/Mamba can provide Python and binary packages, while `uv pip install` can still install PyPI packages into that environment.

## Troubleshooting

- If Java is missing or too old, install a compatible JDK before retrying Pyserini.
- If dependency resolution fails, check Pyserini's current PyPI metadata and extras names before pinning anything.
- If `uv` fails with `Failed to initialize cache` under `~/.cache/uv`, rerun the command with `--cache-dir .uv-cache`.
- If `uv` is installed but `command -v uv` returns nothing, either add the user script directory, often `~/.local/bin`, to `PATH`, or use `python -m uv` only after `python -c "import uv"` succeeds.
- If optional dependencies fail, try core `pyserini` first, then install `faiss-cpu` or other optional packages separately only if the requested workflow needs them.
- If the environment already contains conflicting packages, create a fresh uv virtualenv and reinstall rather than mutating a broken environment in place.
- If `uv add pyserini` or `uv pip install pyserini` pulls a large dependency set, including PyTorch, Transformers, ONNX Runtime, and PyArrow, that is expected for recent Pyserini releases.
- If a Conda environment is already active and should be reused, target it explicitly with `uv pip install --python "$CONDA_PREFIX/bin/python" pyserini` to avoid installing into the wrong interpreter.

## Safety Notes

Do not run commands that download large indexes or models unless the user asked for functional retrieval verification or explicitly approved downloads. Do not remove an existing `.venv`, lockfile, or dependency pin unless the user requested a reset.
