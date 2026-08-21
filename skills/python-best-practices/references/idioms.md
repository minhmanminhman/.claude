# Idioms

Python rewards knowing the short way. The point is not brevity for its own sake - idiomatic code
is the code the next reader recognises without parsing.

## Comprehensions, and when to refuse one

*"There should be one - and preferably only one - obvious way to do it."*

**Yes**
```python
big = [x for x in values if x > 4]
by_id = {user.id: user for user in users}
names = {user.name for user in users}
```

**No**
```python
big = []
for x in values:
    if x > 4:
        big.append(x)

big = list(filter(lambda x: x > 4, values))
```

`filter(lambda ...)` and `map(lambda ...)` do the same work with more machinery. `map` without a
lambda is fine - `map(str.strip, lines)` reads well.

**Refuse the comprehension** when it needs two `for` clauses plus a condition, or when the
expression no longer fits on a line. A comprehension you have to decode is worse than the loop
it replaced.

**No**
```python
result = [transform(x, y) for x in outer if x.ok for y in x.inner if y.enabled]
```

**Yes**
```python
result = []
for x in outer:
    if not x.ok:
        continue
    result.extend(transform(x, y) for y in x.inner if y.enabled)
```

Use a generator expression when you are only iterating once. `sum(p.price for p in cart)` never
builds the list.

## Truthiness and identity

Empty containers, empty strings, `0`, and `None` are all falsy. Lean on that.

**Yes**
```python
if items:
    ...
if not name:
    ...
if value is None:
    ...
if flag:
    ...
```

**No**
```python
if len(items) > 0:
    ...
if name == "":
    ...
if value == None:
    ...
if flag == True:
    ...
```

One real exception: when `0` and `None` mean different things, truthiness merges them and you
need the explicit check.

```python
if timeout is not None:      # 0 is a valid timeout, so `if timeout:` would be a bug
    sock.settimeout(timeout)
```

Same trap with `if not count:` when `count == 0` is legitimate.

## Iteration

```python
for i, line in enumerate(lines, start=1):        # not: for i in range(len(lines))
    ...

for name, score in zip(names, scores, strict=True):   # strict= catches length mismatch
    ...

for key, value in mapping.items():               # not: for key in mapping
    ...

first, *rest = parts                             # unpacking beats parts[0] / parts[1:]
```

`zip(..., strict=True)` raises when the inputs differ in length rather than silently truncating -
*"errors should never pass silently."*

Never mutate a collection while iterating it. Build a new one, or iterate a copy.

**Yes**
```python
items = [x for x in items if x.valid]
```

**No**
```python
for x in items:
    if not x.valid:
        items.remove(x)      # skips elements, silently
```

## Strings

f-strings for everything. `%` and `.format()` are legacy.

```python
msg = f"retry {attempt} of {limit} for {url}"
debug = f"{payload=}"                # renders as: payload={'a': 1}
amount = f"{price:.2f}"
```

Build a string from parts with `join`, not `+=` in a loop - repeated concatenation is quadratic.

```python
report = "\n".join(f"{k}: {v}" for k, v in stats.items())
```

The one place `%` survives is logging, where deferring the format matters:

```python
logger.debug("parsed %s rows from %s", count, path)   # not formatted unless DEBUG is on
```

## Paths and files

`pathlib` over `os.path` string surgery.

```python
from pathlib import Path

config = Path(base) / "conf" / "app.toml"
if config.exists():
    data = config.read_text(encoding="utf-8")

for py in Path("src").rglob("*.py"):
    ...
```

Always pass `encoding=` when reading or writing text. The default is platform-dependent and it
will differ between your machine and CI.

Anything that must be closed goes in a `with`:

```python
with open(src, encoding="utf-8") as fin, open(dst, "w", encoding="utf-8") as fout:
    fout.write(transform(fin.read()))

with lock:
    ...
```

## Flat over nested

*"Flat is better than nested."* Handle the failures first and return early, so the happy path
stays at one indent level.

**Yes**
```python
def charge(order):
    if not order.items:
        raise EmptyOrderError(order.id)
    if order.total <= 0:
        raise InvalidAmountError(order.total)
    return gateway.submit(order)
```

**No**
```python
def charge(order):
    if order.items:
        if order.total > 0:
            return gateway.submit(order)
        else:
            raise InvalidAmountError(order.total)
    else:
        raise EmptyOrderError(order.id)
```

## EAFP over LBYL

Easier to ask forgiveness than permission. Try it, catch the failure - checking first is a race
condition and a second lookup.

**Yes**
```python
try:
    value = mapping[key]
except KeyError:
    value = default
```

**Yes**
```python
value = mapping.get(key, default)
```

**No**
```python
if key in mapping:          # two lookups; and for files, the state can change between the check
    value = mapping[key]    # and the use
else:
    value = default
```

LBYL is right when the check is cheap and the failure is expected in normal operation.

## Dataclasses

A class that is only `__init__` assignments should be a dataclass.

**Yes**
```python
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Session:
    user_id: str
    token: str
    scopes: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)
```

You get `__init__`, `__repr__`, and `__eq__`. `frozen=True` makes it hashable and stops
accidental mutation; `slots=True` cuts memory and catches typo'd attribute assignment.

Reach for `NamedTuple` when you need tuple unpacking, `TypedDict` when the data arrives as a
dict from JSON, and `pydantic` when you need validation at a trust boundary.

## Mutable default arguments

The default is created once, at function definition, and shared by every call.

**No**
```python
def add(item, bucket=[]):     # bucket persists across calls
    bucket.append(item)
    return bucket
```

**Yes**
```python
def add(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket
```

## Generators

Yield when the caller consumes one at a time or the sequence is large. Nothing is materialised.

```python
def parse(path: Path) -> Iterator[Record]:
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                yield Record.from_line(line)
```

Return a list instead when the caller needs `len()`, indexing, or more than one pass.

## Smaller things worth knowing

```python
x, y = y, x                                   # swap, no temp
sorted(users, key=lambda u: u.created_at)     # key=, not cmp
sorted(users, key=operator.attrgetter("created_at"))
counts = collections.Counter(words)
groups = collections.defaultdict(list)
first = next((u for u in users if u.admin), None)
text = value or "unknown"                     # careful: 0 and "" take the fallback too
```

Use `match` for genuine structural dispatch on shapes, not as a switch over a few strings - a
dict lookup or an `if`/`elif` chain is clearer for that.
