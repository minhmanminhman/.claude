# Imports

## Layout

Top of the file, one import per line, three groups separated by a blank line:

```python
"""Session storage backed by Redis."""

from __future__ import annotations

import json
import logging
from pathlib import Path

import redis
from pydantic import BaseModel

from myapp import config
from myapp.errors import StorageError
```

1. Standard library
2. Third party
3. Local

Order: module docstring, then `from __future__` imports, then dunders (`__all__`, `__version__`),
then the three groups. `ruff check --select I --fix` sorts and groups all of it, so configure it
once rather than doing it by hand.

## Module or symbol?

Split by where the thing comes from.

**Symbols from stdlib and third party.** This is the ecosystem convention and reading
`typing.Optional` or `dataclasses.dataclass` at every use site is noise.

```python
from pathlib import Path
from dataclasses import dataclass
from collections.abc import Iterator
```

**The module from your own package.** Import the module and call through it.

```python
from myapp import sessions

session = sessions.get(user_id)
```

Two reasons. Provenance: `sessions.get(...)` says where `get` lives, while a bare `get(...)`
imported from somewhere leaves the reader hunting. And circular imports: `from myapp import
sessions` binds a module object that can still be partially initialised, whereas
`from myapp.sessions import get` demands that `get` already exist at import time. A cycle the
first form survives, the second form kills with an `ImportError` at startup.

Exception: types and exceptions you name constantly are fine to import directly, since they are
usually leaf modules with no cycle risk.

```python
from myapp.errors import StorageError   # errors imports nothing, so no cycle
```

## Never wildcard

*"Explicit is better than implicit."*

```python
from os.path import *   # no
```

You lose provenance, you silently shadow builtins and earlier imports, and no tool can tell
which names are actually used. The only tolerated case is a package `__init__.py` re-exporting
a curated `__all__`, and even there naming the symbols is better.

## Absolute over relative

```python
from myapp.storage import redis_backend   # yes
from ..storage import redis_backend       # only in a deep, stable package layout
```

Absolute imports survive a file being moved and read the same from anywhere. Explicit relative
imports are acceptable inside a large package where the absolute path would be tediously long,
but implicit relative imports do not exist in Python 3 at all.

## Breaking a circular import

When two modules genuinely need each other, the fix is usually structural, not clever:

1. Move the shared thing into a third module both can import. Best answer nearly always.
2. Import the module rather than the symbol (see above).
3. Import inside the function that needs it. Works, but it hides a dependency and pays the lookup
   on every call, so leave a comment saying which cycle it breaks.
4. For annotation-only needs, use `TYPE_CHECKING`.

```python
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from myapp.sessions import Session


def render(session: Session) -> str:
    ...
```

With `from __future__ import annotations` the annotation is never evaluated at runtime, so the
import is only needed by the type checker. This is the clean way to type against a module you
cannot import for real.

## `__all__`

Declare the public surface of any module others import from:

```python
__all__ = ["Session", "SessionStore", "get"]
```

It documents intent, controls `from module import *` for the people who ignore the advice above,
and lets linters flag an unused internal name without flagging a deliberate re-export.
