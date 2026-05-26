# Repo Project Instructions

## Scope and stack
- Primary language: Python (`pyserini/`, `tests/`, `integrations/`, most `scripts/`).
- Secondary runtime dependency: Java 21 via PyJNIus for Anserini/Lucene integration.
- Build backend: `setuptools` via `pyproject.toml`.
- Packaging target: `pyserini` package only (`tests` and `integrations` excluded from wheel).

## Hard requirements
- Use Python 3.11 for development consistency.
- Use Java 21 (`JAVA_HOME` must point to a Java 21 install).
- Keep `tools/` submodule initialized (`anserini-tools`); many eval workflows depend on it.

## Repository layout (high signal)
- `pyserini/`: core library and CLI entry modules (`python -m pyserini.*`).
- `tests/core`, `tests/optional`: unit tests (unittest-based).
- `integrations/core`, `integrations/optional`: regression/integration tests and paper reproductions.
- `docs/`: user docs, reproducibility guides, release notes, and Sphinx source.
- `scripts/`: dataset/model-specific utilities and reproduction helpers.
- `tools/`: git submodule with evaluation binaries/scripts.
- `bin/`: runnable shell helpers for common retrieval setups.

## Development setup workflow
1. Clone with submodules:
   - `git clone ... --recurse-submodules`
2. Build evaluation tools from submodule:
   - `cd tools/eval && tar xvfz trec_eval.9.0.4.tar.gz && cd trec_eval.9.0.4 && make && cd ../../..`
   - `cd tools/eval/ndeval && make && cd ../../..`
3. Install editable package:
   - `pip install -e .`
4. Build Anserini separately and copy fatjar into:
   - `pyserini/resources/jars/`

## Test workflow
- Baseline suite command from docs:
  - `python -m unittest`
- Tests are `unittest` style; prefer targeted execution while iterating, then full run before merging.
- `tests/optional` and `integrations/optional` may require extra dependencies/models/indexes; do not assume they run in minimal envs.
- For retrieval regressions, prefer validating with tiny fixtures in `tests/resources` before heavyweight corpora.

## Linting/formatting expectations
- Only explicit formatter config in repo root is Black (`[tool.black]`, `skip-string-normalization = true`).
- No repo-root ruff/flake8/mypy config is present; avoid introducing new tooling unless requested.
- Preserve existing import/style conventions in touched files; keep diffs minimal and local.

## Docs/build workflow
- Sphinx docs live in `docs/source`.
- Build docs from `docs/`:
  - `make html` (via `docs/Makefile` and `sphinx-build`).
- Keep code/doc links consistent with existing docs pages under `docs/`.

## Pyserini-specific engineering guardrails
- Maintain CLI/module stability (`python -m pyserini.search.lucene`, `pyserini.search.faiss`, eval modules).
- Avoid breaking prebuilt index names, topic IDs, and eval script interfaces referenced in docs.
- Be explicit about deterministic vs non-deterministic behavior for on-the-fly neural inference.
- Prefer extending existing encoder/search abstractions (`pyserini/encode`, `pyserini/search`, `pyserini/index`) over adding one-off pathways.
- Keep heavyweight downloads out of tests; use cached/prebuilt resources or small fixtures.

## Dependency guidance
- Core deps are large (Torch/Transformers/ONNX); optional extras include Faiss, spaCy, UniIR, VLM2Vec.
- If adding dependencies, justify impact on install friction and cross-platform compatibility.
- For features depending on optional packages, gate imports cleanly and fail with actionable errors.

## Change and review checklist
- Run relevant tests locally (`python -m unittest` at minimum for touched scope).
- Update docs when CLI flags, expected metrics, or workflows change.
- Do not commit built artifacts, downloaded indexes, or local cache outputs.
- Keep reproducibility claims tied to concrete commands/expected metrics in docs.
