# {{cookiecutter.project_name}}

## Overview

{{cookiecutter.project_description}}

## Build & Test

| Command | What it does |
| --- | --- |
| `make install` | `uv sync` the environment and install the pre-commit hooks (one-time setup) |
| `make check` | Lock-file consistency, pre-commit on all files, {{cookiecutter.type_checker}}{% if cookiecutter.deptry == "y" %}, deptry{% endif %} |
| `make test` | pytest{% if cookiecutter.codecov == "y" %} with coverage{% endif %} |
{%- if cookiecutter.docs_tool != "none" %}
| `make docs` | Serve the {{cookiecutter.docs_tool}} docs site locally; `make docs-test` builds it in strict mode |
{%- endif %}

`make install` runs `uv run pre-commit install`, so there is no separate hook-install step.
Pre-commit includes `detect-private-key`, `check-added-large-files`, and `gitleaks`; a
commit that trips one of them is meant to fail.

## Project Structure

{% if cookiecutter.layout == "src" -%}
- `src/{{cookiecutter.project_slug}}/` — package source
{%- else -%}
- `{{cookiecutter.project_slug}}/` — package source
{%- endif %}
- `tests/` — pytest suite
- `data/{raw,interim,processed,external,metadata}/` — data directories; contents are
  gitignored, only the `.gitkeep` placeholders are tracked
- `notebooks/`, `scripts/`, `models/`, `reports/`, `references/`, `examples/` — scaffolded
  and empty; delete what the project does not use
{%- if cookiecutter.docs_tool == "mkdocs" %}
- `docs/` — mkdocs source (`index.md`, `modules.md`). Living docs (TODO, CHANGELOG,
  EDGECASES, DECISIONS, ARCHITECTURE) also live here but `exclude_docs` in `mkdocs.yml`
  keeps them out of the built site
{%- elif cookiecutter.docs_tool == "zensical" %}
- `docs/` — zensical source (`index.md`, `modules.md`). Zensical has no equivalent of
  mkdocs' `exclude_docs`, so living docs placed here (TODO, CHANGELOG, EDGECASES,
  DECISIONS, ARCHITECTURE) are published with the site; keep them elsewhere if that matters
{%- endif %}

Update this section as the layout settles.

## Conventions

- `/format` applies ruff formatting and Google-style docstrings to Python files.
- Ruff config lives in `pyproject.toml`; do not add per-file overrides without a reason.
