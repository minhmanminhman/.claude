# Docstrings and Comments

## What a docstring is for

A docstring is API documentation. It says what the code does, what it takes, what it gives back,
and what it raises.

It is not a changelog, not a design journal, and not a place to record measurements. Keep all of
this out:

- Results and metrics ("cuts latency by 40%")
- Progress notes ("TODO: refactor once v2 lands", "temporary until the migration")
- Justification of a chosen value ("we picked 30s because 10s was flaky")
- History ("previously used a dict, switched to a list")

Those belong in the commit message, the PR, or an issue - places that carry a date and an author.
In a docstring they rot silently and mislead the next reader. The same rule governs comments.

## When to write one

Public modules, classes, functions, and methods. Skip it for a private helper whose name and
signature already say everything - a docstring that restates the signature is noise.

**Pointless**
```python
def get_user_id(user: User) -> str:
    """Get the user id."""
    return user.id
```

**Worth writing**
```python
def get_user_id(user: User) -> str:
    """Return the canonical id, resolving aliases to the primary account."""
    ...
```

## One-liners

Most functions need one line. Imperative mood - "Return", not "Returns" - closing quotes on the
same line, no blank line before or after.

```python
def load_config(path: Path) -> Config:
    """Return the parsed configuration from a TOML file."""
```

## Multiline: Google style

When there is more to say, summary line, blank line, then sections.

```python
def train(data: list[tuple[str, str]], *, epochs: int = 10) -> Classifier:
    """Train a classifier on labelled colour-category pairs.

    Runs until the loss plateaus or the epoch budget is exhausted, whichever
    comes first.

    Args:
        data: Pairs of colour name and category label.
        epochs: Maximum passes over the data.

    Returns:
        A classifier fitted to the data.

    Raises:
        ValueError: If the data contains fewer than two distinct labels.

    Example:
        >>> classifier = train([("green", "foo"), ("orange", "bar")])
        >>> classifier.predict("green")
        'foo'
    """
```

Closing `"""` on its own line. Summary line fits on one line and ends with a period.

## Do not repeat types

The signature already states them, and a checker enforces it there. Restating a type in the
docstring gives you two copies of one fact, and they diverge the first time the signature
changes.

**No**
```python
Args:
    path (str): The path to the file.
    retries (int): Number of retries.
```

**Yes**
```python
Args:
    path: Location of the config file, absolute or relative to the project root.
    retries: How many times to retry before raising. Zero disables retrying.
```

Say what the argument *means*, what values are valid, and what a caller needs to know that the
type cannot express.

## Classes

Document the class and its constructor arguments in the class docstring. `__init__` does not get
its own.

```python
@dataclass
class Person:
    """A human being, as far as this system is concerned.

    Attributes:
        name: Full name as given, not normalised.
        age: Age in whole years at the last birthday.
    """

    name: str
    age: int
```

## Modules

One line at the top saying what the module is for. Longer only if the module has a concept a
reader needs before touching any function in it.

```python
"""Session storage and retrieval, backed by Redis."""
```

## Comments

Use them sparingly. Prefer making the code say it.

**No**
```python
# If the sign is a stop sign
if sign.color == "red" and sign.sides == 8:
    stop()
```

**Yes**
```python
def is_stop_sign(sign: Sign) -> bool:
    return sign.color == "red" and sign.sides == 8


if is_stop_sign(sign):
    stop()
```

A named function is checkable, reusable, and cannot drift out of sync with the condition. A
comment can, and eventually does.

The comments worth keeping explain what the code cannot: a non-obvious constraint, a workaround
for a specific upstream bug, an ordering requirement that looks arbitrary.

```python
# S3 returns 404 for a bucket that exists but is in another region, so a missing
# object and a wrong region are indistinguishable here.
```

Block comments start with `# ` and sit at the indent level of the code they describe. Inline
comments are rare and need two spaces before the `#`.

Every `TODO` carries a tracking reference, otherwise it is a wish:

```python
# TODO(#412): drop this shim once the v1 endpoint is retired.
```

Strunk and White apply. A comment is prose, and the same rules about cutting needless words hold.
