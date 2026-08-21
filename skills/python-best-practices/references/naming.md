# Naming

A name is read far more often than it is written. PEP 8's overriding principle: names should
reflect how a thing is *used*, not how it happens to be implemented.

## Conventions

| Thing | Style | Example |
|---|---|---|
| Variables, functions, methods | `lower_case_with_underscores` | `parse_header`, `retry_count` |
| Modules | `lowercase`, underscores if it helps | `sessions.py`, `http_client.py` |
| Packages | `lowercase`, avoid underscores | `canteen`, not `can_teen` |
| Classes | `CapWords` | `SessionStore` |
| Exceptions | `CapWords` ending in `Error` | `ConfigParseError` |
| Constants | `ALL_CAPS_WITH_UNDERSCORES` | `MAX_RETRIES`, `DEFAULT_TIMEOUT` |
| Type variables | short `CapWords` | `T`, `KeyT`, `T_co` |
| Internal | `_single_leading_underscore` | `_cache`, `_build_index()` |
| Name-mangled | `__double_leading_underscore` | `__slots_map` |

`self` for instance methods, `cls` for class methods. Trailing underscore to dodge a keyword:
`class_`, `id_`, `from_`.

## Never use these as names

`l`, `O`, and `I` alone. In most fonts they are indistinguishable from `1`, `0`, and `l`.

Builtins. Shadowing `list`, `dict`, `id`, `type`, `input`, `filter`, `next`, or `hash` works right
up until the line that needs the real one.

**No**
```python
def summarise(list, type):
    id = hash(type)          # hash() is fine here, but list() and type() are gone
    return list[:id % 10]
```

**Yes**
```python
def summarise(items, kind):
    offset = hash(kind)
    return items[: offset % 10]
```

## Single letters are fine when the scope is two lines

*Exception to "no short names": when the meaning is obvious from the immediate context.*

```python
for e in elements:
    e.mutate()

total = sum(p.price for p in cart)
```

The moment the block grows past a few lines, or the variable crosses a `if`/`for` boundary, name
it properly. `i`, `j`, `k` for indices and `_` for a deliberately unused value are always fine.

## Drop redundant labels

The module already says it. Repeating it in every symbol makes call sites stutter.

**Yes**
```python
import audio

core = audio.Core()
controller = audio.Controller()
```

**No**
```python
from audio import *

core = AudioCore()
controller = AudioController()
```

Same inside a class: `Session.get_session_id()` should be `Session.id` or `Session.get_id()`.

## Prefer reverse notation

Group by the noun, then narrow. Related names sort together, autocomplete becomes useful, and
the shared concept is visible at a glance.

**Yes**
```python
elements = ...
elements_active = ...
elements_defunct = ...
```

**No**
```python
elements = ...
active_elements = ...
defunct_elements = ...
```

This is a preference, not a rule. Do not rename an existing codebase to match it.

## Booleans and predicates

Prefix with `is_`, `has_`, `can_`, or `should_` so the name reads as the condition it guards.

```python
if is_expired(token) and not has_refresh(token):
    raise AuthError("token expired and cannot be refreshed")
```

Avoid negated names. `is_not_ready` produces `if not is_not_ready:`, which nobody parses on the
first read.

## Public and internal

A single leading underscore marks a name as internal: not imported by outsiders, free to change.
Double leading underscore triggers name mangling, which exists to stop a subclass colliding with
a base class attribute, not to make things private. Use it only when you are designing for
inheritance and genuinely need the collision protection.

Declare the public surface with `__all__`. Anything undocumented and unlisted is internal by
default.
