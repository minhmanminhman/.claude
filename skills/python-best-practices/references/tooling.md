# Tooling

## What the formatter owns

`ruff format` decides all of this. Do not review it, do not comment on it, do not fix it by hand:

- Indentation and continuation-line alignment
- Blank lines between definitions
- Whitespace around operators, after commas, inside brackets
- Trailing commas in multiline structures
- Quote style
- Where a long line wraps

A bullet list of these rules in a review is pure cost - one command guarantees them. Spend the
attention on naming, structure, error handling, and types, which no tool can settle.

## The stack

| Job | Tool | Command |
|---|---|---|
| Format | ruff | `ruff format .` |
| Lint and import sort | ruff | `ruff check --fix .` |
| Type check | mypy | `mypy src/` |
| Test | pytest | `pytest` |
| Env and deps | uv | `uv sync`, `uv run pytest` |

Ruff replaces black, isort, flake8, pyupgrade, and most of pylint, in one binary that runs in
well under a second on a large codebase. If a project already uses black plus isort plus flake8,
leave it alone unless asked - the output is near-identical and the churn is not worth it.

## A working pyproject.toml

```toml
[project]
name = "myapp"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["httpx>=0.27"]

[dependency-groups]
dev = ["pytest>=8", "mypy>=1.11", "ruff>=0.6"]

[tool.ruff]
line-length = 88
target-version = "py312"
src = ["src"]

[tool.ruff.lint]
select = [
    "E", "W",    # pycodestyle
    "F",         # pyflakes
    "I",         # isort
    "N",         # pep8-naming
    "UP",        # pyupgrade
    "B",         # bugbear: mutable defaults, loop-variable capture, and friends
    "SIM",       # simplify
    "RUF",       # ruff's own
]
ignore = ["E501"]   # the formatter handles line length

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101"]   # assert is the point in tests

[tool.mypy]
python_version = "3.12"
strict = true
warn_unreachable = true

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-q --strict-markers"
```

`B` (flake8-bugbear) is the rule set that earns its place fastest - it catches mutable default
arguments, `except` clauses that swallow too much, and loop variables captured by closures.

## Layout

```
myapp/
├── pyproject.toml
├── src/
│   └── myapp/
│       ├── __init__.py
│       └── sessions.py
└── tests/
    ├── conftest.py
    └── test_sessions.py
```

The `src/` layout means tests import the installed package, not the working directory. That
catches a missing `__init__.py` or a file left out of the wheel before your users do.

## Suppressing a rule

Name the rule and give a reason. A blanket `# noqa` hides the next problem too.

```python
import config  # noqa: F401  # side-effect import registers the plugins
```

If a rule fights the codebase everywhere, turn it off in `pyproject.toml` once rather than
scattering suppressions.

## pre-commit

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

Worth it on a shared repo, since it stops formatting churn arriving in review. Skip it on a
solo project where the editor already formats on save.

## Order to run things

```bash
ruff format . && ruff check --fix . && mypy src/ && pytest
```

Format first so the linter is not reporting on code that is about to move.
