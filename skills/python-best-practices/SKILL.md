---
name: python-best-practices
description: >
  Guide for writing idiomatic, modern Python (3.12+), grounded in PEP 8, PEP 257, the Zen of
  Python, and current ecosystem practice. Use this skill whenever Python is the deliverable
  rather than the tool, that is when:
  (1) writing a new Python module, function, class, or script,
  (2) reviewing, refactoring, or modernizing existing Python,
  (3) the user asks whether code is "pythonic", or mentions PEP 8 or PEP 257,
  (4) choosing names, structuring imports, or writing docstrings,
  (5) designing exceptions and error handling,
  (6) adding or fixing type hints, or configuring mypy or pyright,
  (7) writing pytest tests,
  (8) configuring ruff, formatting, or pyproject.toml.
  Use it even when the user never says "style" - Python being written or reviewed is reason
  enough. Skip it when Python is only the vehicle: running a script to get its output, chasing
  one specific traceback, throwaway REPL or notebook lines, or data analysis where the numbers
  are the deliverable and the code is scaffolding.
license: MIT
compatibility: Python 3.12+ (degrade to the project's requires-python), ruff, pytest
metadata:
  version: "1.0.0"
allowed-tools: Bash(python:*) Bash(python3:*) Bash(ruff:*) Bash(mypy:*) Bash(pytest:*) Read Write Edit Glob Grep
---

# Python Best Practices

Python has a strong idiom culture, and code that fights it costs every later reader. These are
the calls a formatter cannot make for you.

## Read the project before applying anything

Open `pyproject.toml` first. Three things there change your advice:

- `requires-python` - everything below assumes 3.12+. If the project targets older, downgrade:
  no `type X = ...` or `def f[T]()` below 3.12, no `X | None` in annotations below 3.10 (it is a
  runtime `TypeError` there, not a warning), no `list[str]` below 3.9.
- `[tool.ruff]` - line length, quote style, lint rules. The project's answer beats the default.
- `[tool.mypy]` or `[tool.pyright]` - how strict the typing is expected to be.

Then skim a neighbouring module. Match what it does.

### What the project decides, and what it does not

*"Special cases aren't special enough to break the rules. Although practicality beats purity."*

**Match the project, silently:** line length, quote style, docstring format, import grouping
style, test layout, whether type hints are used at all. These are arbitrary. Consistency is the
only real argument for any particular answer, so the project already has the winning argument.
Reformatting a codebase to your preference is vandalism with good intentions.

**Raise regardless of local habit** - these are bugs wearing a style costume:

1. Bare `except:` or a caught exception silenced with no logging and no reason
2. Mutable default arguments (`def f(items=[])`)
3. `assert` used to validate runtime input (stripped entirely under `python -O`)
4. Files, locks, connections, or subprocesses opened without a context manager
5. `== None`, `== True`, `== False`
6. Mutating a list or dict while iterating over it
7. `raise NewError(...)` inside an `except` block without `from`, throwing away the cause
8. Wildcard imports (`from x import *`)

Raise them once, plainly, with the fix. Do not moralise, and do not rewrite the file around them
unless asked.

## Do not hand-audit what the formatter owns

`ruff format` settles indentation, blank lines, whitespace around operators, trailing commas,
continuation-line alignment, quote normalisation, and line wrapping. Checking those by hand is
slower and less reliable than running the command, so do not comment on them and do not spend
review lines on them. Run the tool, move on to what it cannot see.

## Reference files

Read only the file the current question needs. Read several in parallel when the task spans them.

- [naming.md](references/naming.md) - naming conventions, redundant labels, reverse notation,
  underscore prefixes, what never to name a variable
- [idioms.md](references/idioms.md) - comprehensions and when to refuse one, truthiness,
  `enumerate`/`zip`, unpacking, f-strings, `pathlib`, dataclasses, EAFP, guard clauses, generators
- [imports.md](references/imports.md) - grouping, absolute vs relative, module vs symbol,
  circular imports, `__all__`, `TYPE_CHECKING`
- [docstrings.md](references/docstrings.md) - PEP 257, one-liners vs Google-style multiline,
  comment discipline, what must never go in a docstring
- [errors.md](references/errors.md) - exception hierarchy design, narrow `try` blocks, chaining,
  logging, context managers, returning errors vs raising
- [typing.md](references/typing.md) - where annotations pay, 3.12 syntax, `Protocol`, `Self`,
  escaping `Any`, mypy configuration
- [testing.md](references/testing.md) - pytest mechanics: `parametrize`, fixtures, `tmp_path`,
  `monkeypatch`, `pytest.raises`, naming
- [tooling.md](references/tooling.md) - ruff, mypy, pytest, pre-commit, a working pyproject.toml

For test *strategy* (what to test, how much, red-green-refactor), use the `testing-strategy` and
`tdd` skills. This skill covers the Python-specific half only.

## Quick reference

### Defaults when the project is silent
`ruff format` + `ruff check` · 88 columns · double quotes · mypy · pytest · Python 3.12+

### Naming
`lower_case_with_underscores` for variables, functions, methods, modules, packages ·
`CapWords` for classes and exceptions (exceptions end in `Error`) · `ALL_CAPS` for constants ·
`_leading_underscore` for internal · never `l`, `O`, or `I` alone · never shadow a builtin
(`list`, `id`, `type`, `input`) · drop redundant labels: `audio.Core`, not `audio.AudioCore`

### Idioms
Comprehension over `append` in a loop, and over `filter(lambda ...)` - *"there should be one
obvious way to do it"* · but a plain loop beats a comprehension that needs two `for`s and an
`if` · truthiness over `len(x) == 0` · `is None`, never `== None` · `enumerate` and `zip` over
index arithmetic · f-strings over `%` and `.format()` · `pathlib` over `os.path` ·
`with` for anything that must be closed · guard clauses over nesting, *"flat is better than
nested"* · `dataclass` over a class that is only `__init__` assignments

### Imports
Three groups, blank line between: stdlib, third-party, local. `ruff check --select I` sorts them.
Symbols from stdlib and third-party (`from pathlib import Path`); the module from your own
package (`from myapp import sessions`, then `sessions.get()`) - intra-package symbol imports are
where circular imports come from. Absolute over relative. Never wildcard: *"explicit is better
than implicit."*

### Docstrings and comments
Public modules, classes, and functions get a docstring. One line for the obvious ones, imperative
mood: `"""Return the parsed config."""` Google style (`Args:` / `Returns:` / `Raises:`) when
there is more to say, and never repeat a type the signature already states. Document `__init__`
in the class docstring. A docstring says what the code does, like API documentation - no results,
no metrics, no progress notes, no defending a chosen value. Same rule for comments. When a
comment is explaining *what* a condition means, extract a named function instead.

### Errors
Catch the narrowest exception that can occur, around the fewest lines that can raise it. Chain
with `raise X from err`. *"Errors should never pass silently. Unless explicitly silenced"* - a
swallowed exception needs a comment saying why, or a log line. Subclass `Exception`, never
`BaseException`. Raise on failure rather than returning `None` as a sentinel.

### Typing
Annotate every public function signature and every dataclass field; skip obvious locals.
Builtin generics (`list[str]`), `X | None`, `Self`, `Protocol` for structural typing. `Any` is an
escape hatch, and each use should be one you can defend.

### Testing
`pytest` functions with plain `assert`. `@pytest.mark.parametrize` instead of copy-pasted test
bodies. `tmp_path` and `monkeypatch` instead of hand-rolled setup and teardown. Long descriptive
names - `test_parse_returns_error_when_header_missing` needs no docstring. No real network, no
real database.
