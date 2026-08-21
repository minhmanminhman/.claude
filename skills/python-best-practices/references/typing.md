# Type Hints

Baseline here is Python 3.12. Check `requires-python` in `pyproject.toml` before using the newest
syntax, and step back if the project targets older - see the version table at the end.

## Where annotations pay

Annotate every public function signature, every method on a public class, and every dataclass
field. That is the contract, and it is where a checker catches real mistakes.

Skip obvious locals. `count: int = 0` tells nobody anything.

```python
def parse(path: Path, *, strict: bool = False) -> list[Record]:
    records: list[Record] = []      # worth it: the empty list has no inferable element type
    total = 0                       # not worth it: obviously an int
    ...
```

Annotate a local when inference cannot get there: an empty container, a value that starts `None`,
or a variable a checker would otherwise widen to `Any`.

If a project has no annotations at all, adding them to the file you are touching is fine. Adding
them across the codebase unasked is not.

## Modern syntax

```python
list[str]                    # not typing.List
dict[str, int]               # not typing.Dict
tuple[int, ...]              # not typing.Tuple
str | None                   # not Optional[str]
int | str                    # not Union[int, str]
```

Import the abstract kinds from `collections.abc`, not `typing`:

```python
from collections.abc import Callable, Iterable, Iterator, Mapping, Sequence
```

Accept the widest type you can use, return the narrowest you can promise. `Sequence[str]` or
`Iterable[str]` as a parameter, `list[str]` as a return.

```python
def normalise(names: Iterable[str]) -> list[str]:
    return [n.strip().lower() for n in names]
```

Never annotate a parameter as `list[str]` when you only iterate it - that rejects a tuple, a
generator, and a set for no reason.

## Mutable containers as parameters

`list` and `dict` are invariant, so `list[Base]` will not accept a `list[Derived]`. Reading
parameters should be `Sequence` or `Mapping`, which are covariant and accept both.

```python
def summarise(rows: Sequence[Row], index: Mapping[str, int]) -> str:
```

## Protocol over ABC

Structural typing: anything with the right shape fits, no inheritance and no registration.

```python
from typing import Protocol

class Writer(Protocol):
    def write(self, data: bytes) -> int: ...


def emit(sink: Writer, payload: bytes) -> None:
    sink.write(payload)
```

Now a file object, a socket, and your own class all satisfy `Writer` without importing it. Use an
ABC instead when you want shared implementation, or when you need `isinstance` to be authoritative.

## Self and generics

```python
from typing import Self

class Builder:
    def with_retries(self, n: int) -> Self:
        self._retries = n
        return self            # Self, so subclasses chain correctly
```

3.12 generics need no `TypeVar` declaration:

```python
def first[T](items: Sequence[T]) -> T | None:
    return items[0] if items else None


class Box[T]:
    def __init__(self, value: T) -> None:
        self.value = value


type Handler = Callable[[Request], Response]     # type alias statement, 3.12+
```

## Escaping Any

`Any` disables checking for everything it touches, and it spreads. Each use should be one you can
justify.

Reach for these first:

- `object` when you accept anything but will only pass it along or `isinstance` it. Unlike `Any`,
  the checker still stops you calling methods on it.
- `Protocol` when you need a shape, not a type.
- `TypedDict` for JSON-shaped dicts with known keys.
- `Literal` for a fixed set of string or int values.
- `cast` when you know something the checker cannot prove. Narrower than `Any` and it documents
  the assumption.

```python
from typing import Literal, TypedDict

Mode = Literal["read", "write", "append"]

class UserPayload(TypedDict):
    id: str
    email: str
    verified: bool
```

## Structured data

`dataclass` for internal records, `TypedDict` for dicts arriving from JSON, `NamedTuple` when the
caller unpacks it, `pydantic` when the data crosses a trust boundary and needs validating at
runtime. Annotations alone are not validation - nothing checks them when the program runs.

## `from __future__ import annotations`

Makes every annotation a string, evaluated only by the checker. Two consequences worth knowing:

- Forward references and `TYPE_CHECKING`-only imports work without quotes.
- Anything reading annotations at runtime - `pydantic`, `dataclasses` with `get_type_hints`,
  FastAPI - has to resolve them, which sometimes breaks.

Use it in modules that are heavy on type-only imports. Leave it out where a runtime library
consumes the annotations.

## Running the checker

```bash
mypy src/
```

```toml
[tool.mypy]
python_version = "3.12"
strict = true
warn_unreachable = true
```

`strict = true` on a new project. On an existing one, turn it on per-module rather than fixing
the whole codebase at once:

```toml
[[tool.mypy.overrides]]
module = "myapp.legacy.*"
ignore_errors = true
```

Silence a specific line with a reason, never a blanket ignore:

```python
result = untyped_lib.call()  # type: ignore[no-any-return]  # upstream has no stubs
```

## Version floor for each feature

| Syntax | Needs |
|---|---|
| `list[str]`, `dict[str, int]` | 3.9 |
| `X \| None`, `match` | 3.10 |
| `Self`, `ExceptionGroup` | 3.11 |
| `type X = ...`, `def f[T]()`, `class Box[T]` | 3.12 |

Below 3.10, `X | None` in an annotation raises `TypeError` at runtime unless
`from __future__ import annotations` is in the file. Use `Optional[X]` there instead.
